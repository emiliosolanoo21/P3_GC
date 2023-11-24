
class Obj(object):
    def __init__(self, filename):
        # Asumiendo que el archivo es un formato .obj
        with open(filename,"r") as file:
            self.lines = file.read().splitlines()

        # Se crean los contenedores de los datos del modelo.
        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        # Por cada l�nea en el archivo
        for line in self.lines:
            # Si la l�nea no cuenta con un prefijo y un valor,
            # seguimos a la siguiente l�nea
            try:
                prefix, value = line.split(" ", 1)
                value = value.lstrip(" ").rstrip(" ")
            except:
                continue

            # Dependiendo del prefijo, parseamos y guardamos la informaci�n
            # en el contenedor correcto

            if prefix == "v": # Vertices
                self.vertices.append( list(map(float, value.split(" "))) )
            elif prefix == "vt": # Texture Coordinates
                self.texcoords.append( list(map(float, value.split(" "))) )
            elif prefix == "vn": # Normals
                self.normals.append( list(map(float, value.split(" "))) )
            elif prefix == "f": # Faces
                self.faces.append([list(map(int, vert.split("/"))) for vert in value.split(" ") ] )

    
