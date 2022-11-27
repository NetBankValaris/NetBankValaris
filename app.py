from flask import Flask, session, render_template, request, redirect, url_for, flash,send_from_directory
import os
from werkzeug.utils import secure_filename
#from flaskext.mysql import MySQL
import pymysql
from datetime import datetime

UPLOAD_FOLDER = '/static/users'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

NU = ""
UPPY = "true"

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/ac_reg", methods=["POST"])
def ac_reg():
    global NU
    global UPPY
    if request.method=="POST":
        file = request.files["Arch"]
        basepath = os.path.dirname (__file__)
        filename = secure_filename(file.filename)
        extension = os.path.splitext(filename)[1]
        nuevonombre = NU + extension
        upload_path = os.path.join(basepath, 'static/users', nuevonombre)
        file.save(upload_path)

        if "Categ" in request.form:
            cat = request.form["Categ"]
        else:
            cat = 1
        NomProy = request.form["NomProy"]
        intdat = request.form["intdat"]
        Nom = request.form["Nom"]
        descripcion = request.form["descripcion"]
        fecha = datetime.today().strftime('%Y-%m-%d')

        conn = pymysql.connect(host="localhost", user="root", passwd="", db="prot")
        cursor = conn.cursor()
        cursor.execute("insert into registro (NomProy, intdat, Nom, Descripcion, fecha, usuario_ref, categoria_ref, verificado) values( %s, %s, %s, %s, %s, %s, %s, %s)", (NomProy, intdat, Nom, descripcion, fecha, NU, cat, 1))
        conn.commit()

    NU = ""
    UPPY = "true"
    return redirect(url_for("index"))
#this
@app.route('/validados', methods=["GET"])
def validados():
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="prot")
    cursor = conn.cursor()
    cursor.execute('select NomProy, descripcion from registro where verificado = 1')
    datos = cursor.fetchall()
    return render_template("index.html", req=datos)
#this
@app.route("/registro")
def registro():
    global UPPY
    global NU
    NU = ""
    UPPY = "true"
    return render_template("registro.html", UP = UPPY)
#this
@app.route("/verifi", methods = ["POST"])
def Verifi():
    global NU
    global UPPY
    UPPY = "true"
    if request.method == "POST":
        Usuario = request.form["Usu"]
        Contra = request.form["Cont"]

        #conn = pymysql.connect(host="localhost", user="root", passwd="", db="prot")
        conn = pymysql.connect(host="localhost", user="root", passwd="", db="prot")
        cursor = conn.cursor()
        cursor.execute("select a.usuario, a.contraseña, b.usuario_ref from validados a left join registro b on a.usuario = b.usuario_ref")
        datos = cursor.fetchall()
        for i in datos:
            if (Usuario == i[0] and Contra == i[1] and i[2] == None):
                UPPY = "false"
                NU = i[0]
        conn = pymysql.connect(host="localhost", user="root", passwd="", db="prot")
        cursor = conn.cursor()
        cursor.execute("select * from categoria")
        datcat = cursor.fetchall()

        return render_template("registro.html" , UP = UPPY, cate = datcat)
#this
@app.route("/proyectos")
def proyectos():
    global prim
    prim = True
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="prot")
    cursor = conn.cursor()
    cursor.execute("select * from registro where verificado = 1")
    proys = cursor.fetchall()
    cursor.execute("select * from categoria")
    cat = cursor.fetchall()
    return render_template("proyectos.html", dats = proys, catTip = cat, Bool = prim,num = 0)

@app.route("/proyectos_fil/<string:id>")
def proyectos_fil(id):
    global prim
    prim = False
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="prot")
    cursor = conn.cursor()
    cursor.execute("select * from registro where verificado = 1 and categoria_ref = %s", (id))
    proys = cursor.fetchall()
    cursor.execute("select * from categoria")
    cat = cursor.fetchall()
    print(type(id))
    return render_template("proyectos.html", dats = proys, catTip = cat, num = int(id), Bool = prim)

if __name__ == "__main__":

 app.run(debug=True)