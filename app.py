from select import select
from flask import Flask, session, render_template, request, redirect, url_for
#from flaskext.mysql import MySQL
import pymysql
from datetime import datetime


app = Flask(__name__)


UPPY = "true"

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/ac_reg", methods=["POST"])
def ac_reg():
    if request.method=="POST":
        NomProy = request.form["NomProy"]
        intdat = request.form["intdat"]
        Nom = request.form["Nom"]
        descripcion = request.form["descripcion"]
        img = request.form["Arch"]
        fecha = datetime.today().strftime('%Y-%m-%d')

        conn = pymysql.connect(host="localhost", user="root", passwd="", db="proyectos")
        cursor = conn.cursor()
        cursor.execute("insert into registro (NomProy, intdat, Nom, Descripcion, Arch, fecha) values(%s, %s, %s, %s, %s, %s)", (NomProy, intdat, Nom, descripcion, img, fecha))
        conn.commit()
    return redirect(url_for("index"))
    
@app.route('/validados', methods=["GET"])
def validados():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='proyectos' )
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
    global UPPY
    if request.method == "POST":
        Usuario = request.form["Usu"]
        Contra = request.form["Cont"]

        conn = pymysql.connect(host="localhost", user="root", passwd="", db="prot")
        cursor = conn.cursor()
        cursor.execute("select * from validados")
        datos = cursor.fetchall()
        for i in datos:
            if Usuario == i[0] and Contra == i[1]:
                UPPY = "false"

        return render_template("registro.html" , UP = UPPY)

if __name__ == "__main__":

 app.run(debug=True)