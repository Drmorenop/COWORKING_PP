import tkinter as tk
from tkinter import simpledialog
import threading
import time
from PIL import Image, ImageTk

#Pide al usuario los datos iniciales y oculta la ventana principal
root = tk.Tk()
root.withdraw()

#Cantidad de filas y columnas
filas = simpledialog.askinteger("Config", "Ingrese número de filas:", minvalue=1, maxvalue=10, parent=root)
columnas = simpledialog.askinteger("Config", "Ingrese número de columnas:", minvalue=1, maxvalue=10, parent=root)

if filas is None or columnas is None:
    root.destroy()
    exit()

#Crear nombres para cada PC 
lista_nombres_pc = []
contador = 1
for _ in range(filas):
    fila_actual = []
    for _ in range(columnas):
        fila_actual.append(f"PC{contador}")
        contador += 1
    lista_nombres_pc.append(fila_actual)

# Estructura para guardar el estado de cada PC:
# [ocupada (bool), nombre/reserva, color, tiempo_restante]
estado_pc = [
    [[False, lista_nombres_pc[f][c], "green", 0] for c in range(columnas)]
    for f in range(filas)
]

def cerrar_splash(splash):
    splash.destroy()
    abrir_ventanas()

def mostrar_splash():
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    splash.configure(bg="white")

    try: #CAMBIAR CUANDO SE INICIE EL PROGRMA [ IMPORTANTE ]
        imagen_logo = Image.open(r"C:\Users\Derito\Desktop\PYTHON\Logo_Coworking.png") #Ruta de mi caepeta personal

        #REdimencionamiento de la imagen
        max_ancho, max_alto = 400, 300
        ancho_original, alto_original = imagen_logo.size
        escala = min(max_ancho / ancho_original, max_alto / alto_original, 1)
        nuevo_ancho = int(ancho_original * escala)
        nuevo_alto = int(alto_original * escala)

        imagen_logo = imagen_logo.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
        imagen_tk = ImageTk.PhotoImage(imagen_logo)

        #Se centra en mediod e la pantalla
        x = (splash.winfo_screenwidth() // 2) - (nuevo_ancho // 2)
        y = (splash.winfo_screenheight() // 2) - (nuevo_alto // 2)
        splash.geometry(f"{nuevo_ancho}x{nuevo_alto}+{x}+{y}")

        etiqueta = tk.Label(splash, image=imagen_tk, bg="white")
        etiqueta.pack()
        splash.image = imagen_tk  # Evitar que se borre la imagen

    except:
        tk.Label(splash, text="Logo no encontrado", font=("Arial", 24), bg="white").pack(pady=20)
        splash.geometry("400x200")

    splash.update()  # Asegura que se dibuje
    splash.after(3000, lambda: cerrar_splash(splash))

def temporizador(boton_usuario, boton_admin, fila, col, tiempo_total):
    estado_pc[fila][col][2] = "red"
    estado_pc[fila][col][3] = tiempo_total

    while estado_pc[fila][col][3] > 0:
        tiempo_restante = estado_pc[fila][col][3]
        nombre_reserva = estado_pc[fila][col][1]
        texto = f"{nombre_reserva}\n{tiempo_restante}s"

        def actualizar_ui():
            if tiempo_restante <= 30:
                boton_usuario.config(text=texto, bg="yellow")
                boton_admin.config(text=texto, bg="yellow")
            else:
                boton_usuario.config(text=texto, bg="red")
                boton_admin.config(text=texto, bg="red")

        ventana_usuario.after(0, actualizar_ui)
        time.sleep(1)
        estado_pc[fila][col][3] -= 1

    def resetear_ui():
        estado_pc[fila][col] = [False, lista_nombres_pc[fila][col], "green", 0]
        boton_usuario.config(text=lista_nombres_pc[fila][col], bg="green")
        boton_admin.config(text=lista_nombres_pc[fila][col], bg="green")

    ventana_usuario.after(0, resetear_ui)

def elegir_tiempo():
    ventana_opciones = tk.Toplevel(root)
    ventana_opciones.title("Seleccionar Tiempo")
    ventana_opciones.geometry("300x200")
    ventana_opciones.grab_set()

    seleccion = {"tiempo": None}
    def set_tiempo(t):
        seleccion["tiempo"] = t
        ventana_opciones.destroy()

    tk.Label(ventana_opciones, text="Elija un paquete de tiempo:", font=("Arial", 12)).pack(pady=10)
    tk.Button(ventana_opciones, text="1min - $1", command=lambda: set_tiempo(60), width=30).pack(pady=5)
    tk.Button(ventana_opciones, text="1min 30s - $2", command=lambda: set_tiempo(90), width=30).pack(pady=5)
    tk.Button(ventana_opciones, text="2min - $3", command=lambda: set_tiempo(120), width=30).pack(pady=5)

    ventana_opciones.wait_window()
    return seleccion["tiempo"]

def reservar_pc(fila, col, boton_usuario, boton_admin):
    if estado_pc[fila][col][0]:  #Si ya está ocupada, salir
        return
    tiempo = elegir_tiempo()
    if not tiempo:
        return
    nombre = simpledialog.askstring("Reserva", "Ingrese su nombre:", parent=root)
    if not nombre:
        return

    estado_pc[fila][col] = [True, nombre, "red", tiempo]
    boton_usuario.config(text=f"{nombre}\n{tiempo}s", bg="red")
    boton_admin.config(text=f"{nombre}\n{tiempo}s", bg="red")

    hilo = threading.Thread(target=temporizador, args=(boton_usuario, boton_admin, fila, col, tiempo), daemon=True)
    hilo.start()

def abrir_ventanas():
    global ventana_usuario, ventana_admin
    ventana_usuario = tk.Toplevel(root)
    ventana_usuario.title("Cliente - Selección de PC")
    ventana_admin = tk.Toplevel(root)
    ventana_admin.title("Administración")

    frame_usuario = tk.Frame(ventana_usuario)
    frame_usuario.pack(padx=10, pady=10)
    frame_admin = tk.Frame(ventana_admin)
    frame_admin.pack(padx=10, pady=10)

    for f in range(filas):
        for c in range(columnas):
            boton_usuario = tk.Button(frame_usuario, text=lista_nombres_pc[f][c], width=12, height=4, bg="green", font=("Arial", 16, "bold"))
            boton_usuario.grid(row=f, column=c, padx=5, pady=5)

            boton_admin = tk.Button(frame_admin, text=lista_nombres_pc[f][c], width=12, height=4, bg="green", state="disabled", font=("Arial", 16, "bold"))
            boton_admin.grid(row=f, column=c, padx=5, pady=5)

            boton_usuario.config(command=lambda ff=f, cc=c, bu=boton_usuario, ba=boton_admin: reservar_pc(ff, cc, bu, ba))

    tk.Button(frame_admin, text="Cerrar Programa", bg="red", fg="white", font=("Arial", 14, "bold"), command=root.destroy)\
        .grid(row=filas, column=0, columnspan=columnas, pady=10)

    ventana_usuario.protocol("WM_DELETE_WINDOW", root.destroy)
    ventana_admin.protocol("WM_DELETE_WINDOW", root.destroy)

#Inicio del progrma
mostrar_splash()
root.mainloop()
