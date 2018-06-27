from wtforms import Form, DateField
#from flask_wtf import FlaskForm 
from wtforms import StringField, TextField, IntegerField, FloatField
from wtforms.fields.html5 import EmailField
from wtforms.fields.html5 import TelField
from wtforms import PasswordField
from wtforms import validators


class LogForm(Form):
	username = StringField('username', 
		[
			validators.length(min =4, max=25, message='Ingrese una cadena mas grande'),
			validators.Required(message='El nombre de usuario es requerido')
		])
	password  = PasswordField('password',
		[
			validators.length(min =8, max=30, message='Ingrese una cadena entre 8 y 30 caracteres '),
			validators.Required(message='El password es requerido')
		]
		)

class CustomerForm(Form):
	nombre = StringField('nombre',[
			validators.length(min = 4, max = 50, message= 'Ingresa un nombre mas grande'),
			validators.Required(message = 'El nombre del cliente es requerido')
		])
	rfc = StringField('rfc',[
			validators.length(min = 12, max = 13, message='El tamanio del RFC no es valido'),
			validators.Required(message = 'El RFC no es valido')
		])
	tel = TelField('tel')
	email = EmailField('email', [
			validators.length(min = 3, max = 50, message='Ingresa un correo entre 3 y 50'),
			validators.Required(message= 'El correo es obligatorio')
		])
	colonia = IntegerField('colonia')
	calle   = StringField('calle', [validators.length(min = 3, max = 50, message = "El nombre de tu calle debe tener minimo 3 caracteres y maximo 50"),
		validators.Required(message="Es obligatorio el nombre de tu calle")])
	num = StringField('num', [validators.length(max = 10, message = "No puedes pasar 10 caracteres")])
	numEx = StringField('numEx',[validators.length(max = 10, message = "No puedes parar 10 caracteres"), validators.Required(message="El campo numero exterior es obligatorio")])



class UnitMeasurement(Form):

	name = StringField('name',[
			validators.length(min = 1, max = 15, message = 'Ingrese un nombre entre 1 y 15 letras'),
			validators.Required(message = 'El nombre es necesario')
		])

	abbreviaton = StringField('abbreviaton', [
			validators.length(min = 1, max = 4, message = 'Ingresa una palabra entre 1 y 4'),
			validators.Required(message = 'La abreviacion es requerida')
		])
	descripcion = StringField('descripcion',[
		validators.length(min = 1, max = 20, message = 'Ingresa una descripcion corta'),
		validators.Required(message = 'Ingrese una descripcion')
	])


class ProductForm(Form):
	id = IntegerField('Codigo', [validators.NumberRange(min = 0), validators.Required(message="El Codigo es requerido")])
	name = StringField('Name',[
		validators.length(min = 3, max = 50, message = 'Ingresa un nombre de producto entre 3 y 50'),
		validators.Required(message='El nombre es requerido')  
		])
	quantity = IntegerField('Cantidad', [validators.NumberRange(min = 0,  max = 1000000000)])
	purchasePrice = FloatField('Precio de compra' ,[validators.NumberRange(min = 0, max = 100000000)]) 
	unitm = IntegerField('unitm', [validators.NumberRange(min = 0, max = 20), validators.Required(message="El codigo de unidad es necesario")])

class ColoniaForm(Form):
	id = IntegerField('id', [validators.NumberRange(min = 0), validators.Required(message="El codigo es requerido")])
	nombre = StringField('nombre', [validators.length(min = 3, max = 35, message = 'Ingresa un nombre de colonia entre 3 y 35'), validators.Required(message="El nombre es requerido")])
	codigo_postal = IntegerField('codigo codigo_postal', [validators.Required(message = "El codigo postal es requerido")])
	id_localidad = IntegerField('id localidad', validators.Required(message = "Necesito una localidad"))

class Localidad(Form):
	id = IntegerField('id',[validators.NumberRange(min = 0), validators.Required(message="El codigo de localidad es requerido")])
	nombre = StringField('nombre', [validators.length(min = 3, max = 35), validators.Required(message = "El Nombre es requerido")])
	id_estado = IntegerField('id estado',[validators.Required(message = "El el id del estado es requerido")])

class Estado(Form):
	id = IntegerField('id', [validators.NumberRange(min = 0), validators.Required(message = "El id del estado es requerido")])
	nombre = StringField('nombre',[validators.Required(message = 'El nombre es requerido')])
	


