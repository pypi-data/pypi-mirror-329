#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 10:57:08 2023

@author: aguerrero
"""
import json
import os 
import datetime


 
def get_absolute_date_and_hour():
    now = datetime.datetime.utcnow()
    absolute_date = now.date()
    absolute_hour = str(now.time().hour)+":"+str( now.time().minute)+":"+str( now.time().second)
    return absolute_date, absolute_hour

def write_log(file_path,message,status,location,code):
    
    [date,hour]=get_absolute_date_and_hour()
    error={
            "description": message,
            "hour": hour,
            "date": date.strftime("%d/%m/%Y"),
            "type": status,
            "locator":location,
            "code":code
        }
    
    file_dir= os.path.dirname(file_path)
    if os.path.isdir(file_dir): 
        if not os.path.isfile(file_path):
            try:
                with open (file_path,"w+") as file:
                    json.dump(error,file, indent=4)
                file.close()
            except Exception as e:
                print(e)
        else: 
            try:
                with open (file_path, 'a+') as file:
                    json.dump(error,file,indent=4)
                file.close()
            except Exception as e:
                print(e)
    else:
        print(file_path)
        print (message)
        print("FATAL ERROR:log_file dir does not exist")
        os.sys.exit()