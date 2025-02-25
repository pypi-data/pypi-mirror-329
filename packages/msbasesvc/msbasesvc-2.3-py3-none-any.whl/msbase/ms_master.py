import multiprocessing
import os
import signal
import time
from typing import Optional, Dict, List

from .ms_base import LOG, MSNacosClient
from .ms_variables import (
    ns_server_addr,
    ns_server_ns,
    ms_service_name,
    ms_service_team,
    ms_instance_addr,
    ms_service_offline_survival,
    worker_reboot_threshold as reboot_wc,
    ms_unix_sock_dir,
)
from .ms_worker import MSWorker


# noinspection PyBroadException
class MSMaster(object):

    def __init__(self, worker_cnt: int, worker_listen: int, uds: bool = False):
        self.at_work: bool = False  # 是否在工作中
        self.worker_num: int = worker_cnt
        self.worker_listen: int = worker_listen  # 端口
        self.workers: Dict[str, MSWorker] = {}
        self.shared_value = multiprocessing.Manager().dict()
        self.uds: bool = uds

        self.sock_dir: str = f'{ms_unix_sock_dir}/{ms_service_name}'
        os.makedirs(self.sock_dir, exist_ok=True)

        self.binds: List[str] = []
        for i in range(self.worker_num):
            bind = self.worker_listen + (i + 1)
            self.binds.append(f'unix://{self.sock_dir}/{bind}.sock' if self.uds else f'[::]:{bind}')

    def start_worker(self, worker: MSWorker) -> None:
        if worker.start_worker().started():
            self.workers[worker.name] = worker
            if reboot_wc > 0:
                self.shared_value[worker.pid] = 0

    def start_workers(self) -> None:
        for i, bind in enumerate(self.binds):
            self.start_worker(MSWorker(i, bind, self.shared_value))

        if len(self.workers) != self.worker_num:
            self.shutdown_workers()
            LOG.error(f'****** 存在启动失败的工作进程, 主进程退出 ******\n')
            raise RuntimeError('Not All Worker Started')
        self.at_work = True

    def wait_for_workers(self) -> None:
        #  监听停止信号
        [signal.signal(si, self.set_workers_shutdown) for si in [signal.SIGTERM, signal.SIGINT]]

        ms_nc = MSNacosClient(
            server_addr=ns_server_addr,
            server_ns=ns_server_ns,
            service_name=ms_service_name,
            service_team=ms_service_team,
            instance_addr=ms_instance_addr,
            instance_listen=self.worker_listen,
            ms_sos=ms_service_offline_survival,
            obtain_data=False,
        )
        try:
            ms_nc.register_instance()  # 注册服务

            err_worker: Optional[MSWorker] = None
            while self.at_work and MSMaster._wait_(8):
                if err_worker and err_worker.killed():
                    LOG.error(
                        f'ErrorWorker Shutdown End !!!, {err_worker}, {err_worker.pid}:{err_worker.work_times()}, '
                        f'{self.shared_value}'
                    )
                    self.start_worker(err_worker.new_worker())
                    err_worker = None
                    continue

                #  检查 Worker 的状态, 判断是否需要重启
                for cur_worker in self.workers.values():
                    if not self.at_work:
                        break

                    wc = cur_worker.work_times()
                    if (wc > reboot_wc > 0 or not cur_worker.is_alive()) and err_worker is None:
                        LOG.error(f'ErrorWorker BEGIN Shutdown, {cur_worker}, WC: {wc}')
                        cur_worker.shutdown()
                        err_worker = cur_worker
        finally:
            ms_nc.deregister_instance()  # 注销服务
            self.shutdown_workers()

    def shutdown_workers(self) -> None:
        LOG.error(f'****** 开始停止所有工作进程 ******')
        [w.shutdown() for w in self.workers.values()]

        [w.wait_for() for w in self.workers.values()]
        LOG.error(f'****** 所有工作进程正常退出 ******')

    def set_workers_shutdown(self, s, f) -> None:
        LOG.error(f'****** 监听到主进程停止信号: {s} ******\n{f}')
        self.at_work = False

    @staticmethod
    def _wait_(t) -> bool:
        try:
            time.sleep(t)
        except:
            pass
        return True
