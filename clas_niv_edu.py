from datetime import date
from funciones import borrar_pantalla
import json
import os

# Ruta del archivo JSON en la carpeta "data"
DIRECTORIO_NIVELES = os.path.join('archivos_json', 'niveles.json')

# Colores ANSI
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"

class Nivel:
    def __init__(self, id, nivel, fecha_creacion=None, active=True):
        self.id = id
        self.nivel = nivel
        self.fecha_creacion = fecha_creacion or date.today()
        self.active = active

    def __str__(self):
        estado = GREEN + "Activo" + RESET if self.active else RED + "Inactivo" + RESET
        return (f"{CYAN}ID: {self.id}{RESET} | Nombre: {self.nivel} | "
                f"Fecha de Creación: {self.fecha_creacion.strftime('%d/%m/%Y')} | Estado: {estado}")

    def __repr__(self):
        return (f"Nivel(id={self.id!r}, nivel={self.nivel!r}, "
                f"fecha_creacion={self.fecha_creacion!r}, active={self.active!r})")

    def to_dict(self):
        return {
            'id': self.id,
            'nivel': self.nivel,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'active': self.active
        }

    @staticmethod
    def from_dict(data):
        fecha_creacion = date.fromisoformat(data['fecha_creacion'])
        return Nivel(
            data['id'],
            data['nivel'],
            fecha_creacion,
            data['active']
        )

# Lista para almacenar los niveles
niveles = []

def agregar_nivel():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID del nivel: " + RESET)
    nivel = input(YELLOW + "Ingrese el nombre o descripción del nivel: " + RESET)
    active = input(YELLOW + "¿Está activo? (sí/no): " + RESET).strip().lower() == 'sí'
    nivel_obj = Nivel(id, nivel)
    nivel_obj.active = active
    niveles.append(nivel_obj)
    guardar_niveles()
    print(GREEN + f"Nivel '{nivel}' agregado con éxito." + RESET)

def ver_niveles():
    borrar_pantalla()
    print(BLUE + "Lista de Niveles:" + RESET)
    for nivel in niveles:
        print(nivel)

def modificar_nivel():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID del nivel a modificar: " + RESET)
    for nivel in niveles:
        if nivel.id == id:
            nuevo_nivel = input(YELLOW + "Ingrese el nuevo nombre o descripción del nivel: " + RESET)
            nuevo_estado = input(YELLOW + "¿Está activo? (sí/no): " + RESET).strip().lower() == 'sí'
            nivel.nivel = nuevo_nivel
            nivel.active = nuevo_estado
            guardar_niveles()
            print(GREEN + f"Nivel con ID {id} modificado con éxito." + RESET)
            return
    print(RED + "Nivel no encontrado." + RESET)

def eliminar_nivel():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID del nivel a eliminar: " + RESET)
    global niveles
    niveles = [nivel for nivel in niveles if nivel.id != id]
    guardar_niveles()
    print(GREEN + f"Nivel con ID {id} eliminado con éxito." + RESET)

def guardar_niveles():
    borrar_pantalla()
    with open(DIRECTORIO_NIVELES, 'w') as file:
        json.dump([nivel.to_dict() for nivel in niveles], file, indent=4)
    print(GREEN + f"Niveles guardados en '{DIRECTORIO_NIVELES}'." + RESET)

def cargar_niveles():
    borrar_pantalla()
    global niveles
    try:
        with open(DIRECTORIO_NIVELES, 'r') as file:
            data = json.load(file)
            niveles = [Nivel.from_dict(item) for item in data]
        print(GREEN + "Niveles cargados exitosamente." + RESET)
    except FileNotFoundError:
        print(RED + f"Archivo '{DIRECTORIO_NIVELES}' no encontrado." + RESET)
    except json.JSONDecodeError:
        print(RED + "Error al decodificar el archivo JSON." + RESET)

def gestion_niveles():
    while True:
        print("\n" + BLUE + "--------------------------------------------------------------------" + RESET)
        print(CYAN + "-----------------------------Gestión de Niveles---------------------------" + RESET)
        print(CYAN + "1. Agregar Nivel" + RESET)
        print(CYAN + "2. Ver Niveles" + RESET)
        print(CYAN + "3. Modificar Nivel" + RESET)
        print(CYAN + "4. Eliminar Nivel" + RESET)
        print(RED + "5. Volver al Menú Principal" + RESET)
        opcion = input(YELLOW + "Selecciona una opción: " + RESET)
        
        if opcion == '1':
            agregar_nivel()
        elif opcion == '2':
            cargar_niveles()
            ver_niveles()
        elif opcion == '3':
            cargar_niveles()
            modificar_nivel()
        elif opcion == '4':
            cargar_niveles()
            eliminar_nivel()
        elif opcion == '5':
            break
        else:
            print(RED + "Opción no válida. Por favor, selecciona una opción válida." + RESET)
