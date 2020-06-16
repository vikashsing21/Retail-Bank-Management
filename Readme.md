# Banking Application -Python Flask

 > The objective of this project is to design simple APIs for a banking application.  
 
## Requirements

 - Python 3.x (or Python 2.x)
 - Virtual Environment
 - pip
 - Flask, SQLAlchemy

## Usage

 - Install either of the python versions (I used Python3.7)
 - Create new virtual environment using ``` python -m venv venv ```
 - Activate the virtual environment using ``` source venv/bin/activate ```
 - Install Requirements Files using ``` pip install -r requirements.txt ```
 - Change user, password, server, database in  ``` config.py ```
 - After Succesfully Connecting to the Database perform migration by running following series of Commands:
 - ``` flask db init ```
 - ``` flask db migrate ```
 - ``` flask db upgrade ```
 - Run the application by running app file using ``` python app.py ``` or use  ``` flask run ``` 
 

## Description of files

 - ***model.py***: Consists Schema definition as per database requirements.
 - ***app.py*** : Functionality to Open a new bank account, get account information, depositing and withdrawing from the account are written here
 
## Status

 - App development Still in Progress...
 
