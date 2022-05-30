import secrets
import pymysql.cursors
import requests
import json
import datetime

DB_IP = secrets.DB_IP
DB_USER = secrets.DB_USER
DB_PASS = secrets.DB_PASS
DB_NAME = secrets.DB_NAME
SenateAPI_Key = secrets.SenateAPI_KEY

url = "https://lda.senate.gov/api/v1/contributions/?contribution_contributor=rifle&contribution_date_after=2014-12-31"

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
    results = response["results"]
    for items in results:
        contrib_items = items["contribution_items"]
        for specific_item in contrib_items:
            specific_item["year"] = specific_item["date"][:4]
            newdate = str(
                datetime.datetime.strptime(specific_item["date"], "%Y-%m-%d").date()
            )
            insert_data = list(
                [
                    specific_item["honoree_name"],
                    specific_item["amount"],
                    specific_item["year"],
                    newdate,
                ]
            )
            try:
                nra_sql = """INSERT INTO NRA (member_name, amount, contrib_year, contrib_date)
            VALUES(%s, %s, %s, %s) ;"""
                mycursor.execute(nra_sql, insert_data)
                connection.commit()
            except Exception as e:
                print(e)
    pagenumber = 1
    print(f"Page {pagenumber} done of {pages}")
    pageend = datetime.datetime.now()
    print(f"Query Elapsed Time: {pageend - pagestart}")
    while response["next"]:
        pagenumber = pagenumber + 1
        pagestart = datetime.datetime.now()
        response = requests.get(response["next"]).json()
        results = response["results"]
        for items in results:
            contrib_items = items["contribution_items"]
            for specific_item in contrib_items:
                specific_item["year"] = specific_item["date"][:4]
                newdate = str(
                    datetime.datetime.strptime(specific_item["date"], "%Y-%m-%d").date()
                )
                insert_data = list(
                    [
                        specific_item["honoree_name"],
                        specific_item["amount"],
                        specific_item["year"],
                        newdate,
                    ]
                )
                try:
                    nra_sql = """INSERT INTO NRA (member_name, amount, contrib_year, contrib_date)
              VALUES(%s, %s, %s, %s) ;"""
                    mycursor.execute(nra_sql, insert_data)
                    connection.commit()
                except Exception as e:
                    print(e)
        print(f"Page {pagenumber} done of {pages}")
        end = datetime.datetime.now()
        print(f"Query Elapsed Time: {end - pagestart}")
        print(f"Total Elapesed Time: {end - start}")
    connection.close()
    print("Done")


#   writedata(response)
#   while response['next']:
#     response = requests.get(response['next']).json()
#     cleandata(response)
#     writedata(response)


#     for nradata in response['results']:
#       for item in nradata['contribution_items']:
#         year = item['date'][:4]
#         newdate = str(
#             datetime.datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%SZ").date()
#     )
#         data = list(statedata.values())
#     coviddata = (data[4], data[7], data[8], data[9], data[10], newdate)
#     try:
#         covid_sql = """INSERT INTO coviddata (citycode,confirmed,deaths,recovered,active_cases,report_date)
#         VALUES(%s, %s, %s, %s, %s, %s) ;"""
#         mycursor.execute(covid_sql, coviddata)
#         covrowcount += 1
#         if covrowcount > 10:
#             connection.commit()
#     except Exception as e:
#         print(e)
#     connection.commit()
#     connection.close()
#     print(f"{covrowcount} data records inserted")
#     print("Update Complete")

#     with open('nracontrib.json', 'w') as f:
#         f.write(response.text)
#         jresponse = json.loads(response.text)
#         while jresponse["next"]:
#             response = requests.get(jresponse["next"])
#             f.write(response.text)
#             jresponse = json.loads(response.text)


download_data()


# with open('nratest.json', 'r') as f:
#     content = f.read()

# print(type(content))

# jcontent = json.loads(content)

# for result in jcontent['results']:
#     for item in result['contribution_items']:
#         year = item['date'][:4]
#         print(item['honoree_name'], item['amount'], year)

# counter = int(jcontent['count'])
# pages=int((counter / 25) + (counter % 25>0))
# print(pages)
