from flask import Flask, session, render_template, request, redirect, url_for
#from flaskext.mysql import MySQL
import pymysql
from datetime import datetime


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/ac_reg", methods=["POST"])
def ac_reg():
    if request.method=="POST":
        Nom = request.form["Nom"]
        NomProy = request.form["NomProy"]
        Desc = request.form["Desc"]
        img = request.form["Arch"]
        fecha = datetime.today().strftime('%Y-%m-%d')
        print(img)
        print(Desc)
        print(fecha)

        conn = pymysql.connect(host="localhost", user="root", passwd="", db="prot")
        cursor = conn.cursor()
        cursor.execute("insert into registro (nombre, NomProy, Descripcion, img, fecha) values(%s, %s, %s, %s, %s)", (Nom, NomProy, Desc, img, fecha))
        conn.commit()
    return redirect(url_for("index"))

"""
@app.route("/muestra")
def muestra():
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="prot")
    cursor = conn.cursor()
    cursor.execute("select img from registro where idReg = 1")
    Dat = cursor.fetchall()
    return render_template("muestra.html", D = Dat[0])
"""
if __name__ == "__main__":

 app.run(debug=True)