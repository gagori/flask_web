from flask import Flask, render_template
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
    
@app.route('/detail/<ids>')
def detail(ids):
    # list_data = Articles()
    cursor = db_connection.cursor()
    sql = f'SELECT * FROM list WHERE id={int(ids)};'
    cursor.execute(sql)
    topic = cursor.fetchone()
    print(topic)
    # for data in list_data:
    #     if data['id'] == int(ids):
    #         article = data
    return render_template('article.html', article1=topic)


if __name__ == '__main__':
    app.run(debug=True)