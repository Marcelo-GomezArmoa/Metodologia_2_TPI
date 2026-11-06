from sqlmodel import SQLModel, create_engine, Session

# Configuración de conexión para PostgreSQL
DATABASE_URL = "postgresql://postgres:Euge1002@localhost:5432/utn_solicitudes_db"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session