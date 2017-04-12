This application creates an interactive database of guitars with images and 
specifications using Python with Flask framework/Jinja2 templating and 
HTML/CSS for styling. SQLAlchemy is used for the database, while corresponding
images are uploaded with Flask and stored on the file system of the server.
Several brands and guitars are included in the guitars.py file, and the user
can add their own brands and guitars once they log in. Users can log in via
OAuth 2.0 providers including Facebook Login and Google Sign in.

#How to Use the Application
---------------------------

	1. Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/VirtualBox)

	2. Clone the [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm)

	3. Initialize Vagrant with 'vagrant init'

	4. Clone this repository to the vagrant VM directory

	5. Launch the Vagrant VM with the command 'vagrant up'

	6. Log into the Vagrant VM with the command 'vagrant ssh'

	7. Navigate to the project's directory within the virtual machine

	8. Run database_setup.py to create the database

	9. Run guitars.py to populate the database

	10. Run catalog.py to run the application

	11. Navigate to localhost:5000 in your browser


#List of Files
--------------

	*catalog.py: The main file which runs the server and contains the Flask
		handlers and configurations.
	*database_setup.py: The database schema for the brands and guitars
	*guitars.py: A list of brands and guitars specificatons to populate the
		database 
	*client_secrets.json: JSON file with client secrets for Google Sign in.
	*fb_client_secrets.json: JSON file with client secrets for Facebook Login
	*templates: Folder for HTML templates
	*static/styles.css: CSS styles
	*static/img: Folder for the images of guitars and brands
	*static/img/outline.png: Default guitar image
	*static/img/logos/defaultlogo.png: Default logo image
	*static/img/sample: Sample images to upload
	*README.MD: This README file

#List of Changes
----------------
	*4/12/17 - Shortened some data in guitars.py to conform to PostgresQL character limit
	*4/12/17 - Started linux_deployment branch and changed database engine from SQLite to PostgresQL/psycopg2 in 3 files
	*4/12/17 - Added vagrant initialization step to README.MD to clarify application use
	*4/12/17 - Changed fbconnect() function to be compatable with latest version of Facebook's Graph API
	*4/11/17 - Removed superfluous .pyc file and .db file
	*2/28/17 - Fixed typos and formatting of JSON functions in catalog.py
	*2/27/17 - Added more files to list of files in README.MD
	*2/27/17 - Initial Commit