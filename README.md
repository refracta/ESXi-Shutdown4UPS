# ESXi-Shutdown4UPS
ESXi 6.7.0 Shutdown Script for SMC1000I with PowerChute Business Edition v10.0


## Installation
### 1. shutdown.py
```
SHUTDOWN_TRY = 15
// The number of times to send a shutdown command to all virtual machines.
SHUTDOWN_WAIT = 10
// Wait time for shutdown vm

FORCE_OFF_TRY = 5
// The number of times to send a force-off command to all virtual machines.
FORCE_OFF_WAIT = 10
// Wait time for forced off vm
```

### 2. shutdown.sh
```
#!/bin/sh
cd /vmfs/volumes/<DATASTORE NAME>/ESXi-Shutdown4UPS
python shutdown.py
# If necessary, set permissions.
```

### 3. shutdown-request.sh
```
sshpass -p "<ESXi Password>" ssh -o StrictHostKeyChecking=no <USER>@<HOST> "vmfs/volumes/<DATASTORE NAME>/ESXi-Shutdown4UPS/shutdown.sh"
# yum install sshpass -y
```

### 4. Upload files to your ESXi/PCBE VM
```
<ESXi Host>
shutdown.py → /vmfs/volumes/<DATASTORE NAME>/ESXi-Shutdown4UPS
shutdown.sh → /vmfs/volumes/<DATASTORE NAME>/ESXi-Shutdown4UPS

<PowerChute VM>
shutdown-request.sh → /opt/APC/PowerChuteBusinessEdition/Agent/cmdfiles
# Default path for PowerChute Business Edition v10.0
```

### 5. Setting up PowerChute Business Edition v10.0
```
Shutdown Settings - Operating System and Application Shutdown - Choose command file - Select 'shutdown-request.sh'

Setting Example)
At runtime limit: 1800 Seconds
Time for operating system to shut down: 50 Seconds
Command file: shutdown-request.sh
Time required for command file to run: 1750 Seconds
```

## Reference
https://github.com/sixdimensionalarray/esxidown

https://github.com/mikejsutherland/esxi-vms-shutdown

https://github.com/matrixlord/ESXi-Shutdown-Check

