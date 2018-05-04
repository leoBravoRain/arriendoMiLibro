posts.service('informacionDetalladaLibroService', function(){

  // funcion que crea el postObject
  this.getLibroObject = function(libro, owner, usuarioLogueadoId, ciudad) { 

    // Datos generaes del libro

    // Se obtiene id de Libro
    var id = libro.pk;

    // Se obtiene titulo de Libro
    var titulo = libro.fields.titulo;

    // Se obtiene autor de Libro
    var autor = libro.fields.autor;

    // Se obtiene resumen
    var resumen = libro.fields.resumen;

    // Se obtiene foto de Libro
    var foto = urlMedia + libro.fields.foto;    

    // Se obtiene fechaCreacion de Libro
    var fechaCreacion = libro.fields.fechaCreacion;

    // Nombre owner

    var nombreOwner = owner.fields.nombre;

    // Foto de owner 
    var fotoOwner = urlMedia + owner.fields.foto;

    // Se obtiene comentario del libro del dueño de libro
    var comentario = libro.fields.comentario;

    // Ciudad de owner
    var ciudad = ciudad.fields.nombre;

    // Datos asociados a como se muestra el libro

    // variable para setear si es arrendatario
    var esArrendatario = false;

    // Si el que carga es arrendatario
    if(fuente == "arrendatario"){

        esArrendatario = true;

        var urlArrendarLibroConId = urlArrendarLibro + id;

    }   

    // Si es owner
    else if(fuente == "owner"){

        // Variable para editar info de libro
        var editarInformacionDeLibro = false;

        // Url para editar libro
        var urlEditarLibroAngular = urlEditarLibro;

        // Url para elimianr libro
        var urlEliminarLibroAngular = urlEliminarLibro;

        // Se obtiene estado de Libro
        var estado = libro.fields.estado;

        // Si owner es dueño de libro
        if(usuarioLogueadoId == owner.pk){

            // Variable para editar info de libro
            editarInformacionDeLibro = true;

        };


        // Cambiar estado de libro
        // var cambiarEstado = urlCambiarEstadoDeLibro + id;
        

    };
    
    // Si es arrendatario
    if(esArrendatario){

        // Se crea la Libro
        var postObject = {"comentario": comentario, "resumen": resumen, "urlArrendarLibro":urlArrendarLibroConId,"esArrendatario":esArrendatario,"foto": foto,"autor": autor, "id":id,"titulo":titulo};
        postObject["nombreOwner"] = nombreOwner;
        postObject["fotoOwner"] = fotoOwner;
        postObject["ciudad"] = ciudad;

    }

    // Si es owner
    else{

        // Se crea la Libro
        var postObject = {"comentario": comentario,"resumen":resumen,"esArrendatario":esArrendatario, "foto": foto,"autor": autor, "id":id,"titulo":titulo,"estado":estado};
        postObject["nombreOwner"] = nombreOwner;
        postObject["fotoOwner"] = fotoOwner;
        postObject["editarInformacionDeLibro"] = editarInformacionDeLibro;
        postObject["urlEditarLibro"] = urlEditarLibroAngular;
        postObject["urlEliminarLibro"] = urlEliminarLibroAngular;
        postObject["ciudad"] = ciudad;
    };

    // Se crea el postObject el que finalmente se agregará a la lista de posteos del template

    return postObject;

  };  

});