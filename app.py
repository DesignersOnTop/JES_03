import os
from flask import Flask, render_template, request, redirect, session, send_from_directory, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime
# Importar el enlace a base de datos MySQL

# Crear la aplicación
app = Flask(__name__)

# Crear una llave secreta
app.secret_key = 'JES'

# Configurar la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'jes'

# Inicializar MySQL
mysql = MySQL(app)
#-----------------------------------------------------

@app.route('/')
def Index():
    return render_template('index.html')
    
@app.route('/login', methods=['POST'])
def login():
    matricula = request.form['matricula-sesion']
    password = request.form['pass-sesion']
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Verificación de estudiantes
    cursor.execute("SELECT * FROM estudiantes WHERE matricula = %s", (matricula,))
    estudiante = cursor.fetchone()
    if estudiante and estudiante['contraseña'] == password:
        session['user_id'] = estudiante['id_estudiante']
        session['role'] = 'estudiante'
        return redirect('/home/estudiante/')

    # Verificación de profesores
    cursor.execute("SELECT * FROM profesores WHERE matricula = %s", (matricula,))
    profesor = cursor.fetchone()
    if profesor and profesor['contraseña'] == password:
        session['user_id'] = profesor['id_profesor']
        session['role'] = 'profesor'
        return redirect('/home/profesor/')

    # Verificación de administradores
    cursor.execute("SELECT * FROM admin WHERE matricula = %s", (matricula,))
    admin = cursor.fetchone()
    if admin and admin['contraseña'] == password:
        session['user_id'] = admin['id_admin']
        session['role'] = 'admin'
        return redirect('/home/admin/')
    return redirect('/')
# =========================================================

# APARTADO DEL PROFESORES EN PYTHON Smailyn 
@app.route('/home/profesor/')
def p_home():
    return render_template('./profesor/p-home-a.html')

@app.route('/profesor/perfil/')
def p_perfil():
    return render_template('./profesor/p-perfil.html')

@app.route('/profesor/refuerzo/libros/')
def p_refuerzo_libros():
    return render_template('./profesor/p-refuerzo-libros.html')

@app.route('/profesor/refuerzo/libros/nombre_libro')
def p_libro_refuerzo():
    return render_template('./profesor/p-libro-refuerzo.html')

@app.route('/profesor/refuerzo/videos/')
def p_refuerzo_videos():
    return render_template('./profesor/p-refuerzo-videos.html')

@app.route('/profesor/agregar/libros/')
def agregar_libro():
    return render_template('/profesor/p-agregar-libro.html')

@app.route('/agregar/libro/', methods=['GET','POST'])
def p_agregar_libro():
    _portada = request.files['portada_libro'].filename
    _titulo = request.form['titulo-libro']
    _materia = request.form['materia-libro']
    _subir = request.files['subir-libro'].filename
    
    tiempo = datetime.now()
    horaActual = tiempo.strftime('%Y%H%M%S')
    
    # if _subir.filename!= " ":
    #     nuevoNombre = horaActual+ "_" + _subir.filename
    #     _subir.save('static/img/'+nuevoNombre)
        
    sql = 'INSERT INTO `libros` (`id`,`portada`, `titulo`, `id_asignatura`, `libro`, `id_curso_seccion`) VALUES (NULL, %s, %s, %s, %s, 2)'
    
    datos = (_portada, _titulo, _materia, _subir)
    
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    
    conexion.commit()
    cursor.close()
    
    return redirect('/profesor/refuerzo/libros/')

@app.route('/profesor/agregar/video/')
def p_agregar():
    return render_template('./profesor/p-agregar-video.html')

@app.route('/agregar/video/profesor/', methods=['POST'])
def p_agregar_video():
    _titulo = request.form['titulo-video']
    _materia = request.form['materia-video']
    _insertar = request.form['insertar-video']
    
    sql = 'INSERT INTO `videos` (`id`, `titulo`, `id_seccion_curso`, `id_asignatura`, `video`) VALUES (NULL, %s, %s, %s, 2)'
    
    datos = (_titulo, _materia, _insertar)
    
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    
    conexion.commit()
    cursor.close()
    
    return redirect('/profesor/refuerzo/videos/')
    

@app.route('/profesor/materiales/')
def p_material_estudio():
    return render_template('/profesor/p-material_estudio.html')

@app.route('/profesor/agregar/material/')
def p_agregar_material():
    return render_template('./profesor/p-agregar-material.html')

@app.route('/profesor/agregar/material', methods=['GET', 'POST'])
def agregar_material():
    if request.method == 'GET':
        id_curso = request.args.get('id_curso')
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT nombre FROM cursos WHERE id_curso = %s", (id_curso,))
        curso_nombre = cursor.fetchone()[0]
        id_asignatura = 1  # Obtener el valor de id_asignatura desde la base de datos o de otra fuente
        return render_template('p-agregar-material.html', curso_nombre=curso_nombre, id_asignatura=id_asignatura)

    elif request.method == 'POST':
        try:
            id_curso = request.form.get('id_curso')
            titulo = request.form.get('titulo')
            material_subido = request.files.get('material')
            fondo = request.files.get('fondo')
            descripcion = request.form.get('descripcion')
            id_asignatura = request.form.get('id_asignatura')

            if not id_curso or not titulo or not material_subido or not fondo or not descripcion or not id_asignatura:
                flash('Error: algunos campos están vacíos')
                return render_template('p-agregar-material.html', error_message='Error: algunos campos están vacíos')

            # Validar tipo de archivo subido
            if material_subido.mimetype not in ['application/pdf', 'image/jpeg']:
                flash('Error: tipo de archivo no permitido')
                return render_template('p-agregar-material.html', error_message='Error: tipo de archivo no permitido')

            # Leer los archivos subidos
            material_subido_data = material_subido.read()
            fondo_data = fondo.read()

            sql = 'INSERT INTO material_estudio (id_curso, titulo, material_subido, fondo, descripcion, id_asignatura) VALUES (%s, %s, %s, %s, %s, %s)'

            datos = (id_curso, titulo, material_subido_data, fondo_data, descripcion, id_asignatura)

            conexion = mysql.connection
            cursor = conexion.cursor()
            cursor.execute(sql, datos)

            conexion.commit()
            cursor.close()

            flash('Material agregado con éxito')
            return redirect(url_for('p_lista_material'))

        except mysql.Error as err:
            flash('Error: ' + str(err))
            return render_template('p-agregar-material.html', error_message='Error: ' + str(err))

        except Exception as e:
            flash('Error: ' + str(e))
            return render_template('p-agregar-material.html', error_message='Error: ' + str(e))
    
@app.route('/profesor/lista/material')
def lista_material():
   
    return render_template('p-lista-material.html')

@app.route('/profesor/materiales')
def listar_materiales():
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM material_estudio')
    materiales = cursor.fetchall()
    cursor.close()
    return render_template('p-material_estudio.html', materiales=materiales)
    

@app.route('/profesor/recurso/estudio/')
def p_recurso_estudio():
    return render_template('./profesor/p-recurso_estudio.html')

@app.route('/profesor/material/subido/')
def p_material_de_curso_subido():
    return render_template('./profesor/p-material-de-curso-subido.html')

@app.route('/profesor/clases/enviadas/')
def p_clases_enviadas():
    return render_template('./profesor/p-clases-enviada.html')

@app.route('/profesor/tarea/estudiante/')
def p_tarea_e():
    return render_template('./profesor/p-tarea-e.html')

@app.route('/profesor/reporte/')
def p_report_a():
    return render_template('./profesor/p-report-a.html')

@app.route('/profesor/perfil/estudiante/')
def p_perfil_e():
    return render_template('./profesor/p-perfil-e.html')

@app.route('/agregar/calificacion', methods=['POST'])
def agregar_calificacion():
    id_estudiante = request.form['id_estudiante']
    id_asignatura = request.form['id_asignatura']
    C1 = request.form['C1']
    C2 = request.form['C2']
    C3 = request.form['C3']
    C4 = request.form['C4']
    calificacion_final = request.form['calificacion_final']

    sql = 'INSERT INTO calificaciones (id_estudiante, id_asignatura, C1, C2, C3, C4, `C. Final`) VALUES (%s, %s, %s, %s, %s, %s, %s)'

    datos = (id_estudiante, id_asignatura, C1, C2, C3, C4, calificacion_final)

    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql,datos)

    conexion.commit()
    cursor.close()

    return redirect(url_for('listar_calificaciones'))



if __name__ == '__main__':
    app.run(port = 3000, debug=True)