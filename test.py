import pymysql

db_connection = pymysql.connect(
	    user    = 'root',
        passwd  = '1234',
    	host    = '127.0.0.1',
    	db      = 'gangnam',
    	charset = 'utf8'
)

cursor = db_connection.cursor()
sql = 'SELECT * FROM list;'
cursor.execute(sql)
topics = cursor.fetchall()
print(topics)


# 생긴 데이터 보니 튜플로()만들어짐. 즉 변경하고 뭐하고 싶으면 리스트로 바꿔서 처리해야지 생각 가능!!