import sys

from fabric import Connection, connection, Config
from invoke import watchers, Responder


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
    for server in servers:
        con = connect_server(server)
        install_dependencies(con)
        install_node(con)


def automate_tools():
    # for tool in tools['mongodb']:
    # con = connect_server(tool)
    # install_dependencies(con)
    # install_mongodb(con)
    # for tool in tools['redis']:
    #     con = connect_server(tool)
    #     install_dependencies(con)
    #     install_redis(con)
    # for tool in tools['rabbit']:
    #     con = connect_server(tool)
    #     install_dependencies(con)
    #     install_rabbitmq(con)
    pass


def connect_server(server: Server):
    return Connection(server.ip, user=server.user, port=22, connect_kwargs={"password": server.password})
    # for when you want everything with sudo
    # return Connection(server.ip, user=server.user, port=22, connect_kwargs={"password": server.password},
    #                   config=Config(overrides={"sudo": {"password": server.password}}))


def install_dependencies(con: Connection, sudo_responder: Responder = None):
    sudo(con, "apt update")
    sudo(con, "apt install git build-essential tcl -y")


def install_redis(con: Connection, sudo_responder: Responder = None):
    sudo(con, "apt update")
    sudo(con, "apt install redis-server -y")
    con.run('echo "supervised systemd" >> /etc/redis/redis.conf')
    sudo(con, "systemctl restart redis.service")
    sudo(con, "apt update")
    sudo(con, "apt install redis-server -y")
    sudo(con, 'echo "supervised systemd" >> /etc/redis/redis.conf')
    sudo(con, "systemctl restart redis.service")


def install_mongodb(con):
    sudo(con, "wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -")
    sudo(con,
         'echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.2 multiverse" | sudo '
         'tee /etc/apt/sources.list.d/mongodb-org-4.2.list')
    sudo(con, 'apt update')
    sudo(con, 'apt install -y mongodb-org')
    sudo(con, 'service mongod start')
    sudo(con, 'systemctl enable mongod.service')
    # TODO: verify mongo installation


def install_rabbitmq(con):
    # con.sudo('cd ~')
    # con.sudo('wget http://packages.erlang-solutions.com/site/esl/esl-erlang/FLAVOUR_1_general/esl-erlang_20.1-1 ~ubuntu~xenial_amd64.deb')
    # con.sudo('dpkg -i esl-erlang_20.1-1\~ubuntu\~xenial_amd64.deb')
    #
    # con.run(
    #     'sudo echo "deb https://dl.bintray.com/rabbitmq/debian xenial main" | sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list', pty=True, watchers=[sudo_pass])
    # con.run('sudo wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -; apt update', pty=True, watchers=[sudo_pass])
    # con.sudo('install rabbitmq-server')
    con.run("echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee /etc/apt/sources.list.d/rabbitmq.list")
    con.run("wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -")
    con.run("sudo apt-get update", pty=True)
    con.run("sudo apt-get install rabbitmq-server", pty=True)

    con.run('sudo systemctl start rabbitmq-server.service', pty=True)
    con.run('sudo systemctl enable rabbitmq-server.service', pty=True)


def install_node(con):
    con.sudo('cd ~; curl -sL https://deb.nodesource.com/setup_8.x -o nodesource_setup.sh')
    con.sudo('bash nodesource_setup.sh')
    sudo(con, 'apt install nodejs')
    sudo(con, 'npm install -g pm2')


def clone_application(con, app_path, url):
    con.run("cd " + app_path)
    con.run("git clone " + url)


def install_application_dependencies(con, app_path):
    con.run("cd " + app_path)
    sudo(con, "npm install --save")


def config_nginx():
    pass


def start_nginx():
    pass


def sudo(con, command):
    con.run('sudo ' + command, pty=True, watchers=[sudo_pass])


def run_application(con, app_path, start_path):
    con.run("cd " + app_path)
    con.run("pm2 start " + start_path)
    con.run('pm2 save')


if __name__ == "__main__":
    sudo_pass = Responder(
        pattern=r'\[sudo\] password for sajad:',
        response='pass1377\n',
    )
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
    automate_tools()
    automate_main_app()
