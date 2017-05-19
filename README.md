# Project: Logs Analysis Tool
With this project I learned how to use advanced SQL queries to analyze data from the logs of a web service 
to answer important questions like "What is the most popular page?" and "When was the error rate high?"

## Dependencies
In order to be able to run the project you will need to have installed:
 - Python 2.7
 - PostgressSQL

Also when postgressSQL is up and running:
 - Create a database named "news" and restore the newsdata.sql dump.
 - Create the following article_views and resquests_by_day database VIEWS
 
Take a look to my good looking SQL Create Views statements below!

``` SQL
CREATE VIEW article_views AS
SELECT 
  a.id,
  count(a.id) AS views
FROM articles AS a 
JOIN log AS l
  ON l.path = CONCAT('/article/', a.slug)
WHERE l.status = '200 OK'
GROUP BY a.id;
```
``` SQL
CREATE VIEW requests_by_day AS
SELECT 
  day,
  requests,
  count(*) AS errors
FROM log,
  (SELECT
   DATE_TRUNC('day', time) AS day,
   count(*) AS requests
   FROM log GROUP BY day) AS rbd
WHERE 
  day = DATE_TRUNC('day', log.time)
  and log.status = '404 NOT FOUND'
GROUP BY day, requests;
``` 
## How to run
1. Keep calm my friend.
2. Clone the source code in your local envarioment
3. Enter to the code directory and run the command: ```python log_analysis.py```
