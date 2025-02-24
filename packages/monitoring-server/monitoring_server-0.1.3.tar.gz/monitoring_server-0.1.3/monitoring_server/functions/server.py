import platform
import shutil
import psutil
from invoke import Context


def shutdown():
    context = Context()
    try:
        system = platform.system()
        if system == "Windows":
            context.run("shutdown -s -t 0", hide=True)
        else:
            context.run("shutdown now", hide=True)
    except Exception as e:
        return f'Error shutting down: {str(e)}'

def get_hardware_consumtion():
    disks = {}
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
        disks[partition.mountpoint] = {
            'fstype': partition.fstype,
            'total': round(usage.total / factor, 2),
            'used': round(usage.used / factor, 2),
            'free': round(usage.free / factor, 2),
            'percent': usage.percent,
            'unit': 'GB'
        }
        total_disk_free += disks[partition.mountpoint]['free']
        total_disk_used += disks[partition.mountpoint]['used']
        total_disk_space += disks[partition.mountpoint]['total']

    disks['total'] = {
        'total': round(total_disk_space, 2),
        'used': round(total_disk_used, 2),
        'free': round(total_disk_free, 2),
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
 
"""
def copy_file_to_server(local_file_path: str = "", server_file_path: str = "/"):

    try:
        shutil.copy2(local_file_path, server_file_path)
        return 'File successfully copied to the server'

    except shutil.Error as e:
        return f'Error copying the file: {str(e)}'
    except IOError as e:
        return f'I/O Error: {str(e)}'
"""