import json
import logging
import multiprocessing
import os
import random
import subprocess
import sys
import threading
import time
import traceback
from datetime import datetime
from typing import List

import httpx
import nacos
import pytz
import yaml
from loguru import logger
from snowflake import SnowflakeGenerator

from .ms_variables import (
    ms_hostname,
    ns_server_addr,
    ns_server_ns,
    ms_service_name,
    ms_service_team,
    ms_instance_addr,
    ms_instance_listen,
    ms_service_offline_survival,
    snowflake_worker_id,
    NGINX_CONF_D_DIR,
)

httpx_logger = logging.getLogger("httpx")
if httpx_logger:
    httpx_logger.setLevel(logging.ERROR)

nacos_logger = logging.getLogger("nacos")
if nacos_logger:
    nacos_logger.setLevel(logging.ERROR)


def _init_ms_():
    log_dir = './logs/' + ms_hostname + '/'
    os.makedirs(name=log_dir, exist_ok=True)

    log_file = ms_service_name + '.{time:YYYY-MM-DD}.log'
    ms_format = (
        "<green>{time}</green> | <level>{level: <6}</level> | {process.id}@{process.name} | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | {extra[trace_id]} | - "
        "<level>{message}</level>"
    )

    logger.remove()
    logger.configure(extra={'trace_id': '_'})
    logger.add(log_dir + log_file, format=ms_format, rotation='00:00', retention='7 weeks', enqueue=True)
    logger.add(sys.stderr, format=ms_format)
    # logger.add(sys.stdout, format=ms_format)

    return logger


LOG = _init_ms_()

# 各个国家对应的时区
CC_TIMEZONE = {
    "UTC": "UTC",
    "MX": "America/Lima",
    "CO": "America/Bogota",
    "PE": "America/Lima",
    "CL": "America/Santiago",
    "PK": "Asia/Karachi"
}


def cc_now(cc: str) -> str:
    """
    将当前UTC时间对象转换成指定国家对应的时区的时间字符串
    """
    country_time = datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(pytz.timezone(CC_TIMEZONE[cc]))
    return country_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


# 雪花算法初始化
class MSSnowflake:

    def __init__(self, worker_id):
        self.ms_snowflake = SnowflakeGenerator(
            instance=int(str(sum(ord(c) for c in ms_hostname)) + str(os.getpid())) % 32,  # 使用主机名作为实例ID不会重复
            seq=worker_id % 1024,
            epoch=1288834974657,  # 固定值不要变更
        )

    def __call__(self) -> int:
        return next(self.ms_snowflake)


# noinspection PyBroadException
def _wait_(t):
    try:
        time.sleep(t)
    except:
        pass


# noinspection PyBroadException
class MSNacosClient:

    def __init__(self,
                 server_addr,
                 server_ns,
                 service_name,
                 service_team,
                 instance_addr,
                 instance_listen,
                 ms_sos,
                 obtain_data: bool,
                 ):
        self._nc_ = nacos.NacosClient(server_addresses=server_addr, namespace=server_ns)
        self.server_addr = server_addr
        self.server_ns = server_ns
        self.service_name = service_name
        self.service_team = service_team

        self.ns_data = None
        if obtain_data is True:
            ms_data = self._nc_.get_config(data_id=service_name, group=service_team, timeout=3)
            if ms_data:
                self.ns_data = json.loads(json.dumps(yaml.safe_load(ms_data)))

        self._hb_state_: bool = True
        self.instance_addr = instance_addr
        self.instance_listen = instance_listen
        self.ms_sos = ms_sos
        self.desc_name = f'{self.instance_addr}:{self.instance_listen}@{self.service_name}'

        self.serv_data = {
            'service_name': self.service_name, 'ip': self.instance_addr, 'port': self.instance_listen,
            'cluster_name': 'DEFAULT', 'group_name': self.service_team, 'enable': True,
            'metadata': {'hn': f'{multiprocessing.current_process().name}@{ms_hostname}', 'RPC': 'GRPC'},
        }

    def register_instance(self) -> None:
        LOG.info(f'****** 开始服务注册[ {self.desc_name} ] ******')

        # 注册服务
        self.serv_data['metadata']['rt'] = datetime.utcnow().strftime('[%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z]'
        if not self._nc_.add_naming_instance(**self.serv_data):
            raise RuntimeError(f'****** 服务注册失败[ {self.desc_name} ] ******')

        LOG.info(f'****** 服务注册成功[ {self.desc_name} ] ******')

        # 发送心跳
        def run():
            hclient = httpx.Client(
                http2=True,
                timeout=httpx.Timeout(connect=3, read=30, write=30, pool=1, ),
                limits=httpx.Limits(max_keepalive_connections=1, max_connections=64, keepalive_expiry=60, ),
            )
            hb_suc = False
            while self._hb_state_:
                try:
                    shbr = hclient.put(
                        url=f'http://{self.server_addr}/nacos/v1/ns/instance/beat',
                        params={
                            'serviceName': self.service_name, 'ip': self.instance_addr, 'port': self.instance_listen,
                            'namespaceId': self.server_ns, 'groupName': self.service_team, 'clusterName': 'DEFAULT',
                        },
                    )
                    if not hb_suc and shbr.status_code == 200:
                        hb_suc = True
                        LOG.info(f"****** 心跳正常: {shbr.text} ******")
                except:
                    hb_suc = False
                    LOG.error(f'****** 心跳异常 ******: {traceback.format_exc()}')
                finally:
                    _wait_(round(random.uniform(3, 6), 1) if hb_suc else 1)
            self.__remove_instance()

        t = threading.Thread(target=run)
        t.daemon = True
        t.start()

    def deregister_instance(self) -> None:
        self._hb_state_ = False
        LOG.error(f'****** 开始注销服务[ {self.desc_name} ] ******')
        self.__remove_instance()
        LOG.error(f'****** 结束注销服务[ {self.desc_name} ] ******')

        LOG.error(f'****** 服务注销后等待{self.ms_sos}秒 ******')
        _wait_(self.ms_sos)  # 等待一段时间, 防止刚刚注销后还有流量进入

    def __remove_instance(self) -> None:
        try:
            if self.serv_data.get('enable'):
                del self.serv_data['enable']

            if self.serv_data.get('metadata'):
                del self.serv_data['metadata']

            self._nc_.remove_naming_instance(**self.serv_data)  # 注销服务
        except:
            pass


_MS_SNOWFLAKE_ = MSSnowflake(snowflake_worker_id)


def next_id() -> int:
    return _MS_SNOWFLAKE_()


def ns_data():
    return MSNacosClient(
        server_addr=ns_server_addr,
        server_ns=ns_server_ns,
        service_name=ms_service_name,
        service_team=ms_service_team,
        instance_addr=ms_instance_addr,
        instance_listen=ms_instance_listen,
        ms_sos=ms_service_offline_survival,
        obtain_data=True,
    ).ns_data


def cost_ms(s):
    return round((time.time() - s) * 1000, 3)


def enable_load_balancer(listen: int, binds: List[str]):
    """
    通过 NGINX 对服务负载均衡
    """
    services: str = ''.join(f'    server {bind};{os.linesep}' for bind in binds)
    server_confs: str = f"""
upstream services {{
{services.rstrip(os.linesep)}
}}

server {{
    listen    {listen} http2;
    location / {{
        grpc_pass grpc://services;
    }}
}}
"""
    with open(f'{NGINX_CONF_D_DIR}/BASE_{ms_service_name}.conf', 'w') as f:
        f.write(server_confs + os.linesep)
    LOG.info(f'NGINX GRPC Server Load Banlance Conf:\n {server_confs}')
    nx_cmd: str = 'NGINX'.lower()
    try:
        subprocess.run([nx_cmd], check=True)  # 尝试启动 NGINX 进程
    except subprocess.CalledProcessError:
        LOG.warning(traceback.format_exc())
        subprocess.run([nx_cmd, '-s', 'reload'], check=True)
