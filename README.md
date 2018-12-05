# Item Catalog
----
by Jasmin Shah, for the purpose of completing fourth lesson of :
[Full-Stack Web Developer Nanodegree](https://www.udacity.com/course/nd004)

# About This project
----
This project is a Game Catalog website built using Flask, SQLAlchemy and Google OAuth. It is developed on Virtual Box with Vagrant File provided by Udacity.

# How to run?
----
1. Install [VirtualBox](https://www.virtualbox.org/)
2. Install [Vagrant](https://www.vagrantup.com/)
3. Clone [this](https://github.com/Jasmin25/Project5) repository
4. Open Terminal
5. cd vagrant
6. vagrant up (turn off the VM with 'vagrant halt')
7. vagrant ssh (type 'exit' to log out)
8. cd catalog
9. To setup the database, run ```python new_database_setup.py```
10. To populate the database with sample values, run ```python populate_db.py```
11. To see the website, run ```python web_app.py```
12. Go to the browser and visit home page [link](http://localhost:5000)

# License
----
The content of this repository is licensed under [MIT License](https://opensource.org/licenses/MIT)
