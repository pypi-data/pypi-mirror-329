import json
class BootArgs():
    def __init__(self):
        super().__init__()
        self.bootargs_name="bootargs.json"

    def load_config(self):
        with open(self.bootargs_name,'r') as f:
            return json.load(file)
    
    def generate_bootargs(self,add_part,bootargs,bootargs_list,mode="os"):
        if mode=="os":
            OS_command='diagstool bootargs'
            temp_bootargs=[]
            for i in bootargs_list:
                if add_part!=i:
                    OS_command+=f"""{f" --r {i.split('=')[0]}" if i!='' else ''}"""
            OS_command+=f"{f' --a {add_part}' if add_part!='' else ''}"
            return OS_command
        elif mode=="rec":
            temp=bootargs.split(" ")
            arr=list()
            for i in temp:
                k=i.split("=")[0]
                if k not in [j.split("=")[0] for j in bootargs_list]:
                    arr.append(i)
            arr.append(add_part)
            return f"setenv {' '.join(map(str, arr))}"
    
    def generate_ssh_bootargs(self,text):
        count=0
        temp=text.split(" ")
        for i in ['rdar102001044=yes','rdar102068389=yes','rdar102068001=yes']:
            if i not in temp:
                temp.append(i)
            else:count += 1
        if count==3:
            return None
        return ' '.join(map(str, temp))


