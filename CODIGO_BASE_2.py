import tkinter as tk
from tkinter import simpledialog
import threading
import time

#NUEVO, OPCIONAL
FILAS = simpledialog.askinteger("Config", "Ingrese número de filas:", minvalue=1, maxvalue=10)
COLUMNAS = simpledialog.askinteger("Config", "Ingrese número de columnas:", minvalue=1, maxvalue=10)

estado_celdas = []
for fila in range(FILAS):
    fila_estado = []
    for col in range(COLUMNAS):
        fila_estado.append([False, "", "green", 0])
    estado_celdas.append(fila_estado)


ventana_d = tk.Tk()
ventana_d.title("Coworking - Editar (D)")

ventana_ad = tk.Toplevel()
ventana_ad.title("Coworking - Solo Vista (AD)")

frame_d = tk.Frame(ventana_d)
frame_d.pack(padx=10, pady=10)

frame_ad = tk.Frame(ventana_ad)
frame_ad.pack(padx=10, pady=10)




def actualizar_estado(boton_d, boton_ad, fila, col):
    tiempo_total = 120
    estado_celdas[fila][col][2] = "red"
    estado_celdas[fila][col][3] = tiempo_total

    while estado_celdas[fila][col][3] > 0:
        tiempo_restante = estado_celdas[fila][col][3]


        nombre = estado_celdas[fila][col][1]
        texto_mostrado = f"{nombre}\n{tiempo_restante}s"
        boton_d.config(text=texto_mostrado)
        boton_ad.config(text=texto_mostrado)


        if tiempo_restante <= 60:
            boton_d.config(bg="yellow")
            boton_ad.config(bg="yellow")

        time.sleep(1)  
        estado_celdas[fila][col][3] -= 1  


    estado_celdas[fila][col] = [False, "", "green", 0]
    boton_d.config(text="", bg="green")
    boton_ad.config(text="", bg="green")


def seleccionar_celda(fila, col, boton_d, boton_ad):
    if estado_celdas[fila][col][0]:  
        return

    nombre = simpledialog.askstring("Reserva", "Ingrese su nombre:")
    if nombre:
        estado_celdas[fila][col][0] = True
        estado_celdas[fila][col][1] = nombre
        boton_d.config(text=nombre, bg="red")
        boton_ad.config(text=nombre, bg="red")


        hilo = threading.Thread(
            target=actualizar_estado, 
            args=(boton_d, boton_ad, fila, col),
            daemon=True
        )
        hilo.start()


for fila in range(FILAS):
    for col in range(COLUMNAS):
        btn_d = tk.Button(frame_d, text="", width=12, height=4, bg="green")
        btn_d.grid(row=fila, column=col, padx=5, pady=5)

        btn_ad = tk.Button(frame_ad, text="", width=12, height=4, bg="green", state="disabled")
        btn_ad.grid(row=fila, column=col, padx=5, pady=5)

        btn_d.config(command=lambda f=fila, c=col, bd=btn_d, ba=btn_ad: seleccionar_celda(f, c, bd, ba))
ventana_d.mainloop()
