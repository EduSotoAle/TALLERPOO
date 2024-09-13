from datetime import date
from funciones import borrar_pantalla
import json
import os

# Ruta del archivo JSON en la carpeta "archivos_json"
DIRECTORIO_PERIODOS_ACADEMICOS = os.path.join('archivos_json', 'periodos.json')

# Colores ANSI
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"

class Periodo:
    def __init__(self, id, descripcion, fecha_inicio, fecha_fin, active):
        self.id = id
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.fecha_creacion = date.today()
        self.active = active

    def __str__(self):
        estado = GREEN + "Activo" + RESET if self.active else RED + "Inactivo" + RESET
        return (f"{CYAN}ID: {self.id}{RESET} | Descripción: {self.descripcion} | "
                f"Fecha de Inicio: {self.fecha_inicio.strftime('%d/%m/%Y')} | "
                f"Fecha de Fin: {self.fecha_fin.strftime('%d/%m/%Y')} | "
                f"Fecha de Creación: {self.fecha_creacion.strftime('%d/%m/%Y')} | Estado: {estado}")

    def __repr__(self):
        return (f"Periodo(id={self.id!r}, descripcion={self.descripcion!r}, "
                f"fecha_inicio={self.fecha_inicio!r}, fecha_fin={self.fecha_fin!r}, "
                f"fecha_creacion={self.fecha_creacion!r}, active={self.active!r})")

    def to_dict(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion,
            'fecha_inicio': self.fecha_inicio.isoformat(),
            'fecha_fin': self.fecha_fin.isoformat(),
            'active': self.active
        }

    @staticmethod
    def from_dict(data):
        fecha_inicio = date.fromisoformat(data['fecha_inicio'])
        fecha_fin = date.fromisoformat(data['fecha_fin'])
        fecha_creacion = date.fromisoformat(data['fecha_creacion']) if 'fecha_creacion' in data else date.today()
        return Periodo(
            data['id'],
            data['descripcion'],
            fecha_inicio,
            fecha_fin,
            data['active']
        )

# Lista para almacenar los períodos académicos
periodos_academicos = []

def agregar_periodo_academico():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID del período académico: " + RESET)
    descripcion = input(YELLOW + "Ingrese la descripción del período académico: " + RESET)
    fecha_inicio = date.fromisoformat(input(YELLOW + "Ingrese la fecha de inicio (YYYY-MM-DD): " + RESET))
    fecha_fin = date.fromisoformat(input(YELLOW + "Ingrese la fecha de fin (YYYY-MM-DD): " + RESET))
    active = input(YELLOW + "¿Está activo? (sí/no): " + RESET).strip().lower() == 'sí'
    periodo_academico = Periodo(id, descripcion, fecha_inicio, fecha_fin, active)
    periodos_academicos.append(periodo_academico)
    guardar_periodos_academicos()
    print(GREEN + f"Período académico '{descripcion}' agregado con éxito." + RESET)

def ver_periodos_academicos():
    borrar_pantalla()
    print(BLUE + "Lista de Períodos Académicos:" + RESET)
    for periodo in periodos_academicos:
        print(periodo)

def modificar_periodo_academico():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID del período académico a modificar: " + RESET)
    for periodo in periodos_academicos:
        if periodo.id == id:
            nueva_descripcion = input(YELLOW + "Ingrese la nueva descripción del período académico: " + RESET)
            nueva_fecha_inicio = date.fromisoformat(input(YELLOW + "Ingrese la nueva fecha de inicio (YYYY-MM-DD): " + RESET))
            nueva_fecha_fin = date.fromisoformat(input(YELLOW + "Ingrese la nueva fecha de fin (YYYY-MM-DD): " + RESET))
            nuevo_estado = input(YELLOW + "¿Está activo? (sí/no): " + RESET).strip().lower() == 'sí'
            periodo.descripcion = nueva_descripcion
            periodo.fecha_inicio = nueva_fecha_inicio
            periodo.fecha_fin = nueva_fecha_fin
            periodo.active = nuevo_estado
            guardar_periodos_academicos()
            print(GREEN + f"Período académico con ID {id} modificado con éxito." + RESET)
            return
    print(RED + "Período académico no encontrado." + RESET)

def eliminar_periodo_academico():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID del período académico a eliminar: " + RESET)
    global periodos_academicos
    periodos_academicos = [periodo for periodo in periodos_academicos if periodo.id != id]
    guardar_periodos_academicos()
    print(GREEN + f"Período académico con ID {id} eliminado con éxito." + RESET)

def guardar_periodos_academicos():
    with open(DIRECTORIO_PERIODOS_ACADEMICOS, 'w') as file:
        json.dump([periodo.to_dict() for periodo in periodos_academicos], file, indent=4)
    print(GREEN + f"Períodos académicos guardados en '{DIRECTORIO_PERIODOS_ACADEMICOS}'." + RESET)

def cargar_periodos_academicos():
    try:
        with open(DIRECTORIO_PERIODOS_ACADEMICOS, 'r') as file:
            data = json.load(file)
            global periodos_academicos
            periodos_academicos = [Periodo.from_dict(item) for item in data]
        print(GREEN + "Períodos académicos cargados exitosamente." + RESET)
    except FileNotFoundError:
        print(RED + f"Archivo '{DIRECTORIO_PERIODOS_ACADEMICOS}' no encontrado." + RESET)
    except json.JSONDecodeError:
        print(RED + "Error al decodificar el archivo JSON." + RESET)

def gestion_periodo_academico():
    while True:
        print("\n" + BLUE + "--------------------------------------------------------------------" + RESET)
        print(BLUE + "-----------------------Gestión de Períodos Académicos---------------------" + RESET)
        print(CYAN + "1. Agregar Período Académico" + RESET)
        print(CYAN + "2. Ver Períodos Académicos" + RESET)
        print(CYAN + "3. Modificar Período Académico" + RESET)
        print(CYAN + "4. Eliminar Período Académico" + RESET)
        print(RED + "5. Volver al Menú Principal" + RESET)
        opcion = input(YELLOW + "Selecciona una opción: " + RESET)
        
        if opcion == '1':
            agregar_periodo_academico()
        elif opcion == '2':
            cargar_periodos_academicos()
            ver_periodos_academicos()
        elif opcion == '3':
            modificar_periodo_academico()
        elif opcion == '4':
            eliminar_periodo_academico()
        elif opcion == '5':
            break
        else:
            print(RED + "Opción no válida. Por favor, selecciona una opción válida." + RESET)
