# Falcon Base Project

This is a base project using The Falcon Web Framework; it performs CRUD operations on different related resources. 
The resources are Message categories and Messages.

The project is based on Chapter 6 of the book: [Building RESTful Python Web Services](https://www.packtpub.com/application-development/building-restful-python-web-services)


### Running the service:

At the terminal, type the following command:

`$ docker-compose up`

After starting the service it will be possible to access it at http://localhost:8080/

### Debugging the service: 

1. First, it is necessary to create a virtual environment 
for the project:

    On the root directory, type the following command to 
    create a virtual environment with the name 'falcon-base', 
    that will use the python 3.7.
    
    `$ virtualenv -p python3.7 falcon-base`
    
    To activate the virtual environment
    
    `$ source ~/falcon-base/bin/activate`

2. After that, we proceed to configure the IDE. In my case: PyCharm

    Click on File -> Settings; then Project -> Project Interpreter
    
    Click on the gear icon at the top right corner, then click Add
    
    Select the 'Existing environment' radio button
    
    On the interpreter field use the following path, changing 'your-root-directory':
    
    `your-root-directory/falcon-base/bin/python3.7`
    
    After that, to properly debug with PyCharm, click on 'Add Configuration...' at the top menu.
    
    Type Alt+Insert and select Python.
    
    At the script path, use the following path, changing 'your-root-directory' accordingly:
    
    `/your-root-directory/falcon-base/bin/gunicorn`
    
    At parameters:
    
    `-w 2 -b 0.0.0.0:8001 --log-config logging.ini main:app -t 180`
    
    At working directory, select the directory where you put this project.
    
3. The project can be debugged using the database with the following command at the terminal:
    
    `$ docker-compose -f compose-testing up`
    
    This will raise the database to be used during the debug.

### Checking for code quality:

At the terminal: 

`$ make lint`

This will run the pylint and pycodestyle

### Checking the tests:

At the terminal: 

`$ make check`

This will run the tests and emmit a coverage report

## TODO: 
* Add the dumping to db for the first time run (Add the feature at main.py and the explanation on Readme)
* Create CI script
https://docs.travis-ci.com/user/docker/
https://github.com/codecov/example-python
* Create CD script to push to ECR