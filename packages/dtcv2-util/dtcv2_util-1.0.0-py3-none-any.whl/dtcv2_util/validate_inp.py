#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 16:49:56 2023

@author: aguerrero
"""

import os.path
import os
import json
from . import log_management as logm
import datetime

location="Validation_input"
# =============================================================================
# VALIDATION OF VARIABLES DEPENDENCE ---> options.json erase the variables that are not readed
# =============================================================================
def validate_dependences(file_path,options_path):
    [dictionary,options_dict]=read_inp(file_path,options_path)
    list_del=[]
    for key in dictionary.keys():
        if "dependence" in options_dict[key].keys():
            variable=options_dict[key]["dependence"]["name"]
            value=options_dict[key]["dependence"]["value"]
            if (not dictionary[variable] in value) or (variable in list_del):
                list_del.append(key)
    rest_dict=dictionary
    for element in list_del: 
        del(rest_dict[element])
    
    return rest_dict,options_dict

# =============================================================================
# VALIDATION OF THE TYPES OF VARIABLES ---> options.json 
# =============================================================================
def validate_restricted_dictionary(dictionary_validation,options_dict):
    flag_error=0
    for key in dictionary_validation.keys():
        
        if options_dict[key]["type"] =="opt":
            if dictionary_validation[key].upper() not in options_dict[key]["value"]:
                logm.write_log(log_file_path, "ERROR: Option selected in "+key+" variable is not allowed. Options available: "+ str(options_dict[key]["value"]), "ERROR", location, "407")
                
                flag_error=1
        else:
            if options_dict[key]["type"] =="val":
                [a,value]= validate_value(dictionary_validation[key], options_dict[key]["value"], key)
                if a==True:
                    flag_error=1
                else:
                   dictionary_validation[key]=value 
            else:
                if options_dict[key]["type"] =="list":
                    list_opt=dictionary_validation[key]
                    ff=False
                    list_o=[]
                    for element in list_opt:
                        [flag,value]=validate_value(element,options_dict[key]["value"], key)
                        if flag is True:
                            ff= True
                        else:
                           list_o.append(value) 
                            
                    if ff==True:
                        flag_error=1
                    else:
                        dictionary_validation[key]=list_o
    return flag_error, dictionary_validation 

def validate_value(value,typev,variable_name):
    #we have to validate logic in order to know which variables will be avoided from type validation
    if typev=="date":
        
        return validate_date(value,variable_name),value
    else:
        if typev=="int":
            try:
                int(value)
                return False, int(value)
            except ValueError:
                logm.write_log(log_file_path, 'ERROR. Please provide a valid int for variable '+variable_name, "ERROR", location, "407")
                return True,None
        else: 
            if typev=="float":
                try:
                    float(value)
                    return False , float(value)
                except ValueError:
                    logm.write_log(log_file_path,'ERROR. Please provide a valid float for variable '+variable_name, "ERROR", location, "407")
                    
                    return True,None
            else: 
                if typev=="str" : #here the path is taken as string, if option of reading path is activated the validation of the path or file will be done in the next stepts
                    try:
                        str(value)
                        return False,value
                    except ValueError:
                        logm.write_log(log_file_path, 'ERROR. Please provide a valid str for variable '+variable_name, "ERROR", location, "407")

                        return True,None
                else:
                    if typev=="path":
                        return check_file_path(value, variable_name)
                    else:
                        if typev=="lat":
                            
                            return validate_coordinates_lat(value, variable_name)
                        else:
                            if typev=="lon":
                                return validate_coordinates_lon(value, variable_name)

def validate_date(value,variable_name):
    try:
        date=datetime.datetime.strptime(value, '%d/%m/%Y')
        return False,date
    except ValueError:
        logm.write_log(log_file_path, 'ERROR. Please provide a valid date format ("DD/MM/YYYY") for variable: '+variable_name, "ERROR", location, "407")
        return True,None
def check_file_path(value,variable_name): #type by default is path
    if os.path.isdir(value) or os.path.isfile(value):
        return False,value
    else:
        logm.write_log(log_file_path, 'ERROR. Folder or file does not exist. Please provide a valid path for variable '+variable_name, "ERROR", location, "407") 
        return True,None   
def validate_coordinates_lat(value,variable_name):
    try:
        value=float(value)        
        if -90<=value and 90>=value:
           return False, value
        else:
           logm.write_log(log_file_path,"Latitude coordinates must be geographic (-90,90) in variable "+variable_name, "ERROR", location, "407")
           return True,None
    except Exception:
        logm.write_log(log_file_path, "Latitude format not valid in "+variable_name, "ERROR", location, "407")
        return True,None
def validate_coordinates_lon(value,variable_name):
    try:
        value=float(value)   
        if -180<=value and 180>=value:
           return False,value
        else:
           logm.write_log(log_file_path, "Longitude coordinates must be geographic (-180,180) in variable "+variable_name, "ERROR", location, "407")
           
           return True,None       
    except Exception:
      logm.write_log(log_file_path, "Longitude format not valid in "+variable_name, "ERROR", location, "407")
      return True,None

# =============================================================================
# READ THE FILES
# =============================================================================
#takes each variable and put the value in the format stabished in options.json
def read_variable(variable_name, option,options_dict):
    
    try:
        opt= options_dict[str(variable_name)] #checks if variable_name_exists
        type_v=opt["type"]#extracts the type of the variable
        if type_v =="opt":
            option=option.replace(" ","").strip()
            return variable_name,option.upper()
        else:
            if  type_v =="val":
                option=option.replace(" ","").strip()
                return variable_name,option
            else:
                if type_v.strip() =="list":
                    list_opt=option.strip().split(" ")
                    return variable_name,list_opt
                   
    except Exception as e:
        logm.write_log(log_file_path, "Variable '"+variable_name+"' has not been found in the options.json. Please check input file and options.json files "+ str(e), "ERROR", location, "407")
        os.sys.exit()
        return None
#create a dictionary with options.json 
def create_dict(options_file_path): 
    
    try:
        with open (options_file_path) as json_file:
            file=json.load(json_file)
            return file
    except Exception as e:
        logm.write_log(log_file_path, "File options.json was not found into the resources folder. Please check the path and the version. "+str(e),"ERROR", location, "500")
        os.sys.exit()
def read_inp(file_path,options_path):
    try:
        options_dict=create_dict(options_path)
        dictionary=dict()
        f2= open(file_path,"r")
        lines=f2.readlines()
        for line in lines:   
            if  (not "!" in line and not "--" in line and line!="\n") : #lines of comments are not taken
                if len(line.strip())>0:#checks if there is not a blank-space line
                    line_splited=line.split("=")
                    values=read_variable(line_splited[0].replace(" ","").strip(), line_splited[1], options_dict)
                    if values is not None:
                        dictionary[values[0]]=values[1]
                    else:
                        os.sys.exit()
        return dictionary,options_dict
    except Exception as e:
        logm.write_log(log_file_path, str(e)+ " ERROR. Input file can not be readed. ", "ERROR", location, "500")
        os.sys.exit()
# =============================================================================
# Validation function
# =============================================================================
def validate_inp(input_file_path,options_file_path,log_path):
       global log_file_path
       log_file_path=log_path
       [rest_dict,opt_dict] = validate_dependences(input_file_path,options_file_path)
       [flag,rest_dict_conv]=validate_restricted_dictionary(rest_dict,opt_dict)
       return rest_dict_conv,flag
#returns the options dictionary (only for the variables needed and the flag of the validation)           


        