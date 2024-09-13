from datetime import date
from funciones import borrar_pantalla
import json
import os

# Ruta del archivo JSON en la carpeta "data"
DIRECTORIO_ESTUDIANTES = os.path.join('archivos_json', 'estudiantes.json')

# Colores ANSI
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"

class Estudiante:
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
        return (f"Estudiante(id={self.id!r}, nombre={self.nombre!r}, "
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
        return Estudiante(data['id'], data['nombre'], data['active'])

# Lista para almacenar los estudiantes
estudiantes = []

def agregar_estudiante():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID del estudiante: " + RESET)
    nombre = input(YELLOW + "Ingrese el nombre del estudiante: " + RESET)
    active = input(YELLOW + "¿Está activo? (sí/no): " + RESET).strip().lower() == 'sí'
    estudiante = Estudiante(id, nombre, active)
    estudiantes.append(estudiante)
    guardar_estudiantes()
    print(GREEN + f"Estudiante {nombre} agregado con éxito." + RESET)

def ver_estudiantes():
    borrar_pantalla()
    print(BLUE + "Lista de Estudiantes:" + RESET)
    for estudiante in estudiantes:
        print(estudiante)

def modificar_estudiante():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID del estudiante a modificar: " + RESET)
    for estudiante in estudiantes:
        if estudiante.id == id:
            nuevo_nombre = input(YELLOW + "Ingrese el nuevo nombre del estudiante: " + RESET)
            nuevo_estado = input(YELLOW + "¿Está activo? (sí/no): " + RESET).strip().lower() == 'sí'
            estudiante.nombre = nuevo_nombre
            estudiante.active = nuevo_estado
            guardar_estudiantes()
            print(GREEN + f"Estudiante con ID {id} modificado con éxito." + RESET)
            return
    print(RED + "Estudiante no encontrado." + RESET)

def eliminar_estudiante():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID del estudiante a eliminar: " + RESET)
    global estudiantes
    estudiantes = [estudiante for estudiante in estudiantes if estudiante.id != id]
    guardar_estudiantes()
    print(GREEN + f"Estudiante con ID {id} eliminado con éxito." + RESET)

def guardar_estudiantes():
    with open(DIRECTORIO_ESTUDIANTES, 'w') as file:
        json.dump([estudiante.to_dict() for estudiante in estudiantes], file, indent=4)
    print(GREEN + f"Estudiantes guardados en '{DIRECTORIO_ESTUDIANTES}'." + RESET)

def cargar_estudiantes():
    try:
        with open(DIRECTORIO_ESTUDIANTES, 'r') as file:
            data = json.load(file)
            global estudiantes
            estudiantes = [Estudiante.from_dict(item) for item in data]
        print(GREEN + "Estudiantes cargados exitosamente." + RESET)
    except FileNotFoundError:
        print(RED + f"Archivo '{DIRECTORIO_ESTUDIANTES}' no encontrado." + RESET)
    except json.JSONDecodeError:
        print(RED + "Error al decodificar el archivo JSON." + RESET)

def gestion_estudiante():
    while True:
        print("\n" + BLUE + "--------------------------------------------------------------------" + RESET)
        print(BLUE + "-------------------------Gestión de Estudiantes-----------------------" + RESET)
        print(CYAN + "1. Agregar Estudiante" + RESET)
        print(CYAN + "2. Ver Estudiantes" + RESET)
        print(CYAN + "3. Modificar Estudiante" + RESET)
        print(CYAN + "4. Eliminar Estudiante" + RESET)
        print(RED + "5. Volver al Menú Principal" + RESET)
        opcion = input(YELLOW + "Selecciona una opción: " + RESET)
        
        if opcion == '1':
            agregar_estudiante()
        elif opcion == '2':
            cargar_estudiantes()
            ver_estudiantes()
        elif opcion == '3':
            cargar_estudiantes()
            modificar_estudiante()
        elif opcion == '4':
            cargar_estudiantes()
            eliminar_estudiante()
        elif opcion == '5':
            break
        else:
            print(RED + "Opción no válida. Por favor, selecciona una opción válida." + RESET)

