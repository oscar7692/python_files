$(document).ready(function(){
	var n_fact = 0;
	$("#semana").on("click",function(event){
		$.ajax({
			url:"/muestraFactura",
			type:"POST",
			data:{val:1},
			success: function(response){
				var facturas = jQuery.parseJSON(response);
				if(typeof facturas == 'object')
				{
					$("#cuerpoTabla").empty();
					for(var i = 0; i < facturas.length; i++ )
					{
						var nuevaFila = "<tr>";
						nuevaFila += "<td>"+facturas[i].id+"</td>";
						nuevaFila += "<td>"+facturas[i].serie+"</td>";
						nuevaFila += "<td>"+facturas[i].folio+"</td>";
						nuevaFila += "<td>"+facturas[i].folfis+"</td>";
					    nuevaFila += "<td>"+facturas[i].fecha+"</td>";
					    nuevaFila += "<td>"+facturas[i].rfc+"</td>";
					    nuevaFila += "<td>"+facturas[i].sub+"</td>";
					    nuevaFila += "<td>"+facturas[i].iva+"</td>";
					    nuevaFila += "<td>"+facturas[i].total+"</td>";
						
						if(facturas[i].folfis != ""){
							nuevaFila += '<td><a href="mostrarPDF?serie='+facturas[i].serie+'&folio='+facturas[i].folio+'" target="_blank"><button type="button" class="btn btn-default btn-xs">Ver</button></a></td>';
							$("#ver_"+n_fact).on("click",function(event){
								alert("Hola"+n_fact);
							});
							n_fact++;
						}

						nuevaFila += "</tr>";
						$("#tabla tbody").append(nuevaFila);
					}
				}
			},
			error: function(error){
				alert("Error en boton mostrar");
			}
		});
	});

	$("#pendientes").on("click",function(event){
		$.ajax({
			url:"/muestraFactura",
			type:"POST",
			data:{val:2},
			success: function(response){
				var facturas = jQuery.parseJSON(response);
				if(typeof facturas == 'object')
				{
					$("#cuerpoTabla").empty();
					for(var i = 0; i < facturas.length; i++ )
					{
						var nuevaFila = "<tr>";
						nuevaFila += "<td>"+facturas[i].id+"</td>";
						nuevaFila += "<td>"+facturas[i].serie+"</td>";
						nuevaFila += "<td>"+facturas[i].folio+"</td>";
						nuevaFila += "<td>"+facturas[i].folfis+"</td>";
					    nuevaFila += "<td>"+facturas[i].fecha+"</td>";
					    nuevaFila += "<td>"+facturas[i].rfc+"</td>";
					    nuevaFila += "<td>"+facturas[i].sub+"</td>";
					     nuevaFila += "<td>"+facturas[i].iva+"</td>";
					    nuevaFila += "<td>"+facturas[i].total+"</td>";
						nuevaFila = nuevaFila + "</tr>";
						$("#tabla tbody").append(nuevaFila);
					}
				}
			},
			error: function(error){
				alert("Error en boton pendientes");
			}
		});
	})
})