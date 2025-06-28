from flask import Flask, render_template,request, session
from flask_cors import CORS
import plotly
import plotly.graph_objs as go
import plotly.express as px
import string, random
import pandas as pd
import numpy as np
import json, os, re, csv
import mysql.connector as connection
from sql_module import get_code, list_diagrams, admins, params, sql_source, list_tables, add_table, get_db, delete_row
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from fileinput import filename
from IPython.display import HTML


UPLOAD_FOLDER = os.path.join('uploads')

 
# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}
app = Flask(__name__)
auth = HTTPBasicAuth()
cors = CORS(app, resources={r"/close": {"origins": "*"}, r"/set_plot": {"origins": "*"}})
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
app.secret_key = 'VERY_SECRET'


users_admin = admins()
print(users_admin)
@auth.verify_password
def verify_password(username, password):
    if username in users_admin and check_password_hash(users_admin.get(username),
                                                 password):
        return username

def create_string(data: list) -> str:
    data = ["'" + i + "'" for i in data]
    return (", ".join(data))

@app.route('/')
def index():
    fig = go.Figure()
    fig.update_layout(title_text='Введите ID', title_x=0.5)
    return render_template('index.html', plot=plotly.io.to_json(fig))



def load_source(id):
    s_type, in_str = sql_source(id)
    if s_type == False:
        df = pd.read_csv(in_str)
    else:
        credintials, query = in_str.split("@")
        credintials = credintials.split("&")
        try:
            mydb = connection.connect(host=credintials[0], database = credintials[1], user=credintials[2],use_pure=True)
        except Exception as e:
            mydb.close()
            print(str(e))
        df = pd.read_sql(query, mydb)
        mydb.close()
    return df



def create_plot(feature, userid):
    template_id, source_id, vars = params(feature)
    df = load_source(source_id)
    df = df.rename(columns=json.loads(vars))
    print(df.columns.values)
    df = (df[df['ID'] == int(userid)])
    #создание global объекта для изменения в exec
    fig = None
    #получение исполняемого кода из бд
    executive_code = get_code(template_id)
    loc = locals()
    exec(executive_code, globals(), loc)
    #вытаскиваем fig из exec
    fig = loc["fig"]
    #общее форматирование для всех графиков
    #убраны отступы по сторонам   
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=60),)
    #отключен зум и перемещение графиков за пределы значений
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    graphJSON = plotly.io.to_json(fig)
    return graphJSON

@app.route('/bar', methods=['GET', 'POST'])
def change_features():
    feature = request.args['selected']
    userid = request.args['id']
    graphJSON= create_plot(feature, userid)
    return graphJSON


#динамические списки графиков
@app.route('/list', methods=['POST'])
def get_list():
    id = request.form.get("user_id")
    features = list_diagrams(id)
    response = app.response_class(
        response=json.dumps(features),
        status=201,
        mimetype='application/json'
    )
    return response

@app.route('/feedback', methods=['POST'])
def get_feedback():
    plot_id = request.form.get("plot_id")
    mark = request.form.get("mark")
    print(plot_id, mark)
    with open('feedback.csv', 'a', newline='') as csvfile:
        fields = ['Plot_ID','Mark']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writerow({fields[0]:plot_id, fields[1]:mark})
    return "", 200


def add_line_breaks(text):
    return text.replace('\n', '<br>')


@app.route('/load_manager', methods=['GET', 'POST'])
@auth.login_required
def load_manager():
    table = request.args['selected']
    db_app = get_db()
    df = pd.read_sql(f"""SELECT * FROM  {table}""", db_app)
    all_id = df["id"].tolist()
    # links = []
    # for id in all_id:
    #     str = f"""=HYPERLINK("http://45.155.204.231:8000/delete?table={table}&id={id}", "Удалить")"""
    #     links.append(str)
    df['id'] = df['id'].apply(lambda x: f'<a href="http://45.155.204.231:8000/delete?table={table}&id={x}">{x}</a>')
    df = df.style.format({'Text': add_line_breaks})
    
    db_app.close()
    result = (df.to_html(classes='table table-stripped', index=False, render_links=False,
    escape=False))
    
    return result



@app.route('/delete', methods=['GET'])
@auth.login_required
def deleter():
    id = request.args['id']
    table = request.args['table']
    delete_row(table, id)
    return render_template("success.html")

@app.route('/list_service', methods=['POST'])
@auth.login_required
def service_list():
    combinations = {
    "select1" : list_tables("plots"),
    "select2" : list_tables("sources"),
    "select3" : list_tables("groups")
    }   
    response = app.response_class(
        response=json.dumps(combinations),
        status=201,
        mimetype='application/json'
    )
    return response


@app.route('/list_headers', methods=['POST'])
@auth.login_required
def headers_list():
    plot_id = request.form.get("plot_id")
    source_id = request.form.get("source_id")
    headers_code = re.findall(r"\@(.*?)\@", get_code(plot_id))
    headers_code = ["@" + i + "@" for i in headers_code]
    df = load_source(source_id)
    if len(headers_code) != 0:
        headers_code.append("ID")
    

    output = {
    "headers_code" : list(set(headers_code)),
    "headers_source" : list(df.columns.values)
    }   
    response = app.response_class(
        response=json.dumps(output),
        status=201,
        mimetype='application/json'
    )
    return response

@app.route('/manager', methods=['GET', 'POST'])
@auth.login_required
def manager():
    return render_template("manager.html")
    
@app.route('/plotly_editor', methods=['GET'])
@auth.login_required
def new_plot():
    return render_template("plotly_editor.html")

@app.route('/add_graph', methods=['GET'])
@auth.login_required
def new_graph():
    return render_template("build.html")

@app.route('/add_source', methods=['GET'])
@auth.login_required
def choose_type():
    return render_template("source_choose.html")

@app.route('/load_sql', methods=['GET'])
@auth.login_required
def sql_page():
    return render_template("source_sql.html")

@app.route('/add_any', methods=['POST'])
@auth.login_required
def add_any():
    table = request.form['table'] 
    headers = list(request.form.keys())
    headers.remove("table")
    params = []
    for h in headers:
        result = request.form[h]  
        params.append(result)
    headers = ", ".join(["`" + val + "`" for val in headers])
    params = create_string(params)
    add_table(table, headers, params)
    #return "", 200
    return render_template("success.html")


@app.route('/load_csv', methods=['POST', 'GET'])
@auth.login_required
def uploadFile():
    if request.method == 'POST':
      # upload file flask
        f = request.files.get('file')
        name = request.form['fname']  
        # Extracting uploaded file name
        data_filename = secure_filename(f.filename)
 
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],
                            data_filename))
        session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],
        data_filename)
        str_out = create_string([name, "0", ("uploads/" + str(f.filename))])
        add_table("sources", "`name`, `type`, `path`", str_out)
        return render_template("success.html")
    else:
        return render_template("source_csv.html")

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port=8000)
