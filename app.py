from flask import Flask, render_template, redirect, request, session, url_for
# from data import Articles
import pymysql
from passlib.hash import pbkdf2_sha256
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = 'gangnam'

db_connection = pymysql.connect(
	    user    = 'root',
        passwd  = '1234',
    	host    = '127.0.0.1',
    	db      = 'gangnam',
    	charset = 'utf8'
)

# 로그아웃상태서 삭제,편집,쓰기 기능이 안되게 하기 위해서.
def is_logged_in(f):
    # @데코레이터 체크기능 함수 만드는 방법
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_logged' in session:
            return f(*args, **kwargs)   # 체크 통과 후 다음의 함수가 시행된다.
        else:
            return redirect(url_for('login'))
    return wrap

# 삭제는 admin만 할 수 있게.
def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['email'] == 'admin@gmail.com' :
            return f(*args, **kwargs)
        else:
            return redirect('/articles')
    return wrap




@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/', methods=['GET', 'POST'])
def index():
    name = "JUNG"
    # print(request.headers)
    print(len(session))      # 로그인 안되면 0, 로그인되면 다른 숫자.
    return render_template('index.html', data=name, user=session)  # 아직 로그인 유지 check는 안하고 있음. 껍데기만 하는중.

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method =='GET':
        return render_template('register.html', user=session)
    else:
        username = request.form["username2"]
        email = request.form["email2"]
        password = pbkdf2_sha256.hash(request.form["password2"])   # 비밀번호를 hash코드로 바꾼 것이 DB에 들어가게 된다.
        cursor = db_connection.cursor()

        # email 중복을 조회하기 위해
        sql_1 = f"SELECT * FROM users WHERE email='{email}'"
        cursor.execute(sql_1)
        user = cursor.fetchone()  # 조회니까 commit없이 fetchone으로 조회.
        print(user)
        if user == None:
            sql = f"INSERT INTO users (username, email, password) VALUES ('{username}', '{email}', '{password}');"
            cursor.execute(sql)
            db_connection.commit()
            return redirect('/')
        else:
            return redirect('/register')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', user=session)
    else:
        email = request.form['email']
        password = request.form['password']
        #이제 db조회
        sql_1 = f"SELECT * FROM users WHERE email='{email}'"
        cursor = db_connection.cursor()
        cursor.execute(sql_1)
        user = cursor.fetchone()
        print(user)                 # email이 기존 DB에 있을때 : 튜플형식으로 조회됨. 없을때 : None뜸.(어떤형식으로 데이터가 오는지 확인해야함!!)
        # return "success"   
        if user == None:
            return redirect('/login')
        else:
            # 이제 비밀번호 확인
            # 조회해온 데이터가 튜플이므로 튜플사용.
            # verify이용.
            # 로그인이 되면 session이라는 dict생기게만듬.
            result =  pbkdf2_sha256.verify(password, user[3])
            if result == True:
                #세션 딕셔너리형태로 저장함.
                session['id']  = user[0]
                session['username'] = user[1]
                session['email'] = user[2]
                session['date'] = user[4]
                session['is_logged'] = True
                print(session)
                return redirect('/')
            else:
                return redirect('login')

@app.route('/logout', methods=['GET','POST'])
def logout():
    session.clear()
    return redirect('/')
            


@app.route('/articles', methods=['GET','POST'])
def articles():
    # list_data = Articles()   # 목업데이터가 아니라 연결된 DB에서 불러오기위함. # DB가 튜플로 만들어지므로 html파일에서 기존 딕셔너리문법 말고, 튜플 인덱스를 사용한다!
    cursor = db_connection.cursor()
    sql = 'SELECT * FROM list;'
    cursor.execute(sql)
    topics = cursor.fetchall()
    print(topics)
    return render_template('articles.html', data = topics, user=session)
    
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
    return render_template('article.html', article1=topic, user=session)

# post방식 구현, request모듈 사용
@app.route('/add_article', methods=['GET','POST'])
@is_logged_in
def add_article():
    if request.method == "GET":
        return render_template('add_article.html', user=session)
    else:
        title = request.form["title"]
        desc = request.form["desc"]
        author = request.form["author"]
        
        cursor = db_connection.cursor()
        sql = f"INSERT INTO list (title, description, author) VALUES ('{title}', '{desc}', '{author}');"
        cursor.execute(sql)
        db_connection.commit()
        return redirect('/articles' )   # /add_article 경로에서 /articles경로로 다시 돌아감.

@app.route('/edit_article/<ids>', methods=['GET','POST'])
# @ 체크함수
@is_logged_in
def edit_article(ids):
    if request.method == 'GET':
        cursor = db_connection.cursor()
        sql = f'SELECT * FROM list WHERE id={int(ids)};'
        cursor.execute(sql)
        topic = cursor.fetchone()       # select 즉, 조회니까 commit없이.
        print(topic)
        return render_template('edit_article.html', article1=topic, user=session)
        
    else:
        title = request.form["title"]
        desc = request.form["desc"]
        author = request.form["author"]

        cursor = db_connection.cursor()
        sql = f"UPDATE list SET title = '{title}', description = '{desc}', author = '{author}' WHERE (id = {int(ids)});"
        cursor.execute(sql)
        db_connection.commit()
        return redirect('/articles')


@app.route('/delete/<ids>', methods=['GET','POST'])
@is_logged_in
@is_admin
def delete(ids):
    cursor =db_connection.cursor()
    sql = f'DELETE FROM list WHERE id={int(ids)};'   # DB에서 Delete Row(s)하는 쿼리문.
    cursor.execute(sql)
    db_connection.commit()         # 수정, 추가시에는 db_connection에다 commit해줘야함. (조회시에는 커서에다 fetch하지만.)
    return redirect('/articles')   # 왜render_template? 데이터를 또 던져줘야..
                                   # redirect로 /articles로 바로 갈 수 있음.


if __name__ == '__main__':
    app.run(debug=True)