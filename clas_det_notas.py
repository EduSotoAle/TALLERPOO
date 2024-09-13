from funciones import borrar_pantalla
import json
import os

# Ruta del archivo JSON en la carpeta "data"
DIRECTORIO_DETALLES_NOTAS = os.path.join('archivos_json', 'detalles_notas.json')

# Colores ANSI
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"

class DetalleNota:
    def __init__(self, id, estudiante, nota1, nota2, recuperacion=None, observacion=None):
        self.id = id
        self.estudiante = estudiante
        self.nota1 = nota1
        self.nota2 = nota2
        self.recuperacion = recuperacion
        self.observacion = observacion

    def __str__(self):
        recuperacion_str = f"Recuperación: {self.recuperacion}" if self.recuperacion is not None else "Recuperación: No disponible"
        observacion_str = f"Observación: {self.observacion}" if self.observacion is not None else "Observación: No disponible"
        return (f"{CYAN}ID: {self.id}{RESET}\n"
                f"Estudiante: {self.estudiante}\n"
                f"Nota 1: {self.nota1}\n"
                f"Nota 2: {self.nota2}\n"
                f"{recuperacion_str}\n"
                f"{observacion_str}\n")

    def to_dict(self):
        return {
            'id': self.id,
            'estudiante': self.estudiante,
            'nota1': self.nota1,
            'nota2': self.nota2,
            'recuperacion': self.recuperacion,
            'observacion': self.observacion
        }

    @staticmethod
    def from_dict(data):
        return DetalleNota(
            data['id'],
            data['estudiante'],
            data['nota1'],
            data['nota2'],
            data.get('recuperacion'),
            data.get('observacion')
        )

    def actualizar_notas(self, nota1=None, nota2=None, recuperacion=None):
        if nota1 is not None:
            self.nota1 = nota1
        if nota2 is not None:
            self.nota2 = nota2
        if recuperacion is not None:
            self.recuperacion = recuperacion

    def agregar_observacion(self, observacion):
        self.observacion = observacion


detalles_notas = []

def agregar_detalle_nota():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID del detalle de la nota: " + RESET)
    estudiante = input(YELLOW + "Ingrese el nombre del estudiante: " + RESET)
    
    try:
        nota1 = float(input(YELLOW + "Ingrese la primera calificación: " + RESET))
        nota2 = float(input(YELLOW + "Ingrese la segunda calificación: " + RESET))
    except ValueError:
        print(RED + "Error: Las calificaciones deben ser números." + RESET)
        return

    recuperacion = input(YELLOW + "Ingrese la nota de recuperación (deje vacío si no aplica): " + RESET)
    recuperacion = float(recuperacion) if recuperacion else None
    observacion = input(YELLOW + "Ingrese observación (deje vacío si no aplica): " + RESET)
    
    # Verificar que el ID no esté duplicado
    for detalle in detalles_notas:
        if detalle.id == id:
            print(RED + f"Error: Ya existe un detalle con el ID {id}." + RESET)
            return
    
    detalle_nota = DetalleNota(id, estudiante, nota1, nota2, recuperacion, observacion)
    detalles_notas.append(detalle_nota)
    guardar_detalles_notas()
    print(GREEN + f"Detalle de nota con ID {id} agregado con éxito." + RESET)

def ver_detalles_notas():
    borrar_pantalla()
    cargar_detalles_notas()
    print(BLUE + "Lista de Detalles de Notas:" + RESET)
    if detalles_notas:
        for detalle in detalles_notas:
            print("\n" + str(detalle))
    else:
        print(YELLOW + "No hay detalles de notas disponibles." + RESET)

def modificar_detalle_nota():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID del detalle de la nota a modificar: " + RESET)
    for detalle in detalles_notas:
        if detalle.id == id:
            print("\nDetalles actuales:")
            print(detalle)
            
            nota1 = input(YELLOW + "Ingrese la nueva primera calificación (deje vacío para mantener la actual): " + RESET)
            nota1 = float(nota1) if nota1 else detalle.nota1
            nota2 = input(YELLOW + "Ingrese la nueva segunda calificación (deje vacío para mantener la actual): " + RESET)
            nota2 = float(nota2) if nota2 else detalle.nota2
            recuperacion = input(YELLOW + "Ingrese la nueva nota de recuperación (deje vacío para mantener la actual): " + RESET)
            recuperacion = float(recuperacion) if recuperacion else detalle.recuperacion
            observacion = input(YELLOW + "Ingrese nueva observación (deje vacío para mantener la actual): " + RESET)
            
            detalle.actualizar_notas(nota1, nota2, recuperacion)
            detalle.agregar_observacion(observacion)
            guardar_detalles_notas()
            print(GREEN + f"\nDetalle de nota con ID {id} modificado con éxito." + RESET)
            return
    print(RED + "\nDetalle de nota no encontrado." + RESET)

def eliminar_detalle_nota():
    borrar_pantalla()
    id = input(YELLOW + "Ingrese el ID del detalle de la nota a eliminar: " + RESET)
    global detalles_notas
    detalles_notas = [detalle for detalle in detalles_notas if detalle.id != id]
    guardar_detalles_notas()
    print(GREEN + f"\nDetalle de nota con ID {id} eliminado con éxito." + RESET)

def guardar_detalles_notas():
    borrar_pantalla()
    with open(DIRECTORIO_DETALLES_NOTAS, 'w') as file:
        json.dump([detalle.to_dict() for detalle in detalles_notas], file, indent=4)
    print(GREEN + f"\nDetalles de notas guardados en '{DIRECTORIO_DETALLES_NOTAS}'." + RESET)

def cargar_detalles_notas():
    global detalles_notas
    try:
        with open(DIRECTORIO_DETALLES_NOTAS, 'r') as file:
            data = json.load(file)  # Falta cerrar el paréntesis aquí
            detalles_notas = [DetalleNota.from_dict(item) for item in data]
    except FileNotFoundError:
        print(RED + f"\nArchivo '{DIRECTORIO_DETALLES_NOTAS}' no encontrado." + RESET)
    except json.JSONDecodeError:
        print(RED + "\nError al decodificar el archivo JSON." + RESET)

def mostrar_menu_detalles_notas():
    borrar_pantalla()
    while True:
        print(f"\n{CYAN}------------------------------------------------------------------------------")
        print(f"---------------------------{YELLOW}Gestión de Detalle de Notas{CYAN}--------------------------")
        print(f"{RESET}{GREEN}1. {RESET}Agregar Detalle de Nota")
        print(f"{GREEN}2. {RESET}Ver Detalles de Notas")
        print(f"{GREEN}3. {RESET}Modificar Detalle de Nota")
        print(f"{GREEN}4. {RESET}Eliminar Detalle de Nota")
        print(f"{GREEN}5. {RESET}Volver al Menú Principal")
        opcion = input(f"{YELLOW}Selecciona una opción: {RESET}")
        
        if opcion == '1':
            borrar_pantalla()
            agregar_detalle_nota()
        elif opcion == '2':
            borrar_pantalla()
            ver_detalles_notas()
        elif opcion == '3':
            borrar_pantalla()
            modificar_detalle_nota()
        elif opcion == '4':
            borrar_pantalla()
            eliminar_detalle_nota()
        elif opcion == '5':
            borrar_pantalla()
            break
        else:
            print(f"{RED}Opción no válida.{RESET} Por favor, selecciona una opción válida.")
