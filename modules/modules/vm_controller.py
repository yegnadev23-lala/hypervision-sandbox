import subprocess

VBOX_PATH = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

def run_vbox_command(args):
    cmd = [VBOX_PATH] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return {"success": True, "output": result.stdout.strip()}
    except FileNotFoundError:
        return {"success": False, "error": "VirtualBox CLI not found at default path."}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr.strip()}

def get_vm_status(vm_name="HyperVision-VM"):
    res = run_vbox_command(["showvminfo", vm_name, "--machinereadable"])
    if not res["success"]:
        return "Offline / Not Found"
    for line in res["output"].split("\n"):
        if line.startswith("VMState="):
            return line.split("=")[1].strip('"')
    return "Unknown"

def control_vm(action, vm_name="HyperVision-VM"):
    if action == "Start VM":
        return run_vbox_command(["startvm", vm_name])
    elif action == "Power Off":
        return run_vbox_command(["controlvm", vm_name, "poweroff"])
    elif action == "Revert to Snapshot":
        run_vbox_command(["controlvm", vm_name, "poweroff"])
        return run_vbox_command(["snapshot", vm_name, "restore", "Clean-State"])
    return {"success": False, "error": "Invalid action selected."}
