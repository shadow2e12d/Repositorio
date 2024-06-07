import tkinter as tk

def enviar_sugerencia():
    sugerencia = entry_sugerencia.get()
    # Aquí puedes guardar la sugerencia en una base de datos o archivo
    
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
def 

ventana.mainloop()
