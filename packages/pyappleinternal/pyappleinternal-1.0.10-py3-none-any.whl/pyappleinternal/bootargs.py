import json
class BootArgs():
    def __init__(self):
        super().__init__()
        self.bootargs_name="bootargs.json"

    def load_config(self):
        with open(self.bootargs_name,'r') as f:
            return json.load(file)
    
    def generate_bootargs(self,name,bootargs_list,text="",mode="os"):
        if mode=="os":
            OS_command='diagstool bootargs'
            temp_bootargs=[]
            for i in bootargs_list:
                if name!=i:
                    OS_command+=f"{f' --r {bootargs_list[i]}' if bootargs_list[i]!='' else ''}"
                else:
                    temp_bootargs.append(i)
            for i in temp_bootargs:
                OS_command+=f"{f' --a {bootargs_list[i]}' if bootargs_list[i]!='' else ''}"
            return OS_command
        elif mode=="rec":
            temp=text.split(" ")
            arr=list()
            for i in temp:
                k=i.split("=")[0]
                if k not in [j.split("=")[0] for j in [*bootargs_list.values()]]:
                    arr.append(i)
            arr.append(bootargs_list[name])
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


