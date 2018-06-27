$(document).ready(function(){

	$("#addEstado").submit(function(event){
		
		if(confirm("¿Desea capturar el estado?")){
			event.preventDefault();
			var $form = $(this), url = $form.attr('action');
			var posting = $.post(url, {nombreEstado : $('#nombreEstado').val()});
			posting.done(function(data){
				alert("data: "+data)
			});
		}else{
			event.preventDefault();
		}
		$('#modalEstado').modal('toggle');
		$('#nombreEstado').val("");
	});

	$("#addLocalidad").submit(function(event){

		if (confirm("¿Desea capturar la Localidad?")){
			alert("Envio de localidad");
			event.preventDefault();
			var $form = $(this), url = $form.attr('action');
			var posting = $.post(url, {nombreLocalidad : $('#nomLocalidad').val(), nombreEstado : $('#estLocalidad').val()});
			posting.done(function(data){
				alert("data "+data)
			});
		}
		else{
			event.preventDefault();
		}
		$('#modalLocalidad').modal('toggle');
		$('#nomLocalidad').val("");
	});

	$("#addColonia").submit(function(event){

		if (confirm("¿Desea capturar la Colonia?")){
			event.preventDefault();
			var $form = $(this), url = $form.attr('action');
			var posting = $.post(url, {nombre : $('#nomAddCol').val(), localidad : $('#locColonia').val(), codigo : $('#codAddCol').val() });
			posting.done(function(data){
				alert("data "+data)
			});
		}
		else{
			event.preventDefault();
		}
		$('#modalColonia').modal('toggle');
		$('#nomAddCol').val("");
		$('#locAddCol').val("");
		$('#codAddCol').val("");
	});

	$("#estColonia").change(function(){
		$.ajax({
			url: "/mostrarLocalidad",
			type: 'POST',
			data: {estado:  $(this).val()},
			success: function(response){
				var listLocalidad = jQuery.parseJSON(response);
				$("#locColonia").empty();
				for(var i = 0; i < listLocalidad.length; i++)
					$("#locColonia").append('<option value="'+listLocalidad[i].id+'">'+listLocalidad[i].nombre+'</option>');	
			},
			error: function(error){
				console.log(error);
			}
		});
	})

	$("#mostEstado").change(function(){
		$.ajax({
			url: "/mostrarLocalidad",
			type: 'POST',
			data: {estado:  $(this).val()},
			success: function(response){
				var listLocalidad = jQuery.parseJSON(response);
				$("#bodyShowTable").empty();
				for(var i = 0; i < listLocalidad.length; i++)
					$("#localidadTable tbody").append('<tr><td>'+listLocalidad[i].id+'</td><td>'+listLocalidad[i].nombre+'</td></tr>');	
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});