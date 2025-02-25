import os
from pyappleinternal.usbmux import list_devices
from pyappleinternal.os_operate import osdevice
from pyappleinternal.recovery_operate import recdevice,list_recovery_devices
import platform
import subprocess
import re
import time


if 'arm' in platform.machine().lower():
    import zeroconf._utils.ipaddress
    import zeroconf._handlers.answers

class find_device():
    def __init__(self):
        super().__init__()
        self.showsample=False
        self.find_status=True

    def run(self,callback=None):
        while self.find_status:
            try:
                self.devices=dict()
                self.recovery_device=list_recovery_devices()
                if self.showsample==True:
                    self.get_local_device()
                self.get_device_info()
                if callback==None:
                    return self.devices,self.recovery_device
                    self.find_status=False
                callback(self.devices,self.recovery_device)
                time.sleep(1)
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
            output=subprocess.check_output(["/usr/libexec/remotectl","dumpstate"],stderr=subprocess.DEVNULL).decode().split("Found")
            for i in output:
                if "Local device" in i:
                    uuid=re.findall(r"UUID: [0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}",i)[0]
                    device_info = {key: value for key, value in re.findall(r"(\w+) => ([^\n]+)", i)}
                    self.devices[device_info.get("UniqueDeviceID","00000000-000000000000000000000000")]=osdevice(device_info.get("UniqueDeviceID","00000000-000000000000000000000000"),self.showsample)
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
        


