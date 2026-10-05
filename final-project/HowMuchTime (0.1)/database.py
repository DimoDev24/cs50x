import sqlite3
from datetime import datetime, timedelta


BASE_DATOS = "usage.db"


# =========================================
# CONEXIÓN
# =========================================

def conectar():
    return sqlite3.connect(BASE_DATOS)


# =========================================
# CREAR BASE DE DATOS
# =========================================

def crear_base_datos():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sesiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aplicacion TEXT NOT NULL,
            inicio TEXT NOT NULL,
            fin TEXT NOT NULL,
            duracion INTEGER NOT NULL,
            fecha TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


# =========================================
# GUARDAR SESIÓN
# =========================================

def guardar_sesion(aplicacion, inicio, fin):

    duracion = int(fin - inicio)

    fecha = datetime.fromtimestamp(
        inicio
    ).strftime("%Y-%m-%d")

    hora_inicio = datetime.fromtimestamp(
        inicio
    ).strftime("%H:%M:%S")

    hora_fin = datetime.fromtimestamp(
        fin
    ).strftime("%H:%M:%S")

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO sesiones
        (aplicacion, inicio, fin, duracion, fecha)
        VALUES (?, ?, ?, ?, ?)
    """, (
        aplicacion,
        hora_inicio,
        hora_fin,
        duracion,
        fecha
    ))

    conexion.commit()
    conexion.close()


# =========================================
# TODAS LAS SESIONES
# =========================================

def obtener_sesiones():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM sesiones
        ORDER BY fecha DESC, inicio DESC
    """)

    sesiones = cursor.fetchall()

    conexion.close()

    return sesiones


# =========================================
# SESIONES DE HOY
# =========================================

def obtener_sesiones_hoy():

    hoy = datetime.now().strftime("%Y-%m-%d")

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM sesiones
        WHERE fecha = ?
        ORDER BY inicio
    """, (hoy,))

    sesiones = cursor.fetchall()

    conexion.close()

    return sesiones


# =========================================
# SESIONES DE ESTA SEMANA
# =========================================

def obtener_sesiones_semana():

    hoy = datetime.now().date()

    inicio_semana = hoy - timedelta(
        days=hoy.weekday()
    )

    fin_semana = inicio_semana + timedelta(
        days=6
    )

    fecha_inicio = inicio_semana.strftime(
        "%Y-%m-%d"
    )

    fecha_fin = fin_semana.strftime(
        "%Y-%m-%d"
    )

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM sesiones
        WHERE fecha BETWEEN ? AND ?
        ORDER BY fecha, inicio
    """, (
        fecha_inicio,
        fecha_fin
    ))

    sesiones = cursor.fetchall()

    conexion.close()

    return sesiones


# =========================================
# SESIONES DE ESTE MES
# =========================================

def obtener_sesiones_mes():

    hoy = datetime.now().date()

    inicio_mes = hoy.replace(day=1)

    if inicio_mes.month == 12:

        siguiente_mes = inicio_mes.replace(
            year=inicio_mes.year + 1,
            month=1
        )

    else:

        siguiente_mes = inicio_mes.replace(
            month=inicio_mes.month + 1
        )

    fin_mes = siguiente_mes - timedelta(
        days=1
    )

    fecha_inicio = inicio_mes.strftime(
        "%Y-%m-%d"
    )

    fecha_fin = fin_mes.strftime(
        "%Y-%m-%d"
    )

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM sesiones
        WHERE fecha BETWEEN ? AND ?
        ORDER BY fecha, inicio
    """, (
        fecha_inicio,
        fecha_fin
    ))

    sesiones = cursor.fetchall()

    conexion.close()

    return sesiones


# =========================================
# TIEMPO POR APLICACIÓN
# =========================================

def obtener_tiempo_por_aplicacion(
    fecha_inicio=None,
    fecha_fin=None
):

    conexion = conectar()
    cursor = conexion.cursor()

    if fecha_inicio is None:

        cursor.execute("""
            SELECT aplicacion, SUM(duracion)
            FROM sesiones
            GROUP BY aplicacion
            ORDER BY SUM(duracion) DESC
        """)

    elif fecha_fin is None:

        cursor.execute("""
            SELECT aplicacion, SUM(duracion)
            FROM sesiones
            WHERE fecha >= ?
            GROUP BY aplicacion
            ORDER BY SUM(duracion) DESC
        """, (fecha_inicio,))

    else:

        cursor.execute("""
            SELECT aplicacion, SUM(duracion)
            FROM sesiones
            WHERE fecha BETWEEN ? AND ?
            GROUP BY aplicacion
            ORDER BY SUM(duracion) DESC
        """, (
            fecha_inicio,
            fecha_fin
        ))

    resultados = cursor.fetchall()

    conexion.close()

    return resultados


# =========================================
# TIEMPO TOTAL
# =========================================

def obtener_tiempo_total(sesiones):

    total = 0

    for sesion in sesiones:
        total += sesion[4]

    return total


# =========================================
# TIEMPO POR DÍA
# =========================================

def obtener_tiempo_por_dia(
    fecha_inicio=None,
    fecha_fin=None
):

    conexion = conectar()
    cursor = conexion.cursor()

    if fecha_inicio is None:

        cursor.execute("""
            SELECT fecha, SUM(duracion)
            FROM sesiones
            GROUP BY fecha
            ORDER BY fecha
        """)

    elif fecha_fin is None:

        cursor.execute("""
            SELECT fecha, SUM(duracion)
            FROM sesiones
            WHERE fecha >= ?
            GROUP BY fecha
            ORDER BY fecha
        """, (fecha_inicio,))

    else:

        cursor.execute("""
            SELECT fecha, SUM(duracion)
            FROM sesiones
            WHERE fecha BETWEEN ? AND ?
            GROUP BY fecha
            ORDER BY fecha
        """, (
            fecha_inicio,
            fecha_fin
        ))

    resultados = cursor.fetchall()

    conexion.close()

    return resultados