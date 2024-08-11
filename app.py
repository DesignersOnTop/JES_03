import os
from flask import Flask, render_template, request, redirect, session, send_from_directory, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime
from werkzeug.utils import secure_filename # Manejar los archivos de manera segura 

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

@app.route('/profesor/agregar/libros/')
def p_agregar_libro():
    return render_template('/profesor/p-agregar-libro.html')

@app.route('/agregar/libro/profesor/', methods=['POST'])
def agregar_libro_pro():
    _titulo = request.form['titulo-libro']
    _materia = request.form['materia-libro']
    _portada = request.files['portada_libro']
    _subir_libro = request.files['subir-libro']

    # Configuración de las carpetas de portadas y materiales
    carpeta_portadas = 'static/portadas'
    carpeta_materiales = 'static/materiales'

    # Asegurarse de que las carpetas existan
    if not os.path.exists(carpeta_portadas):
        os.makedirs(carpeta_portadas)

    if not os.path.exists(carpeta_materiales):
        os.makedirs(carpeta_materiales)

    # Guardar los archivos
    portada_filename = secure_filename(_portada.filename)
    material_filename = secure_filename(_subir_libro.filename)

    portada_path = os.path.join(carpeta_portadas, portada_filename)
    material_path = os.path.join(carpeta_materiales, material_filename)

    _portada.save(portada_path)
    _subir_libro.save(material_path)

    # Consulta SQL para insertar el libro en la base de datos
    sql = 'INSERT INTO `libros` (`titulo`, `id_asignatura`, `id_curso`, `subir_libro`, `portada`) VALUES (%s, %s, 1, %s, %s)'
    
    datos = (_titulo, _materia, material_path, portada_path)
    
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    
    conexion.commit()
    cursor.close()
    
    return redirect(url_for('p-libro-refuerzo'))



@app.route('/eliminar/libro/<int:id>', methods=['POST'])
def eliminar_libro(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM libros WHERE id_libro = %s', (id,))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('p-refuerzo-libros'))

@app.route('/profesor/refuerzo/libros', methods=['GET'])
def listar_libros():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM libros')
    libros = cursor.fetchall()
    cursor.close()

    return render_template('refuerzo_libros.html', libros=libros)



# @app.route('/agregar/libro/', methods=['GET','POST'])
# def ():
#     _portada = request.files['portada_libro'].filename
#     _titulo = request.form['titulo-libro']
#     _materia = request.form['materia-libro']
#     _subir = request.files['subir-libro'].filename
    
#     tiempo = datetime.now()
#     horaActual = tiempo.strftime('%Y%H%M%S')
    
    # if _subir.filename!= " ":
    #     nuevoNombre = horaActual+ "_" + _subir.filename
    #     _subir.save('static/img/'+nuevoNombre)
        
    # sql = 'INSERT INTO `libros` (`id`,`portada`, `titulo`, `id_asignatura`, `libro`, `id_curso_seccion`) VALUES (NULL, %s, %s, %s, %s, 2)'
    
    # datos = (_portada, _titulo, _materia, _subir)
    
    # conexion = mysql.connection
    # cursor = conexion.cursor()
    # cursor.execute(sql,datos)
    
    # conexion.commit()
    # cursor.close()
    
    # return redirect('/profesor/refuerzo/libros/')

@app.route('/profesor/refuerzo/videos/')
def p_refuerzo_videos():
    return render_template('./profesor/p-refuerzo-videos.html')



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

@app.route('/profesor/agregar/material/', methods=['GET', 'POST'])
def agregar_material():
    # Obtener los datos del formulario
    fondo_material = request.files['fondo_material']
    nombre_material = request.form['nombre_material']
    recurso_de_estudio = request.files['recurso_de_estudio']
    descripcion_material = request.form['descripcion_material']
    
    # Obtener los IDs de curso y asignatura
    id_curso = request.form.get('id_curso', type=int)
    id_asignatura = request.form.get('id_asignatura', type=int)
    
    # Debug: Imprimir los valores recibidos
    print(f"ID Curso: {id_curso}, ID Asignatura: {id_asignatura}")
    print(f"Nombre Material: {nombre_material}, Descripción: {descripcion_material}")
    print(f"Archivos recibidos: {fondo_material.filename}, {recurso_de_estudio.filename}")

    if not id_curso or not id_asignatura:
        flash('Curso o asignatura no proporcionados.', 'error')
        print("Error: Curso o asignatura no proporcionados.")
        return redirect(url_for('p_material_estudio'))

    # Verificar que el curso y la asignatura existen
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM cursos WHERE id_curso = %s', (id_curso,))
    curso = cursor.fetchone()
    cursor.execute('SELECT * FROM asignaturas WHERE id_asignatura = %s', (id_asignatura,))
    asignatura = cursor.fetchone()
    cursor.close()

    # Debug: Verificar la existencia de curso y asignatura
    print(f"Curso encontrado: {curso}")
    print(f"Asignatura encontrada: {asignatura}")

    if not curso or not asignatura:
        flash('Curso o asignatura no válido.', 'error')
        print("Error: Curso o asignatura no válido.")
        return redirect(url_for('p_material_estudio'))

    # Ruta donde se almacenarán los archivos subidos
    if not os.path.exists('static'):
        os.makedirs('static')
        print("Directorio 'static' creado.")

    fondo_filename = secure_filename(fondo_material.filename)
    recurso_filename = secure_filename(recurso_de_estudio.filename)
    fondo_material_path = os.path.join('static', fondo_filename)
    recurso_de_estudio_path = os.path.join('static', recurso_filename)

    # Debug: Imprimir las rutas de los archivos guardados
    print(f"Guardando fondo en: {fondo_material_path}")
    print(f"Guardando recurso en: {recurso_de_estudio_path}")

    try:
        # Guardar los archivos en el servidor
        fondo_material.save(fondo_material_path)
        recurso_de_estudio.save(recurso_de_estudio_path)
        print("Archivos guardados exitosamente.")

        # Preparar la consulta SQL para insertar el nuevo material
        sql = """INSERT INTO material_estudio (id_curso, id_asignatura, titulo, fondo, material_subido, descripcion) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        
        datos = (id_curso, id_asignatura, nombre_material, fondo_filename, recurso_filename, descripcion_material)

        # Debug: Imprimir la consulta y los datos
        print(f"Ejecutando SQL: {sql}")
        print(f"Datos a insertar: {datos}")
       
        conexion = mysql.connection
        cursor = conexion.cursor()
        cursor.execute(sql, datos)
        
        conexion.commit()
        flash('Material agregado exitosamente.', 'success')
        print("Material agregado a la base de datos exitosamente.")
    except Exception as e:
        print(f"Error al insertar en la base de datos: {e}")
        flash('Ocurrió un error al intentar guardar el material.', 'error')
    finally:
        cursor.close()

    # Redirigir a la página de materiales de estudio
    return redirect('/profesor/p-materiales_estudio.html')


# Ruta para mostrar el formulario de agregar material
@app.route('/profesor/agregar/material/<int:id_curso>/<int:id_asignatura>')
def formulario_agregar_material(id_curso, id_asignatura):
    return render_template('agregar_material.html', id_curso=id_curso, id_asignatura=id_asignatura)

@app.route('/profesor/eliminar/material/', methods= ['POST'])
def eliminar_material():
    id_material = request.form["id_material"]

    if id_material in 'material_estudio':
        sql = 'DELETE FROM material_estudio WHERE id_material = %s', (id_material)
        return redirect('/profesor/p-material_estudio.html')
    
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql)
    
    conexion.commit()
    cursor.close()
  
# @app.route('/profesor/lista/material')
# def lista_material():
   
#     return render_template('./profesores/p-lista-material.html')

@app.route('/profesor/materiales')
def material_estudios():
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM material_estudio')
    materiales = cursor.fetchall()
    cursor.close()
    return render_template('./profesores/p-material_estudio.html', materiales=materiales)
    

@app.route('/profesor/recurso/estudio/')
def p_recurso_estudio():
    return render_template('./profesor/p-recurso_estudio.html')

@app.route('/profesor/recurso/estudio/<int:id>')
def recurso_estudio(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM material_estudio WHERE id_material = %s', (id,))
    material = cursor.fetchone()
    cursor.close()
    
    if material:
        return render_template('./profesores/p-recurso_estudio.html', material=material)
    else:
        return "Material no encontrado", 404

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

    return redirect(url_for('./profesor/p-material_estudio.html'))



if __name__ == '__main__':
    app.run(port = 3000, debug=True)