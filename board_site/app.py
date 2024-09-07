from flask import Flask, render_template, request, redirect, url_for
from db import get_connection

app = Flask(__name__)

# 게시글 목록 조회
@app.route('/')
def index():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
        posts = cursor.fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# 게시글 작성
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO posts (title, content) VALUES (%s, %s)"
            cursor.execute(sql, (title, content))
            connection.commit()
        connection.close()
        return redirect(url_for('index'))
    
    return render_template('create.html')

# 게시글 수정
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    connection = get_connection()
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        with connection.cursor() as cursor:
            sql = "UPDATE posts SET title = %s, content = %s WHERE id = %s"
            cursor.execute(sql, (title, content, id))
            connection.commit()
        connection.close()
        return redirect(url_for('index'))
    
    # 게시글 조회 후 수정 페이지에 데이터 전달
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
        post = cursor.fetchone()
    connection.close()
    return render_template('update.html', post=post)

# 게시글 삭제
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "DELETE FROM posts WHERE id = %s"
        cursor.execute(sql, (id,))
        connection.commit()
    connection.close()
    return redirect(url_for('index'))

# 게시글 검색
@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '')
    search_type = request.args.get('search_type', 'all')

    connection = get_connection()
    with connection.cursor() as cursor:
        if search_type == 'title':
            sql = "SELECT * FROM posts WHERE title LIKE %s"
            cursor.execute(sql, ('%' + keyword + '%',))
        elif search_type == 'content':
            sql = "SELECT * FROM posts WHERE content LIKE %s"
            cursor.execute(sql, ('%' + keyword + '%',))
        else:  # 'all' or any other value
            sql = "SELECT * FROM posts WHERE title LIKE %s OR content LIKE %s"
            cursor.execute(sql, ('%' + keyword + '%', '%' + keyword + '%'))

        posts = cursor.fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)
