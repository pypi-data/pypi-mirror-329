#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 17:36:41 2023

@author: aguerrero
"""

import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.10' #First version 
PACKAGE_NAME = 'dtcv2_util' #For DTGEO general 
AUTHOR = 'Alejandra Guerrero - DTGEO' 
AUTHOR_EMAIL = 'aguerrero@geo3bcn.csic.es' 
URL = 'https://gitlab.geo3bcn.csic.es/dtgeo/dtc-v2/meteo-gfs' 
LICENSE = 'MIT' 
DESCRIPTION = 'Library for workflow management' #DTC-V2
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') #Referencia al documento README con una descripción más elaborada
LONG_DESC_TYPE = "text/markdown"


#Required packages (automatically installed if they are not installed)
INSTALL_REQUIRES = [
      'datetime',
      'xarray',
      'requests',
      'netcdf4',
      
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    package_data={
      PACKAGE_NAME: ['resources/*'],},
    include_package_data=True
)
