# encoding: utf-8
# se calcula la fecha de emisión en formato ISO 8601

from flask  import Flask
from flask  import render_template
from flask  import send_from_directory
from flask  import request
from flask import redirect
from flask import url_for

from models import db
from models import Product
from models import PriceList
from models import Estado
from models import Customer
from models import unitMeasurement
from models import Localidad
from models import Colonia
from models import Factura
from models import RelacionFactura
from config import DevelopmentConfig

from facturacion_moderna import facturacion_moderna

import json
import forms
import datetime
import base64
from M2Crypto import RSA
from lxml import etree as ET
import hashlib
import os


from datetime import datetime

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


@app.route('/')
def index():
	title = "Facturacion"
	return render_template('index.html', title = title)




@app.route('/login' , methods = ['GET', 'POST'])
def login():
	
	print('Entraste al Logeo')
	login_form = forms.LogForm(request.form)
	
	if request.method == 'POST' and  login_form.validate():
		print "cumpli la condicion"
		print login_form.username.data
		print login_form.password.data

	return render_template('login.html', form = login_form)

@app.route('/customers')
def customers():
	title = "Clientes"
	estado = db.session.query(Estado).order_by(Estado.nombre).all()
	if len(estado) == 0:
		return render_template('customers.html',title = title, estado = [], localidad = [], colonia = [])
	localidad = db.session.query(Localidad).order_by(Localidad.nombre).filter(Localidad.estado_id == estado[0].id)
	if  localidad.count() == 0:
		#print "La localidad es None"
		return render_template('customers.html',title = title, estado = estado, localidad = [] , colonia = [])

	colonia = db.session.query(Colonia).order_by(Colonia.nombre).filter(Colonia.localidad_id == localidad[0].id)
	return render_template('customers.html',title = title, estado = estado, localidad = localidad, colonia = colonia)

@app.route('/products',  methods = ['GET', 'POST'])
def products():
	unit = db.session.query(unitMeasurement).all()
	unit_form = forms.UnitMeasurement();
	product_form = forms.ProductForm(request.form)
	title = "Productos"

	if request.method == 'POST' and product_form.validate():
		
		product = Product(id =  product_form.id.data,
			name = product_form.name.data.upper(),
			quantity = product_form.quantity.data,
			purchasePrice = product_form.purchasePrice.data,
			unit_m = product_form.unitm.data
		)

		db.session.add(product)
		db.session.commit()

	return render_template('products.html',title = title, form1 = product_form, unit = unit, unit_form = unit_form)

@app.route('/searchproducts', methods = ['GET', 'POST'])
def searchProducts():
	if request.method == 'POST':
		if request.form.get('id') is not None:
			product = db.session.query(Product).filter(Product.id==request.form.get('id')).first()
			if product is  not None:
				response  = {'id':product.id ,'name':product.name, 'purchase':product.purchasePrice}
				return    json.dumps(response)
			else:
				response  = {'id':-1}
				return json.dumps(response)
		elif request.form.get('name') is not None:
			listProduct = []
			product = db.session.query(Product).filter(Product.name.like("%"+request.form.get('name')+"%"))
			if  product.count():
				for p in product:
					response  = {'id':p.id ,'name':p.name, 'purchase':p.purchasePrice}
					listProduct.insert(len(listProduct),response)
			return json.dumps(listProduct)


@app.route('/unit', methods = ['GET', 'POST'])
def unit():
	print('Procesando formas')
	unit_form = forms.UnitMeasurement(request.form);
	if request.method == 'POST' and unit_form.validate():
		unit = unitMeasurement(name = unit_form.name.data.upper(), abbreviation = unit_form.abbreviaton.data.upper(), descripcion = unit_form.descripcion.data.upper())
		db.session.add(unit)
		db.session.commit()
	return redirect(url_for('products'))

@app.route('/ajax-login', methods = ['GET', 'POST'])
def ajax_log():

	if request.method == 'POST':
		listProduct = []
		product = db.session.query(Product).all()
		for p in product:	
			response  = {'id':p.id ,'name':p.name, 'purchase':p.purchasePrice}
			listProduct.insert(len(listProduct),response)
		return json.dumps(listProduct)
	else:
		return redirect(url_for('products'))

@app.route('/configuracion')
def conf():
	estado = db.session.query(Estado).all()
	localidad = db.session.query(Localidad).all()
	title = "Configuracion"
	return render_template('configuracion.html', title = title, estado = estado, localidad = localidad)

@app.route('/addEstado' , methods = ['GET', 'POST'])
def addEstado():
	if request.method == 'POST':
		if request.form.get('nombreEstado') is not None:
			edo = Estado(nombre = request.form.get('nombreEstado').upper())
			db.session.add(edo)
			db.session.commit()
			return "OK"
		else:
			return "BAD"
	else: 
		return "NOT POST"


@app.route('/addLocalidad', methods = ['GET', 'POST'])
def addLocalidad():
	if request.method == 'POST':
		if request.form.get('nombreLocalidad') is not None and request.form.get('nombreEstado') is not None:
			print request.form.get('nombreLocalidad')
			print request.form.get('nombreEstado')
			localidad = Localidad(nombre = request.form.get('nombreLocalidad').upper(), estado_id = request.form.get('nombreEstado'));
			db.session.add(localidad);
			db.session.commit();
		else:
			print "No hay nada por hacer"
	return "Fin add"


@app.route('/mostrarLocalidad', methods = ['GET','POST'])
def mostrarLocalidad():
	if request.method == 'POST':
		if request.form.get('estado') is not None:
			localidad = db.session.query(Localidad).order_by(Localidad.nombre).filter(Localidad.estado_id == request.form.get('estado'))
			listLocalidad = []
			for loc in localidad:
				response  = {'id':loc.id ,'nombre':loc.nombre}
				listLocalidad.insert(len(listLocalidad),response)
			return json.dumps(listLocalidad)
		else:
			return "No esta el campo"
	return "ERROR";

@app.route('/mostrarColonia', methods = ['POST'])
def mostrarColonia():
	if request.method == 'POST':
		if request.form.get('localidad') is not None:
			localidad = db.session.query(Colonia).filter(Colonia.localidad_id == request.form.get('localidad'))
			listColonia = []
			for loc in localidad:
				response  = {'id':loc.id ,'nombre':loc.nombre}
				listColonia.insert(len(listColonia),response)
			return json.dumps(listColonia)
		else:
			return "No esta el campo"
	return "ERROR";

@app.route('/addColonia', methods = ['GET','POST'])
def addColonia():
	if request.method == "POST":
		if request.form.get("nombre") is not None and request.form.get("localidad") is not None and request.form.get("codigo") is not None:
			colonia = Colonia(nombre =  request.form.get("nombre").upper(), codigoPostal = request.form.get("codigo"), localidad_id = request.form.get("localidad"));
			db.session.add(colonia);
			db.session.commit();
			return "No es NULL"
	print request.form.get("nombre")
	print request.form.get("localidad")
	print request.form.get("codigo")
	return "ERROR";


@app.route('/mostrarClientes', methods =['POST'])
def mostrarClientes():
	if request.method == "POST":
		listCliente = []
		customer = db.session.query(Customer).all()
		for c in customer:
			response  = {'id':c.id ,'name':c.name, 'rfc':c.rfc, 'phone':c.phone, 'email':c.email, 'activo':c.active }
			listCliente.insert(len(listCliente),response)
		return json.dumps(listCliente)
	else:
		return "MALO"


@app.route('/addCustomer', methods = ['POST'])
def addCustomer():
	custForm = forms.CustomerForm(request.form)
	if request.method == "POST" and custForm.validate():
		customer = Customer(
			name = custForm.nombre.data.upper(),
			rfc = custForm.rfc.data.upper(),
			phone = custForm.tel.data,
			email = custForm.email.data,
			calle = custForm.calle.data.upper(),
			num_ext = custForm.numEx.data,
			num_in = custForm.num.data,
			colonia_id = custForm.colonia.data
		);
		db.session.add(customer)
		db.session.commit()
		return "Exito"
	else:
		mensaje = ""
		for campo in custForm:
			for error in campo.errors:
				mesaje = error + mensaje
		return mensaje


@app.route('/searchCustomer', methods = ['POST'])
def searchCustomer():
	
	if request.method == 'POST':
		listCustomer = []
		if request.form.get('palabra') is not None:
			customer = db.session.query(Customer).filter(Customer.name.like("%"+request.form.get('palabra')+"%"))
		elif request.form.get('rfc') is not None:
			customer = db.session.query(Customer).filter(Customer.rfc==request.form.get('rfc'))
		else:
			return "mal"
		for c in customer:
			response  = {'id':c.id ,'name':c.name, 'rfc':c.rfc}
			listCustomer.insert(len(listCustomer),response)
		return json.dumps(listCustomer)
	else:
		return "no post"

@app.route('/searchCustomerFact', methods = ['POST'])
def searchCustomerFact():
	print "Estoy en searchCustomerFact"
	if request.method == 'POST':
		if request.form.get('rfc') is not None:
			customer = db.session.query(Customer).filter(Customer.rfc==request.form.get('rfc')).first()
			if customer is not None:
				response  = {'id':customer.id ,'name':customer.name, 'rfc':customer.rfc}
				return json.dumps(response)
			else:
				return json.dumps({'id':-1})
		else:
			return json.dumps({'id':-1})
	else:
		return json.dumps({'id':-1})

@app.route('/crearFactura' , methods  = ['POST'])
def crearFactura():
	if request.method == 'POST':
		if request.form.get('datos') is not None and request.form.get('rfc') is not None and request.form.get('folio') is not None and request.form.get('serie') is not None:
			factura = db.session.query(Factura).filter(Factura.serie == request.form.get('serie')).filter(Factura.folio == request.form.get('folio')).first()
			if factura is  None:
				factura = Factura(
					serie = request.form.get('serie'),
					folio = request.form.get('folio'),
					timbrada = False,
					folioFiscal = "",
					rfc_cliente = request.form.get('rfc')
				)
				db.session.add(factura)
				db.session.commit()

				#Recuperamos la informacion a facturar
				data  = json.loads(request.form.get('datos'))
				for elemento in data:
					producto = db.session.query(Product).filter(Product.id == elemento['id']).first()
					factura = db.session.query(Factura).filter(Factura.serie == request.form.get('serie')).filter(Factura.folio == request.form.get('folio')).first()
					relacion = RelacionFactura(id_factura = factura.id, id_producto = producto.id, numero_unidades = elemento['n_u'], precio_salvado = producto.purchasePrice)
					db.session.add(relacion)
					db.session.commit()

				respuesta = timbrar(request.form.get('serie'),request.form.get('folio'))
				return json.dumps({'id':respuesta})
			else:
				print "La factura ya esta ocupada"
				return json.dumps({'id':-1})
		return json.dumps({'id':-2})
	else:
		return json.dumps({'id':-3})

def sella_xml(cfdi, numero_certificado, archivo_cer, archivo_pem):
	keys = RSA.load_key(archivo_pem)
	cert_file = open(archivo_cer, 'r')
	cert = base64.b64encode(cert_file.read())
	xdoc = ET.fromstring(cfdi)
	comp = xdoc.get('Comprobante')
	xdoc.attrib['Certificado'] = cert
	xdoc.attrib['NoCertificado'] = numero_certificado

	xsl_root = ET.parse('utilerias/xslt33/cadenaoriginal_3_3.xslt')
	xsl = ET.XSLT(xsl_root)
	cadena_original = xsl(xdoc)
	digest = hashlib.new('sha256', str(cadena_original)).digest()
	sello = base64.b64encode(keys.sign(digest, "sha256"))

	comp = xdoc.get('Comprobante')
	xdoc.attrib['Sello'] = sello
	print ET.tostring(xdoc)
	return ET.tostring(xdoc)



@app.route('/mostrarPDF', methods = ['GET','POST'])
def mostrarPDF():
	serie = request.args.get('serie','error')
	folio = request.args.get('folio','error')
	print "serie: " +serie
	print "folio: "+folio
	print "ERROR"
	folder = 'comprobantes'
  	return send_from_directory(directory="comprobantes",filename=serie+"-"+str(folio)+".pdf",mimetype='application/pdf')


@app.route('/mostrarXML', methods = ['GET','POST'])
def mostrarXML():
	serie = request.args.get('serie','error')
	folio = request.args.get('folio','error')
	print "serie: " +serie
	print "folio: "+folio
	folder = 'comprobantes'
  	return send_from_directory(directory="comprobantes",filename=serie+"-"+str(folio)+".xml",mimetype='application/xml')

def timbrar(serie, folio):
	'''
	serie = "JAL"
	folio = 1
	folder = 'comprobantes'
	comprobante = os.path.join(folder, serie+"-"+str(folio))
	print comprobante
  	return send_from_directory(directory="comprobantes",filename="JAL-1.pdf",mimetype='application/pdf')
  	'''

	debug = True
	#se calcula la fecha de emision en formato ISO 8601
  	fecha_actual = str(datetime.now().isoformat())[:19]
	rfc_emisor = "ESI920427886"

	numero_certificado = "20001000000200000192"
	archivo_cer = "utilerias/certificados/20001000000200000192.cer"
	archivo_pem = "utilerias/certificados/20001000000200000192.key.pem"

	url_timbrado = "https://t1demo.facturacionmoderna.com/timbrado/wsdl"
	user_id = "UsuarioPruebasWS"
	user_password = "b9ec2afa3361a59af4b4d102d3f704eabdf097d4"


	factura = db.session.query(Factura).filter(Factura.serie == serie).filter(Factura.folio == folio).first()
	if factura is None:
		return -5

	if factura.timbrada:
		return -2

	cliente = db.session.query(Customer).filter(factura.rfc_cliente == Customer.rfc).first()
	RFC = cliente.rfc
	NOMBRE = cliente.name
	relaciones = db.session.query(RelacionFactura).filter(RelacionFactura.id_factura == factura.id)
	total = 0;
	subTotal = 0;
	subTraslados = 0;

	conceptos =""
	for relacion in relaciones:
		producto = db.session.query(Product).filter(Product.id == relacion.id_producto).first()
		numero_unidades = str(relacion.numero_unidades)
		valorUnitario = "{0:.2f}".format(relacion.precio_salvado)
		importe = "{0:.2f}".format(float(valorUnitario) * float(numero_unidades))
		descripcion = producto.name
		importeTraslado = "{0:.2f}".format( float(importe) * float(0.16))
		subTotal = subTotal + float(importe)
		subTraslados = subTraslados + float(importeTraslado)
		concepto = """<cfdi:Concepto ClaveProdServ="01010101" NoIdentificacion="AULOG001" Cantidad="{numero_unidades}" ClaveUnidad="H87" Unidad="Pieza" Descripcion="{descripcion}" ValorUnitario="{valorUnitario}" Importe="{importe}">
		<cfdi:Impuestos>
			<cfdi:Traslados>
				<cfdi:Traslado Base="{importe}" Impuesto="002" TipoFactor="Tasa" TasaOCuota="0.160000" Importe="{importeTraslado}"/>
      		</cfdi:Traslados>
  		</cfdi:Impuestos>
		</cfdi:Concepto>""".format(**locals())
		conceptos = conceptos + concepto

	total = subTotal + subTraslados
	#Formateamos nuestras cadenas
	total = "{0:.2f}".format(total)
	subTotal = "{0:.2f}".format(subTotal)
	subTraslados = "{0:.2f}".format(subTraslados)

	cfdi = """<?xml version="1.0" encoding="UTF-8"?>
<cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/3" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sat.gob.mx/cfd/3 http://www.sat.gob.mx/sitio_internet/cfd/3/cfdv33.xsd" Version="3.3" Serie="{serie}" Folio="{folio}" Fecha="{fecha_actual}" Sello="" FormaPago="03" NoCertificado="" Certificado="" CondicionesDePago="CONTADO" SubTotal="{subTotal}"  Moneda="MXN" Total="{total}" TipoDeComprobante="I" MetodoPago="PUE" LugarExpedicion="68050">
  <cfdi:Emisor Rfc="{rfc_emisor}" Nombre="FACTURACION MODERNA SA DE CV" RegimenFiscal="601"/>
  <cfdi:Receptor Rfc="{RFC}" Nombre="{NOMBRE}" UsoCFDI="G01"/>
  <cfdi:Conceptos>""".format(**locals()) 


  	pie = """</cfdi:Conceptos>
<cfdi:Impuestos TotalImpuestosTrasladados="{subTraslados}">
    <cfdi:Traslados>
      <cfdi:Traslado Impuesto="002" TipoFactor="Tasa" TasaOCuota="0.160000" Importe="{subTraslados}"/>
  </cfdi:Traslados>
</cfdi:Impuestos>
</cfdi:Comprobante>""".format(**locals())

  	cfdi = cfdi + conceptos + pie
  	cfdi = sella_xml(cfdi, numero_certificado, archivo_cer, archivo_pem)

  	params = {'emisorRFC': rfc_emisor, 'UserID': user_id, 'UserPass': user_password}
  	options = {'generarCBB': False, 'generarPDF': True, 'generarTXT': False}
  	cliente = facturacion_moderna.Cliente(url_timbrado, params, debug)

  	if cliente.timbrar(cfdi, options):
  		folder = 'comprobantes'
  		if not os.path.exists(folder): os.makedirs(folder)
  		# cliente.uuid Nos puede dar el folio fiscal
  		comprobante = os.path.join(folder, serie+"-"+str(folio))
  		for extension in ['xml', 'pdf', 'png', 'txt']:
  			if hasattr(cliente, extension):
  				print extension
  				print cliente
  				with open(("%s.%s" % (comprobante, extension)), 'wb' if extension in ['pdf','png'] else 'w') as f: f.write(getattr(cliente, extension))
  				print("%s almacenado correctamente en %s.%s" % (extension.upper(), comprobante, extension))
		factura.timbrada = True
		factura.folioFiscal = cliente.uuid
		db.session.commit()
		print 'Timbrado exitoso'
	  	return 1

	else:
		print("[%s] - %s" % (cliente.codigo_error, cliente.error))
		return -3

def calcularDetalles(id):
	total = 0;
	subTotal = 0;
	subTraslados = 0;
	relaciones = db.session.query(RelacionFactura).filter(RelacionFactura.id_factura == id)
	for relacion in relaciones:
		numero_unidades = str(relacion.numero_unidades)
		valorUnitario = "{0:.2f}".format(relacion.precio_salvado)
		importe = "{0:.2f}".format(float(valorUnitario) * float(numero_unidades))
		importeTraslado = "{0:.2f}".format( float(importe) * float(0.16))
		subTotal = subTotal + float(importe)
		subTraslados = subTraslados + float(importeTraslado)

	total = subTotal + subTraslados
	#Formateamos nuestras cadenas
	total = "{0:.2f}".format(total)
	subTotal = "{0:.2f}".format(subTotal)
	subTraslados = "{0:.2f}".format(subTraslados)
	return subTotal, subTraslados, total



@app.route('/muestraFactura', methods  = ['POST'])
def muestraFactura():
	facturas = []
	if int(request.form.get('val')) == 1:
		factura = db.session.query(Factura).all()
	elif int(request.form.get('val')) == 2:
		factura = db.session.query(Factura).filter(Factura.timbrada == 0)		
	for f in factura:
			sub , iva, total = calcularDetalles(f.id)
			response = {'id':f.id , 'serie':f.serie, 'folio':f.folio, 'folfis':f.folioFiscal, 'rfc':f.rfc_cliente, 'fecha': f.fecha.strftime("%d/%m/%y"), 'total':total , 'sub':sub ,'iva':iva}
			facturas.append(response)
		
	return json.dumps(facturas)

@app.route('/facturar')
def facturar():
	title = "Facturacion"
	return render_template('facturar.html', title = title)


if __name__ == '__main__':
	db.init_app(app)
	with app.app_context():
		db.create_all()
	#app.run(host = '0.0.0.0')
	app.run(debug = True, port = 8000)