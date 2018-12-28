# Falcon Base Project

This is a base project using The Falcon Web Framework

## TODO: 
Next: Create and pre-populate db


### Creating the virtual enviroment for the project

On the root directory, type the following command to create a virtual enviroment with the name 'falcon-base', 
that will use the python 3.7.

`$ virtualenv -p python3.7 falcon-base`

To activate the virtual enviorment

`$ source ~/falcon-base/bin/activate`

### Configuring PyCharm

Click on File -> Settings 

Project -> Project Interpreter

Click on the gear icon at the top right corner, then click Add

Select the 'Existing enviroment' radio button

On the interpreter field use the following path, changing 'your-root-directory':

`your-root-directory/falcon-base/bin/python3.7`