-- El proyecto aun no tiene un nombre --


La aplicación es una mejora de animelist donde un usuario crea su cuenta y en esta guarda y crea una lista de animes que ha visto donde puede ponerle nota y comentario 


MODELS:

- usuarios: HECHO
    - nombre usuario
    - email 
    - contraseña hash
    - descripcion personal | None
    - imagen usuario | None
    - created_at

- usuario_amigos (tabla intermedia): HECHO
    - user_id
    - friend_id
    - estado (pendiente, aceptado)
    - fecha

- user_actor_doblaje (tabla intermedia): HECHO
    - user_id
    - actor_id

- animes: HECHO
    - nombre anime
    - descripcion
    - mumero capitulos
    - imagen portada


- anime_genero (tabla intermedia): DONE
    - anime_id
    - genero_id

- anime actores de doblaje(tabla intermedia entre animes y actores):  DONE
    - anime_id FK
    - actor_id FK
    - personaje
    - idioma

- lita_anime (tabla intermedia entre usuarios y animes): DONE
    - user_id FK
    - anime_id FK
    - comentario 
    - fecha de inicio
    - fecha terminado
    - estado (viendo, completado, dropeado, lo vere)
    - puntuacion

- genero: DONE
    - nombre
    - descripcion

- actor_doblaje: DONE
    - nombre
    - descripcion
    - imagen

