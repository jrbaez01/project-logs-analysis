#! /usr/bin/env python2.7
import psycopg2

# '''
# CREATE VIEW article_views
# AS SELECT a.id, count(a.id) AS views
# FROM articles AS a JOIN log AS l
# ON l.path = CONCAT('/article/', a.slug)
# WHERE l.status = '200 OK'
# GROUP BY a.id;
#
# CREATE VIEW requests_by_day
# AS SELECT day, requests, count(*) AS errors
# FROM log, (SELECT DATE_TRUNC('day', time) AS day,
# count(*) AS requests
# FROM log GROUP BY day) AS rbd
# WHERE day = DATE_TRUNC('day', log.time)
# and log.status = '404 NOT FOUND'
# GROUP BY day, requests;
# '''

queries = [
    (
        '\nWhat are the most popular three articles of all time?',
        '''
            SELECT
                articles.title,
                article_views.views
            FROM articles, article_views
            WHERE articles.id = article_views.id
            ORDER BY views DESC
            limit 3;
        ''',
        '\t=> %s -- %s views'
    ),
    (
        '\nWho are the most popular article authors of all time?',
        '''
            SELECT
                authors.name,
                SUM(article_views.views) AS total_views
            FROM authors
            JOIN articles
                ON authors.id = articles.author
            JOIN article_views
                ON articles.id = article_views.id
            GROUP BY authors.name
            ORDER BY total_views DESC;
        ''',
        '\t=> %s -- %s views'
    ),
    (
        '\nOn which days did more than 1% of requests lead to errors?',
        '''
            SELECT
                to_char(day, 'Month DD, YYYY') AS day,
                to_char(errors*100.0/requests, 'FM0.90') AS errors
            FROM requests_by_day
            WHERE errors*100.0/requests > 1
            ORDER BY errors DESC;
        ''',
        '\t=> %s -- %s%% errors'
    ),
]

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
        for query in queries:
            question, query, answer = query
            print question
            cursor.execute(query)
            results = cursor.fetchall()
            for result in results:
                print answer % result

conn.close()
print '==============================================================\nThanks!'
