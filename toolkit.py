#python libraries needed for a project
from genericpath import getsize
import os
import pandas as pd
import numpy as np
import yaml
import psycopg2
import time

#self-defined functions start here...

class my_function(object):
    """
    the class name, my_function can be any name. 
    This name will be the project-specific function to be called in the main script.
    """

    def __init__(self, config_file="configuration.yml"):

        """
        config_file is the reference name for the yaml file created in the same folder
        Variables created:
          read_config
          config_param 
          table
          flatfile1
          paths
          sql_path
          data_path
          connection
        """

        if config_file is None:
            print("The configuration yaml file is missing. Please provide one")
        
        with open(config_file, "r") as read_config:
            self.config_param = yaml.safe_load(read_config)
            
            """""
            data source1:
            Using "format" to add the year value at the end of a table name from the database
            """""
        for table in self.config_param["db_tables"]:
            self.config_param["db_tables"][table]=self.config_param["db_tables"][table].format(year=self.config_param["year"])

            """
           data source2:
           Loading any flat files can go here using pd.read_csv
            """
            self.flatfile1 = pd.read_csv(self.config_param["name_program_uses"])

            """"
            data source3:
            SQL queries for subsets, not the whole tables in the database
            Using "format" to add the year value at the end of a table name from the database
            """

            for paths in self.config_param["paths"]:
                paths = self.config_param["paths"][paths].format(year=self.config_param["year"])
                if not os.path.exists(paths):
                    os.makedirs(paths, exist_ok=True)
                    print("creating: {paths}".format(path=paths))
            self.sql_path=self.config_param["paths"]["sql_path"].format(year=self.config_param["year"])
            self.data_path=self.config_param["paths"]["data_path"].format(year=self.config_param["year"])

            self.db_params = {
                "host": os.environ.get("KEY_FOR_HOST"),
                "user": os.environ.get("KEY_FOR_USER"),
                "dbname": os.environ.get("KEY_FOR_DBNAME"),
                "password": os.environ.get("KEY_FOR_PWD")
            }

#    def connection(self,params):
#        try:
#            connection=psycopg2.connect(
#            host="the_host_address",
#            user="the_user_name",
#            dbname="data_base_name",
#            password="the_password")
#            return connection, connection.cursor()
#        except psycopg2.Error as e:
#            print("bad connection attempt, ", e)
   
    def connection(self,params):
        try:
            connection=psycopg2.connect(
            **params)
            return connection, connection.cursor()
        except psycopg2.Error as e:
            print("bad connection attempt, ", e)
            
    def stat(self,df,categorical_field,field="field_value"):
        f={"field_value": ['count','min','max','mean','median']}
        if len(categorical_field)>0:
            data_df=df.groupby(["category","enhanced_loan_type"]+categorical_field).agg(f)
        else:
            data_df=df.groupby(["category","enhanced_loan_type"]).agg(f)
        data_df=data_df.droplevel(level=0,axis=1)
        return data_df

    def subset_conditions(self,slice,dtype,categorical_field,base_sql_file=None,output=None,print_sql=True,save_sql=False,save_csv=True,refresh=False,not_clause=""): 
     """
     These default values for each parameter are going to defined in the following
     """
     if output is None:
         s=""
         for string in categorical_field:
             s+=string[0:3]
         output=slice.replace(" ","")+s+"_end_of_the_file_name"
         output=output.lower()
     if(self.config_param["DEBUG"]): print(output)

     """
     Important step: every time to run the program, start with query only when the file 
     is not there.
     """     
     if (os.path.exists(self.data_path + output) and os.path.getsize(self.data_path + output) > 1 and refresh== False):
         print("Data loading from {paths}".format(path=self.data_path + output)) 
         data_df=pd.read_csv(self.data_path + output, dtype=dtype)
     else:
        sql_fields={ 
            "field_category": self.config_param["subsets"][slice]["slice_name"]
            ,"slice": slice
            ,"subset_cond": self.config_param["subsets"][slice]["where"]
            ,"field": self.config_param["subsets"[slice]["field"] 
            }
     
     if not sql_fields or "table" not in sql_fields.keys() or sql_fields["table"] is None:
        sql_fields["table"]=self.config_param["db_tables"]["table1"]

     # read subsets clause
     with open(sql_fields["where","r"] as in_sql:
         where=in_sql.read()
     # format SQL and subsets clause
     sql_fields["where"]=where.format(
         schema=self.confi_param["schema"]
         ,field=sql_fields["field"]
         ,not_clause=""
         )
    if base_sql_file is None: 
        base_sql="""
        SELECT
        '{category}' AS CATEGORY
        ,{DE2} as DE2_real_name
        ,{field} AS field_value
        ,DE1

        FROM
        {schema}.{table}
        {where}
        {DE2_real_name}


        """
        full_sql=base_sql.format(**sql_fields)

        else:
            with open(base_sql_file,"r") as in_sql:
                base_sql=in_sql.read()
            full_sql=base_sql.format(**sql_fields)

     return data_df
    
    def sql_logic_1(year_date):
        count_sql = """SELECT * FROM {schema}.{table1}"""
        conn=psycopg2.connect(host="host_name",user="user_name",dbname="db_name",
        password="my_password")
        cur=conn.cursor()
        cur.execute(count_sql.format(year_date=year_date))
        count_df=pd.DataFrame(cur.fetchall(),column=[desc[0] for desc in cur.description])
        count_df.to_csv("../folder_saving_output/file_name_{suffix}.csv".format(year_date=year_date),index=false)
        conn.close()
        return sql_logic_1

