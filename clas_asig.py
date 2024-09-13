from datetime import date
from funciones import borrar_pantalla
import json
import os

# Ruta del archivo JSON en la carpeta "data"
DIRECTORIO_ASIGNATURAS = os.path.join('archivos_json', 'asignaturas.json')

# Colores ANSI
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"

class Asignatura:
    def __init__(self, id, descripcion, nivel, active):
        self.id = id
        self.descripcion = descripcion
        self.nivel = nivel
        self.fecha_creacion = date.today()
        self.active = active

    def __str__(self):
        estado = GREEN + "Activo" + RESET if self.active else RED + "Inactivo" + RESET
        return (f"{CYAN}ID: {self.id}{RESET} | Descripción: {self.descripcion} | Nivel: {self.nivel} | "
                f"Fecha de Creación: {self.fecha_creacion.strftime('%d/%m/%Y')} | Estado: {estado}")

    def to_dict(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion,
            'nivel': self.nivel,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'active': self.active
        }

    @staticmethod
    def from_dict(data):
        fecha_creacion = date.fromisoformat(data['fecha_creacion'])
        return Asignatura(data['id'], data['descripcion'], data['nivel'], data['active'])

# Lista para almacenar las asignaturas
asignaturas = []

def agregar_asignatura():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID de la asignatura: " + RESET)
    descripcion = input(YELLOW + "Ingrese la descripción de la asignatura: " + RESET)
    nivel = input(YELLOW + "Ingrese el nivel académico de la asignatura: " + RESET)
    active = input(YELLOW + "¿Está activa? (sí/no): " + RESET).strip().lower() == 'sí'
    
    # Validar que no se repita el ID
    for asignatura in asignaturas:
        if asignatura.id == id:
            print(RED + f"Ya existe una asignatura con el ID {id}. Inténtelo de nuevo." + RESET)
            return
    
    nueva_asignatura = Asignatura(id, descripcion, nivel, active)
    asignaturas.append(nueva_asignatura)
    guardar_asignaturas()
    print(GREEN + f"Asignatura '{descripcion}' agregada con éxito." + RESET)

def ver_asignaturas():
    borrar_pantalla()
    print(BLUE + "Lista de Asignaturas:" + RESET)
    for asignatura in asignaturas:
        print(asignatura)

def modificar_asignatura():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID de la asignatura a modificar: " + RESET)
    for asignatura in asignaturas:
        if asignatura.id == id:
            nueva_descripcion = input(YELLOW + "Ingrese la nueva descripción de la asignatura: " + RESET)
            nuevo_nivel = input(YELLOW + "Ingrese el nuevo nivel académico de la asignatura: " + RESET)
            nuevo_estado = input(YELLOW + "¿Está activa? (sí/no): " + RESET).strip().lower() == 'sí'
            asignatura.descripcion = nueva_descripcion
            asignatura.nivel = nuevo_nivel
            asignatura.active = nuevo_estado
            guardar_asignaturas()
            print(GREEN + f"Asignatura con ID {id} modificada con éxito." + RESET)
            return
    print(RED + "Asignatura no encontrada." + RESET)

def eliminar_asignatura():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID de la asignatura a eliminar: " + RESET)
    global asignaturas
    asignaturas = [asignatura for asignatura in asignaturas if asignatura.id != id]
    guardar_asignaturas()
    print(GREEN + f"Asignatura con ID {id} eliminada con éxito." + RESET)

def guardar_asignaturas():
    borrar_pantalla()
    with open(DIRECTORIO_ASIGNATURAS, 'w') as file:
        json.dump([asignatura.to_dict() for asignatura in asignaturas], file, indent=4)
    print(GREEN + f"Asignaturas guardadas en '{DIRECTORIO_ASIGNATURAS}'." + RESET)

def cargar_asignaturas():
    borrar_pantalla()
    global asignaturas
    try:
        with open(DIRECTORIO_ASIGNATURAS, 'r') as file:
            data = json.load(file)
            asignaturas = [Asignatura.from_dict(item) for item in data]
        print(GREEN + "Asignaturas cargadas exitosamente." + RESET)
    except FileNotFoundError:
        print(RED + f"Archivo '{DIRECTORIO_ASIGNATURAS}' no encontrado." + RESET)
    except json.JSONDecodeError:
        print(RED + "Error al decodificar el archivo JSON." + RESET)

def gestion_asignaturas():
    cargar_asignaturas()  # Cargar asignaturas automáticamente al iniciar
    while True:
        print("\n" + BLUE + "--------------------------------------------------------------------" + RESET)
        print(CYAN + "---------------------------Gestión de Asignaturas----------------------------" + RESET)
        print(CYAN + "1. Agregar Asignatura" + RESET)
        print(CYAN + "2. Ver Asignaturas" + RESET)
        print(CYAN + "3. Modificar Asignatura" + RESET)
        print(CYAN + "4. Eliminar Asignatura" + RESET)
        print(RED + "5. Volver al Menú Principal" + RESET)
        opcion = input(YELLOW + "Selecciona una opción: " + RESET)
        
        if opcion == '1':
            agregar_asignatura()
        elif opcion == '2':
            ver_asignaturas()
        elif opcion == '3':
            modificar_asignatura()
        elif opcion == '4':
            eliminar_asignatura()
        elif opcion == '5':
            break
        else:
            print(RED + "Opción no válida. Por favor, selecciona una opción válida." + RESET)
