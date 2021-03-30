
# => 도전과제 할 때 따옴표를 제거해주세요
import psycopg2
import csv
import os
# 아래 변수들의 명칭을 변경하면 테스트가 정상 작동 안할 수 있습니다.

if __name__ == '__main__': # 직접 실행

    class ConnectionSet:
        def __init__(self):
            self.host = 'ec2-54-211-176-156.compute-1.amazonaws.com'
            self.user = 'oxyjeoubcrvgnd'
            self.password = 'cda41dbcc9da52941de12e3dc61ade0c2fcb77e34aff7619ed0ee04e9568aa57'
            self.database = 'd441brlclr7kf'

    cn = ConnectionSet()

    connection = psycopg2.connect(
        host=cn.host,
        user=cn.user,
        password=cn.password,
        database=cn.database
    )


# set cursor
cursor = connection.cursor()

# movies table 존재 유무 체크
check_table = """SELECT EXISTS (
    SELECT 1 FROM information_schema.tables
    WHERE table_name='rating_users');
"""
cursor.execute(check_table)

res = cursor.fetchone()
if len(res) > 0:
    print(res)

with open('user_rating.csv') as df:
    reader = csv.DictReader(df)
    
    for n, lines in enumerate(reader):
        insert_line = []
        insert_line.append(n+1)
        insert_line.append(int(lines['userId']))
        insert_line.append(float(lines['rating']))
        insert_line.append(int(lines['movieId']))
        # print(insert_line)
        c = str(insert_line).replace('[','').replace(']','')

        _,r = divmod(n, 1000)
        if r == 0:
            print(c)

        sql = f"""
        INSERT INTO rating_users (id, user_id, rating, movie_id) 
        VALUES ({c})
        """
        cursor.execute(sql)
        # get processing

# commit table delet 부터 실행
connection.commit()

# commit 후
cursor.execute("SELECT * FROM rating_users")
# check update
print(cursor.fetchone())

# close
cursor.close()
connection.close()
