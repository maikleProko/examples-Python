import docker


class DockerCommunicator():

    def restart_nginx(self):
        res = 1  # cannot found container
        client = docker.from_env()
        container_list = client.containers.list()
        for i in container_list:
            if i.name == 'autolab-remote-service_nginx':
                i.exec_run('nginx -s reload')
                res = 0
        return res

    def show_containers(self):
        client = docker.from_env()
        print(client.containers.list())
