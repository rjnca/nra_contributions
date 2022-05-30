import secrets
import pymysql.cursors
import requests
import json
import datetime

DB_IP = secrets.DB_IP
DB_USER = secrets.DB_USER
DB_PASS = secrets.DB_PASS
DB_NAME = secrets.DB_NAME
url = "https://lda.senate.gov/api/v1/contributions/?contribution_contributor=rifle&contribution_date_after=2019-12-31"

payload = {}
headers = {"Auhtorization": secrets.SenateAPI_Key}


def download_data():
    connection = pymysql.connect(
        host=DB_IP,
        user=DB_USER,
        password=DB_PASS,
        charset="utf8mb4",
        db=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
    )

    mycursor = connection.cursor()
    start = datetime.datetime.now()
    pagestart = datetime.datetime.now()
    response = requests.get(url, headers=headers, data=payload).json()
    print(f"Record count {response['count']}")
    reccount = int(response["count"])
    pages = (reccount / 25) + (reccount % 25 > 0)
    print(f"This should be {pages} pages")
    for result in response['results']:
        for specific_item in result['contribution_items']:
            if specific_item['honoree_name'] != 'Not Applicable':
                lastname, firstname = items['honoree_name'].split(',')
            else:
                lastname = 'Congressional Committee'
                firstname = 'National Republican'
            rowid = lastname + specific_item['date']
            specific_item["year"] = specific_item["date"][:4]
            newdate = str(
                datetime.datetime.strptime(specific_item["date"], "%Y-%m-%d").date()
            )
            insert_data = list(
                [
                    rowid,
                    lastname,
                    firstname,
                    specific_item["amount"],
                    specific_item["year"],
                    newdate,
                ]
            )
            try:
                nra_sql = """INSERT INTO NRA (rowid, member_first_name, member_last_name, amount, contrib_year, contrib_date)
            VALUES(%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE rowid=rowid;"""
                mycursor.execute(nra_sql, insert_data)
                connection.commit()
            except Exception as e:
                print(e)
            print(insert_data)
    pagenumber = 1
    print(f"Page {pagenumber} done of {pages}")
    pageend = datetime.datetime.now()
    print(f"Query Elapsed Time: {pageend - pagestart}")

    while response["next"]:
        pagenumber = pagenumber + 1
        pagestart = datetime.datetime.now()
        response = requests.get(response["next"]).json()
        for items in response['results']:
            for specific_item in items['contribution_items']:
                if specific_item['honoree_name'] != 'Not Applicable':
                    lastname, firstname = items['honoree_name'].split(',')
                else:
                    lastname = 'Congressional Committee'
                    firstname = 'National Republican'
                rowid = lastname + specific_item['date']
                specific_item["year"] = specific_item["date"][:4]
                newdate = str(
                    datetime.datetime.strptime(specific_item["date"], "%Y-%m-%d").date()
                )
                insert_data = list(
                    [ rowid,
                        lastname,
                        firstname,
                        specific_item["amount"],
                        specific_item["year"],
                        newdate,
                    ]
                )
                try:
                    nra_sql = """INSERT INTO NRA (member_name, amount, contrib_year, contrib_date)
              VALUES(%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE rowid=rowid;"""
                    mycursor.execute(nra_sql, insert_data)
                    connection.commit()
                except Exception as e:
                    print(e)
            print(insert_data)
        print(f"Page {pagenumber} done of {pages}")
        end = datetime.datetime.now()
        print(f"Query Elapsed Time: {end - pagestart}")
        print(f"Total Elapesed Time: {end - start}")
    connection.close()
    print("Done")

download_data()
