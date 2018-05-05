from PIL import Image

# Funcion para rotar imagens si provienen de iOs (ya que por defecto se rotan en PC, pero en cellphones no aparecen rotadas)
def imageAutorotate(foto):

    with Image.open(foto) as image:
        file_format = image.format
        exif = image._getexif()

        # image.thumbnail((1667, 1250), resample=Image.ANTIALIAS)

        # if image has exif data about orientation, let's rotate it
        orientation_key = 274 # cf ExifTags
        if exif and orientation_key in exif:
            orientation = exif[orientation_key]

            rotate_values = {
                3: Image.ROTATE_180,
                6: Image.ROTATE_270,
                8: Image.ROTATE_90
            }

            if orientation in rotate_values:
                image = image.transpose(rotate_values[orientation])

        image.save(foto.path, file_format)