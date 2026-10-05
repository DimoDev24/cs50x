import time
import win32gui
import win32process
import psutil
from datetime import datetime
import os

from database import crear_base_datos, guardar_sesion


PROCESOS_IGNORADOS = {
    "explorer.exe",
    "SearchHost.exe",
    "StartMenuExperienceHost.exe",
    "ShellExperienceHost.exe",
    "ApplicationFrameHost.exe",
}

ARCHIVO_ESTADO = "tracker_status.txt"


def obtener_aplicacion_activa():

    ventana = win32gui.GetForegroundWindow()

    if not ventana:
        return None

    try:

        _, pid = win32process.GetWindowThreadProcessId(ventana)

        proceso = psutil.Process(pid)

        nombre = proceso.name()

        if nombre in PROCESOS_IGNORADOS:
            return None

        return nombre

    except (psutil.NoSuchProcess, psutil.AccessDenied):

        return None


def formatear_tiempo(segundos):

    segundos = int(segundos)

    horas = segundos // 3600

    minutos = (segundos % 3600) // 60

    segundos = segundos % 60

    if horas > 0:
        return f"{horas}h {minutos}m {segundos}s"

    if minutos > 0:
        return f"{minutos}m {segundos}s"

    return f"{segundos}s"


def mostrar_sesion(aplicacion, inicio, fin):

    duracion = fin - inicio

    hora_inicio = datetime.fromtimestamp(inicio).strftime("%H:%M:%S")

    hora_fin = datetime.fromtimestamp(fin).strftime("%H:%M:%S")

    print()

    print("--------------------------------")

    print(f"Aplication: {aplicacion}")

    print(f"Beggining:     {hora_inicio}")

    print(f"End:        {hora_fin}")

    print(f"Duration:   {formatear_tiempo(duracion)}")

    print("--------------------------------")

    print()


crear_base_datos()

aplicacion_actual = None
inicio_sesion = None

with open(ARCHIVO_ESTADO, "w") as archivo:
    archivo.write("active")

print("================================")
print("      HowMuchTime - Tracker")
print("================================")
print()
print("Database: usage.db")
print("Detecting usage time...")
print("Press Ctrl+C to stop.")
print()


try:

    while True:

        nueva_aplicacion = obtener_aplicacion_activa()

        if nueva_aplicacion != aplicacion_actual:

            ahora = time.time()

            if aplicacion_actual is not None and inicio_sesion is not None:

                mostrar_sesion(
                    aplicacion_actual,
                    inicio_sesion,
                    ahora
                )

                guardar_sesion(
                    aplicacion_actual,
                    inicio_sesion,
                    ahora
                )

                print("Sesion saved.")

            aplicacion_actual = nueva_aplicacion

            inicio_sesion = ahora

            if aplicacion_actual is not None:

                print(
                    f">>> Nueva aplicación: "
                    f"{aplicacion_actual}"
                )

        time.sleep(0.2)


except KeyboardInterrupt:

    ahora = time.time()

    print()
    print("================================")
    print("       Tracker Stopped")
    print("================================")

    if aplicacion_actual is not None and inicio_sesion is not None:

        mostrar_sesion(
            aplicacion_actual,
            inicio_sesion,
            ahora
        )

        guardar_sesion(
            aplicacion_actual,
            inicio_sesion,
            ahora
        )

        print("Last Sesion Saved.")

finally:

    if os.path.exists(ARCHIVO_ESTADO):
        os.remove(ARCHIVO_ESTADO)