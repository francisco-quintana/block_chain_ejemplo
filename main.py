
# Flask
from flask import render_template, redirect, url_for, flash, request
# Local config
from app import create_app
from datetime import datetime
import dbconfig
#se importa la función para hash
import hasheo
#se importa la base de datos

###HACER QUE CUANDO SE SUBAN LOS DATOS SE SUBA A 6 COLECCIONES
###BOTON DE CHECAR QUE RECORRE TODAS LAS COLECCIONES PARA VER QUE EVERYTHING IS FINE


# se crea la aplicación de flask
app = create_app()

#se le designa el nombre a la ruta
@app.route('/', methods=['GET','POST'])
def blog():
    #variables que se usan en la página
    context = {
        'title':'Blog'
    }
    #si se hace submit se ejecuta el siguiente código
    leng=dbconfig.db_users.main.count()
    chain=dbconfig.db_users.main.find({})
    if request.method == 'POST':
        col=dict()
        col=['francisco','adrian','melissa','joshua','victor','main']
        n=dbconfig.db_users.main.count()
        if n>0:
            collection = dbconfig.db_users.main
            ahash=""
            cursor = collection.find({'_id':n-1},{'hash':1})
            for x in cursor:
                ahash=x['hash']
            mensaje=request.form.get('mensaje')
            hs_non=hasheo.hashear(mensaje+ahash)
            now = datetime.now()
            tiempo = now.strftime("%H:%M:%S")
            user="francisco"
            for x in col:
                dbconfig.db_users[x].insert_one({
                '_id': n,
                'usuario':user,
                'hora': tiempo,
                'hash': hs_non[0],
                'nonce':hs_non[1],
                'ahash':ahash,
                'mensaje':mensaje
            })
        else:
            mensaje=request.form.get('mensaje')
            hs_non=hasheo.hashear(mensaje)
            now = datetime.now()
            tiempo = now.strftime("%H:%M:%S")
            user="francisco"
            for x in col:
                dbconfig.db_users[x].insert_one({
                '_id': n,
                'usuario':user,
                'hora': tiempo,
                'hash': hs_non[0],
                'nonce':hs_non[1],
                'mensaje':mensaje
            })
    
    #template que se va usar y variables que va a usar
    return render_template('home.html', **context,blockchain=chain)


@app.route('/success')
def success():
    #se crean llaves publicas y privadas RSA
    public_key=1
    private_key=2
    #se le pasan las variables creadas a el template
    return render_template('success.html',pukey=public_key,prkey=private_key)
