import paramiko
import os
from scp import SCPClient
import stat
import time
from PIL import Image
import re
class SSHTransports():
    def __init__(self,udid):
        super().__init__()
        self.udid=udid
        self.host="localhost"
        self.username="root"
        self.client_on=None
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sock=paramiko.ProxyCommand(f"/usr/libexec/remotectl netcat {self.udid} com.apple.internal.ssh")
            

    def is_connect(self):
        return self.client.get_transport() is not None and self.client.get_transport().is_active()
    
    def connect(self):
        if not self.is_connect():
            self.client.connect(hostname=self.host, username=self.username,key_filename=f'{os.path.expanduser("~")}/.ssh/id_ed25519',sock=self.sock,timeout=5)
    
    def command_exec(self,command,timeout=5):
        try:
            self.connect()
            stdin, stdout, stderr = self.client.exec_command(command,timeout=timeout)
            output = stdout.read().decode('utf-8').strip()
            outerr = stderr.read().decode('utf-8').strip()
            return output+outerr
        except Exception as e:
            print(e)
            return False

    def command_invoke_shell(self,command):
        try:
            self.connect()
            self.client_on= self.client.invoke_shell()
            self.client_on.send("mkdir /tmp/take_photo &>/dev/null \n")
            self.client_on.send("cd /tmp/take_photo\n")
            self.client_on.send("OSDToolbox display -s 1 &\n")
            self.client_on.send("killall h16isp\n")
            self.client_on.send("h16isp -j\n")
            self.client_on.send("forget\n")
            self.client_on.send("on\n")
            self.client_on.send("v\n")
            self.client_on.send(command)
        except Exception as e:print(e)
    
    def tele_on(self):
        self.cam_mode=1
        self.command_invoke_shell("start 1 139 0 \n")
    
    def swide_on(self):
        self.cam_mode=4
        self.command_invoke_shell("start 4 139 0 \n")

    def default_on(self):
        self.cam_mode=0
        self.command_invoke_shell("start 0 255 0 \n")

    def focus(self):
        if self.client_on!=None:
            self.client_on.send(f"f {self.cam_mode}\n")

    def exit_cam(self):
        if self.client_on!=None:
            self.client_on.close()
            self.client_on=None

    def save_image(self):
        try:
            self.client_on.send(f"\n")
            self.client_on.recv(2048)
            self.client_on.send(f"p 1\n")
            time.sleep(1)
            output =  self.client_on.recv(2048).decode('utf-8')
            match = re.search(r'(?i)\./\S+\.(jpg|png|jpeg|tiff|bmp|heif|heic|raw)', output)
            if match:
                filename = os.path.basename(match.group(0))
                timestamp = int(time.time())
                self.download(f'/tmp/take_photo/{filename}',os.path.expanduser(f"~/Desktop/photo_{timestamp}.jpg"))
            else:
                self.screenshot(True)
        except Exception as e:print(e)
    

    def upload(self,local_path,remote_path):
        try:
            self.connect()
            scp = SCPClient(self.client.get_transport(), progress=self.progress)  # 添加进度回调
            scp.put(local_path, remote_path, recursive=True)
            scp.close()
        except Exception as e:
            print(e)
    
    def download(self,remote_path,local_path):
        try:
            self.connect()
            scp = SCPClient(self.client.get_transport(), progress=self.progress)  # 添加进度回调
            scp.get(remote_path, local_path, recursive=True)
            scp.close()
        except Exception as e:
            print(e)

    def delete(self,remote_path):
        status=True
        remote_file_name = os.path.basename(remote_path)
        try:
            self.connect()
            sftp=self.client.open_sftp()
            if self.is_remote_directory(sftp,remote_path):
                for item in sftp.listdir(remote_path):
                    item_path = f"{remote_path}/{item}"
                    self.delete_file(item_path)
                sftp.rmdir(remote_path)
            else:
                sftp.remove(remote_path)
        except Exception as e:
            status=False
        finally:
            sftp.close()
            return status

    def movefile(self,original_path,target_path):
        status=True
        try:
            self.connect()
            sftp = self.client.open_sftp()
            sftp.rename(original_path, target_path)
        except Exception as e:
            status = False
        finally:
            sftp.close()  
            return status  

    def is_remote_directory(self, sftp,remote_path):
        try:
            return stat.S_ISDIR(sftp.stat(remote_path).st_mode)
        except IOError:
            return False
        
    def mkdir(self,remote_path):
        status=True
        try:
            self.connect()
            sftp = self.client.open_sftp()
            sftp.mkdir(remote_path)
        except Exception as e:
            status=False
        finally:
            return status
            
    def list_files_with_stat(self,remote_path):
        file_reslut={}
        try:
            self.connect()
            sftp=self.client.open_sftp()
            files=sftp.listdir_attr(remote_path)
            for file in files:
                filename=file.filename
                if stat.S_ISDIR(file.st_mode):
                    filetype="Directory"
                elif stat.S_ISLNK(file.st_mode):
                    filetype="Symlink"
                else:filetype="File"
                filepath=os.path.join(remote_path,filename)
                if filetype=="Symlink":filepath=self.get_real_link(filepath)
                size = self.convert_size(file.st_size)
                file_extension = filename.split(".")[-1].lower() if "." in filename else ""
                file_reslut[filename]={
                    "file_path":filepath,
                    "file_type":filetype,
                    "file_size":size,
                    "file_extension":file_extension
                }
        except Exception as e:
            file_reslut=None
        finally:
            sftp.close()
            return file_reslut
    
    def convert_size(self,size):
        if size < 1000:
            return f"{size} B"
        elif size < 1000 * 1000:
            return f"{size / 1000:.2f} KB"
        elif size < 1000 * 1000 * 1000:
            return f"{size / (1000 * 1000):.2f} MB"
        else:
            return f"{size / (1000 * 1000 * 1000):.2f} GB"

    def get_real_link(self,link_path):
        target_path=None
        try:
            self.connect()
            sftp = self.client.open_sftp()
            target_path = sftp.readlink(link_path)
        except Exception as e:
            pass
        finally:
            sftp.close()
            return target_path
    
    def compress(self,save_path,enter_path,remote_name):
        try:
            file_path=os.path.splitext(save_path)[0]
            remote_list=" ".join(remote_name)
            self.command_exec(f'cd {enter_path};tar -czvf {file_path}.tar.gz {remote_list}')
            return True
        except Exception as e:
            return str(e)
        
    def decompress(self,remote_path):
        try:
            result = self.command_exec(f'cd {os.path.dirname(remote_path)};tar -xvf {remote_path}')
            return True
        except Exception as e:
            return str(e)
    
    def get_bootargs(self):
        try:
            result=self.command_exec("diagstool bootargs --print",timeout=3).replace("boot-args=",'')
            return result
        except:return False

    def set_bootargs(self,text):
        try:
            self.command_exec(f'OSDToolbox display -s 1 &>/dev/null & nvram boot-args="{text}";OSDToolbox appswitch -b')
            return True
        except:return False

    def screenshot(self,cut=False):
        try:
            timestamp = int(time.time())
            png_path=f"/tmp/screenshot_{timestamp}.png"
            self.command_exec(f"/usr/local/bin/CADebug -c '{png_path}'")
            local_path=os.path.expanduser(f"~/Desktop/screenshot_{timestamp}.png")
            self.download(png_path, local_path)
            if cut==True:
                image = Image.open(local_path)
                width, height = image.size
                new_height = height*0.642
                crop_box = (0, (height - new_height) // 2, width, (height + new_height) // 2)  # 上下裁剪
                cropped_image = image.crop(crop_box)
                cropped_image.save(local_path)
        except Exception as e:print(e)

    def playsound(self):
        try:
            random_int=int(str(time.time()).split('.')[1][0])
            self.mkdir("/tmp/sound")
            self.upload(f"{os.path.dirname(os.path.abspath(__file__))}/sound/{random_int}.mp3", "/tmp/sound/")
            self.command_exec(f"figplayAV -volume 1.0 /tmp/sound/{random_int}.mp3 &")
        except Exception as e:print(e)


    def progress(self, filename, size, sent):
        percent = (sent / size) * 100
        print(f"File: {filename} | Progress: {percent:.2f}%")
    
    

    

