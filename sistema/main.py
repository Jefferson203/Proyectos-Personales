from flask import Flask, render_template, request, flash, redirect, url_for, session
import psycopg2, random,smtplib, urllib.request
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

# Configuración de la base de datos
DB_HOST = "localhost"
DB_NAME = "proyecto_X"
DB_USER = "postgres"
DB_PASS = "76729987"

# Establecer la conexión a la base de datos
def get_db_connection():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    return conn

# Configuración de sesiones
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.secret_key = 'myclave-secreta'

# Ruta raíz que redirige a /login
@app.route('/', methods=["GET"])
def log():
    return redirect(url_for('login'))

conn = get_db_connection()


@app.route('/login/', methods=['GET', 'POST'])
def login():

    cursor = conn.cursor()
    # Compruebe si existen solicitudes POST de "nombre de usuario" y "contraseña" (formulario enviado por el usuario)
    #if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    if request.method == 'POST' and 'username' and 'password' :
        username = request.form['username']
 
        password = request.form['password']
        print(f"Este es el usuario: {username} y esta es la contraseña: {password}")

        # Check if account exists using MySQL
        #cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        cursor.execute('''
                           SELECT c.id_cuenta, u.id_dni,c.des_contraseña, 
                            cu.ind_estado as Estado, c.est_default FROM ctaUsuario cu, 
                            cuenta c, usuario u where c.id_cuenta=cu.id_cuenta 
                            and u.id_dni=cu.id_dni and cu.ind_estado=%s and u.usuario = %s
                           ''', ('activo',username,))
            # Fetch one record and return result
        account = cursor.fetchone()
        print(account)
        if account:
            password_rs = account[2]
            estadoUsu = account[4]

            print("estado cuenta : "+str(estadoUsu))
            
           
            # Si la cuenta existe en la tabla de usuarios en la base de datos
             #check_password_hash(password_rs, password):
            # _hashed_password = generate_password_hash(password)
            if (password_rs == password):
                codigoV=random.randint(500, 1000)
                # codigoV=10
                # Crear datos de sesión, podemos acceder a estos datos en otras rutas
                session['loggedin'] = True
                session['id'] = account[0]
                session['des_password']=password_rs
                session['codigoValidacion']=codigoV
                # session['username'] = account['username']
                # Redirect to home page
                if (str(estadoUsu) in '0'):                    
                    url = 'https://www.google.com' # URL para verificar si hay conexión a internet

                    try:
                        urllib.request.urlopen(url)
                        print('Conexión a Internet activa')
                        username = "sanjuanbautista2030@gmail.com"
                        password = "twfpbjoxniiqhkrc"
                        mail_from = "sanjuanbautista2030@gmail.com"
                        mail_to = account['id_cuenta']
                        mail_subject = "Código de validación"
                        mail_body = ("Este es el código de validación "+str(codigoV))

                        mimemsg = MIMEMultipart()
                        mimemsg['From']=mail_from
                        mimemsg['To']=mail_to
                        mimemsg['Subject']=mail_subject
                        mimemsg.attach(MIMEText(mail_body, 'plain'))
                        connection = smtplib.SMTP(host='smtp.gmail.com', port=587)
                        connection.starttls()
                        connection.login(username,password)
                        connection.send_message(mimemsg)
                        connection.quit()
                        return render_template('welcome.html', account=account, codigoV=codigoV,usuario=session['id'])
                    except:
                          print('No hay conexión a Internet')
                          return render_template('error.html')
                               

                else:
                    
                    return redirect(url_for('menu'))

            else:
                flash('Usuario o contraseña incorrectos.', 'error')
        else:
            flash('Usuario o contraseña incorrectos.', 'error')
    # else:
    #     flash('Incorrect username/password')
 
    return render_template('login.html')




@app.route('/menu')
def menu():
    if 'loggedin' in session:
        cursor = conn.cursor()
        
        
        try:
            
            cursor.execute('''
                SELECT t.id_dni, c.id_cuenta, o.des_opcion, o.id_opcion, o.icon_name 
                FROM usuario t, ctaUsuario ctaT, cuenta c, rolUsuario rolT, rol r, opcion o 
                WHERE t.id_dni = ctaT.id_dni 
                AND ctaT.id_cuenta = c.id_cuenta 
                AND rolT.id_usuario = t.id_dni 
                AND r.id_rol = rolT.id_rol 
                AND o.id_rol = r.id_rol 
                AND c.id_cuenta = %s 
                AND o.ind_estado = %s 
            ''', (session['id'], 'Disponible'))
            
            account2 = cursor.fetchall()
            
            cursor.execute('''
                SELECT t.id_dni AS DNI, des_nombres, c.id_cuenta, c.des_contraseña, c.est_default, r.des_rol 
                FROM usuario t, ctaUsuario ctaT, cuenta c, rolUsuario rolT, rol r 
                WHERE t.id_dni = ctaT.id_dni 
                AND ctaT.id_cuenta = c.id_cuenta 
                AND rolT.id_usuario = t.id_dni 
                AND r.id_rol = rolT.id_rol 
                AND c.id_cuenta = %s
            ''', [session['id']])
            
            account = cursor.fetchone()
            
            conn.commit()
            return render_template('dashboard.html', account=account, account2=account2)
        
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            flash('Error al cargar la información. Por favor, inténtelo de nuevo más tarde.', 'error')
            return redirect(url_for('menu'))  # Redirigir a otra página en caso de error

    else:
        return render_template('sessionesreset.html')

        

@app.route('/perfil')
def perfil(): 
    
    cursor = conn.cursor()
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor.execute('select t.id_dni,des_nombres, telefono, c.id_cuenta,c.des_contraseña,c.est_default,r.des_rol,t.ind_estado,t.nacionalidad from usuario t, ctaUsuario ctaT, cuenta c, rolUsuario rolT, rol r where t.id_dni=ctaT.id_dni and ctaT.id_cuenta=c.id_cuenta and rolT.id_usuario=t.id_dni and r.id_rol=rolT.id_rol and c.id_cuenta = %s', [session['id']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('perfil.html', account=account)
    
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/content/inicio')
def content_inicio():
    return render_template('partials/inicio.html')

@app.route('/content/registrodeusuarios')
def content_registrodeusuarios():
    return render_template('partials/registrodeusuarios.html')

@app.route('/content/gestiondeusuarios')
def content_gestiondeusuarios():
    return render_template('partials/gestióndeusuarios.html')

@app.route('/content/checklist')
def content_checklist():
    return render_template('partials/checklist.html')

@app.route('/content/matrizdeescalamiento')
def content_matrizdeescalamiento():
    return render_template('partials/matrizdeescalamiento.html')

@app.route('/content/horarios')
def content_horarios():
    return render_template('partials/horarios.html')


# Ruta para cerrar sesión
@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('codigoValidacion', None)
   session.pop('login_attempts',None)
   return redirect(url_for('login'))
  


if __name__ == "__main__":
    app.run(debug=True, port=2009)
