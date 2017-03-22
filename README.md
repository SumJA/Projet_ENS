# LBMC Converge data viewer :

This website is made to present the data and the results of two research projects on the convergent evolution:
Convergdent and Convergenomix (http://lbbe.univ-lyon1.fr/convergenomix/). 

For the moment, only the visualisation of an entire family is possible, and the website is configure to work locally.

The database of the website is also available in this repository with a script to import the research results on it.

 ## Getting Started
 _Prerequisites :_
To use the database importation scripts you need to have the version 3.5 (or above) of python.
The scripts work only if the data respect the standard format.

The website is build with the framework Django1.10.5 => Please make sure that you have Django1.10.5 installed.

### Installing step 1 :

First of all you need to create the database and import data on it :

**I Data Base**

 * Creation script of the database : bddsqlsql.sql
 You can found this script in the Database directory.
 
 * A png of the database's relational model is available in the Database directory.
 
 * Test data : 
 You can import the data of the gene family 'F00000' to test the app.
 The directory : Database/data contains all the script allowing you to insert the information available dor this family.
 You need to have a mysql server and its configuration information.

 * The data importation scripts are in the directory script_import:
    * argparser.py : Arguments for importing the data
    * config_db.py : The database configuration
    * get_data.py : Extract data from files.
    * import_data.py : Import data in the database.
    * GetEqEnsemblIdGeneName.R : Create gene name and ensembl ID equivalence tsv tables. 

    **_1. Create the database :_**
    
    To create the database you just need to run the bddsqlsql.sql on your mysql server.
    
    **_2. Configure the database info_**
    
    Open the config_db.py file and edit the databse information :
    
    For exemple :
    ```python
    config = {
      'user': 'USERNAME',
      'password': '*********',
      'host': 'localhost',
      'database': 'mydb',
      'raise_on_warnings': True,
    }
    ```
    
    **_3. Import data_**
 
_Running the importation :_
To import data into the database execute the import_data.py script in your terminal.
You'll need to give some arguments :

    `python3.5 import_data.py -d DIRECTORY_PATH -e EXPRESSIN_LEVEL_FILENAME -s SPECIES_METADATA_FILENAME [-f FAMILY_NAME]`

For more information on the arguments, execute the following code:
    
    'python3.5 argparser.py --help'
 
   **_4.Scripts information :_**

   * argparser.py : Arguments for importing the data.
   * config_db.py : The database configuration. You need to configure this file before inserting data in the database.
   * get_data.py : Extract data from files. To use this script you need to give arguments : 
   for the moment you can only import data family by family. To import data from an expression file you can overwrite the
   method import_a_expr of the ImportData class in import_data.py.
   
   `python3.5 import_data.py -d DIRECTORY_PATH -e EXPRESSIN_LEVEL_FILENAME -s SPECIES_METADATA_FILENAME -f FAMILY_NAME`

   For more information on the arguments, execute the following code:
    
    'python3.5 argparser.py --help'
   This script contains a class allowing the extraction of data from the directory given in argument.
   * import_data.py : Import data in the database. See the previous section for more information.
   * GetEqEnsemblIdGeneName.R : Create gene name and ensembl ID equivalence tsv tables. 

   For more information about a script: 
   
    'python3.5 [script_name].py --help'
   
### Installing step 2:

You now have a database.
Lets see how to configure the website :

**II Django**

 **_1. Installation_**

    'sudo apt-get install python3-pip
    sudo aptitude install python3-django
    sudo pip install django'

OR

    'pip install Django==1.10'

Fore more information or if you have a problem installing Django see 
https://docs.djangoproject.com/en/1.10/topics/install/#installing-official-release 

 **_2. Configuration_**

You just need to configure Django. Open the Django's settings file : /ProjetENS/settings.py.
* Configure the database connexion :
Here the configuration to run the website locally: 
Fore more information see https://docs.djangoproject.com/en/1.10/ref/settings/#databases
```python
       DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydb',
        'USER': 'USERNAME',
        'PASSWORD': '********',
        'HOST': 'localhost',
        'PORT': 3306,
        'TEST': {
            'NAME': 'mytestdatabase',
        },
    }
}
   ```
* If you want to run the app on production make sure to turn the Debug off:

   ```python
       DEBUG = True
   ```
For Quick-start development settings - unsuitable for production see 
https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

  **_3. Run the website locally_**
  
 We are going to use Django's development server. Just execute this in the terminal :
  
  `python3.5 manage.py runserver x.x.x.x:8080`
   
  where x.x.x.x is ip and 8080 is the port.
  Now all you need it to enter x.x.x.x:8080 in browser on the network connected device.
  For more information see https://docs.djangoproject.com/en/1.10/intro/tutorial01/
  
  **_4. The app structure_**
  
  The website files are in the ProjetENS directory. In this directory you can find different files :
  * The outer ProjetENS/ root directory is just a container for the project. Its name doesn’t matter to Django; you can rename it to anything you like.
  * manage.py: A command-line utility that lets you interact with this Django project in various ways. You can read all the details about manage.py in django-admin and manage.py.
  * The inner ProjetENS/ directory is the actual Python package for the project. Its name is the Python package name you’ll need to use to import anything inside it (e.g. mysite.urls).
  * ProjetENS/__init__.py: An empty file that tells Python that this directory should be considered a Python package. If you’re a Python beginner, read more about packages in the official Python docs.
  * ProjetENS/settings.py: Settings/configuration for this Django project. Django settings will tell you all about how settings work.
  * ProjetENS/urls.py: The URL declarations for this Django project; a “table of contents” of the Django-powered site. You can read more about URLs in URL dispatcher.
  * ProjetENS/wsgi.py: An entry-point for WSGI-compatible web servers to serve the project. See How to deploy with WSGI for more details.
  
  Polls App :
  With Django a project is a collection of configuration and apps for a particular website. A project can contain multiple apps. An app can be in multiple projects.
  * ProjetENS/research/ : the app to visualise the data on the database.
  
  ==> Fore more information see https://docs.djangoproject.com/en/1.10/intro/tutorial01/
  
   ## Data visualization :
   All you need to do is write a family name/Gene name/Gene EnsemblID/Species name in the search field. (Note that for the moment only the search by family name is available).
   
