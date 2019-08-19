import sys
from fabric import *


class Server:
    def __init__(self, ip, user, password):
        self.ip = ip
        self.user = user
        self.password = password


def read_info_from_file(path):
    config = open(path, "r")
    current_list = servers
    for line in config:
        if line[0:2] == "--":
            current_list = tools[line[2:-1]]
        else:
            server_data = line[0:-1].split(" ")
            if len(server_data) > 1:
                current_list.append(Server(ip=server_data[0], user=server_data[1], password=server_data[2]))
            else:
                print("false line")


def automate_main_app():
    pass


def automate_tools():
    pass


def connect_server():
    pass


def install_dependencies():
    pass


def install_redis():
    pass


def install_mongodb():
    pass


def install_rabbitmq():
    pass


def clone_application():
    pass


def install_application_dependencies():
    pass


def config_nginx():
    pass


def start_nginx():
    pass


def run_application():
    pass


if __name__ == "__main__":
    servers = []
    tools = {
        "mongodb": [],
        "redis": [],
        "rabbit": []
    }
    path = "./config"
    if len(sys.argv) > 1:
        path = sys.argv[1]
    read_info_from_file(path)
    automate_main_app()
