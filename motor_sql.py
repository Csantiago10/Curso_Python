import uuid
# Importamos las herramientas de construcción de SQLAlchemy
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Crear la Base (El Molde Maestro)
# Todas nuestras clases heredarán de aquí para que SQLAlchemy sepa que son tablas.
Base = declarative_base()

# 2. Definir el Modelo (Tu clase Libro transformada)
class LibroSQL(Base):
    __tablename__ = 'libros' # Nombre de la tabla en la base de datos

    # Definimos las COLUMNAS (Ya no son simples atributos)
    id = Column(String, primary_key=True) # La llave maestra
    nombre = Column(String)
    categoria = Column(String)
    autor = Column(String)
    editorial = Column(String)
    paginas = Column(Integer)
    cantidad = Column(Integer)

    # El constructor es opcional en SQLAlchemy, pero útil para generar el ID automático
    def __init__(self, nombre, categoria, autor, editorial, paginas, cantidad):
        self.id = str(uuid.uuid4()) # Generamos el UUID aquí
        self.nombre = nombre
        self.categoria = categoria
        self.autor = autor
        self.editorial = editorial
        self.paginas = paginas
        self.cantidad = cantidad

    def __repr__(self):
        # Esto es solo para que al imprimir el objeto se vea bonito en consola
        return f"<Libro(nombre='{self.nombre}', editorial='{self.editorial}')>"

# 3. Conectar el Motor (Engine)
# 'sqlite:///biblioteca.sqlite' significa: Crea un archivo local llamado biblioteca.sqlite
motor = create_engine('sqlite:///biblioteca.sqlite', echo=True) 
# echo=True hará que veas en consola el SQL real que Python escribe por ti (¡Magia!)

# 4. Crear las Tablas
# Esta línea le dice a la base de datos: "Si no existen las tablas, créalas ya".
Base.metadata.create_all(motor)

# 5. Crear la Sesión (El Gestor)
# La sesión es tu "mano" para meter y sacar datos.
Session = sessionmaker(bind=motor)
session = Session()

print("\n🚀 ¡Base de Datos SQL inicializada correctamente!\n")

# --- PRUEBA: INSERTAR UN LIBRO (CREATE) ---
print("--- Insertando un libro ---")
nuevo_libro = LibroSQL("Cien Años de Soledad", "Novela", "Gabo", "Sudamericana", 400, 10)

# A. Añadir a la zona de espera (Staging)
session.add(nuevo_libro)

# B. Confirmar la transacción (Commit) -> Aquí es cuando se guarda en el disco
session.commit() 

print(f"Libro guardado con ID: {nuevo_libro.id}")

# --- PRUEBA: LEER UN LIBRO (READ) ---
print("\n--- Consultando la base de datos ---")
# Traducido: SELECT * FROM libros WHERE nombre = 'Cien Años de Soledad'
libro_encontrado = session.query(LibroSQL).filter_by(nombre="Cien Años de Soledad").first()

if libro_encontrado:
    print(f"¡Encontrado! {libro_encontrado.nombre} - Stock: {libro_encontrado.cantidad}")
else:
    print("No se encontró nada.")