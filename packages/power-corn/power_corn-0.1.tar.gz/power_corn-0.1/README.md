# Power Corn v1.0

A project to measure and record energy consumption data of the servers

## Instalación

1. Install ipmitool. This is a requirements since we use it to measure the energy comsupmtion of the servers [IBM Power ](https://www.ibm.com/docs/es/power8?topic=power8-p8eih-p8eih-ipmitool-htm).

   ```bash
    apt-get install ipmitool
   ```

2. Install the app with pip:
   ```bash
   pip install powercorn
   ```
3. crontab config/cronjobs.txt
