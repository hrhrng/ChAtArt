

def run_sql(sql_to_run: str) -> str:
    """
    run sql and get the url of the result
    :param sql_to_run:
    :return: url of the result
    """
    return "https://baidu.com/q?{s}".format(s=sql_to_run)

