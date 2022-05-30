import pymysql
import datetime
import secrets

connection = pymysql.connect(
    host=secrets.DB_IP,
    user=secrets.DB_USER,
    password=secrets.DB_PASS,
    charset="utf8mb4",
    db=secrets.DB_NAME,
    cursorclass=pymysql.cursors.DictCursor,
)

mycursor = connection.cursor()


start = datetime.datetime.now()


createdb = "CREATE DATABASE congress"
drop_nra_query = "drop table if exists NRA;"
create_nra_query = """CREATE TABLE NRA (member_name varchar(100), amount float, contrib_year year, contrib_date date)"""


tb = "describe nra"


try:
    mycursor.execute(drop_nra_query)
    connection.commit()
    print("NRA Table Deleted")
    mycursor.execute(create_nra_query)
    connection.commit()
    print("NRA Table Created Successfully")
except Exception as e:
    print("Exception error occured :", e)

connection.close()
end = datetime.datetime.now()
print(f"Elapsed Time: {end - start}")
