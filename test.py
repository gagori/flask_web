# import pymysql

# db_connection = pymysql.connect(
# 	    user    = 'root',
#         passwd  = '1234',
#     	host    = '127.0.0.1',
#     	db      = 'gangnam',
#     	charset = 'utf8'
# )

# cursor = db_connection.cursor()
# sql = 'SELECT * FROM list;'
# cursor.execute(sql)
# topics = cursor.fetchall()
# print(topics)


# # 생긴 데이터 보니 튜플로()만들어짐. 즉 변경하고 뭐하고 싶으면 리스트로 바꿔서 처리해야지 생각 가능!!

from passlib.hash import pbkdf2_sha256

hash = pbkdf2_sha256.hash("1234")
print(hash)               # 비밀번호 등을 해쉬코드로 바꾸는 것을 encoding이라고 한다. <-> decoding

# 우리는 decode할 순 없지만 verify로 동일한지 확인할 수 있다.

result = pbkdf2_sha256.verify("1234", hash)
print(result)