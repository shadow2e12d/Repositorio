import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import pandas as pd

# Configuración de la conexión a la base de datos
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'BuzonDeVoz',
    'raise_on_warnings': True
}

def connect_db():
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            print("Conexión a la base de datos realizada con éxito.")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_tables():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Eliminar la tabla buzonvoz si existe
            cursor.execute("DROP TABLE IF EXISTS buzonvoz")

            # Crear tabla datos
            create_table_datos = """
            CREATE TABLE IF NOT EXISTS datos (
                credencial INT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                apellido VARCHAR(20) NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_table_datos)

            # Crear tabla retroalimentacion_mensajes
            create_table_retroalimentacion = """
            CREATE TABLE IF NOT EXISTS retroalimentacion_mensajes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                motivo VARCHAR(255) NOT NULL,
                mensaje TEXT NOT NULL,
                retroalimentacion TEXT
            );
            """
            cursor.execute(create_table_retroalimentacion)

            conn.commit()
            print("Tablas creadas con éxito.")
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"Error al crear las tablas: {err}")
            if conn:
                conn.rollback()
            cursor.close()
            conn.close()

def add_datos():
    credencial = entry_credencial.get()
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    
    if not credencial or not nombre or not apellido:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return
    
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO datos (credencial, nombre, apellido) VALUES (%s, %s, %s)"
            cursor.execute(query, (credencial, nombre, apellido))
            conn.commit()
            cursor.close()
            conn.close()
            refresh_table(tree_datos, "datos")
        except mysql.connector.Error as err:
            print(f"Error al añadir datos: {err}")
            if conn:
                conn.rollback()
            cursor.close()
            conn.close()

def add_retroalimentacion():
    motivo = entry_motivo.get()
    mensaje = entry_mensaje.get()
    retroalimentacion = entry_retroalimentacion.get()
    
    if not motivo or not mensaje:
        messagebox.showerror("Error", "Los campos Motivo y Mensaje son obligatorios.")
        return
    
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO retroalimentacion_mensajes (motivo, mensaje, retroalimentacion) VALUES (%s, %s, %s)"
            cursor.execute(query, (motivo, mensaje, retroalimentacion))
            conn.commit()
            cursor.close()
            conn.close()
            refresh_table(tree_retroalimentacion, "retroalimentacion_mensajes")
        except mysql.connector.Error as err:
            print(f"Error al añadir datos: {err}")
            if conn:
                conn.rollback()
            cursor.close()
            conn.close()

def refresh_table(tree, table_name):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            for i in tree.get_children():
                tree.delete(i)
            for row in rows:
                tree.insert("", "end", values=row)
        except mysql.connector.Error as err:
            print(f"Error al obtener datos: {err}")

def delete_datos():
    selected_item = tree_datos.selection()
    if selected_item:
        item = tree_datos.item(selected_item)
        credencial = item['values'][0]
        delete_data("datos", "credencial", credencial)
    else:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un registro para eliminar")

def delete_retroalimentacion():
    selected_item = tree_retroalimentacion.selection()
    if selected_item:
        item = tree_retroalimentacion.item(selected_item)
        mensaje_id = item['values'][0]
        delete_data("retroalimentacion_mensajes", "id", mensaje_id)
    else:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un mensaje para eliminar")

def delete_data(table_name, column_name, value):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = f"DELETE FROM {table_name} WHERE {column_name} = %s"
            cursor.execute(query, (value,))
            conn.commit()
            cursor.close()
            conn.close()
            refresh_table(tree_datos, "datos")
            refresh_table(tree_retroalimentacion, "retroalimentacion_mensajes")
        except mysql.connector.Error as err:
            print(f"Error al eliminar datos: {err}")
            if conn:
                conn.rollback()
            cursor.close()
            conn.close()

def update_datos():
    selected_item = tree_datos.selection()
    if selected_item:
        item = tree_datos.item(selected_item)
        credencial = item['values'][0]
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        
        if not nombre or not apellido:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                query = "UPDATE datos SET nombre = %s, apellido = %s WHERE credencial = %s"
                cursor.execute(query, (nombre, apellido, credencial))
                conn.commit()
                cursor.close()
                conn.close()
                refresh_table(tree_datos, "datos")
            except mysql.connector.Error as err:
                print(f"Error al actualizar datos: {err}")
                if conn:
                    conn.rollback()
                cursor.close()
                conn.close()
    else:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un registro para actualizar")

def update_retroalimentacion():
    selected_item = tree_retroalimentacion.selection()
    if selected_item:
        item = tree_retroalimentacion.item(selected_item)
        mensaje_id = item['values'][0]
        motivo = entry_motivo.get()
        mensaje = entry_mensaje.get()
        retroalimentacion = entry_retroalimentacion.get()
        
        if not motivo or not mensaje:
            messagebox.showerror("Error", "Los campos Motivo y Mensaje son obligatorios.")
            return
        
        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                query = "UPDATE retroalimentacion_mensajes SET motivo = %s, mensaje = %s, retroalimentacion = %s WHERE id = %s"
                cursor.execute(query, (motivo, mensaje, retroalimentacion, mensaje_id))
                conn.commit()
                cursor.close()
                conn.close()
                refresh_table(tree_retroalimentacion, "retroalimentacion_mensajes")
            except mysql.connector.Error as err:
                print(f"Error al actualizar datos: {err}")
                if conn:
                    conn.rollback()
                cursor.close()
                conn.close()
    else:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un mensaje para actualizar")

# Crear las tablas al inicio
create_tables()

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Gestión de Buzón de Voz")

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Crear los frames para cada tabla
frame_datos = ttk.Frame(notebook, width=400, height=400)
frame_retroalimentacion = ttk.Frame(notebook, width=400, height=400)

frame_datos.pack(fill='both', expand=True)
frame_retroalimentacion.pack(fill='both', expand=True)

notebook.add(frame_datos, text="Datos")
notebook.add(frame_retroalimentacion, text="Retroalimentación de Mensajes")

# Frame para la entrada de datos en datos
frame_datos_inputs = ttk.LabelFrame(frame_datos, text="Añadir/Actualizar Usuario")
frame_datos_inputs.pack(fill="both", expand="yes", padx=20, pady=10)

ttk.Label(frame_datos_inputs, text="Credencial").grid(row=0, column=0)
entry_credencial = ttk.Entry(frame_datos_inputs, width=30)
entry_credencial.grid(row=0, column=1)

ttk.Label(frame_datos_inputs, text="Nombre").grid(row=1, column=0)
entry_nombre = ttk.Entry(frame_datos_inputs, width=30)
entry_nombre.grid(row=1, column=1)

ttk.Label(frame_datos_inputs, text="Apellido").grid(row=2, column=0)
entry_apellido = ttk.Entry(frame_datos_inputs, width=30)
entry_apellido.grid(row=2, column=1)

ttk.Button(frame_datos_inputs, text="Añadir Usuario", command=add_datos).grid(row=3, column=0, pady=10)
ttk.Button(frame_datos_inputs, text="Actualizar Usuario", command=update_datos).grid(row=3, column=1, pady=10)
ttk.Button(frame_datos_inputs, text="Eliminar Usuario", command=delete_datos).grid(row=4, column=0, pady=10, columnspan=2)

# Tabla de datos
tree_datos = ttk.Treeview(frame_datos, columns=("credencial", "nombre", "apellido", "fecha_registro"), show='headings')
tree_datos.heading("credencial", text="Credencial")
tree_datos.heading("nombre", text="Nombre")
tree_datos.heading("apellido", text="Apellido")
tree_datos.heading("fecha_registro", text="Fecha de Registro")
tree_datos.pack(fill="both", expand=True)

# Frame para la entrada de datos en retroalimentación
frame_retroalimentacion_inputs = ttk.LabelFrame(frame_retroalimentacion, text="Añadir/Actualizar Mensaje")
frame_retroalimentacion_inputs.pack(fill="both", expand="yes", padx=20, pady=10)

ttk.Label(frame_retroalimentacion_inputs, text="Motivo").grid(row=0, column=0)
entry_motivo = ttk.Entry(frame_retroalimentacion_inputs, width=30)
entry_motivo.grid(row=0, column=1)

ttk.Label(frame_retroalimentacion_inputs, text="Mensaje").grid(row=1, column=0)
entry_mensaje = ttk.Entry(frame_retroalimentacion_inputs, width=30)
entry_mensaje.grid(row=1, column=1)

ttk.Label(frame_retroalimentacion_inputs, text="Retroalimentación").grid(row=2, column=0)
entry_retroalimentacion = ttk.Entry(frame_retroalimentacion_inputs, width=30)
entry_retroalimentacion.grid(row=2, column=1)

ttk.Button(frame_retroalimentacion_inputs, text="Añadir Mensaje", command=add_retroalimentacion).grid(row=3, column=0, pady=10)
ttk.Button(frame_retroalimentacion_inputs, text="Actualizar Mensaje", command=update_retroalimentacion).grid(row=3, column=1, pady=10)
ttk.Button(frame_retroalimentacion_inputs, text="Eliminar Mensaje", command=delete_retroalimentacion).grid(row=4, column=0, pady=10, columnspan=2)

# Tabla de retroalimentación
tree_retroalimentacion = ttk.Treeview(frame_retroalimentacion, columns=("id", "motivo", "mensaje", "retroalimentacion"), show='headings')
tree_retroalimentacion.heading("id", text="ID")
tree_retroalimentacion.heading("motivo", text="Motivo")
tree_retroalimentacion.heading("mensaje", text="Mensaje")
tree_retroalimentacion.heading("retroalimentacion", text="Retroalimentación")
tree_retroalimentacion.pack(fill="both", expand=True)

# Inicializar tablas con datos
refresh_table(tree_datos, "datos")
refresh_table(tree_retroalimentacion, "retroalimentacion_mensajes")

root.mainloop()
