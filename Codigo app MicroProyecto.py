import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class RegistroJugador(tk.Toplevel):
    def __init__(self, parent, conn, c):
        super().__init__(parent)
        self.title("Registro de Jugador")
        self.parent = parent
        self.conn = conn
        self.c = c

        # Crear tabla Jugador si no existe
        self.c.execute('''CREATE TABLE IF NOT EXISTS Jugador (
                            ID INTEGER PRIMARY KEY,
                            Nombre TEXT,
                            Edad INTEGER,
                            Pais TEXT
                            )''')

        # Etiquetas y campos de entrada para Jugador
        label_id = ttk.Label(self, text="ID:")
        label_id.grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = ttk.Entry(self)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        label_nombre = ttk.Label(self, text="Nombre:")
        label_nombre.grid(row=1, column=0, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(self)
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        label_edad = ttk.Label(self, text="Edad:")
        label_edad.grid(row=2, column=0, padx=5, pady=5)
        self.entry_edad = ttk.Entry(self)
        self.entry_edad.grid(row=2, column=1, padx=5, pady=5)

        label_pais = ttk.Label(self, text="País:")
        label_pais.grid(row=3, column=0, padx=5, pady=5)
        self.entry_pais = ttk.Entry(self)
        self.entry_pais.grid(row=3, column=1, padx=5, pady=5)

        button_obtener_id = ttk.Button(self, text="Obtener ID", command=self.obtener_id)
        button_obtener_id.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.button_registrar = ttk.Button(self, text="Registrar Jugador", command=self.registrar_jugador, state="disabled")
        self.button_registrar.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Cerrar ventana cuando se cierre la ventana
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def obtener_id(self):
        self.c.execute("SELECT MAX(ID) FROM Jugador")
        max_id = self.c.fetchone()[0]
        if max_id is not None:
            siguiente_id = max_id + 1
        else:
            siguiente_id = 1
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, siguiente_id)
        self.entry_nombre.focus()
        self.entry_nombre.bind("<Return>", lambda event: self.entry_edad.focus())
        self.button_registrar.config(state="normal")

    def registrar_jugador(self):
        jugador_id = self.entry_id.get()
        nombre = self.entry_nombre.get()
        edad = self.entry_edad.get()
        pais = self.entry_pais.get()

        # Verificar si el ID ya está registrado
        self.c.execute("SELECT * FROM Jugador WHERE ID=?", (jugador_id,))
        if self.c.fetchone() is not None:
            print("El ID ya está registrado.")
        else:
            # Insertar nuevo jugador
            self.c.execute("INSERT INTO Jugador (ID, Nombre, Edad, Pais) VALUES (?, ?, ?, ?)", (jugador_id, nombre, edad, pais))
            self.conn.commit()
            print("Jugador registrado correctamente.")
            # Abrir la ventana para agregar datos después de registrar el jugador
            self.open_agregar_datos(jugador_id)

    def close_window(self):
        self.destroy()

    def open_agregar_datos(self, jugador_id):
        self.withdraw()
        iniciar_cuenta = IniciarCuenta(self, self.conn, self.c)
        iniciar_cuenta.show_main_window()


class AgregarDatos(tk.Toplevel):
    def __init__(self, parent, conn, c, jugador_id):
        super().__init__(parent)
        self.title("Agregar Datos")
        self.parent = parent
        self.conn = conn
        self.c = c
        self.jugador_id = jugador_id  # Store the ID of the logged-in player

        # Crear tabla Videojuego si no existe
        self.c.execute('''CREATE TABLE IF NOT EXISTS Videojuego (
                            Titulo TEXT,
                            Año_Lanzamiento INTEGER,
                            Genero TEXT,
                            Desarrollador TEXT,
                            Plataforma TEXT,
                            Jugador_ID INTEGER,
                            FOREIGN KEY (Jugador_ID) REFERENCES Jugador(ID)
                            )''')

        # Crear tabla Coleccion si no existe
        self.c.execute('''CREATE TABLE IF NOT EXISTS Coleccion (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            Fecha_Adquisicion TEXT,
                            Estado TEXT
                            )''')

        # Etiquetas y campos de entrada para Videojuego
        label_titulo = ttk.Label(self, text="Título:")
        label_titulo.grid(row=0, column=0, padx=5, pady=5)
        self.entry_titulo = ttk.Entry(self)
        self.entry_titulo.grid(row=0, column=1, padx=5, pady=5)

        label_anio_lanzamiento = ttk.Label(self, text="Año de Lanzamiento:")
        label_anio_lanzamiento.grid(row=1, column=0, padx=5, pady=5)
        self.entry_anio_lanzamiento = ttk.Entry(self)
        self.entry_anio_lanzamiento.grid(row=1, column=1, padx=5, pady=5)

        label_genero = ttk.Label(self, text="Género:")
        label_genero.grid(row=2, column=0, padx=5, pady=5)
        self.entry_genero = ttk.Entry(self)
        self.entry_genero.grid(row=2, column=1, padx=5, pady=5)

        label_desarrollador = ttk.Label(self, text="Desarrollador:")
        label_desarrollador.grid(row=3, column=0, padx=5, pady=5)
        self.entry_desarrollador = ttk.Entry(self)
        self.entry_desarrollador.grid(row=3, column=1, padx=5, pady=5)

        label_plataforma = ttk.Label(self, text="Plataforma:")
        label_plataforma.grid(row=4, column=0, padx=5, pady=5)
        self.entry_plataforma = ttk.Entry(self)
        self.entry_plataforma.grid(row=4, column=1, padx=5, pady=5)

        button_videojuego = ttk.Button(self, text="Agregar Videojuego", command=self.insertar_videojuego)
        button_videojuego.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        # Etiquetas y campos de entrada para Colección
        label_titulo_coleccion = ttk.Label(self, text="Fecha de Aquisición:")
        label_titulo_coleccion.grid(row=7, column=0, padx=5, pady=5)
        self.entry_titulo_coleccion = ttk.Entry(self)
        self.entry_titulo_coleccion.grid(row=7, column=1, padx=5, pady=5)

        label_estado = ttk.Label(self, text="Estado:")
        label_estado.grid(row=8, column=0, padx=5, pady=5)
        self.entry_estado = ttk.Entry(self)
        self.entry_estado.grid(row=8, column=1, padx=5, pady=5)

        button_coleccion = ttk.Button(self, text="Agregar a Colección", command=self.insertar_coleccion)
        button_coleccion.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        # Cerrar ventana cuando se cierre la ventana
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def eliminar_restriccion_unique(self):
        # Eliminar la restricción UNIQUE en la columna Titulo
        self.c.execute("DROP INDEX IF EXISTS idx_videojuego_titulo;")

    def insertar_videojuego(self):
        self.eliminar_restriccion_unique()
        titulo = self.entry_titulo.get()
        año_lanzamiento = self.entry_anio_lanzamiento.get()
        genero = self.entry_genero.get()
        desarrollador = self.entry_desarrollador.get()
        plataforma = self.entry_plataforma.get()

        # Insertar el videojuego
        self.c.execute("INSERT INTO Videojuego (Titulo, Año_Lanzamiento, Genero, Desarrollador, Plataforma, Jugador_ID) VALUES (?, ?, ?, ?, ?, ?)", (titulo, año_lanzamiento, genero, desarrollador, plataforma, self.jugador_id))
        self.conn.commit()
        print("Videojuego agregado correctamente.")

    def insertar_coleccion(self):
        fecha_adquisicion = self.entry_titulo_coleccion.get()
        estado = self.entry_estado.get()
        self.c.execute("INSERT INTO Coleccion (Fecha_Adquisicion, Estado) VALUES (?, ?)", (fecha_adquisicion, estado))
        self.conn.commit()
        print("Juego agregado a la colección correctamente.")

    def close_window(self):
        self.parent.deiconify()
        self.destroy()


class IniciarCuenta(tk.Toplevel):
    def __init__(self, parent, conn, c):
        super().__init__(parent)
        self.title("Iniciar Cuenta")
        self.parent = parent
        self.conn = conn
        self.c = c
        self.jugador_id = None  # Store the ID of the logged-in player

        # Etiquetas y campos de entrada para iniciar sesión
        label_id = ttk.Label(self, text="ID:")
        label_id.grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = ttk.Entry(self)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        label_nombre = ttk.Label(self, text="Nombre:")
        label_nombre.grid(row=1, column=0, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(self)
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        button_iniciar = ttk.Button(self, text="Iniciar Sesión", command=self.iniciar_sesion)
        button_iniciar.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Cerrar ventana cuando se cierre la ventana
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def iniciar_sesion(self):
        jugador_id = self.entry_id.get()
        nombre = self.entry_nombre.get()

        # Verificar si el ID y el nombre coinciden
        self.c.execute("SELECT * FROM Jugador WHERE ID=? AND Nombre=?", (jugador_id, nombre))
        if self.c.fetchone() is not None:
            print("Inicio de sesión exitoso.")
            self.jugador_id = jugador_id  # Store the ID of the logged-in player
            self.show_buttons()
        else:
            messagebox.showerror("Error", "ID y nombre no coinciden.")

    def show_buttons(self):
        # Limpiar widgets de inicio de sesión
        self.entry_id.destroy()
        self.entry_nombre.destroy()
        self.destroy_buttons()

        # Botón para agregar datos
        button_agregar_datos = ttk.Button(self, text="Agregar Datos", command=self.open_agregar_datos)
        button_agregar_datos.grid(row=0, column=0, padx=5, pady=5)

        # Botón para ver videojuegos
        button_ver_videojuegos = ttk.Button(self, text="Ver Videojuegos", command=self.ver_videojuegos)
        button_ver_videojuegos.grid(row=0, column=1, padx=5, pady=5)

        # Botón para borrar videojuegos
        button_borrar_videojuegos = ttk.Button(self, text="Borrar Videojuegos", command=self.borrar_videojuegos)
        button_borrar_videojuegos.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def open_agregar_datos(self):
        self.withdraw()
        agregar_datos = AgregarDatos(self, self.conn, self.c, self.jugador_id)

    def ver_videojuegos(self):
        # Retrieve video games added by the logged-in player
        self.c.execute("SELECT * FROM Videojuego WHERE Jugador_ID=?", (self.jugador_id,))
        videojuegos = self.c.fetchall()

        # Create a new window to display the video games
        ver_videojuegos_window = tk.Toplevel(self)
        ver_videojuegos_window.title("Videojuegos Agregados")
    
        # Display the video games in a list or a table
        if videojuegos:
            for i, videojuego in enumerate(videojuegos, start=1):
                label = ttk.Label(ver_videojuegos_window, text=f"{i}. Título: {videojuego[0]}, Año de Lanzamiento: {videojuego[1]}, Género: {videojuego[2]}, Desarrollador: {videojuego[3]}, Plataforma: {videojuego[4]}")
                label.pack(pady=5)
        else:
            label = ttk.Label(ver_videojuegos_window, text="No se han agregado videojuegos aún.")
            label.pack(pady=5)

    def borrar_videojuegos(self):
        self.withdraw()
        borrar_videojuegos = BorrarVideojuegos(self, self.conn, self.c, self.jugador_id, self.show_main_window)

    def close_window(self):
        self.parent.deiconify()
        self.destroy()

    def destroy_buttons(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_main_window(self):
        self.parent.deiconify()

class BorrarVideojuegos(tk.Toplevel):
    def __init__(self, parent, conn, c, jugador_id, callback):
        super().__init__(parent)
        self.title("Borrar Videojuegos")
        self.parent = parent
        self.conn = conn
        self.c = c
        self.jugador_id = jugador_id
        self.callback = callback

        # Etiquetas y campos de entrada para borrar videojuegos
        label_titulo = ttk.Label(self, text="Título del Videojuego:")
        label_titulo.grid(row=0, column=0, padx=5, pady=5)
        self.entry_titulo = ttk.Entry(self)
        self.entry_titulo.grid(row=0, column=1, padx=5, pady=5)

        button_borrar = ttk.Button(self, text="Borrar", command=self.borrar_videojuego)
        button_borrar.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Cerrar ventana cuando se cierre la ventana
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def borrar_videojuego(self):
        titulo = self.entry_titulo.get()
        # Check if the video game exists before attempting deletion
        self.c.execute("SELECT * FROM Videojuego WHERE Titulo=? AND Jugador_ID=?", (titulo, self.jugador_id))
        if self.c.fetchone() is not None:
            self.c.execute("DELETE FROM Videojuego WHERE Titulo=? AND Jugador_ID=?", (titulo, self.jugador_id))
            self.conn.commit()
            print("Videojuego borrado correctamente.")
            self.callback()  # Show the main window again
        else:
            messagebox.showerror("Error", f"No se encontró ningún videojuego con el título '{titulo}'.")


    def close_window(self):
        self.parent.deiconify()
        self.destroy()



class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Principal")

        self.conn = sqlite3.connect('MicroProyecto.db')
        self.c = self.conn.cursor()

        self.button_registro = ttk.Button(self, text="Registrar Jugador", command=self.open_registro)
        self.button_registro.pack(pady=10)

        self.button_iniciar = ttk.Button(self, text="Iniciar Cuenta", command=self.open_iniciar_cuenta)
        self.button_iniciar.pack(pady=10)

    def open_registro(self):
        self.withdraw()
        registro_jugador = RegistroJugador(self, self.conn, self.c)

    def open_iniciar_cuenta(self):
        self.withdraw()
        iniciar_cuenta = IniciarCuenta(self, self.conn, self.c)

    def __del__(self):
        self.conn.close()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
