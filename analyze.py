# A list of tuples with the question, sql query and answer format
# [(quetion, sqlquery, answer)]
# that will be fetched by the log_analysis.py tool

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
    )
]
