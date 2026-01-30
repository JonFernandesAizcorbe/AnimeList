

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.security.passwords import hash_password


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
    from app.models.anime_list import AnimeListORM  

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

        # AnimeORM(name="", studio="", description="", num_caps="" , image="", banner="", genres=[genre_dict.get()])

        default_anime = [
            AnimeORM(name="Frieren", studio="MADHOUSE", description="La aventura ha terminado, pero la vida continúa para una maga elfa que apenas comienza a comprender el significado de la vida. Frieren, la maga elfa, y sus valientes compañeros aventureros han derrotado al Rey Demonio y han traído la paz a la tierra. Pero Frieren sobrevivirá mucho tiempo al resto de su antiguo grupo. ¿Cómo comprenderá el significado de la vida para quienes la rodean? Décadas después de su victoria, el funeral de uno de sus amigos la enfrenta a su casi inmortalidad. Frieren se propone cumplir los últimos deseos de sus camaradas y se encuentra en una nueva aventura...", num_caps=28, image="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx154587-qQTzQnEJJ3oB.jpg", banner="https://s4.anilist.co/file/anilistcdn/media/anime/banner/154587-ivXNJ23SM1xB.jpg" , genres=[genre_dict.get("Aventura"), genre_dict.get("Fantasía")], color="#94ffa9"),
            AnimeORM(name="Gachiakuta", studio="STUDIO BONES ", description="Un niño vive en un pueblo flotante, donde los pobres sobreviven y los ricos viven una vida suntuosa, simplemente arrojando su basura al abismo. Sin embargo, cuando es acusado falsamente de asesinato, su condena injusta lo lleva a un castigo inimaginable: el exilio al borde del abismo, junto con el resto de la basura. En la superficie, los desechos de la humanidad han engendrado monstruos feroces, y para recorrer el camino de la venganza contra quienes lo arrojaron al Infierno, un niño tendrá que convertirse en un guerrero...", num_caps=24 , image="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx178025-cWJKEsZynkil.jpg", banner="https://s4.anilist.co/file/anilistcdn/media/anime/banner/178025-WvcXi1J2SGRa.jpg", genres=[genre_dict.get("Acción"), genre_dict.get("Drama"), genre_dict.get("Fantasía")], color="#ebb62d"),
            AnimeORM(name="Chainsaw man", studio="MAPPA", description="Denji es un adolescente que vive con Pochita, un demonio motosierra. Debido a la deuda que le dejó su padre, ha estado viviendo en la miseria, pagando su deuda recolectando cadáveres demoníacos con Pochita. Un día, Denji es traicionado y asesinado. Al desvanecerse, hace un contrato con Pochita y revive como 'Chainsaw Man', un hombre con corazón de demonio.", num_caps=12 , image="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx127230-DdP4vAdssLoz.png", banner="https://s4.anilist.co/file/anilistcdn/media/anime/banner/127230-o8IRwCGVr9KW.jpg", genres=[genre_dict.get("Acción"), genre_dict.get("Drama"), genre_dict.get("Terror"), genre_dict.get("Sobrenatural")], color="#8a2c0f"),
            AnimeORM(name="Re:Zero kara Hajimeru Isekai Seikatsu ", studio="WHITE FOX", description="En la historia, Subaru Natsuki es un estudiante ordinario de secundaria que está perdido en un mundo alternativo, donde es rescatado por una hermosa niña de pelo plateado. Él se queda cerca de ella para devolver el favor, pero el destino con el que está cargada es más de lo que Subaru puede imaginar. Los enemigos atacan uno por uno, y ambos son asesinados. Entonces descubre que tiene el poder de rebobinar la muerte, de vuelta a la época en que llegó por primera vez a este mundo. Pero solo él recuerda lo que ha sucedido desde entonces.", num_caps=25, image="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx189046-wHJEsaV5gzZB.jpg", banner="https://s4.anilist.co/file/anilistcdn/media/anime/banner/21355-f9SjOfEJMk5P.jpg" , genres=[genre_dict.get("Acción"), genre_dict.get("Aventura"), genre_dict.get("Drama")], color="#e34f85"),
            AnimeORM(name="Shangri-La Frontier", studio="C2C", description="'¿Cuándo fue la última vez que jugué un juego que no era una mierda?' Este es un mundo en el futuro cercano donde los juegos que utilizan pantallas de visualización se clasifican como retro. Cualquier cosa que no pueda seguir el ritmo de la tecnología de realidad virtual de última generación se llama un 'juego de mierda', y se ve un gran número de juegos de mierda que salen. Aquellos que dedican sus vidas a limpiar estos juegos se llaman 'cazadores de juegos de mierda', y Rakuro Hizutome es uno de ellos. El juego que ha elegido para abordar a continuación es Shangri-La Frontier, un 'juego de buen nivel' que tiene un total de treinta millones de jugadores. Amigos en línea... Un mundo expansivo... Encuentros con rivales... ¡Estos están cambiando el destino de Rakuro y todos los demás jugadores! ¡El mejor cuento de aventuras de juego del jugador más fuerte de 'juego de mierda' comienza ahora!", num_caps=25 , image="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx151970-xtIx3VqEk02X.jpg", banner="https://s4.anilist.co/file/anilistcdn/media/anime/banner/151970-Tnnfp0f7NOzj.jpg", genres=[genre_dict.get("Acción"), genre_dict.get("Aventura"), genre_dict.get("Comedia")], color="#6ec8f2"),
            AnimeORM(name="Mob Psycho 100 ", studio="STUDIO BONES", description="La historia gira en torno a 'Mob', un niño que explotará si su capacidad emocional alcanza el 100%. Este chico con poderes psíquicos se ganó su apodo de 'Mafia' porque no se destaca entre otras personas. Mantiene sus poderes psíquicos embotellados para que pueda vivir normalmente, pero si su nivel emocional alcanza los 100, algo abrumará a todo su cuerpo.", num_caps=12 , image="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx21507-6YUSbh2m0N1p.jpg", banner="https://s4.anilist.co/file/anilistcdn/media/anime/banner/21507-Qx8bGsLXUgLo.jpg", genres=[genre_dict.get("Acción"), genre_dict.get("Comedia"), genre_dict.get("Drama"), genre_dict.get("Sobrenatural")], color="#f25226"),
            AnimeORM(name="Kusuriya no Hitorigoto ", studio="OLM", description="Maomao vivió una vida pacífica con su padre boticario. Hasta que un día, se vende como humilde sirviente al palacio del emperador. Pero ella no estaba destinada a una vida obediente entre la realeza. Así que cuando los herederos imperiales se enferman, ella decide intervenir y encontrar una cura. Esto llama la atención de Jinshi, un apuesto funcionario del palacio que la promueve. ¡Ahora se está haciendo un nombre para sí misma resolviendo misterios médicos!", num_caps=24, image="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx161645-QLbzHXiYRgV2.jpg", banner="https://s4.anilist.co/file/anilistcdn/media/anime/banner/161645-oqzTZYIvviWI.jpg", genres=[genre_dict.get("Drama"), genre_dict.get("Misterio")], color="#ef5d5d"),
            AnimeORM(name="Jujutsu Kaisen ", studio="MAPPA", description="Un niño lucha... por 'la muerte correcta'.Dificultades, arrepentimiento, vergüenza: los sentimientos negativos que los humanos sienten se convierten en Maldiciones que acechan en nuestra vida cotidiana. Las Maldiciones corren desenfrenadas por todo el mundo, capaces de llevar a la gente a una terrible desgracia e incluso a la muerte. Además, las Maldiciones solo pueden ser exorcizadas por otra Maldición.Itadori Yuji es un niño con una tremenda fuerza física, aunque vive una vida de escuela secundaria completamente ordinaria. Un día, para salvar a un amigo que ha sido atacado por las Maldiciones, se come el dedo del Espectro de Doble Cara, llevando la Maldición a su propia alma. A partir de entonces, comparte un cuerpo con el espectro de doble cara. Guiado por el más poderoso de los brujos, Gojou Satoru, Itadori es admitido en la Escuela Técnica Técnica de Brujería de Tokio, una organización que lucha contra las Maldiciones... y así comienza la historia heroica de un niño que se convirtió en una Maldición para exorcizar una Maldición, una vida de la que nunca podría volver atrás.", num_caps=24 , image="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx113415-LHBAeoZDIsnF.jpg",banner="https://s4.anilist.co/file/anilistcdn/media/anime/banner/113415-jQBSkxWAAk83.jpg", genres=[genre_dict.get("Acción"), genre_dict.get("Drama"), genre_dict.get("Sobrenatural")], color="#ef5d5d"),
            AnimeORM(name="HUNTER×HUNTER", studio="MADHOUSE", description="Una nueva adaptación del manga del mismo nombre de Togashi Yoshihiro. Un cazador es aquel que viaja por el mundo haciendo todo tipo de tareas peligrosas. Desde la captura de criminales hasta la búsqueda en lo profundo de tierras desconocidas para cualquier tesoro perdido. Gon es un niño cuyo padre desapareció hace mucho tiempo, siendo un cazador. Él cree que si también pudiera seguir el camino de su padre, algún día podría reunirse con él. Después de cumplir 12 años, Gon abandona su casa y asume la tarea de ingresar al examen Hunter, conocido por su baja tasa de éxito y alta probabilidad de muerte para convertirse en un cazador oficial. Se hace amigo de la Kurapika impulsada por la venganza, el futuro médico Leorio y el rebelde ex asesino Killua en el examen, con su amistad prevaleciendo a lo largo de los muchos juicios y amenazas que vienen al asumir la peligrosa carrera de un cazador.", num_caps=148 , image="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx11061-y5gsT1hoHuHw.png", banner="https://s4.anilist.co/file/anilistcdn/media/anime/banner/11061-8WkkTZ6duKpq.jpg", genres=[genre_dict.get("Acción"), genre_dict.get("Aventura"), genre_dict.get("Fantasía")], color="#fff280"),
            AnimeORM(name="Summer Time Render ", studio="OLM", description="Una historia de ciencia ficción y verano llena de suspenso ambientada en una pequeña isla con Shinpei Aijiro, cuyo amigo de la infancia Ushio Kofune murió. Él regresa a su ciudad natal por primera vez en dos años para el funeral. Sou Hishigata, su mejor amigo, sospecha que algo está mal con la muerte de Ushio, y que alguien puede morir después. Un siniestro presagio se escucha cuando toda una familia de al lado desaparece repentinamente al día siguiente. Además, Mio implica una 'sombra' tres días antes de la muerte de Ushio.", num_caps=25, image="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx129201-HJBauga2be8I.png", banner="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx129201-HJBauga2be8I.png", genres=[genre_dict.get("Acción"), genre_dict.get("Drama"), genre_dict.get("Misterio")], color="#3480ea"),
            AnimeORM(name="BLEACH", studio="Studio Pierrot", description="Ichigo Kurosaki es un estudiante de secundaria bastante normal, aparte del hecho de que tiene la capacidad de ver fantasmas. Esta habilidad nunca impactó su vida de una manera importante hasta el día en que se encuentra con el Shinigami Kuchiki Rukia, quien lo salva a él y a la vida de su familia de un Hollow, un espíritu corrupto que devora las almas humanas. Herido durante la lucha contra el Hollow, Rukia elige la única opción disponible para derrotar al monstruo y pasa sus poderes Shinigami a Ichigo. Ahora obligado a actuar como un sustituto hasta que Rukia se recupera, Ichigo caza a los Hollows que plagan su ciudad.", num_caps=366 , image="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx269-d2GmRkJbMopq.png", banner="https://s4.anilist.co/file/anilistcdn/media/anime/banner/269-08ar2HJOUAuL.jpg", genres=[genre_dict.get("Acción"), genre_dict.get("Aventura"), genre_dict.get("Sobrenatural")], color="#ebb62d"),
            AnimeORM(name="NARUTO ", studio="Studio Pierrot", description="Naruto Uzumaki, un ninja hiperactivo y con cabeza de nudillo, vive en Konohagakure, el pueblo de Hojas Ocultas. Momentos antes de su nacimiento, un enorme demonio conocido como el Kyuubi, el Zorro de Nueve colas, atacó a Konohagakure y causó estragos. Para poner fin al alboroto de los Kyuubi, el líder de la aldea, el 4o Hokage, sacrificó su vida y selló a la monstruosa bestia dentro del recién nacido Naruto. Rechazado por la presencia de los Kyuubi dentro de él, Naruto lucha por encontrar su lugar en el pueblo. Se esfuerza por convertirse en el Hokage de Konohagakure, y se encuentra con muchos amigos y enemigos en el camino.", num_caps=220 , image="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx20-dE6UHbFFg1A5.jpg", banner="https://s4.anilist.co/file/anilistcdn/media/anime/banner/20-HHxhPj5JD13a.jpg", genres=[genre_dict.get("Acción"), genre_dict.get("Aventura"), genre_dict.get("Comedia"), genre_dict.get("Drama")], color="#ef5d5d"),
            AnimeORM(name="Dandadan ", studio="Science SARU ", description="Esta es una historia sobre Momo, una chica de secundaria que proviene de una familia de médiums espirituales, y su compañero de clase Okarun, un fanático de la ocultidad. Después de que Momo rescata a Okarun de ser acosado, comienzan a hablar. Sin embargo, se produce una discusión entre ellos, ya que Momo cree en fantasmas, pero niega que los alienígenas existen, y Okarun cree en los extraterrestres, pero niega que los fantasmas existen. Para demostrar el uno al otro en lo que creen que es real, Momo va a un hospital abandonado donde se ha visto un OVNI y Okarun va a un túnel que se rumorea que está embrujado. Para su sorpresa, cada uno de ellos se encuentra con actividades paranormales abrumadoras que trascienden la comprensión. En medio de estos predicamentos, Momo despierta su poder oculto y Okarun gana el poder de una maldición para superar estos nuevos peligros! Su amor fatídico también comienza!? ¡La historia de la batalla oculta y la adolescencia comienza!", num_caps=12 , image="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx171018-60q1B6GK2Ghb.jpg", banner="https://s4.anilist.co/file/anilistcdn/media/anime/banner/171018-SpwPNAduszXl.jpg", genres=[genre_dict.get("Acción"), genre_dict.get("Comedia"), genre_dict.get("Drama")], color="#ef5d5d"),
            AnimeORM(name="Bocchi the Rock!", studio="CloverWorks", description="Hitori Gotou, “Bocchi-chan”, es una chica que es tan introvertida y tímida con la gente que siempre comenzaría sus conversaciones con “Ah...” Durante sus años de secundaria, comenzó a tocar la guitarra, queriendo unirse a una banda porque pensó que podría ser una oportunidad para que incluso alguien tímido como ella también brille. Pero como no tenía amigos, terminó practicando la guitarra durante seis horas todos los días sola. Después de convertirse en una guitarrista experta, subió videos de sí misma tocando la guitarra a Internet bajo el nombre de “Guitar Hero” y fantaseó con actuar en el concierto del festival cultural de su escuela. Pero no solo no pudo encontrar ningún compañero de banda, antes de darse cuenta, ¡ella estaba en la escuela secundaria y todavía no podía hacer un solo amigo! Estaba muy cerca de convertirse en una encerrada, pero un día, Nijika Ijichi, la batería de Kessoku Band, se acercó a ella. Y por eso, su vida cotidiana comenzó a cambiar poco a poco...", num_caps=12 , image="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx130003-HTDmeL4RGeJ4.png", banner="https://s4.anilist.co/file/anilistcdn/media/anime/banner/130003-FEBlngeJSTEm.jpg", genres=[genre_dict.get("Comedia"), genre_dict.get("Música"), genre_dict.get("Slice of life")], color="#ebb62d")
        ]

        db.add_all(default_anime)
        db.commit()


        password_admin = "admin"
        password_user1 = "user1"
        password_user2 = "user2"
        pwd = hash_password(password_admin)
        pwd1 = hash_password(password_user1)
        pwd2 = hash_password(password_user2)

        default_user = [
            UserORM(user_name="admin", email="1234@gmail.com", password_hash=pwd),
            UserORM(user_name="user1", email="user1@gmail.com", password_hash=pwd1),
            UserORM(user_name="user2", email="user2@gmail.com", password_hash=pwd2)
        ]
        
        # agregar usuarios
        db.add_all(default_user)
        db.commit()

        default_anime_list = [
            AnimeListORM(user_id=1, anime_id=1, score=100),
            AnimeListORM(user_id=2, anime_id=1, score=75),
            AnimeListORM(user_id=3, anime_id=1, score=1),
            AnimeListORM(user_id=1, anime_id=2, score=10),
            AnimeListORM(user_id=2, anime_id=2, score=50),
            AnimeListORM(user_id=3, anime_id=2, score=55)

        ]

        db.add_all(default_anime_list)
        db.commit()

    finally:
        db.close()

