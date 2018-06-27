from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Factura(db.Model):
	__tablename__ = 'factura'
	id = db.Column(db.Integer, primary_key = True)
	serie = db.Column(db.String(4),  nullable = False)
	folio = db.Column(db.Integer, nullable = False)
	timbrada = db.Column(db.Boolean, nullable = False)
	folioFiscal = db.Column(db.String(100))
	fecha = db.Column(db.DateTime, default  =datetime.datetime.now, nullable = False)
	rfc_cliente = db.Column(db.String(13), nullable = False)

class RelacionFactura(db.Model):
	__tablename__ = 'relacion_factura'
	id = db.Column(db.Integer, primary_key = True)
	id_factura = db.Column(db.Integer, nullable = False)
	id_producto = db.Column(db.Integer, nullable = False)
	numero_unidades = db.Column(db.Integer, nullable = False)
	precio_salvado = db.Column(db.Integer, nullable = False)


class unitMeasurement(db.Model):
	__tablename__ = 'u_measurement'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(15), unique = True, nullable = False)
	abbreviation = db.Column(db.String(4), unique = True, nullable = False)
	descripcion = db.Column(db.String(20), unique=True, nullable = False)



class Product(db.Model):
	__tablename__ = 'product'
	id = db.Column(db.Integer, primary_key = True, autoincrement=False)
	name = db.Column(db.String(50),unique=True ,nullable = False)
	quantity = db.Column(db.Integer, nullable = False)
	purchasePrice = db.Column(db.Float, nullable = False)
	active = db.Column(db.Boolean, nullable = False, default = True)
	unit_m =  db.Column(db.Integer, db.ForeignKey('u_measurement.id'), nullable = False)
	create_date = db.Column(db.DateTime, default = datetime.datetime.now, nullable = False)


class PriceList(db.Model):
	__tablename__ = 'price_list'
	id = db.Column(db.Integer, primary_key = True)
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable = False , index = True)
	sale_price = db.Column(db.Float, nullable = False)
	create_date = db.Column(db.DateTime, default = datetime.datetime.now, nullable = False)
	

class Estado(db.Model):
	__tablename__ = "estado"
	id = db.Column(db.Integer, primary_key = True)
	nombre = db.Column(db.String(20), nullable = False, unique = True)

class Localidad(db.Model):
	__tablename__ = "localidad"
	id = db.Column(db.Integer, primary_key = True)
	nombre = db.Column(db.String(35), nullable = False)
	estado_id = db.Column(db.Integer, db.ForeignKey('estado.id'), nullable = False, index = True)


class Colonia(db.Model):
	__tablename__ = 'colonia'
	id = db.Column(db.Integer, primary_key = True)
	nombre = db.Column(db.String(35), nullable = False)
	codigoPostal = db.Column(db.Integer, nullable = False, index = True)
	localidad_id = db.Column(db.Integer, db.ForeignKey('localidad.id'), nullable = False, index = True)


class Customer(db.Model):
	__tablename__ ='customer'
	id     = db.Column(db.Integer, primary_key = True ,autoincrement = True)
	name   = db.Column(db.String(50), nullable = False)
	rfc    = db.Column(db.String(13), unique=True, nullable = False, index = True)
	phone  = db.Column(db.String(13), unique=True, nullable = False)
	email  = db.Column(db.String(50), unique = True, nullable  = False)
	active = db.Column(db.Boolean, nullable = False, default = True)
	calle  = db.Column(db.String(50), nullable = False)
	num_ext = db.Column(db.String(10), nullable = False)
	num_in = db.Column(db.String(10), nullable = True)
	colonia_id = db.Column(db.Integer, db.ForeignKey('colonia.id'), nullable = False, index = True)
	create_date = db.Column(db.DateTime, default  =datetime.datetime.now, nullable = False)



class Proveedor(db.Model):
	__tablename__ = 'proveedor'
	id     = db.Column(db.Integer, primary_key = True)
	name   = db.Column(db.String(50), nullable = False)
	rfc    = db.Column(db.String(13), unique=True, nullable = False, index = True)
	phone  = db.Column(db.String(13), unique=True, nullable = False)
	email  = db.Column(db.String(50), unique = True, nullable  = False)
	active = db.Column(db.Boolean, nullable = False, default = True)
	calle  = db.Column(db.String(50), nullable = False)
	num_in = db.Column(db.String(10), nullable = True)
	colonia_id = db.Column(db.Integer, db.ForeignKey('colonia.id'), nullable = False, index = True)
	create_date = db.Column(db.DateTime, default  =datetime.datetime.now, nullable = False)


		



