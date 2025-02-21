import os
from pyappleinternal.lockdown import create_using_usbmux
from pyappleinternal.services.crash_reports import CrashReportsManager
from pyappleinternal.services.afc import AfcService
from pyappleinternal.services.diagnostics import DiagnosticsService
from pyappleinternal.SSHTransports import SSHTransports
from pyappleinternal.copyUnrestricted import copyUnrestricted
import platform
from pathlib import Path
import sys
import re
import subprocess
import textwrap
import time

if 'arm' in platform.machine().lower():
    import zeroconf._utils.ipaddress
    import zeroconf._handlers.answers

class osdevice():
    def __init__(self,udid,internal=False):
        super().__init__()
        self.udid=udid
        self.internal=internal
        self.authorized_path=Path(os.path.join(os.path.dirname(sys.argv[0]), ".ssh"))
        self.init()
    
    def init(self):
        self.ecid=self.udid.split("-")[1]
        self.copyUnrestricted=copyUnrestricted(self.udid,self.internal)
        self.authorized()
        if self.internal==False:
            self.info=self.get_device_info()
            self.set_device_info(self.info)
        self.ssh_client=SSHTransports(self.udid)
        self.command_exec=self.ssh_client.command_exec
    
    def set_device_info(self,info):
        self.mlbsn=info.get("device_info",{}).get("MLBSerialNumber","")
        self.sn=info.get("device_info",{}).get("SerialNumber",'') if info.get("device_info",{}).get("SerialNumber",'')!='' else self.mlbsn
        self.battery_level=info.get("batt",{}).get("CurrentCapacity","")
        self.hwmodel=info.get("device_info",{}).get("HardwareModel","")
        self.os_ver=info.get("device_info",{}).get("BuildVersion","")

    def shutdown(self):
        try:
            with create_using_usbmux(self.udid) as lockdown:
                ds = DiagnosticsService(lockdown)
                ds.shutdown()
            lockdown.close()
        except Exception as e:pass

    def enter_recovery(self):
        try:
            with create_using_usbmux(self.udid) as lockdown:
                lockdown.enter_recovery()
            lockdown.close()
        except Exception as e:pass

    def enter_diags(self):
        try:
            self.command_exec("nvram boot-command='diags' ; nvram auto-boot='true' ; reboot")
        except:print(e)

    def reboot(self):
        try:
            with create_using_usbmux(self.udid) as lockdown:
                ds = DiagnosticsService(lockdown)
                ds.restart()
            lockdown.close()
        except Exception as e:pass

    def sysdiagnose(self):
        try:
            with create_using_usbmux(self.udid) as lockdown:
                cr = CrashReportsManager(lockdown)
                cr.pull(f"{os.path.expanduser(f'~/Desktop/sysdiagnose_{lockdown.udid}')}", erase=True)
            lockdown.close()
        except Exception as e:pass

    def get_batt(self):
        try:
            with create_using_usbmux(self.udid) as lockdown:
                ds = DiagnosticsService(lockdown)
            lockdown.close()
            return ds.get_battery()
        except Exception as e:
            return {}

    def authorized(self):
        try:
            self.copyUnrestricted.authorized_keys(self.authorized_path)
        except:print(e)
    
    def set_ssh_host(self):
        if os.path.exists(f'{os.path.expanduser("~")}/.ssh')!=True:
                os.makedirs(f'{os.path.expanduser("~")}/.ssh')
        host="ProxyCommand /usr/libexec/remotectl netcat -F %h com.apple.internal.ssh"
        otherhost="Include config.d/config_iosmenu"
        host_auth=textwrap.dedent("""
        Host *.rsd
            # This host entry is generated by remotectl setup-ssh
            ProxyCommand /usr/libexec/remotectl netcat -F %h com.apple.internal.ssh
            ProxyUseFdpass yes
            ServerAliveInterval 1
            ServerAliveCountMax 3
            StrictHostKeyChecking no
            UserKnownHostsFile /dev/null
            User root
            ControlPersist no""")
        case=re.compile(host,re.DOTALL)
        try:
            with open(f'{os.path.expanduser("~")}/.ssh/config', 'r+') as f:
                content=f.read()
                if otherhost in content:
                    subprocess.run(f"rm -rf $HOME/.ssh/config & echo '{host_auth}' >> $HOME/.ssh/config", shell=True)
                if case.search(content)==None:
                    f.write(host_auth)
        except:subprocess.run(f"echo '{host_auth}' >> $HOME/.ssh/config", shell=True)
    
    def open_terminal(self):
        self.set_ssh_host()
        applescript = f'''
            tell application "Terminal" 
                do script "ssh {self.udid}.rsd"
            end tell
        '''
        subprocess.call(['osascript','-e',applescript])

    def command_terminal(self,command,error=False):
        command_txt=re.sub(r'([\\\\\'"])', r'\\\1', command)
        script = f"""
        tell application "Terminal"
            set found_window to false
            repeat with w in windows
                if name of w contains "{self.udid}" then
                    do script "{command_txt}" in w
                    set found_window to true
                    activate
                    return found_window -- 找到窗口后返回 true
                end if
            end repeat
            return found_window -- 如果没有找到窗口，返回 false
        end tell
        """
        result=subprocess.run(['osascript', '-e', script],stdout=subprocess.PIPE)
        if 'false' in result.stdout.decode() and error==False:
            self.open_terminal()
            self.command_terminal(command,True)

    def get_device_info(self):
        try:
            result_data = dict()
            with create_using_usbmux(self.udid) as lockdown:
                result_data['batt'] = self.get_batt()
                result_data['device_info'] = lockdown.all_values
            lockdown.close()
            return result_data
        except Exception as e:
            return {}