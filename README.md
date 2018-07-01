# udacity-FSD
Udacity-Item-catalog-Project

Restaurant Menu App for Item catalog project This is a python module that creates a
website and JSON API for a list of restaurants. Each restaurant displays their menus
and also provides user authentication using Google. Registered users will have ability
to edit and delete their own items. This application uses Flask, SQL Alchemy, jQuery,
CSS, JavaScript, and OAuth2 to create Item catalog website.
Installation
1. virtualBox
2.Vagrant
3.python 2.7
4.Amazon AWS Lightsail Ubuntu Linux Instance
Instructions to Run the project
Setting up OAuth 2.0
1. You will need to sign up for a google account and set up a client id and secret.
2. Visit http://console.developers.google.com for google setup.

Setting up the Environment
- Create an Amazon AWS Lightsail account.
- Create a Ubuntu Linux-based instance on Lightsail.
- Create new instance i.e. my_instance_name on Lightsail.
- Create and attach a static ip for your Lightsail instance.
The IP address and SSH port details:
<!-- blank line -->
IP address: http://13.126.237.43
<!-- blank line -->
URL: http://ec2-13-126-237-43.ap-south-1.compute.amazonaws.com/
<!-- blank line -->
Port: 2200

<h2>Steps Taken:</h2>

- Connect to  Ubuntu Linux instance using ssh
Create User:
- Enter Root: sudo su
- Set ubuntu password using: passwd ubuntu You will be asked to set a new UNIX password.
- Make ubuntu a super user with: usermod -aG sudo ubuntu
- Exit Root with exit command: exit
- Enter ubuntu account as super user: sudo su - ubuntu
- Create grader user: sudo adduser grader
- Set UNIX Password for grader user when prompted. When prompted for Full Name add: Grader
- Make grader a super user with: usermod -aG sudo grader
- Enter grader account as super user: sudo su - grader
- Create catalog user and set UNIX Password: sudo adduser catalog When prompted for Full Name add: Database Catalog 
<h2>Login and settings:</h2>
<ul>
<li> logged in as the super user grader: sudo su <li> grader </li>
<li>Enter hosts file: sudo nano /etc/hosts.</li>
<li> Add Port 2220 to sshd_config file: sudo nano /etc/ssh/sshd_config</li>
<li> Underneath the existing Port 22 (or SSH port) write: Port 2200</li>
<li> Edit PermitRootLogin prohibit<li>password to: PermitRootLogin no</li>
<li> Edit PasswordAuthentication no to: PasswordAuthentication yes</li>
<li> Save this file.</li>
  </ul>
<h2>Configure Firewall:</h2>

- Set Firewall with:
  - sudo default ufw deny incoming
  - sudo default ufw allow outgoing
  - sudo ufw allow 2200/tcp
  - sudo ufw allow 80/tcp
  - sudo ufw allow www
  - sudo ufw allow ssh
- Start Firewall and Check Status with:
  - sudo ufw enable
  - sudo ufw status 
  - sudo service ssh restart

### Create SSH Key Pairs
- Login in as root with: sudo su
- Create ssh directory and apply permissions to grader:
- sudo mkdir /home/grader/.ssh
- sudo chown grader:grader /home/grader/.ssh
- sudo chmod 70 /home/grader/ssh
- Login as user grader: sudo su - grader
- Create SSH Key pair with: ssh-keygen -t rsa
<!-- blank line -->
[How to Create SSH Keys with PuTTY on Windows][identifier] ?
<!-- blank line -->
[identifier]: https://www.digitalocean.com/docs/droplets/how-to/add-ssh-keys/create-with-putty/
<!-- blank line -->
### Add SSH Key Pairs
- Login in as root with: sudo su
- go to the ssh directory in the grader directory:
```
cd /home/grader/
cd ssh
```
Edit the authorized_keys file with: sudo nano authorized_keys
Add SSH key into the file and save.

<!-- blank line -->
### Installations needed on Ubuntu Instance:
- APACHE2
- PostgreSQL
- Additional Packages
```
sudo apt-get install python-psycopg2 python-flask
sudo apt-get install python-sqalchemy python-pip
sudo apt-get install python-dev

sudo pip install sqlalchemy
sudo pip install python-psycopg2
sudo pip install Flask-SQLAlchemy
sudo pip install oauth2client
sudo pip install --upgrade oauth2client
sudo pip install requests
sudo pip install httplib2
sudo pip install flask-seasurf
```
<!-- blank line -->
## Configure Application on Instance

### Create Catalog Configuration File
1. create a .conf file: sudo nano /etc/apache2/sites-available/UdacityFSD.conf
2. Move catalog.conf file to sites-available: sudo mv catalog.conf /etc/apache2/sites-available/
3. Delete temp directory: sudo rm -rf temp
4. Check .conf file is in directory:
```
sudo cd /etc/apache2/sites-available/
sudo ls
```
6. Edit configuration file email: sudo nano catalog.conf
7. Add your email address in place of youremail@youremailprovider.com.
8. Disable default configuration with: sudo a2dissite 000-default.conf
9. Enable catalog configuration file with: sudo a2ensite catalog.conf
10.Restart Apache with: sudo service apache2 restart

### Create PostgreSQL Database
1. Login to postgresql user with: sudo su - postgresql
2. Connect to psql
3. Create database and mark catalog user as owner: CREATE DATABASE catalog WITH OWNER catalog
4. Connect to database with: \c catalog

### Create the .wsgi File
1. Create the .wsgi File under /var/www/udacity-FSD
2. Open that file and following snipet
```
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/udacity-FSD/")

from FinalProject import app as application
application.secret_key = 'super_secret_key'
```
<!-- blank line -->
### Final Step
Restart Apache sudo service apache2 restart
<!-- blank line -->

### Referances Used
- https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
- https://discussions.udacity.com/t/google-sign-in-permission-denied-to-generate-login-hint-for-target-domain/243708/2
- https://stackoverflow.com/questions/45420672/target-wsgi-script-cannot-be-loaded-as-python-module-raspberry-pi 
