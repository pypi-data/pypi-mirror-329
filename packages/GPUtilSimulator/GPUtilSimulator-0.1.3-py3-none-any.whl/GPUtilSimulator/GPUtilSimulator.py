# LICENSE
#
# MIT License
#
# Copyright (c) 2025 bryan_ro
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import psutil
import random
import uuid
import hashlib

class GPUModel:
    def __init__(self, name, vram, model_id):
        self.name = name
        self.vram = vram
        self.model_id = model_id


gpusModels = [
    GPUModel(name="NVIDIA GeForce RTX 4090", vram=24, model_id="RTX4090"),
    GPUModel(name="NVIDIA GeForce RTX 4080", vram=16, model_id="RTX4080"),
    GPUModel(name="NVIDIA GeForce RTX 4070 Ti", vram=12, model_id="RTX4070Ti"),
    GPUModel(name="NVIDIA GeForce RTX 4070", vram=12, model_id="RTX4070"),
    GPUModel(name="NVIDIA GeForce RTX 4060 Ti", vram=8, model_id="RTX4060Ti"),
    GPUModel(name="NVIDIA GeForce RTX 4060", vram=8, model_id="RTX4060"),
    GPUModel(name="NVIDIA RTX A6000", vram=48, model_id="RTX_A6000"),
    GPUModel(name="NVIDIA RTX A5000", vram=24, model_id="RTX_A5000"),
    GPUModel(name="NVIDIA Titan RTX", vram=24, model_id="TitanRTX"),
    GPUModel(name="NVIDIA Quadro RTX 8000", vram=48, model_id="QuadroRTX8000"),
]

class GPU:
    def __init__(self, ID, gpu_uuid, load, memoryTotal, memoryUsed, driver, gpu_name, serial, display_mode, display_active, temp_gpu):
        self.id = ID
        self.uuid = gpu_uuid

        self.load = round(load, 2)
        self.memoryUtil = float(memoryUsed)/float(memoryTotal)
        self.memoryTotal = round(memoryTotal, 2)
        self.memoryUsed = round(memoryUsed, 2)
        self.memoryFree = round(memoryTotal - memoryUsed, 2)
        self.driver = driver
        self.name = gpu_name
        self.serial = serial
        self.display_mode = display_mode
        self.display_active = display_active
        self.temperature = round(temp_gpu, 2)


def getGPUs(qtdGPUs=1):
    gpus = []

    for i in range(qtdGPUs):
        for modelGPU in gpusModels:
            gpu_uuid = generate_uuid_with_salt(get_mac_address(), i)
            gpu_load = (psutil.cpu_percent() / 100) + random.uniform(-0.5, 0.5)
            gpu_load = max(0.0, min(gpu_load, 1.0))
            gpu_memory_total = modelGPU.vram
            gpu_memory_used = gpu_memory_total * gpu_load
            gpu_driver = 555.85
            gpu_name = modelGPU.name
            gpu_serial = None
            gpu_active = ("Enabled" if gpu_load == 0 else "Disabled")
            gpu_mode = gpu_active
            temp_gpu = 100 * gpu_load

            gpus.append(GPU(None, gpu_uuid, gpu_load, gpu_memory_total, gpu_memory_used, gpu_driver, gpu_name, gpu_serial, gpu_active, gpu_mode, temp_gpu))


    return  gpus


def generate_uuid_with_salt(mac_address: str, salt: int) -> str:
    data = f"{mac_address}-{salt}".encode()
    hashed = hashlib.sha1(data).digest()
    return str(uuid.UUID(bytes=hashed[:16], version=5))


def get_mac_address():
    interfaces = psutil.net_if_addrs()

    for interface_name, addresses in interfaces.items():
        for addr in addresses:
            if addr.family == psutil.AF_LINK:
                mac = addr.address
                if mac and mac != "00:00:00:00:00:00":
                    return mac

    return None