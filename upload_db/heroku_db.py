"""
Part 3

클라우드 데이터베이스에 'passenger' 라는 테이블을 생성하고 titanic.csv 에 있는 데이터를 'passenger' 테이블로 옮깁니다.

passenger 테이블의 필드는 데이터에 알맞게 추가합니다 (필드명은 자유입니다).
아래에는 각 필드에 해당하는 데이터 타입입니다.
- Survived: INT
- Pclass: INT
- Name: VARCHAR(128)
- Sex: VARCHAR(12)
- Age: FLOAT
- Siblings/Spouses Aboard: INT
- Parents/Children Aboard: INT
- Fare: FLOAT

다 옮긴 뒤에 'passenger' 테이블이 있는 데이터베이스 정보를 아래 입력합니다.

아래 psycopg2.connect 를 이용해 connection 변수가 데이터베이스와 연결할 수 있도록 다음 변수들에 알맞은 정보를 담습니다:

- host: 데이터베이스 호스트 주소를 입력합니다.
- user: 데이터베이스 유저 정보를 입력합니다.
- password: 데이터베이스 비밀번호를 입력합니다.
- database: 데이터베이스 이름을 입력합니다.
"""

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
else : # case for pytest test에서 호출하면
    host = 'arjuna.db.elephantsql.com'
    user = 'wewamckt'
    password = 'JDurOyNFVtqky8JGYI95um32troSPY8X'
    database = 'wewamckt'

    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

# set cursor
cursor = connection.cursor()

# movies table 존재 유무 체크
check_table = """SELECT EXISTS (
    SELECT 1 FROM information_schema.tables
    WHERE table_name='movies');
"""
cursor.execute(check_table)

res = cursor.fetchone()
if len(res) > 0:
    print(res)
    # sql = """DROP TABLE passenger"""
    # cursor.execute(sql)
    # # commit으로 실제로 삭제, 지금안해도 마지막 commit할때 쿼리문 순서대로 실행됨
    # # connection.commit()

# create table
# cursor.execute(
# """
# CREATE TABLE passenger (
#     id INTEGER PRIMARY KEY,
#     Survived INTEGER,
#     Pclass INTEGER,
#     Name VARCHAR(128),
#     Sex VARCHAR(12),
#     Age FLOAT,
#     Siblings_Spouses_Aboard INTEGER ,
#     Parents_Children_Aboard INTEGER ,
#     Fare FLOAT
# );
# """)

mapper = {
      'movieId': int()
    , 'title': str()
    , 'genres':str()
    , 'weight_rating':float()
}

with open('movies_db.csv') as df:
    reader = csv.DictReader(df)
    
    for n, lines in enumerate(reader):
        insert_line = []
        insert_line.append(n+1)
        insert_line.append(int(lines['movieId']))
        insert_line.append(str(lines['title']).replace("\'","\""))
        insert_line.append(str(lines['genres']))
        insert_line.append(float(lines['weight_rating']))
        # print(insert_line)
        c = str(insert_line).replace('[','').replace(']','')
        print(c)
        sql = f"""
        INSERT INTO movies (id, movie_id, title, genre, weight_rating ) 
        VALUES ({c})
        """
        cursor.execute(sql)
        # get processing


# commit table delet 부터 실행
connection.commit()

# commit 후
cursor.execute("SELECT * FROM movies")
# check update
print(cursor.fetchone())

# close
cursor.close()
connection.close()
