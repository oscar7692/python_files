$(document).ready(function(){
	$("#checkSearch").change(function(){
		if($(this).val() == "FALSE"){
			$("#labelSearch").text("Palabra Clave")
			$(this).val("TRUE")
			$("#inputSearch").prop('type', 'text')
			$("#inputSearch").prop('name','name')
		}
		else{
			$("#labelSearch").text("Codigo")
			$(this).val("FALSE")
			$("#inputSearch").prop('type', 'number')
			$("#inputSearch").prop('name','id')
		}	
	})

	function ajax_show(){
		$.ajax({
			url: 'ajax-login',
			type: 'POST',
			success: function(response){
				var listProduct = jQuery.parseJSON(response)
				if(typeof listProduct == 'object'){
					$("#bodyTable").empty();
					for(var i = 0; i < listProduct.length; i++){
						$("#productsTable tbody").append('<tr><td>'+listProduct[i].id+'</td><td>'+listProduct[i].name+'</td><td>'+listProduct[i].purchase+'</td></tr>');
					}
				}else{
					if(listProduct === false){
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
	}
	$("#mostrarP").on('click', ajax_show);
	
	$("#searchForm").submit( function(event){
		event.preventDefault();
		var $form = $(this), url = $form.attr('action');
		//if ($('#inputSearch'))
		var posting;
		if ($('#inputSearch').attr('type') == 'number'){
			posting = $.post(url, {id : $('#inputSearch').val()});
			posting.done(function(data){
				data = jQuery.parseJSON(data);
				$("#bodySearchTable").empty();
				if(data.id != -1){
					$("#messageSearch").empty();
					$("#messageSearch").prop("class", "row alert alert-success");
					$("#messageSearch").append("El producto se encuentra");
					$("#searchTable tbody").append('<tr><td>'+data.id+'</td><td>'+data.name+'</td><td>'+data.purchase+'</td></tr>');
				}
				else{
					alert("No se encuentra el producto");
					$("#messageSearch").empty();
					$("#messageSearch").prop("class", "row alert alert-danger");
					$("#messageSearch").append("No se encontro  el producto");
				}
			});
		}
		else{
			posting = $.post(url, {name : $('#inputSearch').val()});
			posting.done(function(data){
				var listProduct = jQuery.parseJSON(data)
				if(typeof listProduct == 'object'){
					$("#bodySearchTable").empty();
					if(listProduct.length == 0){
						alert("Ninguna coincidencia");
						$("#messageSearch").empty();
						$("#messageSearch").prop("class", "row alert alert-danger");
						$("#messageSearch").append("No se encontro ni una coincidencia");
					}else{
						for(var i = 0; i < listProduct.length; i++){
							$("#searchTable tbody").append('<tr><td>'+listProduct[i].id+'</td><td>'+listProduct[i].name+'</td><td>'+listProduct[i].purchase+'</td></tr>');
						}
						$("#messageSearch").empty();
						$("#messageSearch").prop("class", "row alert alert-success");
						$("#messageSearch").append(listProduct.length + " productos encontrados");
					}
				}else{
					if(listProduct === false){
						alert('The response was a string "false", parseJSON will convert it to bool')
					}else{
						alert('The response was something else')
					}
				}
			});
		}
	});


});