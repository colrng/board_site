import pymysql

def get_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',  # MySQL 사용자 이름
        password='0826',  # MySQL 비밀번호
        database='bulletin_board',  # 사용할 데이터베이스 이름
        port=3306,
        cursorclass=pymysql.cursors.DictCursor  # 결과를 딕셔너리로 반환
    )
    return connection
