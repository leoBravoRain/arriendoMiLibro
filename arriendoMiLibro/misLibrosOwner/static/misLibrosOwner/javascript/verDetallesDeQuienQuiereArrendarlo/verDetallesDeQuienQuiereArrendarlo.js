$(document).ready(function(){

	// Evento para manejar inicio de periodo de arriendo de libro
	$(".iniciarPeriodoDeArriendo").click(function(){

		// // Confirmar que desea iniciar periodo de arriendo
		// var confirmar = confirm("¿Estás seguro que quieres inicar el periodo de arriendo?");

		// // Si confirma
		// if(confirmar){

		var idLibro = this.id;

		// Llamado ajax
		$.ajax({

			type: "GET",
			url: urlIniciarPeriodoDeArriendo,
			data: {"idLibro": idLibro},
			success: function(response){

				// Si respuesta fue correcta
				if(response.success){

					// redireccionar hacia template
					location.assign(urlMisLibrosOwner);
					
				};

			},

		});

		// }

		// // Si no confirma
		// else{

		// };


	});

});