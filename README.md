Download the project folder and navigate into
project folder from cmd or terminal
------------------------------------------------------------------------------
Install the virtualenv package

On macOS and Linux:
python3 -m pip install --user virtualenv

On Windows:
py -m pip install --user virtualenv
------------------------------------------------------------------------------
To create a virtual environment, go to your project’s directory 
and run venv.

On macOS and Linux:
python3 -m venv celeryEnv

On Windows:
py -m venv celeryEnv

-------------------------------------------------------------------------------

Activating a virtual environment
Before you can start installing or using packages in your 
virtual environment you’ll need to activate it.
Activating a virtual environment will put the virtual 
environment-specific python and pip executables into your shell’s PATH.

On macOS and Linux:

source env/bin/activate
On Windows:

.\env\Scripts\activate
You can confirm you’re in the virtual environment by checking 
 location of your Python interpreter, it should point to the env directory.

On macOS and Linux:

which python
.../env/bin/python
On Windows:

where python
.../env/bin/python.exe

------------------------------------------------------------------------------
Make sure that you are in project folder in cmd or terminal
Following command will install required packages

pip install -r requirements.txt
-------------------------------------------------------------------------------
To test this MongoDB should be installed on your machine and it should be running
Following is the mongodb installation tutorial.
https://docs.mongodb.com/manual/installation/#mongodb-community-edition-installation-tutorials

-------------------------------------------------------------------------------

After installation of packages.
From project directory run the following command.
python3 app.py (For macOS, Linux)
py app.py (For Windows)

After successful running the above command you will get the link,
copy paste the  http://127.0.0.1:5000/ in browser.
--------------------------------------------------------------------------------