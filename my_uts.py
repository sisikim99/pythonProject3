import pymysql
import cx_Oracle
import pandas as pd
import requests

dsn = cx_Oracle.makedsn('localhost', 1521, 'xe')
seoul_api_key = "654e4d6d74726c6133394642467848"
riot_api_key = "RGAPI-3fab9083-66ad-4814-bf4c-08e06dd6810e"


def df_creater(url):
    url = url.replace('(인증키)', seoul_api_key).replace('xml', 'json').replace('/5/', '/1000/')
    res = requests.get(url).json()
    key = list(res.keys())[0]
    data = res[key]['row']
    df = pd.DataFrame(data)
    return df


def db_open():
    global db
    global cursor
    db = cx_Oracle.connect(user='ICIA', password='1234', dsn=dsn)
    cursor = db.cursor()
    print("oracle open")


def oracle_execute(q):
    global db
    global cursor
    try:
        if 'select' in q:
            df = pd.read_sql(sql=q, con=db)
            return df
        cursor.execute(q)
        return "oracle query success"
    except Exception as e:
        print(e)


def oracle_close():
    global db
    global cursor
    try:
        db.commit()
        cursor.close()
        db.close()
        return "oracle close"
    except Exception as e:
        print(e)


# mysql

def connect_mysql(db):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db=db, charset='utf8')
    return conn


def mysql_execute(query, conn):
    cursor_mysql = conn.cursor()
    cursor_mysql.execute(query)
    result = cursor_mysql.fetchall()
    return result


def mysql_execute_dict(query, conn):
    cursor_mysql = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor_mysql.execute(query)
    result = cursor_mysql.fetchall()
    return result


def get_puuid(user):
    url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{user}?api_key={riot_api_key}"
    res = requests.get(url).json()
    return res['puuid']


def get_matchid(puuid,num):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={num}&api_key={riot_api_key}"
    res = requests.get(url).json()
    return res


def get_match_timeline(matchid):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchid}?api_key={riot_api_key}"
    res1 = requests.get(url).json()
    url2 = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchid}/timeline?api_key={riot_api_key}"
    res2 = requests.get(url2).json()
    return res1, res2