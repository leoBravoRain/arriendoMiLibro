posts.service('informacionGeneralLibroService', function(){


  // funcion que crea el postObject
  this.getPostObject = function(libro) { 

    // Se obtiene id de Libro
    var id = libro.pk;

    // Se obtiene titulo de Libro
    var titulo = libro.fields.titulo;

    // Se obtiene autor de Libro
    var autor = libro.fields.autor;

    // Se obtiene foto de Libro
    var foto = urlMedia + libro.fields.foto;    

    // Se obtiene fechaCreacion de Libro
    var fechaCreacion = libro.fields.fechaCreacion;

    // url para ver detalles del libro
    var urlDetalleslibroConId = urlDetallesLibro + id;

    // variable para setear si es arrendatario
    var esArrendatario = false;

    // Si el que carga es arrendatario
    if(fuente == "arrendatario"){

        esArrendatario = true;


    }   

    // Si es owner
    else if(fuente == "owner"){

        // Se obtiene estado de Libro
        var estado = libro.fields.estado;

        // estado leible que se muestra en la pagina
        var estadoLeible = "Disponible";

        // variable para setear si libro lo quieren arrendar
        // var quierenArrendarElLibro = false;

        // Si estado es que quieren arrendarlo
        if(estado == "quierenArrendarlo"){

            estadoLeible = "Alguien quiere arrendarlo";

            // url para ver detalles de quien quiere arrendar
            var urlDetallesDeArriendo = urlDetallesDeQuienQuiereArrendarlo + id;

            // Texto para mostrar
            var textoParaRedirigirHaciaSituacionDeArriendo = "Ver quien quiere arrendarlo";
            
        }

        // Si es que estado es Arrendado
        else if(estado == "arrendado"){

            estadoLeible = "Arrendado";

            // url para ver detalles de arriendo
            var urlDetallesDeArriendo = urlDetallesDeArriendoDeLibro + id;

            // Texto para mostrar
            var textoParaRedirigirHaciaSituacionDeArriendo = "Ver detalles del arriendo";

        };

    };
    
    // Si es arrendatario
    if(esArrendatario){

        // Se crea la Libro
        var postObject = {"urlDetalleslibro":urlDetalleslibroConId,"esArrendatario":esArrendatario,"foto": foto,"autor": autor, "id":id,"titulo":titulo};

    }

    // Si es owner
    else{

        // Se crea la Libro
        var postObject = {"urlDetalleslibro":urlDetalleslibroConId,"esArrendatario":esArrendatario, "foto": foto,"autor": autor, "id":id,"titulo":titulo,"estado":estadoLeible};
        
        postObject["urlDetallesDeArriendo"] = urlDetallesDeArriendo;
        postObject["textoParaRedirigirHaciaSituacionDeArriendo"] = textoParaRedirigirHaciaSituacionDeArriendo;

    };

    // Se crea el postObject el que finalmente se agregará a la lista de posteos del template

    return postObject;

  };  

});