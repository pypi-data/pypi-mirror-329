import os
import subprocess
from pathlib import Path

def make_authorized_key():
    authorized_path=Path(os.path.join(os.path.dirname(sys.argv[0]), ".ssh"))
    try:
        if os.path.exists(f'{os.path.expanduser("~")}/.ssh')!=True:
            os.makedirs(f'{os.path.expanduser("~")}/.ssh')
        authorized_path.mkdir(exist_ok=True,parents=True)
        subprocess.run("test -f ~/.ssh/id_ed25519.pub || ssh-keygen -t ed25519 -N '' -f ~/.ssh/id_ed25519 &>/dev/null",stderr=subprocess.DEVNULL, shell=True)
        authorized_keys=subprocess.check_output(["cat ~/.ssh/id_ed25519.pub"], shell=True,stderr=subprocess.DEVNULL)
        subprocess.run(f"echo {authorized_keys.decode().strip()}> '{os.path.join(self.authorized_path,'authorized_keys')}'", shell=True)
    except Exception as e:print(e)