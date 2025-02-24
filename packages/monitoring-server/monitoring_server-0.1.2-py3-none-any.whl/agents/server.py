import threading
import time
import platform
import shutil
import socket
import json
import psutil
import requests
from invoke import Context
from brokers.agent import AbstractAgent


HEADERS = {
    'Content-Type': 'application/json',
    'Secret-key': 'cloud-wfs-secret-key-2024'
}


def post_data(data, server_id):
    URL = f'http://127.0.0.1:8000/api/v1/server/{server_id}/server_consumtion/'
    # URL = f'http://54.37.15.154:8001/api/v1/server/{server_id}/server_consumtion/'
    data = json.dumps(data)
    requests.post(URL, data, headers=HEADERS)


def get_local_ip():
    """Obtiene la dirección IP de la máquina local"""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(local_ip)
    return local_ip


class ServerAgent(AbstractAgent):
    STREAM_SERVER_CONSUMTION = False
    _thread = None
    step = 1

    def __init__(self, *args, **kwargs):
        super(ServerAgent, self).__init__(*args, **kwargs)
    
    def __hardware_consumtion__(self):
        disks_list = []
        total_disk_free = 0
        total_disk_used = 0
        total_disk_space = 0
        factor = 1073741824

        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_frequency = psutil.cpu_freq(percpu=False).current
        cpu_cores = psutil.cpu_count()
        memory = psutil.virtual_memory()
        network_io = psutil.net_io_counters()

        for partition in psutil.disk_partitions():
            usage = psutil.disk_usage(partition.mountpoint)
            disks_list.append({
                'partition': partition.mountpoint[0],
                'fstype': partition.fstype,
                'total': round(usage.total / factor, 2),
                'used': round(usage.used / factor, 2),
                'free': round(usage.free / factor, 2),
                'percent': usage.percent,
                'unit': 'GB'
            })
            total_disk_free += disks_list[-1]['free']
            total_disk_used += disks_list[-1]['used']
            total_disk_space += disks_list[-1]['total']

        disks = {
            'disks': disks_list,
            'total': {
                'total': round(total_disk_space, 2),
                'used': round(total_disk_used, 2),
                'free': round(total_disk_free, 2),
            }
        }

        data = {
            'cpu': {
                'percent': cpu_usage,
                'frequency': cpu_frequency / 1000,
                'cores': cpu_cores
            },
            'memory': {
                'total': round(memory.total / factor, 2),
                'available': round(memory.available / factor, 2),
                'used': round(memory.used / factor, 2),
                'free': round(memory.free / factor, 2),
                'percent': memory.percent,
                'unit': 'GB'
            },
            'disks': disks,
            'network': {
                'sent': network_io.bytes_sent,
                'receive': network_io.bytes_recv
            }
        }
        return data
    
    def __run_hardware_consumtion__(self, data):
        # Este es el ciclo que se ejecutará en el hilo separado
        while self.STREAM_SERVER_CONSUMTION:
            print('getting hardware consumtion, data:', data)
            self.get_hardware_consumtion(data)
            time.sleep(self.step)

    def start_run(self, data):
        print("Estoy mandando la solicitud...")
        return "Hello World"

    def get_hardware_consumtion(self, data):
        self.step = data.get('step', self.step)
        server_id = data.get('id', None)
        data = self.__hardware_consumtion__()
        # print('full_data: ', data)
        post_data(data, server_id)
        return data
    
    def start_hardware_consumtion(self, data):
        print('starting consume')
        self.STREAM_SERVER_CONSUMTION = True
        if not self._thread or not self._thread.is_alive():
            if str(data['ip']) == str(get_local_ip()):
                self._thread = threading.Thread(target=self.__run_hardware_consumtion__, args=(data,))
                self._thread.start()
    
    def stop_hardware_consumtion(self, data):
        print('stop consume')
        self.STREAM_SERVER_CONSUMTION = False
        if self._thread is not None:
            if str(data['ip']) == str(get_local_ip()):
                self._thread.join()
        return data
    
    def shutdown(self, data):
        context = Context()
        try:
            system = platform.system()
            if system == "Windows":
                context.run("shutdown -s -t 0", hide=True)
            else:
                context.run("shutdown now", hide=True)
        except Exception as e:
            return f'Error shutting down: {str(e)}'
