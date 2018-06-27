$(document).ready(function(){
	var n_input = 0;

	function calcularTotales(){
		var subtotal = 0;
		for(var i = 0; i < n_input+1; i++)
			subtotal = subtotal + Number($("#total_"+i).val());
		var iva = parseFloat(0.16) *  parseFloat(subtotal) ;
		$("#subtotal").val(subtotal);
		$("#iva").val(iva);
		$("#total").val( iva + subtotal);
	}


	$("#btnAdd").on('click',function(event){

		if($("#folio").val() == ""){
			alert("Necesito el folio");
			event.preventDefault();
			return "";
		}

		if(confirm("Desea agregar otro elemento a la factura") == false){
			event.preventDefault();
			return;
		}

		n_input++;
		var newElement = '<div class="row"><div class="col-md-3"><input id="cod_'+n_input+'" class="form-control" type="number" required></div><div class="col-md-3"><input id="nom_'+n_input+'" class="form-control" type="text"   required readonly></div><div class="col-md-2"><input id="pre_'+n_input+'" class="form-control" type="number" required readonly></div><div class="col-md-2"> <input id="nu_'+n_input+'" class="form-control" type="number" rquired></div><div class="col-md-2"><input id="total_'+n_input+'" class="form-control" type="number" required readonly></div></div>';
		$('#formFactura').append(newElement);


		$("#cod_"+n_input).on("keyup",function(e){
			if (e.keyCode == 13)
			{
				var codigo = $(this).val();
				$.ajax({url: "/searchproducts",type: 'POST',data: {id:  $(this).val()},
					success: function(response){
						var producto = jQuery.parseJSON(response);
						if(producto.id >= 0)
						{
							alert("El producto con el id "+codigo +" si se encuentra")
							$("#nom_"+n_input).val(producto.name);
							$("#pre_"+n_input).val(producto.purchase);
							$("#nu_"+n_input).val("");
							$("#total_"+n_input).val("");
							calcularTotales();
						}
						else
						{
							alert("No se encuentra el producto con el codigo "+codigo);
							$("#nom_"+n_input).val("");
							$("#pre_"+n_input).val(0);
							$("#nu_"+n_input).val(0);
							$("#total_"+n_input).val(0);
							calcularTotales();
							$("#cod_"+n_input).val("");	
						}
				},
					error: function(error){
						alert("Error")
						alert(error)
					}
				});
			}		
		});

		$("#nu_"+n_input).on("keyup", function(e){
			if(e.keyCode == 13){
				if( !($("#pre_"+n_input).val().length === 0) ){
					$("#total_"+n_input).val($("#pre_"+n_input).val() * $(this).val());
				}
				calcularTotales();
			}
		});


	});

	$("#cod_0").on("keyup focus",function(e){
		if (e.keyCode == 13)
		{
			var codigo = $(this).val();
			$.ajax({url: "/searchproducts",type: 'POST',data: {id:  $(this).val()},
				success: function(response){
					var producto = jQuery.parseJSON(response);
					if(producto.id >= 0)
					{
						alert("El producto con el id "+codigo +" si se encuentra")
						$("#nom_0").val(producto.name);
						$("#pre_0").val(producto.purchase);
						$("#nu_0").val("");
						$("#total_0").val("");
						calcularTotales();
					}
					else
					{
						alert("No se encuentra el producto con el codigo "+codigo);
						$("#nom_0").val("");
						$("#pre_0").val("");
						$("#nu_0").val("");
						$("#total_0").val(0);
						calcularTotales();
						$("#cod_0").val("");
					}
				},
				error: function(error){
					alert("Error")
					alert(error)
				}
			});
			
		}
	});

	$("#nu_0").on("keyup", function(e){
		if(e.keyCode == 13){
			if( !($("#pre_0").val().length === 0) ){
				$("#total_0").val($("#pre_0").val() * $(this).val());
			}
			calcularTotales();
		}
	});

	$("#rfc").on("keyup", function(e){
		if(e.keyCode == 13){
			$.ajax({url: "/searchCustomerFact",type: 'POST',data: {rfc:  $(this).val()},
					success: function(response){
						var cliente = jQuery.parseJSON(response);
						if(cliente.id >= 0)
						{
							$("#nombre").val(cliente.name);
						}
						else
						{
							alert("El cliente con el rfc "+$("#rfc").val()+"no se encuentra")
							$("#rfc").val("");
						}
				},
					error: function(error){
						alert("Error")
						alert(error)
					}
			});
		}
	});

	$("#btnFact").on("click", function(event){

		if($("#rfc").val().length === 0){
			alert("Es necesario el rfc");
			return;
		}


		if ($("#folio").val().length === 0){
			alert("Es necesario el folio");
			return;
		}


		for(var i  = 0; i < n_input+1; i++){
			alert("Checador")
			if( $("#cod_"+i).val().length === 0 ){
				alert("El codigo del campo: "+  (i +1));
				return;
			}
			if( $("#nu_"+i).val().length === 0){
				alert("El numero de unidades del campo: "+(i +1));
				return;
			} 
		}


		if(!confirm("Desea Emitir Facturar con la serie "+ $("#serie").val() + " folio "+$("#folio").val())){
			return;
		}


		arr =[];
		for(var i  = 0; i < n_input+1; i++){
			elemento = {id:$("#cod_"+i).val() , n_u: $("#nu_"+i).val()};
			arr.push(elemento);
		}

		$.ajax({url: "/crearFactura",type: 'POST',data: {'datos':JSON.stringify(arr), 'rfc': $("#rfc").val(),'serie': $("#serie").val(),'folio':$("#folio").val()},
				success: function(response){
					switch (jQuery.parseJSON(response).id){
						case -5: 
							alert("Ocurrio algun problema en el almacenamiento");
						break;
						case -3: 
							alert("Problema al momento de consumir el web service");
						break;
						case -2: 
							alert("La factura ya esta timbrada");
						break;
						case -1: 
							alert("La serie y folio ya estan registrados");
						break;
						case 1: 
							alert("Exito al almacenar la factura");
							window.location.href = "http://localhost:8000/facturar";
						break;
					}
				},
				error: function(error){
						alert(error);
				}
		});
	});

});