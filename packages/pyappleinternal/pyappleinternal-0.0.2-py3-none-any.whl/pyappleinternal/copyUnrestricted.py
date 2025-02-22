import os
from pyappleinternal.lockdown import create_using_usbmux,LockdownClient
from pyappleinternal.services.crash_reports import CrashReportsManager
from pyappleinternal.services.afc import AfcService
from pyappleinternal.services.diagnostics import DiagnosticsService
from pyappleinternal.usbmux import list_devices
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import math
import platform
from pathlib import Path

if 'arm' in platform.machine().lower():
    import zeroconf._utils.ipaddress
    import zeroconf._handlers.answers

class copyUnrestricted():
    def __init__(self,udid,sample=False):
        super().__init__()
        self.thread_num=10
        self.download_thread=10
        self.udid=udid
        self.afc=False
        self.AfcService=AfcService
        self.AfcService.SERVICE_NAME = 'com.apple.afc.unrestricted'
        self.AfcService.RSD_SERVICE_NAME = 'com.apple.afc.unrestricted.shim.remote'
        if sample==False:
            self.Lockdown_init()
    
    def Lockdown_init(self):
        try:
            self.lockdown=create_using_usbmux(self.udid)
            self.afc = self.AfcService(self.lockdown)
        except Exception as e:
            try:
                self.AfcService.SERVICE_NAME = 'com.apple.afc'
                self.AfcService.RSD_SERVICE_NAME = 'com.apple.afc.shim.remote'
                self.lockdown=create_using_usbmux(self.udid)
                self.afc = self.AfcService(self.lockdown)
            except:self.afc= False
        
    def download(self,remote,local):
        try:
            self.afc.pull(remote, local)
            return True
        except Exception as e:
            print(e)
            return False
    
    def upload(self,local,remote):
        try:
            if not self.afc.exists(remote):
                    self.afc.makedirs(remote)
            self.afc.push(local, remote)
            return True
        except Exception as e:
            print(e)
            return False
    
    def find_filename(self,remote,name):
        try:
            result_data=[]
            files=self.afc.listdir(remote)
            if name=='':
                return [os.path.join(remote,i) for i in files]
            for i in files:
                result=re.findall(name, i)
                if len(result)>0 and result[0]==i:
                    result_data.append(os.path.join(remote,i))
            return result_data
        except Exception as e:
            print(e)
            return result_data

    def type_change(self,text):
        if text=="S_IFDIR":
            return "Directory"
        elif text=="S_IFLINK":
            return "Symlink"
        else:return "File"

        
    def get_file_stat(self,remote,files,exec_type=None):
        file_stats = {}
        try:
            lockdown=create_using_usbmux(self.udid)
            afc = self.AfcService(lockdown)
            for f in files:
                path=os.path.join(remote, f)
                stat = afc.stat(path)
                filetype=self.type_change(stat.get("st_ifmt", ""))
                if filetype=="Symlink":path=stat.get("LinkTarget", "")
                file_extension = f.split(".")[-1].lower() if "." in f else ""
                file_stats[f] = {
                    "file_path": path,
                    "file_type": filetype,
                    "file_size": self.convert_size(stat.get("st_size", "")),
                    "file_extension": file_extension
                }
        except Exception as e:
            if exec_type==None:
                self.get_file_stat(remote,files,exec_type="Error")
            print(e)
        return file_stats

    def split_list(self,lst, num_chunks):
        chunk_size = math.ceil(len(lst) / num_chunks)
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
        
    def list_files_with_stat(self, remote):
        file_lists = dict()
        if self.afc==False:return file_lists
        try:
            files = self.afc.listdir(remote)
            self.thread_num=int(len(files)/200) if int(len(files)/200)!=0 else 1
            self.thread_num=self.thread_num if self.thread_num<=10 else 10
            file_batches = self.split_list(np.array(files), self.thread_num)
            with ThreadPoolExecutor(max_workers=self.thread_num) as executor:
                future_to_file = {executor.submit(self.get_file_stat, remote,file): file for file in file_batches}
                for future in as_completed(future_to_file):
                    file = future_to_file[future]
                    try:
                        stat = future.result()
                        file_lists.update(stat)
                    except Exception as e:print(e)
        except Exception as e:
            return self.list_files_with_stat(remote)
        return file_lists
        

    def convert_size(self,size):
        if size=="":
            return None
        if size < 1000:
            return f"{size} B"
        elif size < 1000 * 1000:
            return f"{size / 1000:.2f} KB"
        elif size < 1000 * 1000 * 1000:
            return f"{size / (1000 * 1000):.2f} MB"
        else:
            return f"{size / (1000 * 1000 * 1000):.2f} GB"
        
    def mkdir(self,remote):
        if self.afc==False:return False
        try:
            if not self.afc.exists(remote):
                self.afc.makedirs(remote)
            return True
        except Exception as e:
            print(e)
            return False
    
    def movefile(self,remote1,remote2):
        if self.afc==False:return False
        try:
            self.afc.rename(remote1, remote2)
            return True
        except Exception as e:
            print(e)
            return False
    
    def delete(self,remote):
        if self.afc==False:return False
        try:
            self.afc.rm(remote, force=True)
            return True
        except Exception as e:
            print(e)
            return False

    def authorized_keys(self,path1=None, path2="/var/root/",times=0):
        try:
            self.upload(path1, path2)
            return True
        except Exception as e:
            if times<2:
                return authorized_keys(path1,path2,times+1)
            else:return False