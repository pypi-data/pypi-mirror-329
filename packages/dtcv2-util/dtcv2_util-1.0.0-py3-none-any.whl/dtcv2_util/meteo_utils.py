#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 17:52:47 2023

@author: aguerrero
"""
import sys
from . import validate_inp as vi
import os
import json
from . import log_management as logm
import shutil
import datetime
from urllib.request import urlopen

#it's the script ID for debbuging
location="Meteo_utils"

#creates class Meteo (meteo is a class more )
class Meteo:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class File_Manager:
    def __init__(self):
        #Assign default values for paths

        self.resources_path="resources"
        self.log_folder="log"
        self.log_file="log_meteo.json"
        self.options_file="options.json"
        self.default_file="default_values.json"
        self.areas_file="areas.json"
        self.servers_file="servers.json"
        self.files=[self.options_file,self.default_file,self.areas_file,self.servers_file]#list of files in resources
        self.meteo_folder="Meteo"
        
        #Those paths will be obtained during execution
        self.file_paths=[]
        self.log_file_path=""
        self.log_folder_path=""
        self.project_path=""
    @staticmethod
    #just reads any json file
    def read_json(file_path, log_file_path):
        try:
            with open(file_path) as json_file:
                return json.load(json_file)
        except Exception as e:
            logm.write_log(log_file_path, "Json file "+file_path+" was not found or contains errors. Please check the path" +str(e), "FATAL-ERROR", location, "500")
            sys.exit()

    #log file management (at initial stage project_file_path is not know)
    def initial_log_file(self,initial_log_folder):
       
        initial_log_file_path=os.path.join(initial_log_folder,self.log_file)
        if not os.path.isfile(initial_log_file_path):
            if not os.path.isdir(initial_log_folder):
                try:
                    
                    os.mkdir(initial_log_folder)
                except Exception as e:
                    print(e)
        else:
            os.remove(initial_log_file_path)
        return initial_log_file_path
    
    #function that manages the creation of the log file and its update if needed
    def log_files(self,project_path,initial_log_folder,initial_log_file_path,path_message):
        log_folder_path=os.path.join(project_path,self.log_folder) 
        log_file_path=os.path.join(log_folder_path,self.log_file) 

        if not os.path.isdir(log_folder_path) :
            try:
                os.mkdir(log_folder_path)
                
                path_message+= ("... Creating log folder in project path")
                if(initial_log_folder!= log_folder_path):
                    shutil.copyfile(initial_log_file_path,log_file_path)
                    
            except Exception as e:
                logm.write_log(initial_log_file_path,str(e), "ERROR", location, "407")
                os.sys.exit()
        else:
            if os.path.isfile(log_file_path):
                path_message+= ("Log Path updated")
                shutil.copyfile(initial_log_file_path,log_file_path)
                os.remove(os.path.join(log_file_path))
                
        
        shutil.rmtree(initial_log_folder) 
        logm.write_log(log_file_path,path_message, "INFORMATION", location, "101")
        self.log_file_path= log_file_path
        self.log_folder_path= log_folder_path

    #defines the location of resources files (default from library or resources folder defined by user)   
    def resources_files_management (self,resources,initial_log_file_path):
        
        absFilePath = os.path.abspath(__file__)
        script_path, filename = os.path.split(absFilePath)
        resources_folder_path=os.path.join(script_path,self.resources_path)
        
        file_paths=[]
        for file in self.files:
            if resources =="default":#if resources == default then resources taken from library resources
                file_paths.append(os.path.join(script_path,resources_folder_path,file))            
            else:
                if os.path.isdir(resources): 
                    #If resources path is given we check if options.json file  exist there--> if not taken from library resources
                    if os.path.isfile(os.path.join(resources,file)):
                        file_paths.append(os.path.join(resources,file))
                        logm.write_log(initial_log_file_path, "File "+file+"  taken from "+resources, "INFORMATION", location, "101")
                    else:
                        if os.path.isfile(os.path.join(resources_folder_path,file)): #if options is not in the given resources path, the options will be taken from library resources
                            file_paths.append(os.path.join(resources_folder_path,self.options_file))
                            logm.write_log(initial_log_file_path, "File "+file+" does not exist in the given resources path. File taken from default library", "WARNING", location, "300")
                        else:
                            logm.write_log(initial_log_file_path, "File "+file+" does not exist. Please verify the paths: "+os.path.join(resources,file)+" and "+os.path.join(resources_folder_path,file), "ERROR", location, "505")
                else:
                    logm.write_log(initial_log_file_path, "Folder "+resources+" does not exist in the given resources path. File taken from the provided resources of the library dtcv2-util ", "WARNING", location, "300")
                    file_paths.append(os.path.join(script_path,resources_folder_path,file))
        self.file_paths= file_paths
    #Definitive files assignation
    def files_absolutes(self,options,initial_log_folder):
        try:
            initial_log_file_path=os.path.join(initial_log_folder,self.log_file)
            path_message=""
            self.meteo_folders(options, path_message, initial_log_file_path)
            self.log_files(self.project_path,initial_log_folder,initial_log_file_path,path_message)
        except Exception as e:
            logm.write_log(initial_log_file_path, str(e)+" Error in defining absolute paths ", "FATAL-ERROR", location, "500")
    
    # Search the project folder and creates the Meteo folder
    def meteo_folders(self,options, path_message, initial_log_file_path):
        
        project_path= options["PROJECT_PATH"]
        if project_path.lower()=="default":
            project_path=os.getcwd()
            
        else:
            if not os.path.isdir(project_path):
                
                logm.write_log(initial_log_file_path, "ERROR. Project path: "+project_path+" doesn't exist. please verify or write <default> to work in the actual folder ", "ERROR", location, "407")
                os.sys.exit()
            if not os.path.isdir(os.path.join(project_path,self.meteo_folder)) :
                try:
                    os.mkdir(os.path.join(project_path,self.meteo_folder))
                    path_message+=(" ...Creating Meteo folder. ")
                except Exception as e:
                    logm.write_log(initial_log_file_path,str(e), "ERROR", location, "407")
                    
                    os.sys.exit()
        path_message+= (" Saving data in "+os.path.join(project_path,self.meteo_folder))
        logm.write_log(initial_log_file_path,path_message, "INFORMATION", location, "101")
        self.project_path= project_path
#This is an interface (class with no arguments) that allows to get all the default values from the server (server json) if server changes HERE is the place to change code 
class ServerManager:
    #reads and returns the default values for server GFS     
    @staticmethod
    def serverGFS(res,resources_file_path,log_file_path):
        try:
            with open (resources_file_path) as json_file:
                
                file=json.load(json_file)
                server=file["GFS"]["server"]
                lev_list=file["GFS"]["lev_list"]
                var_list=file["GFS"]["var_list"]
                if res==0.5:
                    lev_list += file["GFS"]["0_5_lev_list"]
                return(server,lev_list,var_list)
        except Exception as e:
            logm.write_log(log_file_path, "File servers.json was not found into the resources folder: "+resources_file_path+". Please check the path and the version. " +str(e), "FATAL-ERROR", location, "500")
            os.sys.exit()   

    # reads and returns the default values for server ERA5       
    @staticmethod
    def serverERA5(servers_file_path,log_file_path):
        try:
            with open (servers_file_path) as json_file:
                file=json.load(json_file)
                params_list=file["ERA5"]
                return params_list
        except Exception as e:
            logm.write_log(log_file_path, "File servers.json was not found into the resources folder. Please check the path and the version. " +str(e), "FATAL-ERROR", location, "500")
            os.sys.exit()         
class Time_Manager:
        
    #Find the best available cycle for GFS depending on the current hour
    @staticmethod
    def find_cycle( target,date):
        lst=[0,6,12,18]
        if target<6:# if hour less than 6h the cycle is 18h of the preceeding day
            date=date-datetime.timedelta(days=1)
            return 18,date
        else:
            for val in lst:
                if val > target:
                    return val-12,date
                    break
                else:
                    if val == target:
                        return val-6,date
                        break
    #current hour               
    @staticmethod
    def get_absolute_date_and_hour():
        try:
            rest = urlopen('http://just-the-time.appspot.com/')
            result = rest.read().strip()
            result_str = result.decode('utf-8')
            now= datetime.datetime.strptime(result_str,'%Y-%m-%d %H:%M:%S')
            absolute_date = now.date()
            absolute_hour = now.time().hour
            return absolute_date, absolute_hour
        except Exception as e:
            print(e)
            now = datetime.datatime.utcnow()
            absolute_date = now.date()
            absolute_hour = now.time().hour
            return absolute_date, absolute_hour

    @staticmethod
    def time_GFS(options,log_file_path,default,res):
        time=[] 
        
        if options["TIME_SOURCE"]=="MANUAL":
            date=datetime.datetime.strptime(options["DATE"], '%d/%m/%Y').date()
            hour="default"
            cycle=int(options["CYCLE"])
            step=options["TIME_RESOLUTION"]
            time.append(min(map(int,options["TIME_STEP"])))
            time.append(max(map(int,options["TIME_STEP"])))
            #GFS res 0.5 and 1 only offer the info every 3 hours
            if res==0.5 or res==1:
                modular=step%int (default["meteo"]["GFS"]["{:.2f}".format(res)]["step"])
                if modular != 0:
                    logm.write_log(log_file_path, "The resolution selected only offers data every "+str(default["meteo"]["GFS"]["{:.2f}".format(res)]["step"])+" hours, the default TIME RESOLUTION = "+str(default["meteo"]["GFS"]["{:.2f}".format(res)]["step"]), "WARNING", location, "300")
                    step=default["meteo"]["GFS"]["{:.2f}".format(res)]["step"]
            
        else:
            [date, hour]=Time_Manager.get_absolute_date_and_hour()
            [cycle,date]=Time_Manager.find_cycle(int(hour),date)
            step=default["meteo"]["GFS"]["{:.2f}".format(res)]["step"]
            time=default["meteo"]["GFS"]["{:.2f}".format(res)]["time"]
        logm.write_log(log_file_path, "METEO: TIME. Time Range : "+str(min(time))+"h - "+str(max(time))+" h. Step (hrs): "+str(step)+" UTC: "+str(hour)+". Downloading data from "+str(date), "INFORMATION", location, "100")
        return date,hour,cycle, step,time
    
    #dates on ERA5 (date init-date end)
    @staticmethod
    def time_ERA5(options,log_file_path):
        times=[]
        date=[]
        try:
            date_start=datetime.datetime.strptime(options["START_DATE"], '%d/%m/%Y').date()
            date.append(date_start)
            date_end=datetime.datetime.strptime(options["END_DATE"], '%d/%m/%Y').date()
            date.append(date_end)
            step=options["TIME_RESOLUTION"]
            if min(map(int,options["TIME_STEP"]))<0:
                times.append(0)
            else:
                times.append(min(map(int,options["TIME_STEP"])))
            #The Time in a day 0 - 23h
            if max(map(int,options["TIME_STEP"]))>23:
                times.append(23)
            else:
                times.append(max(map(int,options["TIME_STEP"])))
            logm.write_log(log_file_path, "METEO: TIME. Time Range : "+str(min(times))+"h - "+str(max(times))+" h. Step (hrs): "+str(step)+ " . Downloading data from "+str(date[0])+"  "+str(date[1]), "INFORMATION", location, "100")
        
            return date,times,step
        except Exception as e:
            logm.write_log(log_file_path,str(e), "ERROR", location, "407")

  

class Area:
    def __init__(self):
        self.lonmin=0
        self.lonmax=0
        self.latmin=0
        self.latmax=0

    # defines the coordinates of the area from values or file
    def areas(self,options,areas_file_path,log_file_path):
    
        
        if options["LOCATION_SOURCE"] == "MANUAL":
            self.lonmin= min(map(float,options["LON_RANGE"]))
            self.lonmax= max(map(float,options["LON_RANGE"]))
            self.latmin= min(map(float,options["LAT_RANGE"]))
            self.latmax= max(map(float,options["LAT_RANGE"]))
        else:
            area=options["AREA_NAME"].lower()
            if options["AREA_FILE"].lower()=="default":
                inputf=os.path.join(areas_file_path)
            else:
                inputf=options["AREA_FILE"]
            logm.write_log(log_file_path, "Reading coordinates of {} from input file: {}".format(area,inputf), "IN-PROGESS", location, "100")
            
            block=File_Manager().read_json(inputf,log_file_path)
            if area in block.keys():
                
                self.lonmin = block[area]["lonmin"] 
                self.lonmax =  block[area]["lonmax"] 
                self.latmin =  block[area]["latmin"] 
                self.latmax =  block[area]["latmax"] 
            else:
                logm.write_log(log_file_path, "ERROR. Area not found in areas file","ERROR", location, "407")
        #return lonmin,lonmax,latmin,latmax      
 
   
class Meteo_initializer:
    def __init__(self,options,file_manager,default,areas_file_path,servers_file_path):
        self.file_manager=file_manager
        self.default=default
        self.areas_file_path=areas_file_path
        self.servers_file=servers_file_path
        self.options=options
        self.area=Area()
        self.server=ServerManager()
        self.time=Time_Manager()
    #reads the meteo.inp and conifure all for the Meteo class creation
    def init_GFS_GDAS(self):
            try:
                #Resolution
                res=self.options["RESOLUTION"]
                #Date  Time
                [date,hour,cycle, step,time]=self.time.time_GFS(self.options,self.file_manager.log_file_path,self.default,res)
                #Output
                if self.options["OUTPUT"].upper()=="AUTO":
                    output = "GFS{date}-{cycle:02d}z-res{res:.2f}.grb".format(date  = date.strftime("%Y%m%d"), 
                                                                cycle = cycle, res=res)
                else:
                    output=self.options["OUTPUT"]
                    if not output.endswith('.grb'):
                        output = output.strip() + '.grb'
                #Area
                self.area.areas(self.options,self.areas_file_path,self.file_manager.log_file_path)
                [lonmin,lonmax,latmin,latmax]=[self.area.lonmin,self.area.lonmax,self.area.latmin,self.area.latmax]
                #Server
                verbose=1
                [server,lev_list,var_list]=self.server.serverGFS(res,self.servers_file,self.file_manager.log_file_path)
                #Meteo class
            
                meteo=Meteo(date=date,cycle=cycle,step=step,time=time,latmin=latmin,latmax=latmax,lonmin=lonmin,lonmax=lonmax,res=res, output=output,verbose=verbose,path=os.path.join(self.file_manager.project_path,self.file_manager.meteo_folder),server=server,var_list=var_list,lev_list=lev_list,log_file=self.file_manager.log_file_path)
            except Exception as e:
                logm.write_log(self.file_manager.log_file_path, str(e), "ERROR", location, "406")
            try:
                meteo=Meteo(date=date,cycle=cycle,step=step,time=time,latmin=latmin,latmax=latmax,lonmin=lonmin,lonmax=lonmax,res=res, output=output,verbose=verbose,path=os.path.join(self.file_manager.project_path,self.file_manager.meteo_folder),server=server,var_list=var_list,lev_list=lev_list,log_file=self.file_manager.log_file_path)
            except Exception as e:
                logm.write_log(self.file_manager.log_file_path, str(e), "ERROR", location, "406")
            
            return meteo

    #reads the meteo.inp and conifure all for the Meteo class creation
    def init_ERA5(self):
            #Files and folders manegem
            
            #Resolution of the GRID 
            res=self.options["RESOLUTION"]
            #Dates (dtart-end) Hours (min max in the day 0-23 default)
            [date, times, step]=self.time.time_ERA5(self.options,self.file_manager.log_file_path)
            
            #Area
            self.area.areas(self.options,self.areas_file_path,self.file_manager.log_file_path)
            [lonmin,lonmax,latmin,latmax]=[self.area.lonmin,self.area.lonmax,self.area.latmin,self.area.latmax]
            verbose=1
            output=self.options["OUTPUT"]
            #Server predetermined values 
            api_key=self.options["API_KEY"]
            server=self.server.serverERA5(self.servers_file,self.file_manager.log_file_path)
            try:
                meteo=Meteo(date=date,times=times,step=step,latmin=latmin,latmax=latmax,lonmin=lonmin,lonmax=lonmax,res=res, output=output,verbose=verbose,project_path=os.path.join(self.file_manager.project_path,self.file_manager.meteo_folder),server=server,log_file=self.file_manager.log_file_path,api_key=api_key)
                
            except Exception as e:
                logm.write_log(self.file_manager.log_file_path, str(e), "ERROR", location, "406")
            return meteo

#main function     
def init_meteo(path_meteo,mode,initial_log_folder,resources):
    
    initial_log_file_path=File_Manager().initial_log_file(initial_log_folder)
    try: 
        file_mng= File_Manager()  
        file_mng.resources_files_management (resources,initial_log_file_path) 
        [options_file_path,default_file_path,areas_file_path,servers_file_path]=file_mng.file_paths
        [options,flag]=vi.validate_inp(path_meteo,options_file_path,initial_log_file_path)
        
        if flag==1:
            os.sys.exit()
        else: 
            default=File_Manager().read_json(default_file_path,initial_log_file_path)
            file_mng.files_absolutes(options,initial_log_folder)
            initial_log_file_path=file_mng.log_file_path
            meteo_in=Meteo_initializer(options,file_mng,default,areas_file_path,servers_file_path)
            
            if options["METEO_SOURCE"]=="GFS" or options["METEO_SOURCE"]=="GDAS":
               meteo=meteo_in.init_GFS_GDAS()
               
            else: 
                if options["METEO_SOURCE"]=="ERA5":
                    meteo= meteo_in.init_ERA5()
            
            return meteo
           
    except Exception as e:
        logm.write_log(initial_log_file_path, "Here "+ str(e), "FATAL-ERROR", location, "500")


"""To do
server ERA5
meteo ERA5
"""