import mysql.connector as connection
from werkzeug.security import generate_password_hash

def get_db():
    try:
        db_app = connection.connect(host="localhost", database = 'app_db', user="vis_read",use_pure=True)
    except Exception as e:
        db_app.close()
        print(str(e))
    return db_app 

def admins():
    db_app = get_db()
    cursor = db_app.cursor()
    cursor.execute(f"""SELECT `user_id`, `password` FROM `users` WHERE `group_id` = "1";""")
    admins = dict(cursor.fetchall())
    db_app.close()
    admins = {str(k):generate_password_hash(p) for k, p in admins.items()}
    return admins
     
def list_tables(table):
    db_app = get_db()
    cursor = db_app.cursor()
    cursor.execute(f"""SELECT `id`, `name` FROM `{table}`""")
    data = dict(cursor.fetchall())
    db_app.close()
    return data

def list_diagrams(user_id):
    db_app = get_db()
    cursor = db_app.cursor()
    try:
        cursor.execute(f"""SELECT `group_id` FROM `users` WHERE `user_id` = {user_id};""")
        group = cursor.fetchone()[0]
        print(group)
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
    
def delete_row(table, id):
    db_app = get_db()
    cursor = db_app.cursor()
    cursor.execute(f"""DELETE FROM `{table}` WHERE `{table}`.`id` = {id}""")
    db_app.commit()
    db_app.close()
    
    

    
    




