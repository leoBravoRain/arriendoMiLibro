posts.controller("postsController",function($scope, informacionGeneralLibroService){

	//Se fijan variables de la aplicacion que se requieren para cargar correctamente el contenido

	//La variable busy es para bloquear/desbloquear el infinite-Scroll. Cuando esta seteado en false se ejecuta se puede hacer infinite-scroll. Cuando esta en true se bloquea el infinite scroll (Esto se hace por que se hacen muchas llamadas cuando se alcanza el final de la pagina)
	$scope.busy = true;

	// Funciones para mostrar aviso de carga de contenido al iniciar llamada ajax
	$("#loadingContent").on('ajaxStart',function(){

		$(this).show();

	});

	// Funciones para ocultar aviso de carga de contenido al iniciar llamada ajax
	$("#loadingContent").on('ajaxStop',function(){

		// $(this).show();

		$(this).hide('slow');
		
	});	

	// Se obtiene los datos iniciales
	$.ajax({

		type:"get",
		url: urlMisLibrosOwner,
		data: {"idLibrosMostrados":JSON.stringify([])},

		success:function(response){

			// Si es que existe alguna tarea para mostrar

			if(response.libros.length>0){

				//se agregan los nuevo posteos obtenidos
				addDataToView(response);

				//Se desbloquea el infinite-scroll
				$scope.$apply(function(){

					$scope.busy = false;

				});

			}

			// Si es qeu no hay datos para mostrar
			
			else{

				//Se bloquea el infinite-scroll para que no se continue pidiendo datos
				$scope.$apply(function(){

					$scope.busy = true;
					
				});

				// Se esconde el icono de cargando contenido
				$("#loadingContent").hide("slow");

			};

		},
	});



	$scope.getEndScroll = function(){

		if($scope.busy){
			return;
		};

		$scope.busy = true;		

		var librosPanel = document.getElementById("librosPanel");

		var libros = librosPanel.getElementsByClassName("libro");

		var idLibrosMostrados = []

		for (var i= 0; i<libros.length;i++){

			idLibrosMostrados.push(libros[i].id);

		}

		$.ajax({

			type:"get",

			url: urlMisLibrosOwner,

			data: {"idLibrosMostrados": JSON.stringify(idLibrosMostrados) },

			success: function(response){

				if(response.libros.length > 0){

					addDataToView(response);

					$scope.$apply(function(){

						$scope.busy = false;

					});
					
				}

				else{

					$scope.$apply(function(){

						$scope.busy = true;

					});

					$("#loadingContent").hide("slow");

				};
			},

		});

	}


	// Se agregan los datos  de los posteos a la pantalla
	function addDataToView(response){


		// Se obtienen las libros
		var libros = response.libros;

		// Se itera sobre cada libro

		// Se verifica si es que existen libros 
		if(libros.length>0){

			// Se itera sobre cada posteo
			for(var i=0;i<libros.length;i++){

				
				//Diccionario que se agrega a la lista posts de angular (del template) por cada posteo enviado por la vista index_view
				var postObject = {}; 

				// Cada poteo
				var libro = libros[i];

				// Se obtiene la libro en formato para ser usado por el temlpate libroAngularJS
				var postObject = informacionGeneralLibroService.getPostObject(libro);

				// Se agrega finalmente el objeto postObject a la lista posts (denomidada postsList en este archivo)
				$scope.$apply(function(){

					if(typeof $scope.postsList == "undefined"){

						$scope.postsList = [postObject];

					}else{

						$scope.postsList.push(postObject);

					};

				});

			};

		};

	};

});