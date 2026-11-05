import random
import tkinter as tk
from tkinter import messagebox


class HundirLaFlota:

    def __init__(self):
        self.flota = {4: 1, 3: 2, 2: 3, 1: 4}
        self.tam_tablero = 10
        self.letras = "ABCDEFGHIJ"

        self.tablero = self.crear_matriz(0)
        self.impactos = self.crear_matriz(0)
        self.ataques = self.crear_matriz("X")
        self.barcos = []

        self.total_barcos = 0
        for tamano in self.flota:
            self.total_barcos = self.total_barcos + self.flota[tamano]

        self.mis_hundidos = 0
        self.rival_hundidos = 0
        self.modo = ""
        self.casilla_marcada = None
        self.casilla_pista = None
        self.fin_partida = False

        self.colocar_flota()

        self.celda = 36
        self.margen = 30
        self.color_fondo = "#0b1e33"
        self.color_panel = "#132f4c"
        self.color_texto = "#e8f1f8"
        self.color_agua1 = "#1b6ca8"
        self.color_agua2 = "#1f78b8"
        self.color_tocado = "#ffd400"
        self.color_hundido = "#ff3b30"
        self.color_barcos = {4: "#2ecc71", 3: "#e0a030", 2: "#b06ad4", 1: "#55b6f2"}

        self.crear_ventana()
        self.dibujar_tableros()


    def crear_matriz(self, valor):
        matriz = []
        for fila in range(self.tam_tablero):
            lista_fila = []
            for columna in range(self.tam_tablero):
                lista_fila.append(valor)
            matriz.append(lista_fila)
        return matriz

    def colocar_flota(self):
        for tamano in self.flota:
            for i in range(self.flota[tamano]):
                self.colocar_barco(tamano)

    def colocar_barco(self, tamano):
        colocado = False
        while not colocado:
            horizontal = random.choice([True, False])
            if horizontal:
                fila = random.randint(0, self.tam_tablero - 1)
                columna = random.randint(0, self.tam_tablero - tamano)
            else:
                fila = random.randint(0, self.tam_tablero - tamano)
                columna = random.randint(0, self.tam_tablero - 1)

            casillas = []
            libre = True
            for i in range(tamano):
                if horizontal:
                    casillas.append([fila, columna + i])
                else:
                    casillas.append([fila + i, columna])
                if self.tablero[casillas[i][0]][casillas[i][1]] != 0:
                    libre = False

            if libre:
                for casilla in casillas:
                    self.tablero[casilla[0]][casilla[1]] = tamano
                self.barcos.append(casillas)
                colocado = True

    def leer_coordenada(self, texto):
        texto = texto.strip().upper()
        if len(texto) < 2:
            return None
        letra = texto[0]
        numero = texto[1:]
        if letra not in self.letras or not numero.isdigit():
            return None
        numero = int(numero)
        if numero < 1 or numero > self.tam_tablero:
            return None
        return [numero - 1, self.letras.index(letra)]

    def nombre_casilla(self, fila, columna):
        return self.letras[columna] + str(fila + 1)

    def buscar_barco(self, fila, columna):
        for barco in self.barcos:
            if [fila, columna] in barco:
                return barco
        return None

    def barco_hundido(self, barco):
        for casilla in barco:
            if self.impactos[casilla[0]][casilla[1]] == 0:
                return False
        return True

    def recibir_ataque(self, fila, columna):
        repetido = self.impactos[fila][columna] == 1
        self.impactos[fila][columna] = 1

        if self.tablero[fila][columna] == 0:
            return "AGUA"

        barco = self.buscar_barco(fila, columna)
        if self.barco_hundido(barco):
            if not repetido:
                self.mis_hundidos = self.mis_hundidos + 1
            return "HUNDIDO"
        return "TOCADO"

    def apuntar_ataque(self, fila, columna, resultado):
        if resultado == "AGUA":
            self.ataques[fila][columna] = "0"
        elif resultado == "TOCADO":
            self.ataques[fila][columna] = "1"
        else:
            self.ataques[fila][columna] = "H"
            self.rival_hundidos = self.rival_hundidos + 1
            direcciones = [[0, 1], [0, -1], [1, 0], [-1, 0]]
            for direccion in direcciones:
                f = fila + direccion[0]
                c = columna + direccion[1]
                while self.dentro(f, c) and (self.ataques[f][c] == "1" or self.ataques[f][c] == "H"):
                    self.ataques[f][c] = "H"
                    f = f + direccion[0]
                    c = c + direccion[1]

    def dentro(self, fila, columna):
        return 0 <= fila < self.tam_tablero and 0 <= columna < self.tam_tablero

    def calcular_pista(self):
        puntos = self.crear_matriz(0)
        for tamano in self.flota:
            for fila in range(self.tam_tablero):
                for columna in range(self.tam_tablero):
                    self.sumar_puntos(puntos, fila, columna, tamano, 0, 1)
                    self.sumar_puntos(puntos, fila, columna, tamano, 1, 0)

        mejor = None
        mejor_puntos = 0
        for fila in range(self.tam_tablero):
            for columna in range(self.tam_tablero):
                if self.ataques[fila][columna] == "X" and puntos[fila][columna] > mejor_puntos:
                    mejor_puntos = puntos[fila][columna]
                    mejor = [fila, columna]
        return mejor

    def sumar_puntos(self, puntos, fila, columna, tamano, paso_fila, paso_columna):
        casillas = []
        tocados = 0
        for i in range(tamano):
            f = fila + paso_fila * i
            c = columna + paso_columna * i
            if not self.dentro(f, c):
                return
            if self.ataques[f][c] == "0" or self.ataques[f][c] == "H":
                return
            if self.ataques[f][c] == "1":
                tocados = tocados + 1
            casillas.append([f, c])

        for casilla in casillas:
            puntos[casilla[0]][casilla[1]] = puntos[casilla[0]][casilla[1]] + 1 + 20 * tocados


    def crear_ventana(self):
        self.ventana = tk.Tk()
        self.ventana.title("Hundir la flota")
        self.ventana.configure(bg=self.color_fondo)
        self.ventana.resizable(False, False)

        titulo = tk.Label(self.ventana, text="HUNDIR LA FLOTA", bg=self.color_fondo,
                          fg=self.color_texto, font=("Impact", 30))
        titulo.grid(row=0, column=0, columnspan=3, pady=(12, 4))

        lado = self.margen + self.celda * self.tam_tablero + 4

        tk.Label(self.ventana, text="MIS BARCOS", bg=self.color_fondo, fg="#7fd1ff",
                 font=("Arial", 13, "bold")).grid(row=1, column=0)
        self.canvas_barcos = tk.Canvas(self.ventana, width=lado, height=lado,
                                       bg=self.color_fondo, highlightthickness=0)
        self.canvas_barcos.grid(row=2, column=0, padx=(16, 8), pady=4)
        self.canvas_barcos.bind("<Button-1>", self.clic_barcos)

        tk.Label(self.ventana, text="MIS ATAQUES", bg=self.color_fondo, fg="#ff9d7f",
                 font=("Arial", 13, "bold")).grid(row=1, column=1)
        self.canvas_ataques = tk.Canvas(self.ventana, width=lado, height=lado,
                                        bg=self.color_fondo, highlightthickness=0)
        self.canvas_ataques.grid(row=2, column=1, padx=8, pady=4)
        self.canvas_ataques.bind("<Button-1>", self.clic_ataques)
        self.canvas_ataques.bind("<Motion>", self.mover_raton)
        self.canvas_ataques.bind("<Leave>", self.salir_raton)

        self.crear_panel()
        self.crear_parte_inferior()
        self.ventana.grid_rowconfigure(3, weight=1)

    def crear_boton(self, padre, texto, comando, color):
        boton = tk.Button(padre, text=texto, command=comando, bg=color, fg="white",
                          activebackground=self.color_agua2, activeforeground="white",
                          relief="flat", font=("Arial", 11, "bold"), cursor="hand2", pady=5)
        return boton

    def crear_panel(self):
        panel = tk.Frame(self.ventana, bg=self.color_panel, width=270, padx=12, pady=10)
        panel.grid(row=1, column=2, rowspan=3, sticky="ns", padx=(8, 16), pady=(0, 14))

        tk.Label(panel, text="MENÚ", bg=self.color_panel, fg=self.color_texto,
                 font=("Arial", 15, "bold")).pack(pady=(0, 6))

        self.boton1 = self.crear_boton(panel, "1. Coordenadas para atacar", self.opcion_atacar, "#1f78b8")
        self.boton1.pack(fill="x", pady=2)
        self.boton2 = self.crear_boton(panel, "2. Ataque recibido", self.opcion_recibido, "#1f78b8")
        self.boton2.pack(fill="x", pady=2)
        self.crear_boton(panel, "3. Visualizar mapas", self.opcion_mapas, "#1f78b8").pack(fill="x", pady=2)
        self.crear_boton(panel, "4. Salir", self.opcion_salir, "#a83232").pack(fill="x", pady=2)

        zona = tk.Frame(panel, bg=self.color_panel, height=190, width=246)
        zona.pack(pady=8)
        zona.pack_propagate(False)

        self.texto_ayuda = tk.Label(zona, text="Elige una opción del menú", bg=self.color_panel,
                                    fg=self.color_texto, font=("Arial", 10), wraplength=240)
        self.texto_ayuda.pack(pady=(4, 6))

        self.entrada = tk.Entry(zona, font=("Consolas", 16, "bold"), justify="center", width=6)
        self.entrada.bind("<KeyRelease>", self.tecla_entrada)
        self.entrada.bind("<Return>", self.pulsar_intro)

        self.zona_resultado = tk.Frame(zona, bg=self.color_panel)
        self.crear_boton(self.zona_resultado, "Agua", self.resultado_agua, "#1b6ca8").pack(side="left", expand=True, fill="x", padx=1)
        self.crear_boton(self.zona_resultado, "Tocado", self.resultado_tocado, "#b8930a").pack(side="left", expand=True, fill="x", padx=1)
        self.crear_boton(self.zona_resultado, "Hundido", self.resultado_hundido, "#c0392b").pack(side="left", expand=True, fill="x", padx=1)
        self.boton_pista = self.crear_boton(zona, "Pista de la IA", self.pedir_pista, "#1e8449")

        self.boton_comprobar = self.crear_boton(zona, "Comprobar", self.comprobar_recibido, "#1e8449")

        self.texto_resultado = tk.Label(panel, text="", bg=self.color_panel, fg=self.color_texto,
                                        font=("Impact", 24))
        self.texto_resultado.pack()

        tk.Label(panel, text="Historial", bg=self.color_panel, fg=self.color_texto,
                 font=("Arial", 10, "bold")).pack(pady=(6, 0))
        self.historial = tk.Listbox(panel, height=6, bg=self.color_fondo, fg=self.color_texto,
                                    font=("Consolas", 10), relief="flat", highlightthickness=0)
        self.historial.pack(fill="x")

    def crear_parte_inferior(self):
        abajo = tk.Frame(self.ventana, bg=self.color_fondo)
        abajo.grid(row=3, column=0, columnspan=2, pady=(2, 14))

        self.marcador = tk.Label(abajo, text="", bg=self.color_fondo, fg=self.color_texto,
                                 font=("Arial", 12, "bold"))
        self.marcador.pack()

        leyenda = tk.Canvas(abajo, width=420, height=38, bg=self.color_fondo, highlightthickness=0)
        leyenda.pack()
        self.dibujar_agua_atacada(leyenda, 8, 1)
        leyenda.create_text(50, 19, text="Agua", fill=self.color_texto, anchor="w", font=("Arial", 10))
        self.dibujar_x(leyenda, 130, 1, self.color_tocado)
        leyenda.create_text(172, 19, text="Tocado", fill=self.color_texto, anchor="w", font=("Arial", 10))
        self.dibujar_x(leyenda, 260, 1, self.color_hundido)
        leyenda.create_text(302, 19, text="Hundido", fill=self.color_texto, anchor="w", font=("Arial", 10))


    def dibujar_tableros(self):
        self.dibujar_mis_barcos()
        self.dibujar_mis_ataques()
        self.marcador.config(text="Mis barcos a flote: " + str(self.total_barcos - self.mis_hundidos)
                             + "/" + str(self.total_barcos)
                             + "      Barcos rivales hundidos: " + str(self.rival_hundidos)
                             + "/" + str(self.total_barcos))

    def dibujar_rejilla(self, canvas):
        canvas.delete("all")
        for i in range(self.tam_tablero):
            x = self.margen + self.celda * i + self.celda / 2
            canvas.create_text(x, 14, text=self.letras[i], fill=self.color_texto, font=("Arial", 12, "bold"))
            canvas.create_text(14, x, text=str(i + 1), fill=self.color_texto, font=("Arial", 12, "bold"))

        for fila in range(self.tam_tablero):
            for columna in range(self.tam_tablero):
                x = self.margen + self.celda * columna
                y = self.margen + self.celda * fila
                if (fila + columna) % 2 == 0:
                    color = self.color_agua1
                else:
                    color = self.color_agua2
                canvas.create_rectangle(x, y, x + self.celda, y + self.celda, fill=color, outline="#134f7d")

    def dibujar_barco(self, canvas, barco):
        color = self.color_barcos[len(barco)]
        primera = barco[0]
        ultima = barco[len(barco) - 1]
        x1 = self.margen + self.celda * primera[1]
        y1 = self.margen + self.celda * primera[0]
        x2 = self.margen + self.celda * (ultima[1] + 1)
        y2 = self.margen + self.celda * (ultima[0] + 1)

        if primera[0] == ultima[0] and len(barco) > 1:
            medio = (y1 + y2) / 2
            puntos = [x1 + 4, y1 + 8, x2 - 12, y1 + 8, x2 - 2, medio, x2 - 12, y2 - 8, x1 + 4, y2 - 8]
        else:
            medio = (x1 + x2) / 2
            puntos = [x1 + 8, y1 + 4, x2 - 8, y1 + 4, x2 - 8, y2 - 12, medio, y2 - 2, x1 + 8, y2 - 12]
        canvas.create_polygon(puntos, fill=color, outline="#0b1e33", width=2)

        for casilla in barco:
            cx = self.margen + self.celda * casilla[1] + self.celda / 2
            cy = self.margen + self.celda * casilla[0] + self.celda / 2
            canvas.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, fill="#0b1e33", outline="")

    def dibujar_x(self, canvas, x, y, color):
        canvas.create_oval(x + 5, y + 5, x + self.celda - 5, y + self.celda - 5, fill="#10202e", outline="")
        canvas.create_line(x + 10, y + 10, x + self.celda - 10, y + self.celda - 10, fill=color, width=4)
        canvas.create_line(x + self.celda - 10, y + 10, x + 10, y + self.celda - 10, fill=color, width=4)

    def dibujar_agua_atacada(self, canvas, x, y):
        canvas.create_oval(x + 8, y + 8, x + self.celda - 8, y + self.celda - 8, outline="white", width=2)
        canvas.create_oval(x + 15, y + 15, x + self.celda - 15, y + self.celda - 15, fill="white", outline="")

    def dibujar_mis_barcos(self):
        canvas = self.canvas_barcos
        self.dibujar_rejilla(canvas)

        for barco in self.barcos:
            self.dibujar_barco(canvas, barco)

        for fila in range(self.tam_tablero):
            for columna in range(self.tam_tablero):
                if self.impactos[fila][columna] == 1:
                    x = self.margen + self.celda * columna
                    y = self.margen + self.celda * fila
                    if self.tablero[fila][columna] == 0:
                        self.dibujar_agua_atacada(canvas, x, y)
                    elif self.barco_hundido(self.buscar_barco(fila, columna)):
                        self.dibujar_x(canvas, x, y, self.color_hundido)
                    else:
                        self.dibujar_x(canvas, x, y, self.color_tocado)

        if self.modo == "recibido":
            self.dibujar_marca(canvas, self.casilla_marcada, "white")

    def dibujar_mis_ataques(self):
        canvas = self.canvas_ataques
        self.dibujar_rejilla(canvas)

        for fila in range(self.tam_tablero):
            for columna in range(self.tam_tablero):
                x = self.margen + self.celda * columna
                y = self.margen + self.celda * fila
                if self.ataques[fila][columna] == "0":
                    self.dibujar_agua_atacada(canvas, x, y)
                elif self.ataques[fila][columna] == "1":
                    self.dibujar_x(canvas, x, y, self.color_tocado)
                elif self.ataques[fila][columna] == "H":
                    self.dibujar_x(canvas, x, y, self.color_hundido)

        self.dibujar_marca(canvas, self.casilla_pista, "#2ecc71")
        if self.modo == "atacar":
            self.dibujar_marca(canvas, self.casilla_marcada, "white")

    def dibujar_marca(self, canvas, casilla, color):
        if casilla is not None:
            x = self.margen + self.celda * casilla[1]
            y = self.margen + self.celda * casilla[0]
            canvas.create_rectangle(x + 2, y + 2, x + self.celda - 2, y + self.celda - 2, outline=color, width=3)

    def animar_disparo(self, canvas, fila, columna, color, radio):
        canvas.delete("disparo")
        if radio <= 24:
            cx = self.margen + self.celda * columna + self.celda / 2
            cy = self.margen + self.celda * fila + self.celda / 2
            canvas.create_oval(cx - radio, cy - radio, cx + radio, cy + radio,
                               outline=color, width=3, tags="disparo")
            self.ventana.after(30, self.animar_disparo, canvas, fila, columna, color, radio + 3)

    def mostrar_resultado(self, resultado):
        if resultado == "AGUA":
            self.texto_resultado.config(text="¡AGUA!", fg="#7fd1ff")
        elif resultado == "TOCADO":
            self.texto_resultado.config(text="¡TOCADO!", fg=self.color_tocado)
        else:
            self.texto_resultado.config(text="¡HUNDIDO!", fg=self.color_hundido)

    def color_resultado(self, resultado):
        if resultado == "AGUA":
            return "white"
        if resultado == "TOCADO":
            return self.color_tocado
        return self.color_hundido


    def preparar_modo(self, modo, ayuda):
        self.modo = modo
        self.casilla_marcada = None
        self.texto_ayuda.config(text=ayuda)
        self.texto_resultado.config(text="")
        self.entrada.pack_forget()
        self.zona_resultado.pack_forget()
        self.boton_pista.pack_forget()
        self.boton_comprobar.pack_forget()

        if modo != "":
            self.entrada.delete(0, "end")
            self.entrada.pack(pady=4)
            self.entrada.focus_set()
        self.dibujar_tableros()

    def opcion_atacar(self):
        self.preparar_modo("atacar", "Di la casilla a tu rival (clic en MIS ATAQUES o escríbela, ej: B7) "
                                     "y marca lo que te conteste:")
        self.zona_resultado.pack(fill="x", pady=4)
        self.boton_pista.pack(fill="x", pady=4)

    def opcion_recibido(self):
        self.preparar_modo("recibido", "Escribe la casilla que te ha dicho tu rival (o haz clic en MIS BARCOS):")
        self.boton_comprobar.pack(fill="x", pady=4)

    def opcion_mapas(self):
        ventana_mapas = tk.Toplevel(self.ventana)
        ventana_mapas.title("Mapas")
        ventana_mapas.configure(bg="#1e1e1e", padx=20, pady=14)
        texto = "Tablero del jugador:\n" + self.texto_mis_barcos()
        texto = texto + "\nTablero de ataques:\n" + self.texto_mis_ataques()
        texto = texto + "\nEn mi tablero: x tocado, H hundido, * agua atacada"
        texto = texto + "\nEn mis ataques: X sin atacar, 0 agua, 1 tocado, H hundido"
        tk.Label(ventana_mapas, text=texto, bg="#1e1e1e", fg="white", justify="left",
                 font=("Consolas", 11)).pack()

    def texto_cabecera(self):
        texto = "    "
        for letra in self.letras:
            texto = texto + letra + " "
        return texto + "\n"

    def texto_mis_barcos(self):
        texto = self.texto_cabecera()
        for fila in range(self.tam_tablero):
            texto = texto + str(fila + 1).rjust(2) + "  "
            for columna in range(self.tam_tablero):
                if self.impactos[fila][columna] == 0:
                    texto = texto + str(self.tablero[fila][columna]) + " "
                elif self.tablero[fila][columna] == 0:
                    texto = texto + "* "
                elif self.barco_hundido(self.buscar_barco(fila, columna)):
                    texto = texto + "H "
                else:
                    texto = texto + "x "
            texto = texto + "\n"
        return texto

    def texto_mis_ataques(self):
        texto = self.texto_cabecera()
        for fila in range(self.tam_tablero):
            texto = texto + str(fila + 1).rjust(2) + "  "
            for columna in range(self.tam_tablero):
                texto = texto + self.ataques[fila][columna] + " "
            texto = texto + "\n"
        return texto

    def opcion_salir(self):
        if self.fin_partida or messagebox.askyesno("Salir", "¿Seguro que quieres salir del juego?"):
            self.ventana.destroy()


    def resultado_agua(self):
        self.registrar_ataque("AGUA")

    def resultado_tocado(self):
        self.registrar_ataque("TOCADO")

    def resultado_hundido(self):
        self.registrar_ataque("HUNDIDO")

    def registrar_ataque(self, resultado):
        casilla = self.leer_coordenada(self.entrada.get())
        if casilla is None:
            messagebox.showwarning("Casilla no válida", "Escribe una casilla de A1 a J10, por ejemplo B7")
            return
        fila = casilla[0]
        columna = casilla[1]
        if self.ataques[fila][columna] != "X":
            messagebox.showwarning("Casilla repetida", "Ya has atacado esa casilla")
            return

        self.apuntar_ataque(fila, columna, resultado)
        self.anotar_historial("Yo -> " + self.nombre_casilla(fila, columna) + ": " + resultado)
        self.casilla_marcada = None
        self.casilla_pista = None
        self.entrada.delete(0, "end")
        self.dibujar_tableros()
        self.mostrar_resultado(resultado)
        self.animar_disparo(self.canvas_ataques, fila, columna, self.color_resultado(resultado), 4)

        if self.rival_hundidos == self.total_barcos:
            self.terminar_partida("¡HAS GANADO!", "Has hundido todos los barcos del rival.")

    def pedir_pista(self):
        self.casilla_pista = self.calcular_pista()
        if self.casilla_pista is not None:
            nombre = self.nombre_casilla(self.casilla_pista[0], self.casilla_pista[1])
            self.texto_ayuda.config(text="La IA cree que lo más probable es " + nombre + " (en verde). "
                                         "Di la casilla a tu rival y marca lo que te conteste:")
            self.entrada.delete(0, "end")
            self.entrada.insert(0, nombre)
        self.dibujar_tableros()

    def comprobar_recibido(self):
        casilla = self.leer_coordenada(self.entrada.get())
        if casilla is None:
            messagebox.showwarning("Casilla no válida", "Escribe una casilla de A1 a J10, por ejemplo B7")
            return
        fila = casilla[0]
        columna = casilla[1]

        repetido = self.impactos[fila][columna] == 1
        resultado = self.recibir_ataque(fila, columna)
        texto = "Rival -> " + self.nombre_casilla(fila, columna) + ": " + resultado
        if repetido:
            texto = texto + " (rep.)"
        self.anotar_historial(texto)
        self.casilla_marcada = None
        self.entrada.delete(0, "end")
        self.dibujar_tableros()
        self.mostrar_resultado(resultado)
        self.animar_disparo(self.canvas_barcos, fila, columna, self.color_resultado(resultado), 4)

        if self.mis_hundidos == self.total_barcos:
            self.terminar_partida("HAS PERDIDO", "Te han hundido todos los barcos.")

    def anotar_historial(self, texto):
        self.historial.insert(0, texto)

    def terminar_partida(self, titulo, mensaje):
        self.fin_partida = True
        self.preparar_modo("", titulo)
        self.texto_resultado.config(text=titulo, fg=self.color_tocado, font=("Impact", 20))
        self.boton1.config(state="disabled")
        self.boton2.config(state="disabled")
        messagebox.showinfo(titulo, mensaje)


    def casilla_del_raton(self, evento):
        columna = (evento.x - self.margen) // self.celda
        fila = (evento.y - self.margen) // self.celda
        if self.dentro(fila, columna):
            return [fila, columna]
        return None

    def elegir_casilla(self, casilla):
        self.entrada.delete(0, "end")
        self.entrada.insert(0, self.nombre_casilla(casilla[0], casilla[1]))
        self.casilla_marcada = casilla
        self.dibujar_tableros()

    def clic_barcos(self, evento):
        casilla = self.casilla_del_raton(evento)
        if self.modo == "recibido" and casilla is not None:
            self.elegir_casilla(casilla)

    def clic_ataques(self, evento):
        casilla = self.casilla_del_raton(evento)
        if self.modo == "atacar" and casilla is not None:
            self.elegir_casilla(casilla)

    def mover_raton(self, evento):
        self.canvas_ataques.delete("raton")
        casilla = self.casilla_del_raton(evento)
        if self.modo == "atacar" and casilla is not None:
            x = self.margen + self.celda * casilla[1]
            y = self.margen + self.celda * casilla[0]
            self.canvas_ataques.create_rectangle(x + 1, y + 1, x + self.celda - 1, y + self.celda - 1,
                                                 outline="#ffffff", width=2, tags="raton")

    def salir_raton(self, evento):
        self.canvas_ataques.delete("raton")

    def tecla_entrada(self, evento):
        self.casilla_marcada = self.leer_coordenada(self.entrada.get())
        self.dibujar_tableros()

    def pulsar_intro(self, evento):
        if self.modo == "recibido":
            self.comprobar_recibido()

    def iniciar(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    juego = HundirLaFlota()
    juego.iniciar()
