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
      cd /root/Kremlin/docker
      docker build -t yunohost .
   ```

 4. Install and run virtualenv
 
   ```bash
      apt-get install python-pip
      pip install virtualenv
      cd /root/docker
      virtualenv ve
      source ve/bin/activate
   ```

 5. Install Kremlin's dependencies and synchronize database (SQLite by default)
 
   ```bash
      pip install -r requirements.txt
      python manage.py syncdb
   ```

 6. Edit public IP range to allow to containers

   ```bash
      vim kremlin/settings.py   # Parameter called "AVAILABLE_PUBLIC_IPS"
   ```

### Development workflow

  1. Clean database, stop docker containers and flush iptables
    ```bash
       rm db.sqlite3
       python manage.py syncdb --noinput
       docker ps | grep yunohost | awk '{print $1'} | xargs -l docker stop &> /dev/null &
       iptables -t NAT -F
    ```

  2. Start Django development server
    ```bash
       python manage.py runserver 0.0.0.0:8000
    ```

  3. Debug & go to 1 :)
