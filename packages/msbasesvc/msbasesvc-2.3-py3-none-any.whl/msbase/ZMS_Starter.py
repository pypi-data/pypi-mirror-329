# DEMO CONFS
MS_ENV_PROFILES = {
    'MSDEVE': {
        'nacos_server_addr': 'test-nacos.datasvc.link:80',
        'nacos_server_ns': 'MS_DEVE',
        'service_name': 'ms-base',
        'service_port': 7777,
        'service_team': 'GLOBAL',
        'service_offline_survival': 1,
        'snowflake_worker_id': 9,
        'worker_num': 1,
        'worker_reboot_threshold': 3,
        'ms_unix_sock_dir': '/var/run',
        'NGINX_CONF_D_DIR': '/etc/nginx/conf.d',
    },
}


def _init_server_():
    return {
        'threads': None,
        'confs': None,
        'add_servicer': None,
        'service_names': None,
    }
