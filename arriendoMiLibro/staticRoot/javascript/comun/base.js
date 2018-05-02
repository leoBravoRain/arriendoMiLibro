$(document).ready(function(){

	// Se usa para que funcione en celulares (Ios) el menu desplegable de la barra de navegacion
	$('.dropdown-toggle').click(function(e) {

		e.preventDefault();

		setTimeout($.proxy(function() {

			if ('ontouchstart' in document.documentElement) {

				$(this).siblings('.dropdown-backdrop').off().remove();

			}

		}, this), 0);

	});

	// funcion para buscar amigos o empresas en buscador para cuando se apreta ENTER en el buscador 

	$(".searchEngine").keyup(function(event){

		// Si se apreta ETNER
		if(event.which == 13){

			// Se toma el texto introcudicto por usuario
			var search = this.value;

			// Se redirige hacia otra url
			window.location.assign(urlSearchResult + search);

		};
	});

	// Funcion para activar popover de las notificaciones
	$('[data-toggle=popover]').popover({ 

		html: true,
		placement: "bottom",
		container: 'body',
		content: function() {

			return $("#divNotificationsApp").html();

		},

	});

});
