from agents.server import ServerAgent
from monitoring_server import settings

def main():
    agent = ServerAgent(**settings.RBMQ_CONFIG)
    print(f'Instancing and running {agent.name()}...')
    agent.start()

if __name__ == '__main__':
    main()