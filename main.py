
# Flask
from flask import render_template, redirect, url_for, flash, request
# Local config
from app import create_app
import ejemplo

# se crea la aplicación de flask
dechain=[]
app = create_app()

#se le designa el nombre a la ruta
@app.route('/', methods=['GET','POST'])
def blog():
    #se declara una variable con la instacia del formulario
    global dechain
    #variables que se usan en la página
    context = {
        'title':'Blog'
    }
    #si se hace submit se ejecuta el siguiente código
    if request.method == 'POST':
        mensaje=request.form.get('mensaje')
        ejemplo.add(mensaje,dechain)
    #template que se va usar y variables que va a usar
    return render_template('home.html', **context,len=len(dechain),dechain=dechain)


@app.route('/success')
def success():
    #se crean llaves publicas y privadas RSA
    public_key=1
    private_key=2
    #se le pasan las variables creadas a el template
    return render_template('success.html',pukey=public_key,prkey=private_key)
