# DoggyLovy

## Documentación y ayuda:
- [Flask]
- [Aprende GIT ahora! curso completo GRATIS desde cero]
   
## Instalación

python y git
- https://www.python.org/
- https://git-scm.com/

Crear una carpeta donde va a estar el proyecto.

Abrir una terminal, colocarse en la carpeta creada y clonar el proyecto con el sig. comando:
```
git clone https://github.com/AniquinSky/DoggyLovy.git
```

Moverse a la carpeta del proyecto clonado
```
cd DoggyLovy
```

Cambiar la rama de git a develop:
```
git switch develop
```
Crear un entorno vortual de python y activarlo:
```
py -3 -m venv .venv
```
Activar el entorno:
```
.venv\Scripts\activate
```

Ya dentro del entorno instalamos flask y dependencias:
```
pip install Flask psycopg2-binary 
```

Levantar ambiente :
> el parámetro --debug puede ser omitido
```
flask --app flaskr run --debug
```
> Para detener el servidor usar `Control + C` en la terminal

> Para salir del ambiente virtual usar el comando: `.venv\Scripts\deactivate`

## Levantar Servidor
```
.venv\Scripts\activate
flask --app flaskr run --debug
```

[Aprende GIT ahora! curso completo GRATIS desde cero]: https://www.youtube.com/watch?v=VdGzPZ31ts8
[Flask]: https://flask.palletsprojects.com/en/3.0.x/
