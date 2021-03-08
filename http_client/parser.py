from typing import List

import requests
import json
import pymysql


def req():

    url = "http://localhost:3000/ra/company-resume"

    headers = {'User-Agent': 'PostmanRuntime/7.26.10'}

    with requests.request(
            method='GET',
            url=url,
            headers=headers
    ) as response_json:
        if response_json.status_code != 200:
            raise Exception(f' code: {response_json.status_code}')
    return response_json.text


def process():
    response_dict = json.loads(req())
    for data in response_dict['data']:
        if not_exists_complaint_by_id(data):
            save_complaint(data)


def not_exists_complaint_by_id(data):
    return len(select(f"""
        select * from complaint where id = '{data['id']}' 
        """)) == 1


def save_complaint(data):
    execute_query(f"""
        insert into complaint (id, created, description, solved, evaluated, title, userName, status) 
        values ('{data['id']}', '{data['created']}', '{data['description']}', '{data['solved']}', '{data['evaluated']}', '{data['title']}', '{data['userName']}', '{data['status']}')
        """)


def select(query: str) -> List:
    db = connection()
    try:
        cursor = db.cursor()
        cursor.execute(query)

        return cursor.fetchall()

    finally:
        db.close()


def execute_query(query: str):
    db = connection()
    try:
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()

    finally:
        db.close()


def connection():
    return pymysql.connect(
        host="localhost",
        port=3350,
        user="root",
        passwd="root",
        db="ra_db")


if __name__ == '__main__':
    process()
