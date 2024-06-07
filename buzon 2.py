import tkinter as tk
from tkinter import messagebox

def enviar_sugerencia():
    sugerencia = entry_sugerencia.get()
    # Aquí puedes guardar la sugerencia en una base de datos o archivo
    # Por ejemplo, podrías imprimir la sugerencia en la consola:
    print(f"Sugerencia recibida: {sugerencia}")
    # O mostrar un cuadro de diálogo para confirmar que se envió la sugerencia:
    messagebox.showinfo("Sugerencia enviada", "¡Gracias por tu sugerencia!")

# Configuración de la ventana
ventana = tk.Tk()
ventana.title("Buzón de Sugerencias")
ventana.geometry("300x150")

# Etiqueta y campo de entrada
label_sugerencia = tk.Label(ventana, text="Escribe tu sugerencia:")
label_sugerencia.pack()
entry_sugerencia = tk.Entry(ventana)
entry_sugerencia.pack()

# Botón para enviar
btn_enviar = tk.Button(ventana, text="Enviar", command=enviar_sugerencia)
btn_enviar.pack()

ventana.mainloop()

