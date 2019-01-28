import psutil
import subprocess
import json
import sys


class Agent():
    def __init__(self, arg):
        self._eval_cpu_percent()
        self._eval_memory_percent()
        self._eval_disk_free_space()
        self._eval_ping()
        self._eval_services(arg)

    def _eval_cpu_percent(self):
        self.cpu_percent = psutil.cpu_percent(interval=1)

    def _eval_memory_percent(self):
        self.memory_percent = psutil.virtual_memory().percent

    def _eval_disk_free_space(self):
        self.disk_free = subprocess.check_output(
            "df -h / | tail -n 1 | awk {'print $4'} | tr -d '\n'",
            shell=True
        ).decode("utf-8")

    def _eval_ping(self):
        self.ping = subprocess.call(
            "ping -c 1 google.com",
            shell=True,
            stdout=subprocess.PIPE
        )

    def _eval_services(self, arg):
        services = {}
        for s in json.loads(arg)["services"]:
            services[s] = subprocess.call(
                "systemctl status " + s,
                shell=True,
                stdout=subprocess.PIPE
            )
        self.services = json.dumps(services)

    def json(self):
        dict_agent = {
            "cpu_percent": self.cpu_percent,
            "memory_percent": self.memory_percent,
            "disk_free": self.disk_free,
            "ping": self.ping,
            "services": self.services
        }
        return json.dumps(dict_agent)


if __name__ == "__main__":
    agent = Agent(sys.argv[1])
    print(agent.json())
