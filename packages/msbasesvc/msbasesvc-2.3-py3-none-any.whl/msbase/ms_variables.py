import os
import socket

from ZMS_Starter import MS_ENV_PROFILES

# ======================================================================================================================
ACTIVED_ENV: str = os.getenv('MS_ACTIVE')  # EG: msdeve, mstest, mslive
if not ACTIVED_ENV or len(ACTIVED_ENV) != 6:
    raise ValueError('Env "MS_ACTIVE" Error')

CurrentProfile = MS_ENV_PROFILES[ACTIVED_ENV.upper()]
CurrentProfile['worker_reboot_threshold'] = CurrentProfile.get('worker_reboot_threshold', 0)
CurrentProfile['unix_sock_dir'] = CurrentProfile.get('unix_sock_dir', '/var/run')
CurrentProfile['NGINX_CONF_D_DIR'] = CurrentProfile.get('NGINX_CONF_D_DIR', '/etc/nginx/conf.d')

for k, v in CurrentProfile.items():  # 配置文件参数校验
    env_value = os.getenv(f'{ACTIVED_ENV}_{k}')
    if env_value is not None:
        CurrentProfile[k] = env_value  # 系统环境变量优先
    if CurrentProfile[k] is None:
        raise ValueError(f'"{k}" Value Error')

ns_server_addr: str = CurrentProfile['nacos_server_addr']
assert len(ns_server_addr) > 0

ns_server_ns: str = CurrentProfile['nacos_server_ns']
assert len(ns_server_ns) > 0

ms_service_team: str = CurrentProfile['service_team']
assert len(ms_service_team) > 0

ms_service_name: str = CurrentProfile['service_name']
assert len(ms_service_name) > 0

host_addr = os.getenv("HOST_IP")
ms_instance_addr: str = host_addr if host_addr else socket.gethostbyname(socket.gethostname())
assert len(ms_instance_addr) > 0

ms_instance_listen: int = CurrentProfile['service_port']
assert ms_instance_listen > 0

ms_service_offline_survival: int = CurrentProfile['service_offline_survival']
assert ms_service_offline_survival >= 0

ms_hostname: str = socket.gethostname()
assert len(ms_hostname) > 0

snowflake_worker_id: int = CurrentProfile['snowflake_worker_id']
assert snowflake_worker_id > 0

worker_num: int = CurrentProfile['worker_num']
assert worker_num > 0

worker_reboot_threshold: int = CurrentProfile['worker_reboot_threshold']
assert snowflake_worker_id >= 0

ms_unix_sock_dir: str = CurrentProfile['unix_sock_dir']
NGINX_CONF_D_DIR: str = CurrentProfile['NGINX_CONF_D_DIR']
# ======================================================================================================================
