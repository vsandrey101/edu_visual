import mysql.connector as connection
from werkzeug.security import generate_password_hash

def get_db():
    try:
        db_app = connection.connect(host="localhost", database = 'app_db', user="admin1", password="admin1",use_pure=True)
    except Exception as e:
        db_app.close()
        print(str(e))
    return db_app 

def admins():
    db_app = get_db()
    cursor = db_app.cursor()
    cursor.execute(f"""SELECT `user_id`, `password` FROM `users`""")
    admins = dict(cursor.fetchall())
    db_app.close()
    admins = {str(k):generate_password_hash(p) for k, p in admins.items()}
    return admins
     
def list_tables(table, user_id):
    db_app = get_db()
    cursor = db_app.cursor()
    cursor.execute(f"""SELECT `id`, `name` FROM `{table}` WHERE tutor_id = {user_id} OR tutor_id = 0""")
    data = dict(cursor.fetchall())
    db_app.close()
    return data

def list_diagrams(group):
    db_app = get_db()
    cursor = db_app.cursor()
    try:
        cursor.execute(f"""SELECT `id`, `name` FROM `diagrams` WHERE `group_id` = {group};""")
        features = list(cursor.fetchall())
    except:
        features = []
    db_app.close()
    return features

def sql_source(source_id):
    db_app = get_db()
    cursor = db_app.cursor()
    cursor.execute(f"""SELECT `path`, `type` FROM `sources` WHERE `id` = {source_id};""")
    source_inf = cursor.fetchall()[0]
    db_app.close()
    #type + path
    return source_inf[1], source_inf[0]

    
    
def params(id):
    db_app = get_db()
    cursor = db_app.cursor()
    cursor.execute(f"""SELECT `template_id`, `source_id`, `vars` FROM `diagrams` WHERE `id` = '{id}'""")
    data_plot = cursor.fetchall()[0]
    db_app.close()
    #template_id, source_id, vars
    return data_plot[0], data_plot[1], data_plot[2]



    
    

# def query_sql(feature, userid, var1, var2):
#     db_app = get_db()
#     cursor = db_app.cursor()
#     cursor.execute(f"""SELECT `query` FROM `queries` WHERE `feature` = "{feature}";""")
#     query = cursor.fetchone()[0]
#     db_app.close()
#     template_values = {
#         'userid': userid,
#         'var1': var1,
#         'var2': var2,
#     }
#     return query.format(**template_values)

def get_code(id):
    db_app = get_db()
    cursor = db_app.cursor()
    cursor.execute(f"""SELECT `code` FROM `plots` WHERE `id` = '{id}'""")
    exec_code = cursor.fetchone()[0]
    return exec_code

# def add_csv(fname, path):
#     db_app = get_db()
#     cursor = db_app.cursor()
#     cursor.execute(f"""INSERT INTO `sources` (`id`, `name`, `type`, `path`) VALUES (NULL, '{fname}', '0', '{path}')""")
#     db_app.commit()
#     db_app.close()
    
# def add_plotly(name, index, code):
#     db_app = get_db()
#     cursor = db_app.cursor()
#     cursor.execute(f"""INSERT INTO `sources` (`id`, `name`, `type`, `path`) VALUES (NULL, '{fname}', '0', '{path}')""")
#     db_app.commit()
#     db_app.close()

# def get_headers(table):
#     db_app = get_db()
#     cursor = db_app.cursor()
#     cursor.execute(f"""SELECT `COLUMN_NAME` FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{table}'""")
#     columns = cursor.fetchall()
#     db_app.close()
#     return  [1:])

def add_table(table, headers, data_str):
    # headers = get_headers(table)
    db_app = get_db()
    cursor = db_app.cursor()
    cursor.execute(f"""INSERT INTO `{table}` (`id`, {headers}) VALUES (NULL, {data_str})""")
    db_app.commit()
    db_app.close()
    
def delete_row(table, id, tutor_id):
    db_app = get_db()
    cursor = db_app.cursor()
    cursor.execute(f"""DELETE FROM `{table}` WHERE `{table}`.`id` = {id} AND `{table}`.`tutor_id` = {tutor_id}""")
    db_app.commit()
    db_app.close()
    

# def get_stud_id(hash, tutor_id):
#     db_app = get_db()
#     cursor = db_app.cursor()
#     cursor.execute(f"""SELECT student_id FROM `students` WHERE `students`.`hash_name` = '{hash}' AND `students`.`tutor_id` = {tutor_id}""")
#     exec_req = cursor.fetchall()
#     if len(exec_req) > 0:
#         #возвращаем id со связанным хэшем
#         return exec_req[0][0]
#     #если нет, то берем предыдущий максимум+1 или 1 при NULL
#     cursor.execute(f"""SELECT COALESCE(MAX(student_id)+1, 1) FROM `students` WHERE `students`.`tutor_id` = {tutor_id}""")
#     exec_req = cursor.fetchone()[0]
#     db_app.close()
#     return exec_req

def get_stud_id(hash, tutor_id):
    db_app = get_db()
    cursor = db_app.cursor()
    cursor.execute(f"""SELECT IF((SELECT COUNT(student_id) FROM `students` WHERE `students`.`hash_name` = '{hash}' AND `students`.`tutor_id` = {tutor_id}) > 0, (SELECT student_id FROM `students` WHERE `students`.`hash_name` = '{hash}' AND `students`.`tutor_id` = {tutor_id} LIMIT 1), (SELECT COALESCE(MAX(student_id)+1, 1) FROM `students` WHERE `students`.`tutor_id` = {tutor_id}));""")
    exec_req = cursor.fetchone()[0]
    db_app.close()
    return exec_req

def get_group_id(name, tutor_id):
    db_app = get_db()
    cursor = db_app.cursor()
    cursor.execute(f"""SELECT `groups`.`id` FROM `groups` WHERE `groups`.`tutor_id` = {tutor_id} AND `groups`.`name` = '{name}';""")
    exec_req = cursor.fetchone()
    if exec_req is None:
        #если нет группы, то создаем
        cursor.execute(f"""INSERT INTO `groups` (`groups`.`tutor_id`, `groups`.`name`) VALUES ({tutor_id}, '{name}');""")
        db_app.commit()
        cursor.execute(f"""SELECT `groups`.`id` FROM `groups` WHERE `groups`.`tutor_id` = {tutor_id} AND `groups`.`name` = '{name}';""")
        exec_req = cursor.fetchone()
    
    db_app.close()
    return exec_req[0]

def add_stud_db(hash, tutor_id, group):
    db_app = get_db()
    cursor = db_app.cursor()
    cursor.execute(f"""SELECT `students`.`id` FROM `students` WHERE `students`.`hash_name` = '{hash}' AND `students`.`tutor_id` = {tutor_id} AND `students`.`groups` = '{group}';""")
    exec_req = cursor.fetchone()
    if exec_req is None:
        stud_id = get_stud_id(hash, tutor_id)
        #если нет записи, то создаем
        cursor.execute(f"""INSERT INTO `students` (`students`.`hash_name`, `students`.`tutor_id`, `students`.`student_id`, `students`.`groups`) VALUES ('{hash}', {tutor_id}, {stud_id}, '{group}');""")
    db_app.commit()
    db_app.close()
    
def get_stud_id_hash(stud_id, group):
    db_app = get_db()
    cursor = db_app.cursor()
    cursor.execute(f"""SELECT `students`.`hash_name` FROM `students` WHERE `students`.`groups` = {group} AND `students`.`student_id` = {stud_id};""")
    exec_req = cursor.fetchone()[0]
    db_app.close()
    return exec_req




#print(get_stud_id("e3cb8fbf7cf35594d3a9613498c74514", 3))
#print(get_group_id("ГР-1-1", 2))
    
    

    
    




