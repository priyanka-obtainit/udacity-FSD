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
IP address: http://13.126.237.43
URL: http://13.126.237.43/login
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
  - sudo ufw allow 123/tcp
  - sudo ufw allow www
  -  sudo ufw allow ssh
- Start Firewall and Check Status with:
  - sudo ufw enable
  - sudo ufw status 
  - sudo service ssh restart

JSON Endpoints
The following are open to the public:
Restaurants JSON: http://localhost:5000/restaurants/JSON - Displays the all
restaurants.
Category Items JSON: / r
  
  estaurants /<path:restaurant id>/menu/JSON - Displays items
for a specific category.
Category Items JSON: / restaurants /<path:restaurant id>/menu/<menuId>/JSON -
Displays data of specific menu of specific restaurants.
  
