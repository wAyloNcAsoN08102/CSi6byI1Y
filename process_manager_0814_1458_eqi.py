# 代码生成时间: 2025-08-14 14:58:25
import asyncio
from sanic import Sanic
from sanic.response import json
import psutil
import subprocess
import sys

# 创建Sanic应用
app = Sanic("ProcessManager")

# 进程管理器类
class ProcessManager:
    def __init__(self):
        self.processes = {}

    def start_process(self, name, command):
        """
        启动一个新进程
        :param name: 进程名称
        :param command: 要执行的命令
        """
        try:
            process = subprocess.Popen(command, shell=True)
            self.processes[name] = process
            return process.pid
        except Exception as e:
            return {"error": str(e)}

    def stop_process(self, name):
        """
        停止一个进程
        :param name: 进程名称
        """
        try:
            process = self.processes.get(name)
            if process:
                process.terminate()
                process.wait()
                del self.processes[name]
                return {"message": "Process stopped successfully"}
            else:
                return {"error": "Process not found"}
        except Exception as e:
            return {"error": str(e)}

    def restart_process(self, name):
        """
        重启一个进程
        :param name: 进程名称
        """
        try:
            stop_result = self.stop_process(name)
            if "error" not in stop_result:
                start_result = self.start_process(name, subprocess.list2cmdline(self.processes[name].cmd))
                if "error" in start_result:
                    return start_result
                return {"message": "Process restarted successfully"}
            else:
                return stop_result
        except Exception as e:
            return {"error": str(e)}

    def list_processes(self):
        """
        列出所有进程
        """
        return {"processes": list(self.processes.keys())}

# 实例化进程管理器
manager = ProcessManager()

# Sanic路由
@app.route("/start/<name>/<command:path>", methods=["GET"])
async def start_process(request, name, command):
    result = manager.start_process(name, command)
    return json(result)

@app.route("/stop/<name:path>", methods=["GET"])
async def stop_process(request, name):
    result = manager.stop_process(name)
    return json(result)

@app.route="/restart/<name:path>", methods=["GET"])
async def restart_process(request, name):
    result = manager.restart_process(name)
    return json(result)

@app.route("/list", methods=["GET"])
async def list_processes(request):
    result = manager.list_processes()
    return json(result)

# 启动Sanic服务器
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)