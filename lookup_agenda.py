#!/usr/bin/python3

from db_table import db_table

import sys

COLUMNS = ["date", "time_start", "time_end", "title", "location", "description", "speaker"]

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

def format_result(result):
    session = "Session" if result["session"] else "Sub"
    return "Date: {} \nTime Start: {} \nTime End: {} \nSession/Subsession: {} \nSession Title: {} \nRoom/Location: {} \nDescription: {} \nSpeakers: {}\n".format(
        result["date"], 
        result["time_start"], 
        result["time_end"], 
        session, 
        result["title"], 
        result["location"], 
        result["description"], 
        result["speaker"]
    )


n = len(sys.argv)

if (n == 3):
    column = sys.argv[1]
    value = sys.argv[2]

    if column not in COLUMNS:
        print("Invalid column")
    else:
        db = create_table()

        ## If the column is not speaker
        if column != "speaker":
            where = {column: value}
            results = db.select(where=where)

            for result in results:
                print(format_result(result))

                ## Get results of sub-sessions too
                if (result["session"]):

                    sub_where = "parent_session = {} AND {} != '{}'".format(result["id"], column, value)
                    sub_results = db.select_custom(where=sub_where)

                    for sub_result in sub_results:
                        print(format_result(sub_result))

        ## If the column is speaker
        else:
            where = "{} LIKE '%{}%'".format(column, value)
            results = db.select_custom(where=where)

            for result in results:
                print(format_result(result))

                ## Get results of sub-sessions too
                if (result["session"]):

                    sub_where = "parent_session = {} AND {} NOT LIKE '%{}%'".format(result["id"], column, value)
                    sub_results = db.select_custom(where=sub_where)

                    for sub_result in sub_results:
                        print(format_result(sub_result))


else:
    print("Incorrect number of arguments passed!")