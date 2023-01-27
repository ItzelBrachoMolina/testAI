from app import db


class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250))
    apellido = db.Column(db.String(250))
    edad = db.Column(db.String(250))
    afinidadMagica = db.Column(db.String(250))


    def __str__(self):
        return (
            f'Id: {self.id}, '
            f'Nombre: {self.nombre}, '
            f'Apellido: {self.apellido}, '
            f'Edad: {self.edad},'
            f'Afinidad Mágica: {self.afinidadMagica},'

        )
