import tkinter as tk
from tkinter import simpledialog
import threading
import time

# Tamaño del tablero
FILAS = 3
COLUMNAS = 3

# Diccionario para guardar el estado de cada celda
estado_celdas = {}

# Ventanas
ventana_d = tk.Tk()
ventana_d.title("Coworking - Editar (D)")
ventana_ad = tk.Toplevel()
ventana_ad.title("Coworking - Solo Vista (AD)")

# Crear frames para las dos ventanas
frame_d = tk.Frame(ventana_d)
frame_d.pack(padx=10, pady=10)
frame_ad = tk.Frame(ventana_ad)
frame_ad.pack(padx=10, pady=10)

# Función para actualizar el color y tiempo restante
def actualizar_estado(boton_d, boton_ad, fila, col):
    clave = f"{fila},{col}"
    tiempo_total = 120  # 2 minutos
    estado_celdas[clave]["color"] = "red"
    for t in range(tiempo_total, 0, -1):
        estado_celdas[clave]["tiempo"] = t
        if t <= 60:
            # Cambiar a amarillo si queda 1 minuto
            boton_d.config(bg="yellow")
            boton_ad.config(bg="yellow")
        time.sleep(1)
    # Resetear después de 3 min (opcional)
    estado_celdas[clave]["ocupado"] = False
    estado_celdas[clave]["nombre"] = ""
    estado_celdas[clave]["tiempo"] = 0
    boton_d.config(text="", bg="green")
    boton_ad.config(text="", bg="green")

# Función al hacer clic en una celda en D
def seleccionar_celda(fila, col, boton_d, boton_ad):
    clave = f"{fila},{col}"
    if estado_celdas[clave]["ocupado"]:
        return
    nombre = simpledialog.askstring("Reserva", "Ingrese su nombre:")
    if nombre:
        boton_d.config(text=nombre, bg="red")
        boton_ad.config(text=nombre, bg="red")
        estado_celdas[clave]["ocupado"] = True
        estado_celdas[clave]["nombre"] = nombre
        threading.Thread(target=actualizar_estado, args=(boton_d, boton_ad, fila, col), daemon=True).start()

# Crear botones en ambas ventanas
for fila in range(FILAS):
    for col in range(COLUMNAS):
        clave = f"{fila},{col}"
        estado_celdas[clave] = {"ocupado": False, "nombre": "", "color": "green", "tiempo": 0}

        # Ventana D (editable)
        btn_d = tk.Button(frame_d, text="", width=10, height=4, bg="green")
        btn_d.grid(row=fila, column=col, padx=5, pady=5)

        # Ventana AD (solo vista)
        btn_ad = tk.Button(frame_ad, text="", width=10, height=4, bg="green", state="disabled")
        btn_ad.grid(row=fila, column=col, padx=5, pady=5)

        # Asociar evento a botón D
        btn_d.config(command=lambda f=fila, c=col, bd=btn_d, ba=btn_ad: seleccionar_celda(f, c, bd, ba))

ventana_d.mainloop()
