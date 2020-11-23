
# Flask
from flask import render_template, redirect, url_for, flash, request
# Local config
from app import create_app
from datetime import datetime
import dbconfig
#se importa la función para hash
import modelo
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
    if request.method == 'POST':
        mensaje=request.form.get('mensaje')
        hs_non=modelo.hashear(mensaje)
        now = datetime.now()
        tiempo = now.strftime("%H:%M:%S")
        #modelo.agregar(tiempo,hs_non[0],hs_non[1],mensaje)
        

    #template que se va usar y variables que va a usar
    return render_template('home.html', **context,len=len(modelo.users),users=modelo.users)


@app.route('/success')
def success():
    #se crean llaves publicas y privadas RSA
    public_key=1
    private_key=2
    #se le pasan las variables creadas a el template
    return render_template('success.html',pukey=public_key,prkey=private_key)
