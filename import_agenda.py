#!/usr/bin/python3

from db_table import db_table
import sys
import xlrd

START_ROW = 15

## Function to escape quotes to allow insertion of texts into the db
def escape_quotes(s):
    return s.replace("'", "''")

## Function to create the table and return the db object
def create_table():

    db = db_table(
        ## Table name
        "agendas", 
        ## Table schema
        { 
            "id": "integer PRIMARY KEY AUTOINCREMENT", 
            "date": "text REQUIRED",
            "time_start": "text REQUIRED",
            "time_end": "text REQUIRED",
            "session": "integer REQUIRED",
            "parent_session": "integer",
            "title": "text REQUIRED",
            "location": "text",
            "description": "text",
            "speaker": "text",
        }
    )

    return db

## Function to insert a single row into the db given the details
def insert_row(db, date, time_start, time_end, session, parent_session, title, location, description, speaker):
    
    session = 1 if (session.strip() == "Session") else 0
    if session:
        ## Will not have a parent session as it is not a sub session
        parent_session = None 

    item = {
        "date": date.strip(),
        "time_start": time_start.strip(),
        "time_end": time_end.strip(),
        "session": session,
        "parent_session": parent_session,
        "title": escape_quotes(title.strip()),
        "location": escape_quotes(location.strip()),
        "description": escape_quotes(description.strip()),
        "speaker": escape_quotes(speaker.strip())
    }

    try:
        row_id = db.insert(item)

        if session:
            return row_id
        else:
            ## If sub session return parent id for future reference
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
            time_start = sh.row(rx)[1].value
            time_end = sh.row(rx)[2].value
            session = sh.row(rx)[3].value
            title = sh.row(rx)[4].value
            location = sh.row(rx)[5].value
            description = sh.row(rx)[6].value
            speaker = sh.row(rx)[7].value

            row_id = insert_row(db, date, time_start, time_end, session, parent_session, title, location, description, speaker)
            parent_session = row_id

    except Exception as e:
        print("Error opening file", e)

else:
    print("Incorrect number of arguments passed!")