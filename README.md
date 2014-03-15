# Kremlin

Kremlin is the homemade YunoHost VPS deployer based on [Docker](https://www.docker.io/) and [Django](https://www.djangoproject.com/).


### How to install

**Tested on Ubuntu 12.04.4 64bit (kernel 3.11, docker 0.9.0)**

 1. [Install Docker](http://docs.docker.io/en/latest/installation/ubuntulinux/#ubuntu-precise-12-04-lts-64-bit)
 2. Clone the Kremlin repository

   ```bash
      git clone https://github.com/YunoHost/Kremlin /root/Kremlin
   ```
   
 3. Build the YunoHost container
 
   ```bash
      cd /root/Kremlin
      docker build -t yunohost .
   ```

 4. Run your first YunoHost instance (to test)
 
   ```bash
      docker run -d yunohost /sbin/init
   ```

 5. Run postinstall manually (to test)
 
   ```bash
      curl -X POST -k https://ip.of.the.container/ynhapi/postinstall -d "domain=mydomain.test&password=myPassword"
   ```

 6. That's it (for now)! :p
