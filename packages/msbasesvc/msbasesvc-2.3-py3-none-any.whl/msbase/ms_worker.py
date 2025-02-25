import multiprocessing
import os
import time
import traceback
import uuid
from typing import Optional

import grpc
from grpc_health.v1 import health_pb2_grpc, health_pb2
from grpc_interceptor import ServerInterceptor
from grpc_reflection.v1alpha import reflection

from ZMS_Starter import _init_server_
from .ms_base import LOG, cost_ms
from .ms_variables import (
    ms_service_offline_survival,
    worker_reboot_threshold,
)


class MSHealthService(health_pb2_grpc.HealthServicer):

    def Check(self, request, context):
        return health_pb2.HealthCheckResponse(status=health_pb2.HealthCheckResponse.SERVING)


class MSTraceIdInterceptor(ServerInterceptor):

    def __init__(self, shared_value):
        super().__init__()
        self.shared_value = shared_value
        self.health_methods = ['/grpc.health.v1.Health/Check']
        self.state = worker_reboot_threshold > 0

    def intercept(self, method, request_or_iterator, context, method_name):
        metadata_dict = dict(context.invocation_metadata())
        trace_id = metadata_dict.get('MS-REQUEST-ID'.lower(), '')
        ua = metadata_dict.get('USER-AGENT'.lower(), '')
        with LOG.contextualize(trace_id=trace_id):
            fix = f'"{str(context.peer()).upper()}" "{ua}" "{method_name}"'
            LOG.info(f'开始: {fix}')
            s = time.time()

            curr_id = os.getpid()
            try:
                res = method(request_or_iterator, context)
                if self.has_shared_value(curr_id) and method_name not in self.health_methods:
                    self.shared_value[curr_id] += 1
            except:
                LOG.error(traceback.format_exc())
                raise
            finally:
                LOG.info(f'结束: {fix}, 耗时: {cost_ms(s)}ms, times: {self.read_shared_value(curr_id)}')
            return res

    def has_shared_value(self, curr_id) -> bool:
        return self.state and self.shared_value and curr_id in self.shared_value

    def read_shared_value(self, curr_id) -> Optional[int]:
        return self.shared_value[curr_id] \
            if self.has_shared_value(curr_id) \
            else None


# noinspection PyBroadException
class MSWorker(multiprocessing.Process):

    def __init__(self, no: int, bind: str, shared_value):
        super().__init__()
        self.daemon = True
        self.no: int = no
        self.bind: str = bind

        self.name: str = f'Worker_{self.no}'
        self.worker_id: str = f'{self.name}_{uuid.uuid4()}'
        self.shutdown_event = multiprocessing.Event()
        self.shared_value = shared_value
        self.write_worker_state(0)

    def run(self):
        try:
            #  启动服务
            serv = _init_server_()

            inters, confs = serv.get('inters', []), serv.get('confs', [])
            inters.append(MSTraceIdInterceptor(self.shared_value))

            new_server = grpc.server(thread_pool=serv['threads'], interceptors=inters, options=confs)
            health_pb2_grpc.add_HealthServicer_to_server(MSHealthService(), new_server)  # 健康检查

            add_servicer, service_name = serv['add_servicer'], serv['service_name']
            add_servicer(new_server)

            if service_name:
                reflection.enable_server_reflection(
                    (
                        reflection.SERVICE_NAME,
                        health_pb2.DESCRIPTOR.services_by_name['Health'].full_name,
                    ) + service_name,
                    new_server,
                )

            new_server.add_insecure_port(self.bind)
            new_server.start()
            LOG.info(f'****** 服务启动完成( {self.bind} ) ******')

            #  正在服务
            self.write_worker_state(1)
            try:
                self.shutdown_event.wait()
            except:
                pass
            self.write_worker_state(2)

            LOG.warning(f'****** 开始停止服务 ******')
            s = time.time()
            new_server.stop(ms_service_offline_survival).wait()
            LOG.warning(f'****** 服务正常停止 ******, 耗时: {cost_ms(s)}ms')
            self.write_worker_state(3)
        except:
            LOG.error(traceback.format_exc())
            self.write_worker_state(4)

    def start_worker(self):
        self.start()
        return self

    def started(self) -> bool:
        while self.read_worker_state() == 0:
            MSWorker._wait_(1)
        return self.read_worker_state() == 1

    def shutdown(self) -> None:
        try:
            if self.is_alive():
                self.shutdown_event.set()
        except:
            pass

    def killed(self) -> bool:
        killed_state: int = 5
        worker_state: int = self.read_worker_state()  # worker_state in [3, 4] 代表 run 函数结束
        if worker_state != killed_state and (not self.is_alive() or worker_state in [3, 4]):
            self.kill()
            worker_state = killed_state
            self.write_worker_state(worker_state)
        return worker_state == killed_state

    def wait_for(self) -> None:
        try:
            self.join()
        except:
            pass

    def work_times(self) -> int:
        return self.shared_value[self.pid] \
            if self.pid in self.shared_value \
            else 0

    def new_worker(self):
        new_worker = MSWorker(self.no, self.bind, self.shared_value)

        if self.pid in self.shared_value:
            del self.shared_value[self.pid]
        if self.worker_id in self.shared_value:
            del self.shared_value[self.worker_id]

        return new_worker

    def write_worker_state(self, state: int) -> None:
        self.shared_value[self.worker_id] = state

    def read_worker_state(self) -> int:
        return self.shared_value.get(self.worker_id)

    @staticmethod
    def _wait_(t):
        try:
            time.sleep(t)
        except:
            pass
