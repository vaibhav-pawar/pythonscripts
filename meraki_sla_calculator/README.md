# Automated Meraki Device Availability Calculator  
A workaround to calculate SLA of all Meraki devices.  
This is a python script for calculating the availability of all devices in a **Meraki Organization**.    
To get the accurate data, the script should run **24x7** on a device having **Python3** installed in it.  
  
### Start the Engine.  
Execute "brun.py" file and fill the necessary configuration to start the script. 
### On Windows
```bash script  
C:\meraki_sla_calculator> python3 -m backend.brun  
```  

### On Linux
```bash script  
user@workspace:~/meraki_sla_calculator$ python3 -m backend.brun  
```  
  
## Release Notes  
##  v0.2
April 30th, 2021 
- **`Improved`** Updated script to use the latest Meraki Dashboard Api **(v1)** instead of **(v0)**.  
- **`New`** Added **Maintenance support** for networks. Network with tag **"Maintenance"** will be excluded from downtime in live tracking.
- **`New`** Added **2 execution methods**. Using Files (used till now) and Database method (MongoDB is used).  
- **`New`** Added support for **Multiple organizations**.  
- **`New`** Added feature to **send Report over email automatically at the end of the month**.  
- **`Improved`** Tuned "**new device detection**" code execution from **45 minutes** to **15 minutes** for more accuracy.  
  
##  v0.1
March 30th, 2021 (First Release)
- Automated **files and folders** creation when script starts.  
- Automated **new device detection** code execution every **45 minutes.**  
- Automated **Excel Report creation of availability of all devices** after every execution of script.  
- Automated **Excel Report creation of availability of all Networks (Lan and Wi-Fi)** after every execution of script.  
- Automated **Monthly report separation** every last day of the month.  
  
## License  
[MIT](https://github.com/akshaymane920/Meraki_Sla_Calculator/blob/master/LICENSE.txt)

