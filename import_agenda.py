#!/usr/bin/python3

from db_table import db_table

import sys
import xlrd

START_ROW = 15

def escape_quotes(s):
    return s.replace("'", "''")

def create_table():

    db = db_table(
            ## Table name
            "agendas", 
            ## Table schema
            { 
                "id": "integer PRIMARY KEY AUTOINCREMENT", 
                "date": "text REQUIRED",
                "start_time": "text REQUIRED",
                "end_time": "text REQUIRED",
                "session": "integer REQUIRED",
                "parent_session": "integer",
                "title": "text REQUIRED",
                "location": "text",
                "description": "text",
                "speakers": "text",
            }
        )

    return db

def insert_row(db, date, start_time, end_time, session, parent_session, title, location, description, speakers):

    session = 1 if (session == "Session") else 0
    if session:
        parent_session = None

    item = {
        "date": date,
        "start_time": start_time,
        "end_time": end_time,
        "session": session,
        "parent_session": parent_session,
        "title": escape_quotes(title),
        "location": escape_quotes(location),
        "description": escape_quotes(description),
        "speakers": escape_quotes(speakers)
    }

    try:
        row_id = db.insert(item)

        if session:
            return row_id
        else:
            return parent_session
    except Exception as e:
        print("Error inserting row", e)

n = len(sys.argv)

if (n == 2):
    
    file_name = sys.argv[1]
    
    try:
        book = xlrd.open_workbook(file_name)
        sh = book.sheet_by_index(0)

        db = create_table()
        parent_session = None

        for rx in range(START_ROW, sh.nrows):
            
            date = sh.row(rx)[0].value
            start_time = sh.row(rx)[1].value
            end_time = sh.row(rx)[2].value
            session = sh.row(rx)[3].value
            title = sh.row(rx)[4].value
            location = sh.row(rx)[5].value
            description = sh.row(rx)[6].value
            speakers = sh.row(rx)[7].value

            row_id = insert_row(db, date, start_time, end_time, session, parent_session, title, location, description, speakers)
            parent_session = row_id

    except Exception as e:
        print("Error opening file", e)

else:
    print("Incorrect number of arguments passed!")