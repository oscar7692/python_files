$(document).ready(function(){
	
	$("#checkSearch").change(function(){
		$("#searchCuerpoTabla").empty();
		$("#inputSearch").val("");

		if($(this).val() == "FALSE"){
			$("#labelSearch").text("Palabra Clave");
			$(this).val("TRUE");
			$("#inputSearch").prop('name','palabra');
			$("#inputSearch").attr('minlength','2');
		}
		else{
			$("#labelSearch").text("RFC");
			$(this).val("FALSE");
			$("#inputSearch").prop('name','rfc');
			$("#inputSearch").attr('minlength','12');
		}	
	})

	/*Incluye el codigo javascript para el registro de un cliente*/
	$("#addCustForm").submit(function(event){
		if (confirm("Desea capturar el cliente")){
			event.preventDefault();
			var $form = $(this), url = $form.attr("action");
			var posting = $.post(url,{nombre :  $("#nameCust").val()  , rfc : $("#rfcCust").val(), tel : $("#telCust").val(), email : $("#emailCust").val(), colonia : $("#colCust").val(),
				calle : $("#calleCust").val(), num :$("#numInCust").val(), numEx : $("#numExCust").val()
			});
			posting.done(function(data){
				var $inputs = $('#addCustForm :input');
				$inputs.each(function() {
					$(this).val("");
    			});
    			alert(data);
    			$("#capturaCliente").modal("toggle");
			})//
		}
		else{
			event.preventDefault();
		}
	});

	/*Sirve para cambiar el select de la captura de los datos*/
	$("#estCust").change(function(){
		$.ajax({
			url: "/mostrarLocalidad",
			type: 'POST',
			data: {estado:  $(this).val()},
			success: function(response){
				var listLocalidad = jQuery.parseJSON(response);
				$("#locCust").empty();
				for(var i = 0; i < listLocalidad.length; i++)
					$("#locCust").append('<option value="'+listLocalidad[i].id+'">'+listLocalidad[i].nombre+'</option>');
				$("#colCust").empty();
				if(listLocalidad.length != 0){
					$.ajax({
						url: "/mostrarColonia",
						type: 'POST',
						data: {localidad:  listLocalidad[0].id},
						success: function(response){
							var listColonia = jQuery.parseJSON(response);
							$("#colCust").empty();
							for(var i = 0; i < listColonia.length; i++)
								$("#colCust").append('<option value="'+listColonia[i].id+'">'+listColonia[i].nombre+'</option>');	
						},
						error: function(error){
							console.log(error);
						}
					});
				}	
			},
			error: function(error){
				console.log(error);
			}
		});
	})

	$("#searchForm").submit(
		function(event){
			event.preventDefault();
			var $form = $(this), url = $form.attr("action");
			var posting;
			if ($("#inputSearch").prop('name') == 'rfc'){
				posting = $.post(url, {rfc : $('#inputSearch').val()});
				posting.done(function(data){
						var listCliente  = jQuery.parseJSON(data);
						$("#searchCuerpoTabla").empty();
						for(var i = 0; i < listCliente.length; i++){
							$("#searchClientesTabla tbody").append('<tr><td>'+listCliente[i].id+'</td><td>'+listCliente[i].name+'</td><td>'+listCliente[i].rfc+'</td></tr>');
						}
				});
			}else if( $("#inputSearch").prop('name') =='palabra'){
				posting = $.post(url, {palabra : $('#inputSearch').val()});
				posting.done(function(data){
					var listCliente  = jQuery.parseJSON(data);
					$("#searchCuerpoTabla").empty();
						for(var i = 0; i < listCliente.length; i++){
							$("#searchClientesTabla tbody").append('<tr><td>'+listCliente[i].id+'</td><td>'+listCliente[i].name+'</td><td>'+listCliente[i].rfc+'</td></tr>');
						}
				});
			}			
		}
	);

	$("#locCust").change(function(){
		$.ajax({
			url: "/mostrarColonia",
			type: 'POST',
			data: {localidad:  $(this).val()},
			success: function(response){
				var listColonia = jQuery.parseJSON(response);
				$("#colCust").empty();
				for(var i = 0; i < listColonia.length; i++)
					$("#colCust").append('<option value="'+listColonia[i].id+'">'+listColonia[i].nombre+'</option>');	
			},
			error: function(error){
				console.log(error);
			}
		});
	})

	//Fin para el formulario de registro de clientes

	$("#mostClientes").on('click',function(){
		$.ajax({
			url: '/mostrarClientes',
			type: 'POST',
			success: function(response){
				var listCliente = jQuery.parseJSON(response)
				if(typeof listCliente == 'object'){
					$("#cuerpoTabla").empty();
					for(var i = 0; i < listCliente.length; i++){
						$("#clientesTabla tbody").append('<tr><td>'+listCliente[i].id+'</td><td>'+listCliente[i].name+'</td><td>'+listCliente[i].rfc+'</td><td>'+listCliente[i].phone+'</td><td>'+listCliente[i].email+'</td><td>'+'<button type="button" class="btn btn-default btn-xs">+</button>'+'</td></tr>');
					}
				}else{
					if(listCliente === false){
						alert('The response was a string "false", parseJSON will convert it to bool')
					}else{
						alert('The response was something else')
					}
				}
			},
			error: function(error){
				console.log(error);
			}
		});
	});
	

});