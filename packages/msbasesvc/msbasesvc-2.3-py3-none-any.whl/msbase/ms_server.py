import json


def run_server():
    from .ms_base import LOG, enable_load_balancer
    from .ms_master import MSMaster

    from .ms_variables import ACTIVED_ENV, CurrentProfile
    LOG.info(f'MS_PROFILE: "{ACTIVED_ENV}"\n{json.dumps(CurrentProfile, indent=4)}')

    from .ms_variables import (worker_num, ms_instance_listen, )
    LOG.info(f'****** [{worker_num}] => Start Worker(s) ******')

    master = MSMaster(worker_num, ms_instance_listen, uds=True)
    master.start_workers()

    enable_load_balancer(ms_instance_listen, master.binds)

    LOG.info(f'****** [{worker_num}] => All Worker Started <= ******')
    master.wait_for_workers()
    LOG.error(f'****** 主进程正常退出 ******\n')
