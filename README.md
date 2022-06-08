# file organization
Scripts, inputs and outputs are recommended to be in the same folder. You can specify the whole directory to make sure the program points to the file. But if the scripts and files are in the same folder, you can shorten the directory it as ../subfolder/file name.extension
## The program flows starts at toolkit.py where the first step is to load all parameters located in the configuration file (yaml). THe toolkit defines all the functions to be used as a class. In main.py, every funtion will be called out in the form: class_name.function_name(paramater=value_defined_in_yaml). For example, my_function.sub_sql(year_date=year_date)
# yaml-configuration file
A YAML file includes all the parameters for database information, file paths, SQL queries, filters for selecting data.
# python-functions as the toolkit
Defining project-specific functions are saved as python objects. These functions are collectively stored as a python program. This is called out as a toolkit in the main python script. Statistical tests or standard calculations that should stay constant can be saved here.
# python-main scripts for business rules
The main python scripts have all calculation rules for answering business questions. It can be visualization plots or tables for statistics. Most development changes should go in here while the yaml and python toolkit stay constant most of the time. 

# SQL
Depending on the type of databases the query works against, there are different python libraries to use. You can streamline the processes: write queries to get an output and then load them in Jupyternotebook to continue data wrangling. For example, postgresSQL is a database and pgAdmin is the application used for running queries. Using the python library, psycopg2, you can wrap up SQL code in python programming without hopping between differerent applications.

# Virtual Environment
How to set up a virtual enviornment for python programs to live in is a key step in building up production codes. As python is not only used in data science projects, we need to create a virtual environment for any data science projects to avoid problems with inconsistent dependencies and verions.

My preferred way to achieve this is to install Jupyter Notebook extension in the code editor Visual Studio Code. Within this tool, I can write some commands in the Terminal to create a virtual envrionment per project.

When in Conda, the steps to create a virtual envionrment, named as test_env are as follows:
1. open Terminal
2. type conda -V
3. type conda update conda
4. type conda create -n test_env python=3.8 anaconda
5. type conda activate test_env
6. type conda install -n test_env [package_name] if you wish to isntall the package to the specific environment.  Failure to specify " -n test_env" will install the package to the root Python installation

The importance of creating a virtual environment for each project, even your projects share a common theme, is to avoid conflict. The base conda is the root for all the virtual envrionments. If you are simply running standalone codes, it should be fine to code in base conda. However, If you are working on multiple projects directly pulling data from produciton databases, it is highly recommend to set up a virtual envrionment for each project.The conflicts occur when the packages for different projects could just be incompatible. As these packages are open-sourced, it is sometimes hard to pin down the issues when one program just stops working even though it worked before. 

When in JupterLab where Anaconda is no longer used,  the steps to create a virtual envionrment, named as test_env are as follows:
1. open Terminal
2. type cd ./new_folder
jupyter-jupyter-7997df465-gsn27:~/analytics$ cd ./Data_quality
3. type python3 -m venv myenv
jupyter-jupyter-7997df465-gsn27:~/analytics/Data_quality$ python3 -m venv myenv 
--system-site-packages
4. type source myenv/bin/activate
jupyter-jupyter-7997df465-gsn27:~/analytics/Data_quality$ source myenv/bin/activ
ate
5. type ipython kernel install --user --name=myenv (myenv) jupyter-jupyter-7997df465-gsn27:~/analytics/Data_quality$ python -m ipyk
ernel install --user --name=myenv
Installed kernelspec myenv in /home/hmda/.local/share/jupyter/kernels/myenv
(myenv) jupyter-jupyter-7997df465-gsn27:~/analytics/Data_quality$
6. type deactivate
jupyter-jupyter-7997df465-gsn27:~/analytics/Data_quality$ deactivate
jupyter-jupyter-7997df465-gsn27:~/analytics/Data_quality$

