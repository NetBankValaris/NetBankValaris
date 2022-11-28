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
PsA = False
Ra = ""

@app.route('/')
def index():
    global PsA
    return render_template("index.html", Pass = PsA)

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
        cursor.execute("insert into registro (NomProy, intdat, Nom, Descripcion, fecha, usuario_ref, categoria_ref, verificado, extarch) values( %s, %s, %s, %s, %s, %s, %s, %s, %s)", (NomProy, intdat, Nom, descripcion, fecha, NU, cat, 0, extension))
        conn.commit()

    NU = ""
    UPPY = "true"
    return redirect(url_for("index"))
#this
@app.route("/registro")
def registro():
    global UPPY
    global NU
    global PsA
    NU = ""
    UPPY = "true"
    return render_template("registro.html", UP = UPPY, Pass = PsA)
#this
@app.route("/verifi", methods = ["POST"])
def Verifi():
    global NU
    global UPPY
    global PsA
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

        return render_template("registro.html" , UP = UPPY, cate = datcat, Pass = PsA)
#this
@app.route("/proyectos")
def proyectos():
    global prim
    global PsA
    prim = True
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="prot")
    cursor = conn.cursor()
    cursor.execute("select * from registro where verificado = 1")
    proys = cursor.fetchall()
    cursor.execute("select * from categoria")
    cat = cursor.fetchall()
    return render_template("proyectos.html", dats = proys, catTip = cat, Bool = prim, num = 0, Pass = PsA)

@app.route("/proyectos_fil/<string:id>")
def proyectos_fil(id):
    global prim
    global PsA
    prim = False
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="prot")
    cursor = conn.cursor()
    cursor.execute("select * from registro where verificado = 1 and categoria_ref = %s", (id))
    proys = cursor.fetchall()
    cursor.execute("select * from categoria")
    cat = cursor.fetchall()
    print(proys)
    return render_template("proyectos.html", dats = proys, catTip = cat, num = int(id), Bool = prim, Pass = PsA)

@app.route("/admin")
def admin():
    global PsA
    print(PsA)
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="prot")
    cursor = conn.cursor()
    cursor.execute("select idReg, nomproy, intdat, nom, descripcion, fecha, usuario_ref from registro where verificado = 0")
    datos = cursor.fetchall()
    cursor.execute("select usuario, contraseña from validados")
    datos2 = cursor.fetchall()
    return render_template("admin.html", pue=datos, pue2=datos2, Pass = PsA)

@app.route('/admin_autorizar/<string:id>')
def admin_autorizar(id):
    global PsA
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='prot')
    cursor = conn.cursor()
    cursor.execute('update registro set verificado=1 where idReg=%s',(id))
    conn.commit()
    return redirect(url_for('admin'))

@app.route('/admin_borrar/<string:id>')
def admin_borrar(id):
    global PsA
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='prot') 
    cursor = conn.cursor()
    cursor.execute('delete from registro where idReg = %s',(id))
    conn.commit()
    return redirect(url_for('admin'))

@app.route('/usuarios')
def usuarios():
    global PsA
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='prot') 
    cursor = conn.cursor()
    cursor.execute('select usuario, contraseña from validados')
    conn.commit()
    return render_template("usuarios.html", Pass = PsA)

@app.route('/usuarios_ingresar', methods=['POST'])
def usuarios_ingresar():
    global PsA
    if request.method == 'POST':
        user = request.form['usuario']
        sec = request.form['contraseña']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='prot')
        cursor = conn.cursor()
        cursor.execute('insert into validados (usuario, contraseña) values (%s, %s)',(user, sec))
        conn.commit()
    return redirect(url_for('admin'))


@app.route('/usuarios_tabla_borrar/<string:id>')
def usuarios_tabla_borrar(id):
    global PsA
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='prot') 
    cursor = conn.cursor()
    cursor.execute('delete from validados where usuario = %s',(id))
    conn.commit()
    return redirect(url_for('admin'))

@app.route('/registro_detalle/<string:id>')
def registro_detalle(id):
    global PsA
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='prot' )
    cursor = conn.cursor()
    cursor.execute('select idreg, nomproy, intdat, nom, descripcion, fecha, usuario_ref, verificado, categoria_ref from registro where idreg=%s',(id))
    datos = cursor.fetchall()
    return render_template("registro_detalle.html", pue=datos, dat=datos[0], Pass = PsA)

@app.route('/registro_fdetalle/<string:id>', methods=['GET'])
def registro_fdetalle(id):
    global PsA
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='prot')
    cursor = conn.cursor()
    cursor.execute('select idreg, nomproy, intdat, nom, descripcion, fecha, usuario_ref, verificado, categoria_ref from registro where idreg=%s',(id))
    datos = cursor.fetchall()
    return render_template("registro_detalle.html", pue = datos, dat=datos[0], Pass = PsA)

@app.route("/admin_security")
def admin_security():
    global PsA
    global Ra
    PsA = False
    Ra = ""
    return render_template("admin_security.html", Pro = Ra, Pass = PsA)

@app.route("/admin_verifi", methods=["POST"])
def admin_verifi():
    if request.method == "POST":
        global PsA
        global Ra
        mail = request.form["Correo"]
        contra = request.form["Cont"]

        if mail == "netbankvalaris@gmail.com" and contra == "Salchipulpos&Koka2005":
            PsA = True    
            return redirect(url_for("admin"))
        else:
            PsA = False
            Ra = "Inc"
            return redirect(url_for('admin_security'))

if __name__ == "__main__":

 app.run(debug=True)