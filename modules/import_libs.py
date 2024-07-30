"""
Imported Libraries and Modules

This code block contains import statements for various Python libraries and modules used in project Airloop.
These imports cover a wide range of functionalities, including working with Google APIs, data manipulation,
report generation, geospatial visualization, web scraping, file management, and more.

The imported libraries and modules include:
- Google API client and authentication modules
- Tabulation and Levenshtein distance calculation utilities
- Date and time handling modules
- Data manipulation and charting tools (openpyxl, numpy, pandas, matplotlib, seaborn)
- File and directory manipulation (shutil, os, sys, glob, pathlib)
- Geospatial visualization libraries (gmplot, folium)
- Web scraping tools (selenium, webdriver-manager)
- Microsoft Office integration (win32com)
- PDF manipulation (PyPDF2)
- Various other utilities and dependencies

These libraries and modules are imported to support different aspects of the project's functionality.
"""

# Essential
import numpy as np
import pandas as pd
import shutil
import os
import sys
import glob
import math
import csv
import re

# Create Embed links from GD
from googleapiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

#embedlink
from tabulate import tabulate
from itertools import count
import Levenshtein
from typing import List, Tuple

# remarks file
import datetime

#report Code
import openpyxl
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font, Color, Alignment, Border, Side
from openpyxl.styles import PatternFill
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.formatting.rule import Rule
from openpyxl.chart.text import RichText
from openpyxl.drawing.text import Paragraph, ParagraphProperties, CharacterProperties
from openpyxl.drawing.text import Font as Font2
from openpyxl.worksheet.header_footer import HeaderFooterItem   
import matplotlib.pyplot as plt
import seaborn as sns
from openpyxl.descriptors.serialisable import Serialisable
from openpyxl.descriptors import (Float, Bool, Integer, NoneSet)
from openpyxl.descriptors.excel import UniversalMeasure, Relation
from openpyxl.worksheet.pagebreak import Break
import gmplot

import geopy.distance
from gmplot import GoogleMapPlotter
import folium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import time

# Import client that belongs to win32com module
from win32com import client

#summary filer
import seaborn
import pathlib
from pathlib import Path
import stat
import warnings
warnings.filterwarnings("ignore")
import winsound
import PyPDF2