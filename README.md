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
Instructions to Run the project
Setting up OAuth 2.0
1. You will need to sign up for a google account and set up a client id and secret.
2. Visit http://console.developers.google.com for google setup.

Setting up the Environment
1. Unzip this folder into vagrant environment.
2. Type command vagrant up, vagrant ssh.
3. In VM, cd /vagrant/CatalogMenu
4. Run python 'FinalProject.py'
5. open your web browser and visit http://localhost:5000/

Note: Database is already generated with data.

JSON Endpoints
The following are open to the public:
Restaurants JSON: http://localhost:5000/restaurants/JSON - Displays the all
restaurants.
Category Items JSON: / restaurants /<path:restaurant id>/menu/JSON - Displays items
for a specific category.
Category Items JSON: / restaurants /<path:restaurant id>/menu/<menuId>/JSON -
Displays data of specific menu of specific restaurants.
