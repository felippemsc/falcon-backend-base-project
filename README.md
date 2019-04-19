# Falcon Base Project

This is a base project using The Falcon Web Framework

## TODO: 
* Create CI script
* Create CD script to push to ECR
* Put images at the README


### Creating the virtual enviroment for the project

On the root directory, type the following command to create a virtual enviroment with the name 'falcon-base', 
that will use the python 3.7.

`$ virtualenv -p python3.7 falcon-base`

To activate the virtual enviorment

`$ source ~/falcon-base/bin/activate`

### Configuring PyCharm
TODO: Add printscreen to better ilustrate

Click on File -> Settings 

Project -> Project Interpreter

Click on the gear icon at the top right corner, then click Add

Select the 'Existing enviroment' radio button

On the interpreter field use the following path, changing 'your-root-directory':

`your-root-directory/falcon-base/bin/python3.7`

After that, to properly debug with PyCharm, click on 'Add Configuration...' at the top menu.

Type Alt+Insert and select Python.

At the script path, use the following path, changing 'your-root-directory' accordingly:

`/your-root-directory/falcon-base/bin/gunicorn`

At parameters:

`-w 2 -b 0.0.0.0:8001 --log-config logging.ini main:app -t 180`

At working directory, select the directory where you put this project.