from flask import Flask, session, render_template, request, redirect, url_for
#from flaskext.mysql import MySQL
import pymysql
from datetime import datetime


app = Flask(__name__)

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
        NomProy = request.form["NomProy"]
        intdat = request.form["intdat"]
        Nom = request.form["Nom"]
        descripcion = request.form["descripcion"]
        img = request.form["Arch"]
        fecha = datetime.today().strftime('%Y-%m-%d')

        conn = pymysql.connect(host="NetBankValaris.mysql.pythonanywhere-services.com", user="NetBankValaris", passwd="Valaris102323", db="NetBankValaris$default")
        cursor = conn.cursor()
        cursor.execute("insert into registro (NomProy, intdat, Nom, Descripcion, Arch, fecha, usuario_ref) values(%s, %s, %s, %s, %s, %s, %s)", (NomProy, intdat, Nom, descripcion, img, fecha, NU))
        conn.commit()
    NU = ""
    UPPY = "true"
    return redirect(url_for("index"))
    
@app.route('/validados', methods=["GET"])
def validados():
    conn = pymysql.connect(host="NetBankValaris.mysql.pythonanywhere-services.com", user="NetBankValaris", passwd="Valaris102323", db="NetBankValaris$default")
    cursor = conn.cursor()
    cursor.execute('select NomProy, descripcion from registro where verificado = 1')
    datos = cursor.fetchall()
    print(datos)
    return render_template("index.html", req=datos)

@app.route("/registro")
def registro():
    global UPPY
    return render_template("registro.html", UP = UPPY)

@app.route("/verifi", methods = ["POST"])
def Verifi():
    global NU
    global UPPY
    UPPY = "true"
    if request.method == "POST":
        Usuario = request.form["Usu"]
        Contra = request.form["Cont"]

        #conn = pymysql.connect(host="localhost", user="root", passwd="", db="prot")
        conn = pymysql.connect(host="NetBankValaris.mysql.pythonanywhere-services.com", user="NetBankValaris", passwd="Valaris102323", db="NetBankValaris$default")
        cursor = conn.cursor()
        cursor.execute("select a.usuario, a.contraseña, b.usuario_ref from validados a left join registro b on a.usuario = b.usuario_ref")
        datos = cursor.fetchall()
        print(datos)
        for i in datos:
            if (Usuario == i[0] and Contra == i[1] and i[2] == None):
                print("Hola")
                UPPY = "false"
                NU = i[0]

        return render_template("registro.html" , UP = UPPY)

@app.route("/proyectos")
def proyectos():
    conn = pymysql.connect(host="NetBankValaris.mysql.pythonanywhere-services.com", user="NetBankValaris", passwd="Valaris102323", db="NetBankValaris$default")
    cursor = conn.cursor()
    cursor.execute("select * from registro where verificado = 1")
    proys = cursor.fetchall()
    print(proys)
    return render_template("proyectos.html", dats = proys)

if __name__ == "__main__":

 app.run(debug=True)