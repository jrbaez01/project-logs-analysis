#! /usr/bin/env python2.7
import psycopg2

import analyze

print '''
==============================================================
 _                        ___              _
| |                      / _ \            | |         (_)
| |     ___   __ _ ___  / /_\ \_ __   __ _| |_   _ ___ _ ___
| |    / _ \ / _` / __| |  _  | '_ \ / _` | | | | / __| / __|
| |___| (_) | (_| \__ \ | | | | | | | (_| | | |_| \__ \ \__ \\
\_____/\___/ \__, |___/ \_| |_/_| |_|\__,_|_|\__, |___/_|___/
              __/ | FSND Udacity Project Tool __/ | by Junior
             |___/                           |___/
=============================================================='''

with psycopg2.connect("dbname=news") as conn:
    with conn.cursor() as cursor:
        for query in analyze.queries:
            question, sqlquery, answer = query
            print question
            cursor.execute(sqlquery)
            results = cursor.fetchall()
            for result in results:
                print answer % result

conn.close()
print '==============================================================\nThanks!'
