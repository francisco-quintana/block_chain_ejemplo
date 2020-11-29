
# Flask
from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from werkzeug.security import generate_password_hash, check_password_hash
# Local config
from app import create_app
from datetime import datetime
from dbconfig
#se importa la función para hash
import hasheo
#se importa la base de datos

# se crea la aplicación de flask
app = create_app()

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Adrian', password='123'))
users.append(User(id=2, username='Francisco', password='123'))
users.append(User(id=3, username='Victor', password='123'))
users.append(User(id=4, username='Melissa', password='123'))
users.append(User(id=5, username='Komaba', password='123'))
users.append(User(id=6, username='Main', password='1234'))


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        for x in users:
            if x.username == username:
                user = [x for x in users if x.username == username][0]
                if user and user.password == password:
                    session['user_id'] = user.id            
                    return redirect('home')
                else:
                    return redirect(url_for('login'))
        return redirect(url_for('login'))
    return render_template('login.html')

#se le designa el nombre a la ruta
@app.route('/home', methods=['GET','POST'])
def blog():
    #variables que se usan en la página
    context = {
        'title':'Blog'
    }
    #si se hace submit se ejecuta el siguiente código
    
    leng=dbconfig.db_users.Main.count()
    chain=dbconfig.db_users.Main.find({})
    if request.method == 'POST':
        col=[]
        counter=0
        for x in users:
            col.append(str(x.username))
        # col=['francisco','adrian','melissa','joshua','victor','main']
        n=dbconfig.db_users.Main.count()
        if n>0:
            collection = dbconfig.db_users.Main
            ahash=""
            cursor = collection.find({'_id':n-1},{'hash':1})
            for x in cursor:
                ahash=x['hash']
            mensaje=request.form.get('mensaje')
            hs_non=hasheo.hashear(mensaje+ahash)
            now = datetime.now()
            tiempo = now.strftime("%H:%M:%S")
            user=g.user.username
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
            user=g.user.username
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

@app.route('/', defaults={'login': ''})
@app.route('/<path:login>')
def catch_all(login):
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()