from flask import Flask, render_template, request, url_for
from flask_migrate import Migrate
from werkzeug.utils import redirect

from database import db
from forms import PersonaForm
#from models import Persona

app = Flask(__name__)

#Configuración de la bd
USER_DB = 'postgres'
PASS_DB = 'admin'
URL_DB = 'localhost'
NAME_DB = 'sap_flask_db'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'


app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)



migrate = Migrate()
migrate.init_app(app, db)

app.config['SECRET_KEY']='llave_secreta'


class Persona(db.Model):
    identificacion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20))
    apellido = db.Column(db.String(20))
    edad = db.Column(db.Integer)
    afinidadMagica = db.Column(db.Integer)



    def __str__(self):
        return (
            f'Id: {self.id}, '
            f'Nombre: {self.nombre}, '
            f'Apellido: {self.apellido}, '
            f'Edad: {self.edad},'
            f'Afinidad Mágica: {self.afinidadMagica},'

        )


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def inicio():

    personas = Persona.query.order_by('id')
    total_personas = Persona.query.count()
    app.logger.debug(f'Listado Personas: {personas}')
    app.logger.debug(f'Total Personas: {total_personas}')
    return render_template('index.html', personas = personas, total_personas = total_personas)

@app.route('/ver/<int:id>')
def ver_detalle(id):

    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Ver persona: {persona}')
    return render_template('detalle.html', persona = persona)

@app.route('/agregar', methods=['GET','POST'])
def agregar():
    persona = Persona()
    personaForm = PersonaForm(obj=persona)
    if request.method == 'POST':
        if personaForm.validate_on_submit():
           personaForm.populate_obj(persona)
           app.logger.debug(f'Persona a insertar: {persona}')
           #Insertamos el nuevo registro
           db.session.add(persona)
           db.session.commit()
           return redirect(url_for('inicio'))
    return render_template('agregar.html', forma = personaForm)

@app.route('/editar/<int:id>', methods=['GET','POST'])
def editar(id):
    persona = Persona.query.get_or_404(id)
    personaForma = PersonaForm(obj=persona)
    if request.method == 'POST':
        if personaForma.validate_on_submit():
            personaForma.populate_obj(persona)
            app.logger.debug(f'Persona a actualizar: {persona}')
            db.session.commit()
            return redirect(url_for('inicio'))
    return render_template('editar.html', forma = personaForma)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Persona a eliminar: {persona}')
    db.session.delete(persona)
    db.session.commit()
    return redirect(url_for('inicio'))