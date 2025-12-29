

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

    # crear todas las tablas
    Base.metadata.create_all(engine)


    db = SessionLocal()
    try:
        existing_user = db.execute(select(UserORM)).scalars().all()
        
        if existing_user:
            return
        
        default_user = [
            UserORM(user_name="Admin", email="1234@gmail.com", password_hash="ASDJOASJDKJASJD")
        ]
        
        # agregar las canciones
        db.add_all(default_user)
        db.commit()
    finally:
        db.close()