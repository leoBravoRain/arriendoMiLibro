posts.controller("postsController",function($scope, informacionDetalladaLibroService){

	// Funciones para mostrar aviso de carga de contenido al iniciar llamada ajax
	$("#loadingContent").on('ajaxStart',function(){

		$(this).show();

	});

	// Funciones para ocultar aviso de carga de contenido al iniciar llamada ajax
	$("#loadingContent").on('ajaxStop',function(){

		$(this).hide('slow');
		
	});	

	// Se obtiene los datos de la libro
	$.ajax({

		type:"get",
		url: urlDetallesLibro,

		success:function(response){

			// Si es que existe alguna libro para mostrar
			if(response.libro.length>0){

				//se agrega la libro

				// Se obtiene la libro en formato para ser usado por el temlpate libroInformacionDetalladaTemplateAngularJS
				var libro = informacionDetalladaLibroService.getLibroObject(response.libro[0], response.owner[0], response.usuarioLogueadoId);

				// Se agrega finalmente el objeto postObject al template
				$scope.$apply(function(){

					$scope.libro = libro;

				});

				// Se esconde el icono de cargando contenido
				$("#loadingContent").hide("slow");

			}

		},
	});

});
