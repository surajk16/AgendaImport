#!/usr/bin/python3

import sys
import xlrd

from db_table import db_table

n = len(sys.argv)

if (n == 2):
    
    file_name = sys.argv[1]
    
    book = xlrd.open_workbook(file_name)
    sh = book.sheet_by_index(0)

    for rx in range(15, sh.nrows):
        
        date = sh.row(rx)[0].value
        start_time = sh.row(rx)[1].value
        end_time = sh.row(rx)[2].value
        session = sh.row(rx)[3].value
        title = sh.row(rx)[4].value
        location = sh.row(rx)[5].value
        description = sh.row(rx)[6].value
        speakers = sh.row(rx)[7].value
        speakers = speakers.split(";")

        print(date, start_time, end_time, session, title, location, speakers)
        

else:
    print("Incorrect number of arguments passed!")