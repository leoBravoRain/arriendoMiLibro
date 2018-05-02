$(document).ready(function(){

	// Buscar algun libro
	$("#buscarLibro").click(function(){

		// Se obtiene el filtro por titulo
		var filtroPorTitulo = document.getElementById("filtroPorTitulo").value;

		// Si valor es vacio
		if(filtroPorTitulo == ""){

			filtroPorTitulo = cualquierTitulo;

		};

		// Filtro por ciudad
		var filtroPorCiudad = document.getElementById("filtroPorCiudad");
		var filtroPorCiudad = filtroPorCiudad.options[filtroPorCiudad.selectedIndex].value;

		// Se envia filtro a urlParaFiltrar
		window.location.replace(urlBuscarLibros + filtroPorTitulo + "/" + filtroPorCiudad);

	});

});