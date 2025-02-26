import usb
import os
from pyappleinternal.irecv import IRecv
import pkg_resources
import platform
if 'arm' in platform.machine().lower():
    import zeroconf._utils.ipaddress
    import zeroconf._handlers.answers

def list_recovery_devices():
    ecid_sn_dict = {}
    try:
        libusb_path=pkg_resources.resource_filename('pyappleinternal', 'libusb-1.0.dylib')
        try:
            backend = usb.backend.libusb1.get_backend(find_library=lambda x: libusb_path)
            devices = usb.core.find(find_all=True, backend=backend)
        except Exception as e:
            devices=[]
            print(e)
            print("libusb-1.0.dylib is not loaded correctly. If you are packaging, you can call the 'generate_libusb' method of pyappleinternal.libusb to generate the libusb-1.0.dylib file on the desktop, and then add it to your project")

        def _populate_device_info(device):
            result=dict()
            for component in device.serial_number.split(' '):
                k, v = component.split(':')
                if k in ('SRNM', 'SRTG') and '[' in v:
                    v = v[1:-1]
                result[k] = v
            return result
        for device in devices:
            if device.iProduct == 3:
                info=_populate_device_info(device)
                if info.get("ECID","")!="":
                    ecid_sn_dict[info.get("ECID","")]=recdevice(info.get("ECID",""))
                    ecid_sn_dict[info.get("ECID","")].sn=info.get("SRNM","") if info.get("SRNM","")!="" else info.get("ECID","")
    except Exception as e:pass
    return ecid_sn_dict

class recdevice():
    def __init__(self,ecid):
        super().__init__()
        self.ecid=ecid
        self.sn=""

    
    def enter_os(self):
        try:
            rec_client=IRecv(ecid=self.ecid)
            rec_client.set_autoboot(True)
            try:
                rec_client.send_command("setenv boot-command fsboot")
            except Exception as e:pass
            rec_client.reboot()
        except Exception as e:pass
    
    def reboot(self):
        try:
            rec_client=IRecv(ecid=self.ecid)
            rec_client.reboot()
        except Exception as e:pass

    def poweroff(self):
        try:
            rec_client=IRecv(ecid=self.ecid)
            rec_client.send_command("poweroff")
        except Exception as e:pass

    def enter_diags(self):
        try:
            rec_client=IRecv(ecid=self.ecid)
            rec_client.set_autoboot(True)
            try:
                rec_client.send_command("setenv boot-command diags")
            except Exception as e:pass
            rec_client.reboot()
        except Exception as e:pass
    
    def set_bootargs(self,text):
        try:
            rec_client=IRecv(ecid=self.ecid)
            rec_client.send_command(f"setenv boot-args {text}")
            rec_client.send_command(f"saveenv")
            return self.get_bootargs()
        except Exception as e:print(e)

    def get_bootargs(self):
        try:
            rec_client=IRecv(ecid=self.ecid)
            bootargs=rec_client.getenv("boot-args")
            bootargs = "" if bootargs is None else bootargs.decode('utf-8').replace('\x00', '')
            return bootargs
        except Exception as e:print(e)
