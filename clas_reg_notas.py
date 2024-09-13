from datetime import date
from funciones import borrar_pantalla
import clas_det_notas
import json
import os

# Ruta del archivo JSON en la carpeta "data"
DIRECTORIO_NOTAS = os.path.join('archivos_json', 'notas.json')

# Colores ANSI
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"

class Nota:
    def __init__(self, id, periodo, profesor, asignatura, active):
        self.id = id
        self.periodo = periodo
        self.profesor = profesor
        self.asignatura = asignatura
        self.detalleNota = []
        self.fecha_creacion = date.today()
        self.active = active

    def __str__(self):
        estado = GREEN + "Activo" + RESET if self.active else RED + "Inactivo" + RESET
        return (f"{CYAN}ID: {self.id}{RESET} | Periodo: {self.periodo} | Profesor: {self.profesor} | "
                f"Asignatura: {self.asignatura} | Fecha de Creación: {self.fecha_creacion.strftime('%d/%m/%Y')} | Estado: {estado}")

    def __repr__(self):
        return (f"Nota(id={self.id!r}, periodo={self.periodo!r}, profesor={self.profesor!r}, "
                f"asignatura={self.asignatura!r}, detalleNota={self.detalleNota!r}, "
                f"fecha_creacion={self.fecha_creacion!r}, active={self.active!r})")

    def to_dict(self):
        return {
            'id': self.id,
            'periodo': self.periodo,
            'profesor': self.profesor,
            'asignatura': self.asignatura,
            'detalleNota': self.detalleNota,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'active': self.active
        }

    @staticmethod
    def from_dict(data):
        fecha_creacion = date.fromisoformat(data['fecha_creacion'])
        return Nota(
            data['id'],
            data['periodo'],
            data['profesor'],
            data['asignatura'],
            data['active']
        )

# Lista para almacenar las notas
notas = []

def agregar_nota():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID de la nota: " + RESET)
    periodo = input(YELLOW + "Ingrese el período de la nota: " + RESET)
    profesor = input(YELLOW + "Ingrese el nombre del profesor: " + RESET)
    asignatura = input(YELLOW + "Ingrese la asignatura: " + RESET)
    active = input(YELLOW + "¿Está activa? (sí/no): " + RESET).strip().lower() == 'sí'
    nota = Nota(id, periodo, profesor, asignatura, active)
    notas.append(nota)
    guardar_notas()
    print(GREEN + f"Nota {id} agregada con éxito." + RESET)

def ver_notas():
    borrar_pantalla()
    cargar_notas()
    print(BLUE + "Lista de Notas:" + RESET)
    for nota in notas:
        print(nota)

def modificar_nota():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID de la nota a modificar: " + RESET)
    for nota in notas:
        if nota.id == id:
            periodo = input(YELLOW + "Ingrese el nuevo período de la nota: " + RESET)
            profesor = input(YELLOW + "Ingrese el nuevo nombre del profesor: " + RESET)
            asignatura = input(YELLOW + "Ingrese la nueva asignatura: " + RESET)
            active = input(YELLOW + "¿Está activa? (sí/no): " + RESET).strip().lower() == 'sí'
            nota.periodo = periodo
            nota.profesor = profesor
            nota.asignatura = asignatura
            nota.active = active
            guardar_notas()
            print(GREEN + f"Nota con ID {id} modificada con éxito." + RESET)
            return
    print(RED + "Nota no encontrada." + RESET)

def eliminar_nota():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID de la nota a eliminar: " + RESET)
    global notas
    notas = [nota for nota in notas if nota.id != id]
    guardar_notas()
    print(GREEN + f"Nota con ID {id} eliminada con éxito." + RESET)

def ver_detalles_nota():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID de la nota para ver los detalles: " + RESET)
    for nota in notas:
        if nota.id == id:
            print(f"{BLUE}Detalles de la Nota con ID {id}:{RESET}")
            print(nota)
            for detalle in nota.detalleNota:
                print(detalle)
            return
    print(RED + "Nota no encontrada." + RESET)

def guardar_notas():
    with open(DIRECTORIO_NOTAS, 'w') as file:
        json.dump([nota.to_dict() for nota in notas], file, indent=4)
    print(GREEN + f"Notas guardadas en '{DIRECTORIO_NOTAS}'." + RESET)

def cargar_notas():
    borrar_pantalla()
    global notas
    try:
        with open(DIRECTORIO_NOTAS, 'r') as file:
            data = json.load(file)
            notas = [Nota.from_dict(item) for item in data]
    except FileNotFoundError:
        print(RED + f"Archivo '{DIRECTORIO_NOTAS}' no encontrado." + RESET)
    except json.JSONDecodeError:
        print(RED + "Error al decodificar el archivo JSON." + RESET)

def mostrar_menu_notas():
    while True:
        print("\n" + BLUE + "---------------------- Menú Detalles de Notas ----------------------" + RESET)
        print(CYAN + "1. Ver Notas" + RESET)
        print(CYAN + "2. Modificar Notas" + RESET)
        print(CYAN + "3. Eliminar Notas" + RESET)
        print(CYAN + "4. Gestión Detalles de Notas" + RESET)
        print(RED + "5. Volver al Menú Principal" + RESET)
        opcion = input(YELLOW + "Selecciona una opción: " + RESET)
        
        if opcion == '1':
            ver_notas()
        elif opcion == '2':
            modificar_nota()
        elif opcion == '3':
            eliminar_nota()
        elif opcion == '4':
            clas_det_notas.mostrar_menu_detalles_notas()
        elif opcion == '5':
            break
        else:
            print(RED + "Opción no válida. Por favor, selecciona una opción válida." + RESET)

