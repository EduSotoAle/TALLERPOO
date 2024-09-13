import clas_per_aca
import clas_niv_edu
import clas_asig
import clas_prof
import clas_stu
import clas_reg_notas
from funciones import borrar_pantalla

# Colores ANSI
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"

def main():
    while True:
        borrar_pantalla()  # Limpia la pantalla antes de mostrar el menú
        print(BLUE + "\n============================ Sistema de Gestión Académica ========================" + RESET)
        print(CYAN + "1. Gestión de Periodos Académicos" + RESET)
        print(CYAN + "2. Gestión de Niveles Educativos" + RESET)
        print(CYAN + "3. Gestión de Asignaturas" + RESET)
        print(CYAN + "4. Gestión de Profesores" + RESET)
        print(CYAN + "5. Gestión de Estudiantes" + RESET)
        print(CYAN + "6. Gestión de Notas" + RESET)  # Cambiado para reflejar la nueva nomenclatura
        print(RED + "7. Salir" + RESET)
        print(BLUE + "===================================================================================" + RESET)
        
        opcion = input(YELLOW + "Selecciona una opción: " + RESET)
        
        if opcion == '1':
            borrar_pantalla()  # Limpia la pantalla antes de mostrar la gestión de periodos académicos
            clas_per_aca.gestion_periodo_academico()
        elif opcion == '2':
            borrar_pantalla()  # Limpia la pantalla antes de mostrar la gestión de niveles educativos
            clas_niv_edu.gestion_niveles()
        elif opcion == '3':
            borrar_pantalla()  # Limpia la pantalla antes de mostrar la gestión de asignaturas
            clas_asig.gestion_asignaturas()
        elif opcion == '4':
            borrar_pantalla()  # Limpia la pantalla antes de mostrar la gestión de profesores
            clas_prof.gestion_profesor()
        elif opcion == '5':
            borrar_pantalla()  # Limpia la pantalla antes de mostrar la gestión de estudiantes
            clas_stu.gestion_estudiante()
        elif opcion == '6':
            borrar_pantalla()  # Limpia la pantalla antes de mostrar la gestión de detalles de notas
            clas_reg_notas.mostrar_menu_notas()
              # Cambiado para reflejar el nuevo método
        elif opcion == '7':
            print(GREEN + "Gracias por usar mi sistema 😊" + RESET)
            break
        else:
            print(RED + "Opción no válida. Por favor, selecciona una opción válida." + RESET)

if __name__ == "__main__":
    main()
