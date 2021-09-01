from flask import Flask, render_template, redirect, request
from data import Articles
import pymysql

db_connection = pymysql.connect(
	    user    = 'root',
        passwd  = '1234',
    	host    = '127.0.0.1',
    	db      = 'gangnam',
    	charset = 'utf8'
)

app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/', methods=['GET', 'POST'])
def index():
    name = "JUNG"
    return render_template('index.html', data=name)

@app.route('/articles', methods=['GET','POST'])
def articles():
    # list_data = Articles()   # 목업데이터가 아니라 연결된 DB에서 불러오기위함. # DB가 튜플로 만들어지므로 html파일에서 기존 딕셔너리문법 말고, 튜플 인덱스를 사용한다!
    cursor = db_connection.cursor()
    sql = 'SELECT * FROM list;'
    cursor.execute(sql)
    topics = cursor.fetchall()
    print(topics)
    return render_template('articles.html', data = topics)
    
@app.route('/detail/<ids>')  # <> params처리
def detail(ids):
    # list_data = Articles()
    cursor = db_connection.cursor()
    sql = f'SELECT * FROM list WHERE id={int(ids)};'
    cursor.execute(sql)
    topic = cursor.fetchone()       # fetchall이면 튜플 속 튜플로 나오니 인덱싱 복잡. fetchone으로 하나의 튜플 인덱싱 이지.
    print(topic)
    # for data in list_data:
    #     if data['id'] == int(ids):
    #         article = data
    return render_template('article.html', article1=topic)

# post방식 구현, request모듈 사용
@app.route('/add_article', methods=['GET','POST'])
def add_article():
    if request.method == "GET":
        return render_template('add_article.html')
    else:
        title = request.form["title"]
        descs = request.form["desc1"]
        author = request.form["author"]
        
        cursor = db_connection.cursor()
        sql = f"INSERT INTO list (title, description, author) VALUES ('{title}', '{descs}', '{author}');"
        cursor.execute(sql)
        db_connection.commit()
        return redirect('/articles')   # /add_article 경로에서 /articles경로로 다시 돌아감.

@app.route('/delete/<ids>', methods=['GET','POST'])
def delete(ids):
    cursor =db_connection.cursor()
    sql = f'DELETE FROM list WHERE id={int(ids)};'   # DB에서 Delete Row(s)하는 쿼리문. DB에서 삭제하면 당연히 사이트에 안뜨겟지 오!
    cursor.execute(sql)
    db_connection.commit()         # 수정, 추가시에는 db_connection에다 commit해줘야함. (조회시에는 커서에다 fetch하지만.)
    return redirect('/articles')   # 왜render_template? 데이터를 또 던져줘야..
                                   # redirect로 /articles로 바로 갈 수 있음.


if __name__ == '__main__':
    app.run(debug=True)