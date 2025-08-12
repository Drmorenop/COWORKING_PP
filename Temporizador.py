import tkinter as tk
from tkinter import messagebox

def iniciar_temporizador(segundos, btn):
    btn.config(state=tk.DISABLED)
    tiempo_restante = segundos

    def actualizar():
        nonlocal tiempo_restante
        if tiempo_restante > 0:
            minutos, segs = divmod(tiempo_restante, 60)
            etiqueta_tiempo.config(text=f"{minutos:02}:{segs:02}")

            if tiempo_restante == 30:
                etiqueta_tiempo.config(bg="yellow")
            tiempo_restante -= 1
            root.after(1000, actualizar)
        else:
            etiqueta_tiempo.config(bg="red")
            messagebox.showinfo("Tiempo terminado", "El temporizador ha finalizado.")
            btn.config(state=tk.NORMAL)

    etiqueta_tiempo.config(bg="green")
    actualizar()


root = tk.Tk()
root.title("Temporizador")
root.geometry("400x200")

etiqueta_tiempo = tk.Label(root, text="00:00", font=("Helvetica", 40))
etiqueta_tiempo.grid(row=0, column=0, columnspan=3, pady=20)

btn1 = tk.Button(root, text="$1 (1 min)", command=lambda: iniciar_temporizador(60, btn1))
btn1.grid(row=1, column=0, padx=10, pady=5)

btn2 = tk.Button(root, text="$2 (1 min 30s)", command=lambda: iniciar_temporizador(90, btn2))
btn2.grid(row=1, column=1, padx=10, pady=5)

btn3 = tk.Button(root, text="$3 (2 min)", command=lambda: iniciar_temporizador(120, btn3))
btn3.grid(row=1, column=2, padx=10, pady=5)

root.mainloop()
