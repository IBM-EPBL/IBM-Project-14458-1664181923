import ibm_db

try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PROTOCOL=TCPIP;PORT=32731;UID=ytl80962;PWD=9VzjxssPbixN82n5;Security=SSL;SSLSecurityCertificate=DigiCertGlobalRootCA.crt", "", "")
    print("Connected to the database")
except:
    print("Error in connecting to the database: ", ibm_db.conn_errormsg())


def register(username, password, email, Gender, age, height, weight, BMI):
    insert_sql = "INSERT INTO  YTL80962.STUDENT1 VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    prep_stmt = ibm_db.prepare(conn, insert_sql)
    ibm_db.bind_param(prep_stmt, 1, username)
    ibm_db.bind_param(prep_stmt, 2, password)
    ibm_db.bind_param(prep_stmt, 3, email)
    ibm_db.bind_param(prep_stmt, 4, Gender)
    ibm_db.bind_param(prep_stmt, 5, age)
    ibm_db.bind_param(prep_stmt, 6, height)
    ibm_db.bind_param(prep_stmt, 7, weight)
    ibm_db.bind_param(prep_stmt, 8, BMI)
    ibm_db.execute(prep_stmt)


def login(username, password):
    select_sql = "SELECT * FROM  YTL80962.STUDENT1 WHERE USERNAME = ? AND PASSWORD = ?"
    prep_stmt = ibm_db.prepare(conn, select_sql)
    ibm_db.bind_param(prep_stmt, 1, username)
    ibm_db.bind_param(prep_stmt, 2, password)
    out = ibm_db.execute(prep_stmt)
    result_dict = ibm_db.fetch_assoc(prep_stmt)
    print(result_dict)
    return result_dict

# def register(name, email, rollno, password):
#     insert_sql = "INSERT INTO  YTL80962.STUDENT VALUES (?, ?, ?, ?,)"
#     prep_stmt = ibm_db.prepare(conn, insert_sql)
#     ibm_db.bind_param(prep_stmt, 1, name)
#     ibm_db.bind_param(prep_stmt, 2, email)
#     ibm_db.bind_param(prep_stmt, 3, rollno)
#     ibm_db.bind_param(prep_stmt, 4, password)
#     ibm_db.execute(prep_stmt)


# def login(name, password):
#     select_sql = "SELECT * FROM  YTL80962.STUDENT WHERE USERNAME = ? AND PASSWORD = ?"
#     prep_stmt = ibm_db.prepare(conn, select_sql)
#     ibm_db.bind_param(prep_stmt, 1, name)
#     ibm_db.bind_param(prep_stmt, 2, password)
#     out = ibm_db.execute(prep_stmt)
#     result_dict = ibm_db.fetch_assoc(prep_stmt)
#     print(result_dict)
#     return result_dict