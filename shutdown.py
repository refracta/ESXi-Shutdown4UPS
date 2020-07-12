#! /usr/bin/python
import subprocess, os, sys, re, time


def getAllVms():
    vms = []
    cmd = "vim-cmd vmsvc/getallvms | sed -e '1d' -e 's/ \[.*$//' | awk '$1 ~ /^[0-9]+$/ {print $1}'"
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    for vm in proc.stdout.readlines():
        vms.append(int(re.search(r'\d+', str(vm)).group()))

    return vms;


def isPowerOnStatus(vm):
    cmd = "vim-cmd vmsvc/power.getstate " + str(vm)
    response = subprocess.check_output(cmd, shell=True)
    return "Powered on" in str(response);

def filterPowerOnVms(vms):
    return list(filter(lambda vm: isPowerOnStatus(vm), vms))

def getPowerOnVms():
    return filterPowerOnVms(getAllVms())

def shutdownVm(vm):
    cmd = "vim-cmd vmsvc/power.shutdown " + str(vm)
    subprocess.check_output(cmd, shell=True)

def forceOffVm(vm):
    cmd = "vim-cmd vmsvc/power.off " + str(vm)
    subprocess.check_output(cmd, shell=True)

def shutdownVms(vms):
    for vm in vms:
        print("SHUTDOWN VM: " + str(vm), flush=True)
        try:
            shutdownVm(vm)
        except:
            print("ERROR SHUTDOWN VM", flush=True)

def forceOffVms(vms):
    for vm in vms:
        print("FORCE OFF VM: " + str(vm), flush=True)
        try:
            forceOffVm(vm)
        except:
            print("ERROR SHUTDOWN VM", flush=True)

def shutdownESXi(second):
    cmd = "esxcli system shutdown poweroff -d " + str(second) + " -r \"Shutdown4UPS\""
    subprocess.check_output(cmd, shell=True)

def setESXiMaintenanceMode(mode):
    cmd = "esxcli system maintenanceMode set -e " + ("true" if mode else "false") + " -t 0"
    subprocess.check_output(cmd, shell=True)

def shutdownServer():
    print("SHUTDOWN SERVER!", flush=True)
    setESXiMaintenanceMode(True)
    shutdownESXi(10)
    setESXiMaintenanceMode(False)
    sys.exit()

def getDateString():
    now = time.localtime()
    return "%04d.%02d.%02d %02d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

os.makedirs('logs', exist_ok=True)
sys.stdout = open('logs/' + getDateString() + ".log" ,'w')

SHUTDOWN_TRY = 15
SHUTDOWN_WAIT = 10

FORCE_OFF_TRY = 5
FORCE_OFF_WAIT = 10

print("SHUTDOWN START", flush=True)
vms = getAllVms()

for i in range(1, SHUTDOWN_TRY + 1):
    try:
        print("SHUTDOWN TRY: " + str(i) + "/" + str(SHUTDOWN_TRY), flush=True)
        vms = filterPowerOnVms(vms)
        print("SHUTDOWN VMS: " + str(vms), flush=True)
        if not vms:
            break
        else:
            shutdownVms(vms)
            print("SHUTDOWN WAIT: " + str(SHUTDOWN_WAIT) + "s", flush=True)
            time.sleep(SHUTDOWN_WAIT)
    except:
        print("SHUTDOWN ERROR")


if not vms:
    print("ALL VMS SHUTDOWN SUCCESSFULLY!")
    shutdownServer()

for i in range(1, FORCE_OFF_TRY + 1):
    try:
        print("FORCE OFF TRY: " + str(i) + "/" + str(FORCE_OFF_TRY), flush=True)
        vms = filterPowerOnVms(vms)
        print("FORCE OFF VMS: " + str(vms), flush=True)
        if not vms:
            break
        else:
            forceOffVms(vms)
            print("FORCE OFF WAIT: " + str(FORCE_OFF_WAIT) + "s", flush=True)
            time.sleep(FORCE_OFF_WAIT)
    except:
        print("FORCE OFF ERROR", flush=True)
        
if not vms:
    shutdownServer()
