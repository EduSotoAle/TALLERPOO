from datetime import date
from funciones import borrar_pantalla
import json
import os

# Ruta del archivo JSON en la carpeta "data"
DIRECTORIO_PROFESORES = os.path.join('archivos_json', 'profesores.json')

# Colores ANSI
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"

class Profesor:
    def __init__(self, id, nombre, active):
        self.id = id
        self.nombre = nombre
        self.fecha_creacion = date.today()
        self.active = active

    def __str__(self):
        estado = GREEN + "Activo" + RESET if self.active else RED + "Inactivo" + RESET
        return (f"{CYAN}ID: {self.id}{RESET} | Nombre: {self.nombre} | "
                f"Fecha de Creación: {self.fecha_creacion.strftime('%d/%m/%Y')} | Estado: {estado}")

    def __repr__(self):
        return (f"Profesor(id={self.id!r}, nombre={self.nombre!r}, "
                f"fecha_creacion={self.fecha_creacion!r}, active={self.active!r})")

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'active': self.active
        }

    @staticmethod
    def from_dict(data):
        fecha_creacion = date.fromisoformat(data['fecha_creacion'])
        return Profesor(data['id'], data['nombre'], data['active'])

# Lista para almacenar los profesores
profesores = []

def agregar_profesor():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID del profesor: " + RESET)
    nombre = input(YELLOW + "Ingrese el nombre del profesor: " + RESET)
    active = input(YELLOW + "¿Está activo? (sí/no): " + RESET).strip().lower() == 'sí'
    profesor = Profesor(id, nombre, active)
    profesores.append(profesor)
    guardar_profesores()
    print(GREEN + f"Profesor {nombre} agregado con éxito." + RESET)

def ver_profesores():
    borrar_pantalla()
    print(BLUE + "Lista de Profesores:" + RESET)
    for profesor in profesores:
        print(profesor)

def modificar_profesor():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID del profesor a modificar: " + RESET)
    for profesor in profesores:
        if profesor.id == id:
            nuevo_nombre = input(YELLOW + "Ingrese el nuevo nombre del profesor: " + RESET)
            nuevo_estado = input(YELLOW + "¿Está activo? (sí/no): " + RESET).strip().lower() == 'sí'
            profesor.nombre = nuevo_nombre
            profesor.active = nuevo_estado
            guardar_profesores()
            print(GREEN + f"Profesor con ID {id} modificado con éxito." + RESET)
            return
    print(RED + "Profesor no encontrado." + RESET)

def eliminar_profesor():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID del profesor a eliminar: " + RESET)
    global profesores
    profesores = [profesor for profesor in profesores if profesor.id != id]
    guardar_profesores()
    print(GREEN + f"Profesor con ID {id} eliminado con éxito." + RESET)

def guardar_profesores():
    with open(DIRECTORIO_PROFESORES, 'w') as file:
        json.dump([profesor.to_dict() for profesor in profesores], file, indent=4)
    print(GREEN + f"Profesores guardados en '{DIRECTORIO_PROFESORES}'." + RESET)

def cargar_profesores():
    borrar_pantalla()
    global profesores
    try:
        with open(DIRECTORIO_PROFESORES, 'r') as file:
            data = json.load(file)
            profesores = [Profesor.from_dict(item) for item in data]
        print(GREEN + "Profesores cargados exitosamente." + RESET)
    except FileNotFoundError:
        print(RED + f"Archivo '{DIRECTORIO_PROFESORES}' no encontrado." + RESET)
    except json.JSONDecodeError:
        print(RED + "Error al decodificar el archivo JSON." + RESET)

def gestion_profesor():
    while True:
        print("\n" + BLUE + "--------------------------------------------------------------------" + RESET)
        print(CYAN + "-------------------------Gestión de Profesores-----------------------" + RESET)
        print(CYAN + "1. Agregar Profesor" + RESET)
        print(CYAN + "2. Ver Profesores" + RESET)
        print(CYAN + "3. Modificar Profesor" + RESET)
        print(CYAN + "4. Eliminar Profesor" + RESET)
        print(RED + "5. Volver al Menú Principal" + RESET)
        opcion = input(YELLOW + "Selecciona una opción: " + RESET)
        
        if opcion == '1':
            agregar_profesor()
        elif opcion == '2':
            cargar_profesores()
            ver_profesores()
        elif opcion == '3':
            cargar_profesores()
            modificar_profesor()
        elif opcion == '4':
            cargar_profesores()
            eliminar_profesor()
        elif opcion == '5':
            break
        else:
            print(RED + "Opción no válida. Por favor, selecciona una opción válida." + RESET)
