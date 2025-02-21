import os
import sys
from pyappleinternal import recovery_operate
from pyappleinternal.usbmux import list_devices
from pyappleinternal.os_operate import osdevice
from pyappleinternal.recovery_operate import recdevice
import platform
from pathlib import Path
import subprocess
import re
import time


if 'arm' in platform.machine().lower():
    import zeroconf._utils.ipaddress
    import zeroconf._handlers.answers

class FindDevice():
    def __init__(self):
        super().__init__()
        self.remotectl="/usr/libexec/remotectl"
        self.authorized_path=Path(os.path.join(os.path.dirname(sys.argv[0]), ".ssh"))
        self.showinternal=False
        self.find_status=True

    def run(self,callback=None):
        self.authorized()
        while self.find_status:
            try:
                self.devices=dict()
                self.recovery_device=recovery_operate.list_recovery_devices()
                if self.showinternal==True:
                    self.get_local_device()
                self.get_device_info()
                if callback==None:
                    return self.devices,self.recovery_device
                    self.find_status=False
                callback(self.devices,self.recovery_device)
                time.sleep(0.75)
            except Exception as e:
                print(e)
                return {},{}
    
    def get_device_info(self):
        for udid in set([device.serial for device in list_devices()]):
            try:
                self.devices[udid]=osdevice(udid)
            except Exception as e:print(e)


    def get_local_device(self):
        try:
            output=subprocess.check_output([f"{self.remotectl}","dumpstate"],stderr=subprocess.DEVNULL).decode().split("Found")
            for i in output:
                if "Local device" in i:
                    uuid=re.findall(r"UUID: [0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}",i)[0]
                    device_info = {key: value for key, value in re.findall(r"(\w+) => ([^\n]+)", i)}
                    self.devices[device_info.get("UniqueDeviceID","00000000-000000000000000000000000")]=osdevice(device_info.get("UniqueDeviceID","00000000-000000000000000000000000"),self.showinternal)
                    self.devices[device_info.get("UniqueDeviceID","00000000-000000000000000000000000")].set_device_info({
                        "device_info":{
                            "HardwareModel":device_info.get("HWModel",""),
                            "ProductType":device_info.get("ProductType",""),
                            "SerialNumber":device_info.get("SerialNumber",""),
                            "ProductVersion":device_info.get("OSVersion",""),
                            "BuildVersion":device_info.get("BuildVersion","")
                            },
                        "batt":{
                            "CurrentCapacity":99
                        }
                    })
            self.recovery_device["00FFFFFFFFFFFFFF"]=recdevice("00FFFFFFFFFFFFFF")
            self.recovery_device["00FFFFFFFFFFFFFF"].sn="FFFFFFFF00"
        except Exception as e:print(e)
        
    def authorized(self):
        try:
            if os.path.exists(f'{os.path.expanduser("~")}/.ssh')!=True:
                os.makedirs(f'{os.path.expanduser("~")}/.ssh')
            self.authorized_path.mkdir(exist_ok=True,parents=True)
            subprocess.run("test -f ~/.ssh/id_ed25519.pub || ssh-keygen -t ed25519 -N '' -f ~/.ssh/id_ed25519 &>/dev/null",stderr=subprocess.DEVNULL, shell=True)
            authorized_keys=subprocess.check_output(["cat ~/.ssh/id_ed25519.pub"], shell=True,stderr=subprocess.DEVNULL)
            subprocess.run(f"echo {authorized_keys.decode().strip()}> '{os.path.join(self.authorized_path,'authorized_keys')}'", shell=True)
        except Exception as e:print(e,"ddd")


