

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase

"""
Configuración de la base de datos
"""

# CONFIGURACIÓN BASE DE DATOS

# crear motor de conexión a base de datos
engine = create_engine(
    "sqlite:///animelist.db",
    echo=True,
    connect_args={"check_same_thread": False}
)





# crear fábrica de sesiones de base de datos
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False
)



# MODELO BASE DE DATOS (sqlalchemy)

# clase base para modelos sqlalchemy
class Base(DeclarativeBase):
    pass


# DEPENDENCIA DE FASTAPI

def get_db():
    db = SessionLocal()
    try:
        yield db # entrega la sesión al endpoint
    finally:
        db.close()



# método inicializar con canciones por defecto
def init_db():
    """
    Inicializa la base de datos con canciones por defecto si está vacía.
    Sólo crea las canciones si no existen ya en la base de datos.
    """
    from app.models.user import UserORM
    from app.models.genre import GenreORM
    from app.models.anime import AnimeORM

    # crear todas las tablas
    Base.metadata.create_all(engine)


    db = SessionLocal()
    try:
        existing_user = db.execute(select(UserORM)).scalars().all()
        
        if existing_user:
            return
        
        default_genre = [
            GenreORM(name="Acción", description=""),
            GenreORM(name="Aventura", description=""),
            GenreORM(name="Comedia", description=""),
            GenreORM(name="Drama", description=""),
            GenreORM(name="Ecchi", description=""),
            GenreORM(name="Fantasía", description=""),
            GenreORM(name="Terror", description=""),
            GenreORM(name="Mahou Shoujo", description=""),
            GenreORM(name="Mecha", description=""),
            GenreORM(name="Música", description=""),
            GenreORM(name="Misterio", description=""),
            GenreORM(name="Psicología", description=""),
            GenreORM(name="Romance", description=""),
            GenreORM(name="Ciencia ficción", description=""),
            GenreORM(name="Slice of life", description=""),
            GenreORM(name="Deportes", description=""),
            GenreORM(name="Sobrenatural", description=""),
            GenreORM(name="Suspense", description="")
        ]
        db.add_all(default_genre)
        db.commit()
        
        # get Genres by name
        genres = db.execute(select(GenreORM)).scalars().all()
        genre_dict = {genre.name: genre for genre in genres}

        for genre in genres:
            db.refresh(genre)

        # AnimeORM(name="", description="", num_caps="" , image="", genres=[genre_dict.get()])

        default_anime = [
            AnimeORM(name="Frieren", description="La aventura ha terminado, pero la vida continúa para una maga elfa que apenas comienza a comprender el significado de la vida. Frieren, la maga elfa, y sus valientes compañeros aventureros han derrotado al Rey Demonio y han traído la paz a la tierra. Pero Frieren sobrevivirá mucho tiempo al resto de su antiguo grupo. ¿Cómo comprenderá el significado de la vida para quienes la rodean? Décadas después de su victoria, el funeral de uno de sus amigos la enfrenta a su casi inmortalidad. Frieren se propone cumplir los últimos deseos de sus camaradas y se encuentra en una nueva aventura...", num_caps=28, image="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx154587-qQTzQnEJJ3oB.jpg" , genres=[genre_dict.get("Aventura"), genre_dict.get("Fantasía")], color="#94ffa9"),
            AnimeORM(name="Gachiakuta", description="Un niño vive en un pueblo flotante, donde los pobres sobreviven y los ricos viven una vida suntuosa, simplemente arrojando su basura al abismo. Sin embargo, cuando es acusado falsamente de asesinato, su condena injusta lo lleva a un castigo inimaginable: el exilio al borde del abismo, junto con el resto de la basura. En la superficie, los desechos de la humanidad han engendrado monstruos feroces, y para recorrer el camino de la venganza contra quienes lo arrojaron al Infierno, un niño tendrá que convertirse en un guerrero...", num_caps="24" , image="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx178025-cWJKEsZynkil.jpg", genres=[genre_dict.get("Acción"), genre_dict.get("Drama"), genre_dict.get("Fantasía")], color="#ebb62d"),
            AnimeORM(name="Chainsaw man", description="Denji es un adolescente que vive con Pochita, un demonio motosierra. Debido a la deuda que le dejó su padre, ha estado viviendo en la miseria, pagando su deuda recolectando cadáveres demoníacos con Pochita. Un día, Denji es traicionado y asesinado. Al desvanecerse, hace un contrato con Pochita y revive como 'Chainsaw Man', un hombre con corazón de demonio.", num_caps="12" , image="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx127230-DdP4vAdssLoz.png", genres=[genre_dict.get("Acción"), genre_dict.get("Drama"), genre_dict.get("Terror"), genre_dict.get("Sobrenatural")], color="#8a2c0f"),
            AnimeORM(name="i", description="La aventura ha terminado, pero la vida continúa para una maga elfa que apenas comienza a comprender el significado de la vida. Frieren, la maga elfa, y sus valientes compañeros aventureros han derrotado al Rey Demonio y han traído la paz a la tierra. Pero Frieren sobrevivirá mucho tiempo al resto de su antiguo grupo. ¿Cómo comprenderá el significado de la vida para quienes la rodean? Décadas después de su victoria, el funeral de uno de sus amigos la enfrenta a su casi inmortalidad. Frieren se propone cumplir los últimos deseos de sus camaradas y se encuentra en una nueva aventura...", num_caps=28, image="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx154587-qQTzQnEJJ3oB.jpg" , genres=[genre_dict.get("Aventura"), genre_dict.get("Fantasía")], color="#94ffa9"),
            AnimeORM(name="ii", description="Un niño vive en un pueblo flotante, donde los pobres sobreviven y los ricos viven una vida suntuosa, simplemente arrojando su basura al abismo. Sin embargo, cuando es acusado falsamente de asesinato, su condena injusta lo lleva a un castigo inimaginable: el exilio al borde del abismo, junto con el resto de la basura. En la superficie, los desechos de la humanidad han engendrado monstruos feroces, y para recorrer el camino de la venganza contra quienes lo arrojaron al Infierno, un niño tendrá que convertirse en un guerrero...", num_caps="24" , image="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx178025-cWJKEsZynkil.jpg", genres=[genre_dict.get("Acción"), genre_dict.get("Drama"), genre_dict.get("Fantasía")], color="#ebb62d"),
            AnimeORM(name="iii", description="Denji es un adolescente que vive con Pochita, un demonio motosierra. Debido a la deuda que le dejó su padre, ha estado viviendo en la miseria, pagando su deuda recolectando cadáveres demoníacos con Pochita. Un día, Denji es traicionado y asesinado. Al desvanecerse, hace un contrato con Pochita y revive como 'Chainsaw Man', un hombre con corazón de demonio.", num_caps="12" , image="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx127230-DdP4vAdssLoz.png", genres=[genre_dict.get("Acción"), genre_dict.get("Drama"), genre_dict.get("Terror"), genre_dict.get("Sobrenatural")], color="#8a2c0f")
        ]

        db.add_all(default_anime)
        db.commit()

        default_user = [
            UserORM(user_name="Admin", email="1234@gmail.com", password_hash="ASDJOASJDKJASJD")
        ]
        
        # agregar las canciones
        db.add_all(default_user)
        db.commit()
    finally:
        db.close()