
@app.route('/prueba')
def prubea():
	title = "Facturacion"
	return render_template('index.html', title = title)
