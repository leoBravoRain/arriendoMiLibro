$(document).ready(function(){

	// Evento para manejar inicio de periodo de arriendo de libro
	$(".terminarPeriodoDeArriendo").click(function(){

		// Confirmar que desea iniciar periodo de arriendo
		// var confirmar = confirm("¿Estás seguro que quieres terminar el periodo de arriendo?");


		// Si confirma
		// if(confirmar){

		var idLibro = this.id;


		// Llamado ajax
		$.ajax({

			type: "POST",
			url: urlTerminarPeriodoDeArriendo,
			data: {"idLibro": idLibro},
			success: function(response){

				// Si respuesta fue exitosa
				if(response.success){

					// redireccion hacia mis libros
					location.assign(urlMisLibrosOwner);

				};

			},

		});

		// }

		// Si no confirma
		// else{

		// };


	});

});