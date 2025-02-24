RBMQ_CONFIG = {
    'host': '51.83.77.53',
    'port': 5672,
    'vhost': '/',
    'exchange': 'cloudwfs_server',
    'queue': 'server_consumtion',
    'routing_key': 'server_consumtion',
    'credentials': {
        'username': 'Admin',
        'password': 'adminadmin'
    }
}  # Actualizado para server monitoring


RBMQ_BACKEND_CONFIG = {
    'host': '54.36.99.208',
    'port': 5672,
    'vhost': '/',
    'exchange': 'cloudwfs_server',
    'queue': 'backend_server_consumtion',
    'routing_key': 'backend_server_consumtion',
    'credentials': {
        'username': 'Admin',
        'password': 'adminadmin'
    }
}

RBMQ_RUN_CONFIG = {
    'host': '54.36.99.208',
    'port': 5672,
    'vhost': '/',
    'exchange': 'models_run_agent',
    'queue': 'models_run',
    'routing_key': 'models_run',
    'credentials': {
        'username': 'Admin',
        'password': 'adminadmin'
    }
}