# Release Notes
##  v0.2
April 30th, 2021 

- **`Improved`** Updated script to use the latest Meraki Dashboard Api **(v1)** for all endpoints, except for **devices status** script still uses **v0**.
- **`New`** Added **Maintenance support** for networks. Network with tag **"Maintenance"** will be excluded from downtime in live tracking.**(valid only for Files execution method)**  
- **`New`** Added **2 execution methods**. Using Files (used till now) and Database method (MongoDB is used).  
- **`New`** Added support for **Multiple organizations**.  
- **`New`** Added feature to **send Report over email automatically at the end of the month**.  
- **`Improved`** Tuned "**new device detection**" code execution from **45 minutes** to **15 minutes** for more accuracy.  
- **`Improved`** Tuned **Notifications** to send email when script starts again.

##  v0.1
March 30th, 2021 (First Release)
- Automated **files and folders** creation when script starts.  
- Automated **new device detection** code execution every **45 minutes.**  
- Automated **Excel Report creation of availability of all devices** after every execution of script.  
- Automated **Excel Report creation of availability of all Networks (Lan and Wi-Fi)** after every execution of script.  
- Automated **Monthly report separation** every last day of the month.  
  
## License  
[MIT](https://github.com/akshaymane920/Meraki_Sla_Calculator/blob/master/LICENSE.txt)

