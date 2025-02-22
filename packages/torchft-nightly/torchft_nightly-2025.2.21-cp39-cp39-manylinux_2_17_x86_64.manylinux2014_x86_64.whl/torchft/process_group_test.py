# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import gc
import io
import multiprocessing
import os
import unittest
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from datetime import timedelta
from typing import Any, Dict, Tuple, cast
from unittest import TestCase, skipUnless
from unittest.mock import Mock

import torch
import torch.distributed as dist
from torch import nn
from torch._C._distributed_c10d import (
    AllgatherOptions,
    AllreduceCoalescedOptions,
    AllreduceOptions,
    AllToAllOptions,
    BarrierOptions,
    BroadcastOptions,
    ReduceOp,
    ReduceScatterOptions,
    _resolve_process_group,
)
from torch.distributed import (
    ReduceOp,
    TCPStore,
    Work,
    _functional_collectives,
    get_world_size,
)
from torch.distributed.device_mesh import init_device_mesh

from torchft.manager import Manager
from torchft.process_group import (
    ErrorSwallowingProcessGroupWrapper,
    ManagedProcessGroup,
    ProcessGroup,
    ProcessGroupBabyGloo,
    ProcessGroupBabyNCCL,
    ProcessGroupDummy,
    ProcessGroupGloo,
    ProcessGroupNCCL,
    ProcessGroupWrapper,
    _DummyWork,
    _ErrorSwallowingWork,
    _ManagedWork,
    extend_device_mesh,
    ft_init_device_mesh,
)


def dummy_init_pg() -> None:
    if not dist.is_initialized():
        dist.init_process_group(
            backend="gloo", rank=0, world_size=1, store=dist.HashStore()
        )


def _test_pg(
    pg: ProcessGroup,
    example_tensor: torch.Tensor = torch.randn((2, 3), dtype=torch.float32),
) -> Dict[str, dist._Work]:
    """
    Helper function to test a set of collective operations on a given process group.
    """

    shape: torch.Size = example_tensor.shape
    dtype: torch.dtype = example_tensor.dtype

    # Create some dummy tensors for testing
    input_tensor = example_tensor.clone()
    output_tensors = [
        [torch.empty_like(input_tensor) for _ in range(get_world_size(pg))]
    ]
    tensor_list = [torch.empty_like(input_tensor)]

    def check_tensors(arg: Any) -> None:  # pyre-ignore[2]
        """Recursively check tensors for expected shape and dtype."""
        if isinstance(arg, torch.Tensor):
            assert arg.dtype == dtype, f"Output dtype mismatch: {arg.dtype} != {dtype}"
            assert arg.shape == shape, f"Output shape mismatch: {arg.shape} != {shape}"
        elif isinstance(arg, (list, tuple)):
            for item in arg:
                check_tensors(item)

    # Test collectives. send/recv require multiple processes to test, so we skip them here
    collectives = [
        ("allreduce", ([input_tensor], AllreduceOptions())),
        ("allreduce", ([input_tensor], ReduceOp.SUM)),
        ("allreduce_coalesced", ([input_tensor], AllreduceCoalescedOptions())),
        ("allgather", (output_tensors, [input_tensor], AllgatherOptions())),
        (
            "alltoall_base",
            (
                output_tensors[0][0],
                input_tensor,
                [input_tensor.shape[0]],
                [input_tensor.shape[0]],
                AllToAllOptions(),
            ),
        ),
        ("barrier", (BarrierOptions(),)),
        ("broadcast", (tensor_list, BroadcastOptions())),
        ("broadcast_one", (input_tensor, 0)),
        (
            "reduce_scatter",
            (output_tensors[0], [[input_tensor]], ReduceScatterOptions()),
        ),
    ]
    works: Dict[str, dist._Work] = {}

    for coll_str, args in collectives:
        try:
            coll = getattr(pg, coll_str)
            work = coll(*args)
            works[coll_str] = work
            work.wait()
            fut = work.get_future()
            fut.wait()
            # Check that all tensor arguments have the expected shapes and dtypes
            check_tensors(args)
        except RuntimeError as e:
            if f"does not support {coll_str}" in str(e):
                # Skip collectives that are not supported by the backend.
                continue
            raise e

    print(works)
    return works


def _test_multi_pg(pg: ProcessGroup, rank: int, tensor: torch.Tensor) -> None:
    """
    Helper function to test a set of collective operations in settings with multiple
    process groups.
    """
    # Test allgather
    tensor_list = [
        torch.zeros(2, dtype=torch.int64, device=tensor.device) for _ in range(2)
    ]
    allgather_tensor = (
        torch.arange(2, dtype=torch.int64, device=tensor.device) + 1 + 2 * rank
    )
    allgather_work = pg.allgather([tensor_list], [allgather_tensor], AllgatherOptions())
    allgather_work.wait()
    torch.testing.assert_close(
        tensor_list[0], torch.tensor([1, 2], device=tensor.device)
    )
    torch.testing.assert_close(
        tensor_list[1], torch.tensor([3, 4], device=tensor.device)
    )

    # Test allreduce
    tc = tensor.clone()
    allreduce_work = pg.allreduce([tc], ReduceOp.SUM)
    allreduce_work.wait()
    expected_tensor = torch.tensor([3], device=tc.device)
    torch.testing.assert_close(tc, expected_tensor)

    # Test allreduce_coalesced
    tensors = [tensor.clone(), tensor.clone() + 1]
    allreduce_coalesced_work = pg.allreduce_coalesced(
        tensors, AllreduceCoalescedOptions()
    )
    allreduce_coalesced_work.wait()
    torch.testing.assert_close(tensors[0], torch.tensor([3], device=tensor.device))
    torch.testing.assert_close(tensors[1], torch.tensor([5], device=tensor.device))

    # Test all-to-all
    input_tensor = torch.tensor([rank + 1, rank + 5], device=tensor.device)
    output_tensor = torch.empty_like(input_tensor)
    alltoall_work = pg.alltoall_base(
        output_tensor, input_tensor, [1, 1], [1, 1], AllToAllOptions()
    )
    alltoall_work.wait()
    if rank == 0:
        expected_alltoall = torch.tensor([1, 2], device=tensor.device)
    else:
        expected_alltoall = torch.tensor([5, 6], device=tensor.device)
    torch.testing.assert_close(output_tensor, expected_alltoall)

    # Test broadcast
    broadcast_tensor = tensor.clone() if rank == 0 else torch.zeros_like(tensor)
    broadcast_work = pg.broadcast([broadcast_tensor], BroadcastOptions())
    broadcast_work.wait()
    expected_broadcast = torch.tensor([1], device=tensor.device)
    torch.testing.assert_close(broadcast_tensor, expected_broadcast)

    # Test broadcast_one
    broadcast_one_tensor = tensor.clone() if rank == 0 else torch.zeros_like(tensor)
    broadcast_one_work = pg.broadcast_one(broadcast_one_tensor, 0)
    broadcast_one_work.wait()
    torch.testing.assert_close(
        broadcast_one_tensor, torch.tensor([1], device=tensor.device)
    )

    # Test barrier
    barrier_work = pg.barrier(BarrierOptions())
    barrier_work.wait()

    # Test send/recv
    if rank == 0:
        send_tensor = tensor.clone()
        send_work = pg.send([send_tensor], 1, 0)
        send_work.wait()
    else:
        recv_tensor = torch.zeros_like(tensor)
        recv_work = pg.recv([recv_tensor], 0, 0)
        recv_work.wait()
        expected = torch.tensor([1], device=tensor.device)
        torch.testing.assert_close(recv_tensor, expected)

    # Test reduce_scatter
    if tensor.device.type == "cuda":
        # reduce scatter not supported on GLOO
        input_tensors = [
            torch.tensor(
                [rank + 1, rank + 3], device=tensor.device, dtype=torch.float32
            ),
            torch.tensor(
                [rank + 5, rank + 7], device=tensor.device, dtype=torch.float32
            ),
        ]
        output_tensor = torch.empty(2, device=tensor.device)
        reduce_scatter_work = pg.reduce_scatter(
            [output_tensor], [input_tensors], ReduceScatterOptions()
        )
        reduce_scatter_work.wait()
        # Input tensors become:
        # rank 0: [[1, 3], [5, 7]]
        # rank 1: [[2, 4], [6, 8]]
        # Therefore expected outputs are:
        # rank 0: [1 + 2 = 3, 3 + 4 = 7]
        # rank 1: [5 + 6 = 11, 7 + 8 = 15]
        if rank == 0:
            expected_reduce_scatter = torch.tensor(
                [3, 7], device=tensor.device, dtype=torch.float32
            )
        else:
            expected_reduce_scatter = torch.tensor(
                [11, 15], device=tensor.device, dtype=torch.float32
            )
        torch.testing.assert_close(output_tensor, expected_reduce_scatter)


class ProcessGroupTest(TestCase):
    def test_gloo(self) -> None:
        store = TCPStore(
            host_name="localhost", port=0, is_master=True, wait_for_workers=False
        )

        store_addr = f"localhost:{store.port}/prefix"
        pg = ProcessGroupGloo()
        pg.configure(store_addr, 0, 1)

        self.assertEqual(pg.size(), 1)

        _test_pg(pg)

        m = nn.Linear(3, 4)
        m = torch.nn.parallel.DistributedDataParallel(m, process_group=pg)
        m(torch.rand(2, 3))

    def test_gloo_timeout(self) -> None:
        store = TCPStore(
            host_name="localhost", port=0, is_master=True, wait_for_workers=False
        )

        store_addr = f"localhost:{store.port}/prefix"
        pg = ProcessGroupGloo(timeout=timedelta(seconds=0.01))
        with self.assertRaisesRegex(
            RuntimeError, "(timeout after 10ms|Socket Timeout)"
        ):
            pg.configure(store_addr, 0, 2)

    # pyre-fixme[56]: Pyre was not able to infer the type of argument
    @skipUnless(torch.cuda.is_available(), "needs CUDA")
    def test_nccl(self) -> None:
        store = TCPStore(
            host_name="localhost", port=0, is_master=True, wait_for_workers=False
        )
        device = "cuda"

        store_addr = f"localhost:{store.port}/prefix"
        pg = ProcessGroupNCCL()
        pg.configure(store_addr, 0, 1)

        self.assertEqual(pg.size(), 1)

        _test_pg(pg, torch.tensor([2], device=device))

        m = nn.Linear(3, 4).to(device)
        m = torch.nn.parallel.DistributedDataParallel(m, process_group=pg)
        m(torch.rand(2, 3, device=device))

        # reconfigure
        store_addr = f"localhost:{store.port}/prefix2"
        pg.configure(store_addr, 0, 1)

        _test_pg(pg, torch.tensor([2], device=device))

        torch.cuda.synchronize()

    def test_baby_gloo(self) -> None:
        store = TCPStore(
            host_name="localhost", port=0, is_master=True, wait_for_workers=False
        )

        store_addr: str = f"localhost:{store.port}/prefix"

        def run(rank: int, store_addr: str = store_addr) -> None:
            pg = ProcessGroupBabyGloo()
            pg.configure(store_addr, rank, 2)

            self.assertEqual(pg.size(), 2)

            tensor = torch.tensor([rank + 1])
            _test_multi_pg(pg, rank, tensor)

        with ThreadPoolExecutor(max_workers=2) as executor:
            a_fut = executor.submit(run, 0)
            b_fut = executor.submit(run, 1)

        a_fut.result()
        b_fut.result()

    def test_baby_gloo_timeout(self) -> None:
        store = TCPStore(
            host_name="localhost", port=0, is_master=True, wait_for_workers=False
        )

        store_addr = f"localhost:{store.port}/prefix"

        a = ProcessGroupBabyGloo(timeout=timedelta(seconds=0.01))
        with self.assertRaisesRegex(TimeoutError, "timed out after 0.01 seconds"):
            a.configure(store_addr, 0, 2)

    def test_reconfigure_baby_process_group(self) -> None:
        store = TCPStore(
            host_name="localhost", port=0, is_master=True, wait_for_workers=False
        )
        store_addr = f"localhost:{store.port}/prefix"

        a = ProcessGroupBabyGloo()
        a.configure(store_addr, 0, 1)
        future_thread_1 = a._future_thread
        future_queue_1 = a._future_queue
        p_1 = a._p

        store_addr = f"localhost:{store.port}/prefix2"
        a.configure(store_addr, 0, 1)
        future_thread_2 = a._future_thread
        future_queue_2 = a._future_queue
        p_2 = a._p

        self.assertNotEqual(future_thread_1, future_thread_2)
        self.assertNotEqual(future_queue_1, future_queue_2)
        self.assertNotEqual(p_1, p_2)

        assert future_thread_1 is not None
        self.assertFalse(future_thread_1.is_alive())
        assert future_queue_1 is not None
        self.assertTrue(future_queue_1.closed())
        assert p_1 is not None
        self.assertFalse(p_1.is_alive())

        assert future_thread_2 is not None
        self.assertTrue(future_thread_2.is_alive())
        assert future_queue_2 is not None
        self.assertFalse(future_queue_2.closed())
        assert p_2 is not None
        self.assertTrue(p_2.is_alive())

    def test_baby_gloo_apis(self) -> None:
        store = TCPStore(
            host_name="localhost", port=0, is_master=True, wait_for_workers=False
        )

        store_addr = f"localhost:{store.port}/prefix"

        a = ProcessGroupBabyGloo(timeout=timedelta(seconds=10))
        a.configure(store_addr, 0, 1)

        _test_pg(a)

        # force collection to ensure no BabyWork objects remain
        gc.collect()

        self.assertEqual(a.num_active_work(), 0)

    # pyre-fixme[56]: Pyre was not able to infer the type of argument
    @skipUnless(torch.cuda.is_available(), "needs CUDA")
    def test_baby_nccl_apis(self) -> None:
        # set to 1 if more than >=2 gpus
        device_id = 1 % torch.cuda.device_count()
        torch.cuda.set_device(device_id)

        store = TCPStore(
            host_name="localhost", port=0, is_master=True, wait_for_workers=False
        )

        store_addr = f"localhost:{store.port}/prefix"

        a = ProcessGroupBabyNCCL(timeout=timedelta(seconds=10))
        try:
            a.configure(store_addr, 0, 1)

            _test_pg(a, torch.randn((2, 3), device="cuda"))

            torch.cuda.synchronize()

            # force collection to ensure no BabyWork objects remain
            gc.collect()

            self.assertEqual(a.num_active_work(), 0)
        finally:
            a.shutdown()
            torch.cuda.synchronize()
            torch.cuda.empty_cache()

    def test_dummy(self) -> None:
        pg = ProcessGroupDummy(0, 1)
        m = nn.Linear(3, 4)
        m = torch.nn.parallel.DistributedDataParallel(m, process_group=pg)
        m(torch.rand(2, 3))

    # pyre-fixme[56]: Pyre was not able to infer the type of argument
    @skipUnless(torch.cuda.device_count() >= 2, "need two CUDA devices")
    def test_baby_nccl_2gpu(self) -> None:
        store = TCPStore(
            host_name="localhost", port=0, is_master=True, wait_for_workers=False
        )

        store_addr: str = f"localhost:{store.port}/prefix"

        def run(rank: int) -> ProcessGroupBabyNCCL:
            a = ProcessGroupBabyNCCL(
                timeout=timedelta(seconds=10.0),
            )
            a.configure(store_addr, rank, 2)
            self.assertEqual(a.size(), 2)

            # We test using set_device to ensure stream device is correct.
            torch.cuda.set_device(rank)
            at = torch.tensor([rank + 1], device="cuda")
            try:
                _test_multi_pg(a, rank, at)
            finally:
                a.shutdown()
            return a

        with ThreadPoolExecutor(max_workers=2) as executor:
            a_fut = executor.submit(run, 0)
            b_fut = executor.submit(run, 1)

        a = a_fut.result()
        b = b_fut.result()

        # cleanup
        torch.cuda.synchronize()
        torch.cuda.empty_cache()

    def test_device_mesh(self) -> None:
        os.environ["MASTER_ADDR"] = "localhost"
        os.environ["MASTER_PORT"] = str(0)
        os.environ["RANK"] = str(0)
        os.environ["WORLD_SIZE"] = str(1)

        mesh_1d = init_device_mesh("cpu", mesh_shape=(1,), mesh_dim_names=("tp",))

        store = TCPStore(
            host_name="localhost", port=0, is_master=True, wait_for_workers=False
        )
        store_addr = f"localhost:{store.port}/prefix"

        pg = ProcessGroupGloo()
        pg.register("test_device_mesh")
        pg.configure(store_addr, 0, 1)

        mesh_2d = extend_device_mesh(mesh_1d, pg)
        mesh_2d.get_group("dp")
        assert mesh_2d.ndim == 2

        pg.unregister()

    def test_functional_collectives(self) -> None:
        dummy_init_pg()

        store = TCPStore(
            host_name="localhost", port=0, is_master=True, wait_for_workers=False
        )
        store_addr = f"localhost:{store.port}/prefix"

        pg = ProcessGroupGloo().register("test_func_col")
        pg.configure(store_addr, 0, 1)

        self.assertEqual(pg.group_name, str(dist.get_pg_count() - 1))

        self.assertIs(_resolve_process_group(pg.group_name), pg)

        try:
            t = torch.zeros(10)
            _functional_collectives.all_reduce(t, "sum", pg).wait()
        finally:
            pg.unregister()

    def test_process_group_wrapper(self) -> None:
        pg = ProcessGroupDummy(0, 1)
        wrapper = ProcessGroupWrapper(pg)
        self.assertIs(wrapper.parent, pg)

        wrapper.configure("addr", 0, 1)
        self.assertEqual(pg.configure_count, 1)

        self.assertEqual(repr(wrapper), "ProcessGroupWrapper(pg=ProcessGroupDummy())")

    def test_error_swallowing_process_group_wrapper(self) -> None:
        pg = ProcessGroupDummy(0, 1)
        wrapper = ErrorSwallowingProcessGroupWrapper(pg)
        self.assertIs(wrapper.parent, pg)

        works = _test_pg(wrapper)
        self.assertIsInstance(list(works.values())[0], _ErrorSwallowingWork)

        err = RuntimeError("test")
        wrapper.report_error(err)
        self.assertEqual(wrapper.error(), err)

        works = _test_pg(wrapper)
        for work in works.values():
            self.assertIsInstance(work, _DummyWork)

    def test_managed_process_group(self) -> None:
        manager = Mock(spec=Manager)
        manager.errored.return_value = None
        manager._pg = ProcessGroupDummy(0, 1)
        pg = ManagedProcessGroup(manager)
        manager.num_participants.return_value = 123

        self.assertEqual(pg.size(), 123)

        works = _test_pg(pg)
        self.assertIsInstance(list(works.values())[0], _ManagedWork)

        self.assertEqual(manager.report_error.call_count, 0)
        self.assertEqual(manager.wrap_future.call_count, 2)
        self.assertEqual(manager.wait_quorum.call_count, 2)


class DeviceMeshTest(TestCase):
    @staticmethod
    def _test_init_device_mesh(world_size: int, rank: int) -> None:
        os.environ["MASTER_ADDR"] = "127.0.0.1"
        os.environ["MASTER_PORT"] = str(12346)
        os.environ["RANK"] = str(rank)
        os.environ["WORLD_SIZE"] = str(4)

        testcase = TestCase()

        manager = Mock(spec=Manager)
        # Even though we only have 4 workers, we can still initialize (2, 4) mesh.
        # That's because the replicate group is NOT phystically created in the
        # real mesh but is virtually added to the mesh via ManagedDeviceMesh.
        device_mesh = ft_init_device_mesh(
            device_type="cpu",
            mesh_shape=(2, world_size),
            mesh_dim_names=("dp_replicate", "dp_shard"),
            replicate_dim=0,
            manager=manager,
        )

        testcase.assertTrue(
            isinstance(device_mesh.get_group("dp_replicate"), ManagedProcessGroup)
        )
        testcase.assertTrue(
            not isinstance(device_mesh.get_group("dp_shard"), ManagedProcessGroup)
        )
        replicate_group = device_mesh.get_group("dp_replicate")
        testcase.assertEqual(
            cast(ManagedProcessGroup, replicate_group)._manager, manager
        )
        replicate_mesh = device_mesh["dp_replicate"]
        testcase.assertEqual(replicate_mesh.get_group(), replicate_group)
        flatten_mesh = device_mesh._flatten("dp")
        manager.num_participants.return_value = 1
        testcase.assertEqual(flatten_mesh.size(), world_size)
        testcase.assertEqual(flatten_mesh.get_local_rank(), dist.get_rank())

    def test_init_device_mesh(self) -> None:
        with ProcessPoolExecutor(max_workers=4) as executor:
            futures = []
            for i in range(4):
                future = executor.submit(self._test_init_device_mesh, 4, i)
                futures.append(future)
