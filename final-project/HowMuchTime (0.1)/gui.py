import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import os

from database import (
    crear_base_datos,
    obtener_sesiones_hoy,
    obtener_sesiones_semana,
    obtener_sesiones_mes,
    obtener_tiempo_por_aplicacion,
    obtener_tiempo_por_dia,
)


# =========================================
# CONFIGURACIÓN
# =========================================

TITULO = "HowMuchTime"

ANCHO = 1100
ALTO = 720

FUENTE = "Segoe UI"

# Colores
FONDO = "#111318"
SIDEBAR = "#181B21"
TARJETA = "#1C2028"
TARJETA_SECUNDARIA = "#20252E"

TEXTO = "#F1F3F5"
TEXTO_SECUNDARIO = "#9AA1AC"

ACENTO = "#6C63FF"
ACENTO_HOVER = "#7B73FF"

BORDER = "#292E38"

BARRA_FONDO = "#2A2F39"


# =========================================
# FUNCIONES
# =========================================

def tracker_activo():

    return os.path.exists("tracker_status.txt")

def formatear_tiempo(segundos):

    segundos = int(segundos)

    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos = segundos % 60

    if horas > 0:
        return f"{horas}h {minutos:02d}m"

    if minutos > 0:
        return f"{minutos}m {segundos:02d}s"

    return f"{segundos}s"


def obtener_datos(periodo):

    if periodo == "Today":

        sesiones = obtener_sesiones_hoy()

        fecha_inicio = datetime.now().strftime(
            "%Y-%m-%d"
        )

    elif periodo == "This Week":

        sesiones = obtener_sesiones_semana()

        hoy = datetime.now().date()

        inicio_semana = hoy - timedelta(
            days=hoy.weekday()
        )

        fecha_inicio = inicio_semana.strftime(
            "%Y-%m-%d"
        )

    else:

        sesiones = obtener_sesiones_mes()

        fecha_inicio = datetime.now().strftime(
            "%Y-%m-01"
        )

    aplicaciones = obtener_tiempo_por_aplicacion(
        fecha_inicio
    )

    tiempo_total = sum(
        sesion[4]
        for sesion in sesiones
    )

    return sesiones, tiempo_total, aplicaciones


# =========================================
# APLICACIÓN
# =========================================

class HowMuchTimeApp:

    def __init__(self, ventana):

        self.ventana = ventana

        self.periodo_actual = "Today"

        self.botones_periodo = {}

        self.configurar_ventana()

        self.crear_estilos()

        self.crear_interfaz()

        self.actualizar_datos()

        self.actualizar_visibilidad_grafico()

        self.actualizar_estado_tracker()


    # =====================================
    # VENTANA
    # =====================================

    def configurar_ventana(self):

        self.ventana.title(TITULO)

        self.ventana.geometry(
            f"{ANCHO}x{ALTO}"
        )

        self.ventana.minsize(
            900,
            600
        )

        self.ventana.configure(
            bg=FONDO
        )


    # =====================================
    # ESTILOS
    # =====================================

    def crear_estilos(self):

        estilo = ttk.Style()

        estilo.theme_use("clam")

        estilo.configure(
            "Treeview",
            background=TARJETA,
            foreground=TEXTO,
            fieldbackground=TARJETA,
            borderwidth=0,
            rowheight=42,
            font=(FUENTE, 10)
        )

        estilo.configure(
            "Treeview.Heading",
            background=TARJETA,
            foreground=TEXTO_SECUNDARIO,
            borderwidth=0,
            font=(FUENTE, 9, "bold")
        )

        estilo.map(
            "Treeview",
            background=[
                ("selected", TARJETA_SECUNDARIA)
            ],
            foreground=[
                ("selected", TEXTO)
            ]
        )

        estilo.configure(
            "Dark.Vertical.TScrollbar",
            background=TARJETA_SECUNDARIA,
            troughcolor=SIDEBAR,
            bordercolor=SIDEBAR,
            arrowcolor=TEXTO_SECUNDARIO
        )

        estilo.map(
            "Dark.Vertical.TScrollbar",
            background=[
                ("active", ACENTO),
                ("pressed", ACENTO_HOVER)
            ]
        )


    # =====================================
    # INTERFAZ
    # =====================================

    def crear_interfaz(self):

        contenedor = tk.Frame(
            self.ventana,
            bg=FONDO
        )

        contenedor.pack(
            fill="both",
            expand=True
        )


        self.crear_sidebar(
            contenedor
        )


        self.crear_contenido(
            contenedor
        )


    # =====================================
    # SIDEBAR
    # =====================================

    def crear_sidebar(self, padre):

        self.sidebar = tk.Frame(
            padre,
            bg=SIDEBAR,
            width=260
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(
            False
        )


        # Logo

        logo = tk.Label(
            self.sidebar,
            text="HowMuchTime",
            bg=SIDEBAR,
            fg=TEXTO,
            font=(FUENTE, 18, "bold")
        )

        logo.pack(
            anchor="w",
            padx=28,
            pady=(32, 2)
        )


        subtitulo = tk.Label(
            self.sidebar,
            text="APPLICATION TRACKER",
            bg=SIDEBAR,
            fg=TEXTO_SECUNDARIO,
            font=(FUENTE, 8, "bold")
        )

        subtitulo.pack(
            anchor="w",
            padx=30,
            pady=(0, 35)
        )


        # Sección

        etiqueta = tk.Label(
            self.sidebar,
            text="OVERVIEW",
            bg=SIDEBAR,
            fg=TEXTO_SECUNDARIO,
            font=(FUENTE, 8, "bold")
        )

        etiqueta.pack(
            anchor="w",
            padx=30,
            pady=(0, 10)
        )

        self.crear_boton_sidebar(
            "Today",
            "Today"
        )

        self.crear_boton_sidebar(
            "This Week",
            "This Week"
        )

        self.crear_boton_sidebar(
            "This Month",
            "This Month"
        )


        # Separador

        separador = tk.Frame(
            self.sidebar,
            bg=BORDER,
            height=1
        )

        separador.pack(
            fill="x",
            padx=25,
            pady=30
        )


        # Estado

        estado_titulo = tk.Label(
            self.sidebar,
            text="TRACKING STATUS",
            bg=SIDEBAR,
            fg=TEXTO_SECUNDARIO,
            font=(FUENTE, 8, "bold")
        )

        estado_titulo.pack(
            anchor="w",
            padx=30
        )


        estado = tk.Frame(
            self.sidebar,
            bg=SIDEBAR
        )

        estado.pack(
            anchor="w",
            padx=30,
            pady=(10, 0)
        )


        self.punto_estado = tk.Label(
            estado,
            text="●",
            bg=SIDEBAR,
            fg=TEXTO_SECUNDARIO,
            font=(FUENTE, 11)
        )

        self.punto_estado.pack(
            side="left"
        )


        self.texto_estado = tk.Label(
            estado,
            text="Tracking inactive",
            bg=SIDEBAR,
            fg=TEXTO_SECUNDARIO,
            font=(FUENTE, 9)
        )

        self.texto_estado.pack(
            side="left",
            padx=7
        )


    # =====================================
    # BOTÓN SIDEBAR
    # =====================================

    def crear_boton_sidebar(
        self,
        texto,
        periodo
    ):

        boton = tk.Button(
            self.sidebar,
            text=texto,
            anchor="w",
            padx=30,
            pady=11,
            borderwidth=0,
            relief="flat",
            bg=SIDEBAR,
            fg=TEXTO_SECUNDARIO,
            activebackground=TARJETA_SECUNDARIA,
            activeforeground=TEXTO,
            font=(FUENTE, 10),
            cursor="hand2",
            command=lambda: self.cambiar_periodo(
                periodo
            )
        )

        boton.pack(
            fill="x",
            pady=2
        )

        self.botones_periodo[periodo] = boton


    # =====================================
    # AJUSTAR ANCHO DE APLICACIONES
    # =====================================

    def actualizar_ancho_apps(self, evento):

        self.canvas_apps.itemconfig(
            self.ventana_apps,
            width=evento.width
        )

    # =====================================
    # CONTENIDO
    # =====================================

    def crear_contenido(self, padre):

        contenido = tk.Frame(
            padre,
            bg=FONDO,
            padx=35,
            pady=30
        )

        contenido.pack(
            side="left",
            fill="both",
            expand=True
        )


        # ---------------------------------
        # HEADER
        # ---------------------------------

        header = tk.Frame(
            contenido,
            bg=FONDO
        )

        header.pack(
            fill="x",
            pady=(0, 28)
        )


        izquierda = tk.Frame(
            header,
            bg=FONDO
        )

        izquierda.pack(
            side="left"
        )


        self.titulo = tk.Label(
            izquierda,
            text="Today",
            bg=FONDO,
            fg=TEXTO,
            font=(FUENTE, 26, "bold")
        )

        self.titulo.pack(
            anchor="w"
        )


        self.fecha = tk.Label(
            izquierda,
            text="",
            bg=FONDO,
            fg=TEXTO_SECUNDARIO,
            font=(FUENTE, 10)
        )

        self.fecha.pack(
            anchor="w",
            pady=(4, 0)
        )


        self.boton_refresh = tk.Button(
            header,
            text="↻  Refresh",
            bg=TARJETA,
            fg=TEXTO,
            activebackground=TARJETA_SECUNDARIA,
            activeforeground=TEXTO,
            borderwidth=0,
            relief="flat",
            padx=18,
            pady=9,
            font=(FUENTE, 9, "bold"),
            cursor="hand2",
            command=self.actualizar_datos
        )

        self.boton_refresh.pack(
            side="right"
        )


        # ---------------------------------
        # TARJETAS
        # ---------------------------------

        tarjetas = tk.Frame(
            contenido,
            bg=FONDO
        )

        tarjetas.pack(
            fill="x",
            pady=(0, 28)
        )


        self.tarjeta_total = self.crear_tarjeta(
            tarjetas,
            "TOTAL USAGE"
        )

        self.tarjeta_total.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )


        self.tarjeta_sessions = self.crear_tarjeta(
            tarjetas,
            "SESSIONS"
        )

        self.tarjeta_sessions.pack(
            side="left",
            fill="both",
            expand=True,
            padx=8
        )


        self.tarjeta_app = self.crear_tarjeta(
            tarjetas,
            "MOST USED APP"
        )

        self.tarjeta_app.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(8, 0)
        )


        # ---------------------------------
        # USAGE OVERVIEW
        # ---------------------------------

        self.marco_grafico = self.crear_grafico(
            contenido
        )

        self.marco_grafico.pack(
            fill="x",
            pady=(0, 20)
        )

        self.marco_grafico.configure(
            height=170
        )

        self.marco_grafico.pack_propagate(
            False
        )


        # ---------------------------------
        # APPLICATIONS TITLE
        # ---------------------------------

        self.titulo_apps = tk.Label(
            contenido,
            text="TIME BY APPLICATION",
            bg=FONDO,
            fg=TEXTO,
            font=(FUENTE, 12, "bold")
        )

        self.titulo_apps.pack(
            anchor="w",
            pady=(0, 12)
        )


        # ---------------------------------
        # APPLICATIONS
        # ---------------------------------

        self.marco_apps = tk.Frame(
            contenido,
            bg=TARJETA,
            highlightthickness=1,
            highlightbackground=BORDER
        )

        self.marco_apps.pack(
            fill="both",
            expand=True
        )


        # ---------------------------------
        # CANVAS APPLICATIONS
        # ---------------------------------

        self.canvas_apps = tk.Canvas(
            self.marco_apps,
            bg=TARJETA,
            highlightthickness=0
        )

        self.scrollbar_apps = ttk.Scrollbar(
            self.marco_apps,
            orient="vertical",
            style="Dark.Vertical.TScrollbar",
            command=self.canvas_apps.yview
        )


        self.contenedor_apps = tk.Frame(
            self.canvas_apps,
            bg=TARJETA,
            padx=22,
            pady=14
        )


        self.contenedor_apps.bind(
            "<Configure>",
            lambda evento: self.canvas_apps.configure(
                scrollregion=self.canvas_apps.bbox("all")
            )
        )


        self.ventana_apps = self.canvas_apps.create_window(
            (0, 0),
            window=self.contenedor_apps,
            anchor="nw"
        )

        self.canvas_apps.bind(
            "<Configure>",
            self.actualizar_ancho_apps
        )


        self.canvas_apps.configure(
            yscrollcommand=self.scrollbar_apps.set
        )


        self.canvas_apps.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar_apps.pack(
            side="right",
            fill="y"
        )

    # =====================================
    # TARJETA
    # =====================================

    def crear_tarjeta(
        self,
        padre,
        titulo
    ):

        tarjeta = tk.Frame(
            padre,
            bg=TARJETA,
            padx=20,
            pady=18
        )


        etiqueta = tk.Label(
            tarjeta,
            text=titulo,
            bg=TARJETA,
            fg=TEXTO_SECUNDARIO,
            font=(FUENTE, 8, "bold")
        )

        etiqueta.pack(
            anchor="w"
        )


        valor = tk.Label(
            tarjeta,
            text="0",
            bg=TARJETA,
            fg=TEXTO,
            font=(FUENTE, 22, "bold")
        )

        valor.pack(
            anchor="w",
            pady=(8, 0)
        )


        tarjeta.valor = valor

        return tarjeta


    # =====================================
    # GRÁFICO DE USO
    # =====================================

    def crear_grafico(self, padre):

        marco = tk.Frame(
            padre,
            bg=TARJETA
        )

        titulo = tk.Label(
            marco,
            text="USAGE OVERVIEW",
            bg=TARJETA,
            fg=TEXTO,
            font=(FUENTE, 12, "bold")
        )

        titulo.pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.grafico = tk.Canvas(
            marco,
            bg=TARJETA,
            highlightthickness=0,
            height=120
        )

        self.grafico.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        return marco


    # =====================================
    # DIBUJAR GRÁFICO
    # =====================================

    def dibujar_grafico(self):

        self.grafico.delete("all")

        if self.periodo_actual == "Today":

            fecha = datetime.now().strftime(
                "%Y-%m-%d"
            )

            datos = obtener_tiempo_por_dia(
                fecha,
                fecha
            )

        elif self.periodo_actual == "This Week":

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

            datos = obtener_tiempo_por_dia(
                fecha_inicio,
                fecha_fin
            )

        else:

            hoy = datetime.now().date()

            fecha_inicio = hoy.replace(
                day=1
            ).strftime("%Y-%m-%d")

            if hoy.month == 12:

                siguiente_mes = hoy.replace(
                    year=hoy.year + 1,
                    month=1,
                    day=1
                )

            else:

                siguiente_mes = hoy.replace(
                    month=hoy.month + 1,
                    day=1
                )

            fecha_fin = (
                siguiente_mes - timedelta(days=1)
            ).strftime("%Y-%m-%d")

            datos = obtener_tiempo_por_dia(
                fecha_inicio,
                fecha_fin
            )


        ancho = self.grafico.winfo_width()
        alto = self.grafico.winfo_height()

        if ancho <= 1 or alto <= 1:

            self.ventana.after(
                100,
                self.dibujar_grafico
            )

            return


        # ---------------------------------
        # SIN DATOS
        # ---------------------------------

        if not datos:

            self.grafico.create_text(
                ancho // 2,
                alto // 2,
                text="No usage data available.",
                fill=TEXTO_SECUNDARIO,
                font=(FUENTE, 10)
            )

            return


        # ---------------------------------
        # DATOS
        # ---------------------------------

        datos_dict = dict(datos)

        fechas = []

        if self.periodo_actual == "Today":

            fechas = [
                datetime.now().strftime("%Y-%m-%d")
            ]

        elif self.periodo_actual == "This Week":

            inicio = datetime.now().date() - timedelta(
                days=datetime.now().date().weekday()
            )

            for i in range(7):

                fecha = inicio + timedelta(days=i)

                fechas.append(
                    fecha.strftime("%Y-%m-%d")
                )

        else:

            inicio = datetime.now().date().replace(
                day=1
            )

            if inicio.month == 12:

                siguiente = inicio.replace(
                    year=inicio.year + 1,
                    month=1
                )

            else:

                siguiente = inicio.replace(
                    month=inicio.month + 1
                )

            dias_mes = (
                siguiente - inicio
            ).days

            for i in range(dias_mes):

                fecha = inicio + timedelta(days=i)

                fechas.append(
                    fecha.strftime("%Y-%m-%d")
                )


        valores = []

        for fecha in fechas:

            valores.append(
                datos_dict.get(fecha, 0)
            )


        maximo = max(valores)

        if maximo == 0:

            maximo = 1


        # ---------------------------------
        # MÁRGENES
        # ---------------------------------

        margen_izquierda = 55
        margen_derecha = 20
        margen_arriba = 20
        margen_abajo = 35

        area_ancho = (
            ancho
            - margen_izquierda
            - margen_derecha
        )

        area_alto = (
            alto
            - margen_arriba
            - margen_abajo
        )


        # ---------------------------------
        # LÍNEA BASE
        # ---------------------------------

        self.grafico.create_line(
            margen_izquierda,
            alto - margen_abajo,
            ancho - margen_derecha,
            alto - margen_abajo,
            fill=BORDER
        )


        # ---------------------------------
        # BARRAS
        # ---------------------------------

        cantidad = len(fechas)

        espacio = area_ancho / cantidad

        ancho_barra = min(
            espacio * 0.55,
            45
        )

        for i, valor in enumerate(valores):

            x_centro = (
                margen_izquierda
                + espacio * i
                + espacio / 2
            )

            altura = (
                valor / maximo
            ) * area_alto

            x1 = x_centro - ancho_barra / 2
            x2 = x_centro + ancho_barra / 2

            y1 = (
                alto
                - margen_abajo
                - altura
            )

            y2 = (
                alto
                - margen_abajo
            )

            if valor > 0:

                self.grafico.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=ACENTO,
                    outline=""
                )


            # Etiqueta

            if self.periodo_actual == "This Week":

                nombre_dia = (
                    datetime.strptime(
                        fechas[i],
                        "%Y-%m-%d"
                    ).strftime("%a")
                )

                texto = nombre_dia

            elif self.periodo_actual == "This Month":

                texto = str(
                    datetime.strptime(
                        fechas[i],
                        "%Y-%m-%d"
                    ).day
                )

            else:

                texto = "Today"


            self.grafico.create_text(
                x_centro,
                alto - 15,
                text=texto,
                fill=TEXTO_SECUNDARIO,
                font=(FUENTE, 8)
            )


            # Tiempo encima de la barra

            if valor > 0:

                self.grafico.create_text(
                    x_centro,
                    y1 - 8,
                    text=formatear_tiempo(valor),
                    fill=TEXTO,
                    font=(FUENTE, 8)
                )


    # =====================================
    # MOSTRAR / OCULTAR GRÁFICO
    # =====================================

    def actualizar_visibilidad_grafico(self):

        if self.periodo_actual == "Today":

            self.marco_grafico.pack_forget()

        else:

            self.marco_grafico.pack(
                before=self.titulo_apps,
                fill="x",
                pady=(0, 20)
            )

            self.marco_grafico.configure(
                height=170
            )

            self.marco_grafico.pack_propagate(False)


    # =====================================
    # CAMBIAR PERIODO
    # =====================================

    def cambiar_periodo(
        self,
        periodo
    ):

        self.periodo_actual = periodo

        self.actualizar_visibilidad_grafico()

        self.actualizar_datos()

        if periodo != "Today":
            self.ventana.after(
                100,
                self.dibujar_grafico
            )

    # =====================================
    # COMPROBAR ESTADO DEL TRACKER
    # =====================================

    def actualizar_estado_tracker(self):

        if tracker_activo():

            self.texto_estado.config(
                text="Tracking active",
                fg="#4ADE80"
            )

            self.punto_estado.config(
                fg="#4ADE80"
            )

        else:

            self.texto_estado.config(
                text="Tracking inactive",
                fg=TEXTO_SECUNDARIO
            )

            self.punto_estado.config(
                fg=TEXTO_SECUNDARIO
            )

        # Volver a comprobar dentro de 1 segundo
        self.ventana.after(
            1000,
            self.actualizar_estado_tracker
        )


    # =====================================
    # ACTUALIZAR DATOS
    # =====================================

    def actualizar_datos(self):

        (
            sesiones,
            tiempo_total,
            aplicaciones
        ) = obtener_datos(
            self.periodo_actual
        )

        # ---------------------------------
        # HEADER
        # ---------------------------------

        self.titulo.config(
            text=self.periodo_actual
        )


        self.fecha.config(
            text=datetime.now().strftime(
                "%A, %B %d, %Y"
            )
        )


        # ---------------------------------
        # SIDEBAR ACTIVO
        # ---------------------------------

        for periodo, boton in self.botones_periodo.items():

            if periodo == self.periodo_actual:

                boton.config(
                    bg=ACENTO,
                    fg="white",
                    activebackground=ACENTO_HOVER,
                    activeforeground="white"
                )

            else:

                boton.config(
                    bg=SIDEBAR,
                    fg=TEXTO_SECUNDARIO,
                    activebackground=TARJETA_SECUNDARIA,
                    activeforeground=TEXTO
                )


        # ---------------------------------
        # TARJETA TOTAL
        # ---------------------------------

        self.tarjeta_total.valor.config(
            text=formatear_tiempo(
                tiempo_total
            )
        )


        # ---------------------------------
        # TARJETA SESIONES
        # ---------------------------------

        self.tarjeta_sessions.valor.config(
            text=str(len(sesiones))
        )


        # ---------------------------------
        # APP MÁS USADA
        # ---------------------------------

        if aplicaciones:

            aplicacion = aplicaciones[0][0]

            self.tarjeta_app.valor.config(
                text=aplicacion,
                font=(FUENTE, 14, "bold")
            )

        else:

            self.tarjeta_app.valor.config(
                text="No data",
                font=(FUENTE, 14, "bold")
            )


        # ---------------------------------
        # LIMPIAR APLICACIONES
        # ---------------------------------

        for widget in self.contenedor_apps.winfo_children():

            widget.destroy()


        # ---------------------------------
        # SIN DATOS
        # ---------------------------------

        if not aplicaciones:

            mensaje = tk.Label(
                self.contenedor_apps,
                text="No application data available.",
                bg=TARJETA,
                fg=TEXTO_SECUNDARIO,
                font=(FUENTE, 10)
            )

            mensaje.pack(
                pady=30
            )

            return


        # ---------------------------------
        # APLICACIONES
        # ---------------------------------

        for indice, (
            aplicacion,
            segundos
        ) in enumerate(aplicaciones):

            porcentaje = 0

            if tiempo_total > 0:

                porcentaje = (
                    segundos / tiempo_total
                ) * 100

            self.crear_fila_aplicacion(
                aplicacion,
                segundos,
                porcentaje
            )


    # =====================================
    # FILA DE APLICACIÓN
    # =====================================

    def crear_fila_aplicacion(
        self,
        aplicacion,
        segundos,
        porcentaje
    ):

        # ---------------------------------
        # CONTENEDOR DE LA APLICACIÓN
        # ---------------------------------

        fila = tk.Frame(
            self.contenedor_apps,
            bg=TARJETA
        )

        fila.pack(
            fill="x",
            pady=(4, 8)
        )


        # ---------------------------------
        # CABECERA DE LA FILA
        # ---------------------------------

        cabecera = tk.Frame(
            fila,
            bg=TARJETA
        )

        cabecera.pack(
            fill="x"
        )


        # ---------------------------------
        # NOMBRE
        # ---------------------------------

        nombre = tk.Label(
            cabecera,
            text=aplicacion,
            bg=TARJETA,
            fg=TEXTO,
            font=(FUENTE, 10, "bold")
        )

        nombre.pack(
            side="left"
        )


        # ---------------------------------
        # TIEMPO
        # ---------------------------------

        tiempo = tk.Label(
            cabecera,
            text=formatear_tiempo(segundos),
            bg=TARJETA,
            fg=TEXTO,
            font=(FUENTE, 10, "bold")
        )

        tiempo.pack(
            side="right"
        )


        # ---------------------------------
        # PORCENTAJE
        # ---------------------------------

        porcentaje_label = tk.Label(
            cabecera,
            text=f"{porcentaje:.1f}%",
            bg=TARJETA,
            fg=TEXTO_SECUNDARIO,
            font=(FUENTE, 9)
        )

        porcentaje_label.pack(
            side="right",
            padx=(0, 25)
        )


        # ---------------------------------
        # BARRA DE FONDO
        # ---------------------------------

        marco_barra = tk.Frame(
            fila,
            bg=BARRA_FONDO,
            height=7
        )

        marco_barra.pack(
            fill="x",
            pady=(7, 0)
        )

        marco_barra.pack_propagate(False)


        # ---------------------------------
        # BARRA DE USO
        # ---------------------------------

        barra = tk.Frame(
            marco_barra,
            bg=ACENTO,
            height=7
        )

        self.ventana.update_idletasks()

        ancho = marco_barra.winfo_width()

        if ancho <= 1:
            ancho = 700

        anchura_barra = int(
            ancho * porcentaje / 100
        )

        # Evitar barras microscópicas
        if porcentaje > 0 and anchura_barra < 4:
            anchura_barra = 4

        barra.place(
            x=0,
            y=0,
            width=anchura_barra,
            height=7
        )


# =========================================
# INICIO
# =========================================

crear_base_datos()

ventana = tk.Tk()

app = HowMuchTimeApp(
    ventana
)

ventana.mainloop()