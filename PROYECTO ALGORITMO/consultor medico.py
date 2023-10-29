import tkinter as tk
from tkinter import ttk
import os
import json

# Directorio para almacenar los archivos de citas
citas_directory = "citas"
ultimo_id = 0

def limpiar_campos():
    for entry in (nombre_entry, telefono_entry, dpi_entry, correo_entry, edad_entry, motivo_entry):
        entry.delete(0, tk.END)

def create_citas_directory():
    if not os.path.exists(citas_directory):
        os.makedirs(citas_directory)

def formatear_fecha(fecha):
    return fecha.replace("/", "_")

def guardar_cita():
    global ultimo_id
    fecha = fecha_entry.get()
    fecha_formateada = formatear_fecha(fecha)
    nombre = nombre_entry.get()
    telefono = telefono_entry.get()
    dpi = dpi_entry.get()
    correo = correo_entry.get()
    edad = edad_entry.get()
    motivo = motivo_entry.get()
    ultimo_id += 1
    id_paciente = ultimo_id

    data = {
        "nombre": nombre,
        "telefono": telefono,
        "dpi": dpi,
        "correo": correo,
        "edad": edad,
        "motivo": motivo
    }
    with open(f"{citas_directory}/{fecha_formateada}.json", "a") as file:
        json.dump(data, file)
        file.write("\n")
    cargar_citas()
    limpiar_campos()

def cargar_citas():
    fecha = fecha_entry.get()
    fecha_formateada = formatear_fecha(fecha)
    citas_text.delete(1.0, tk.END)
    try:
        with open(f"{citas_directory}/{fecha_formateada}.json", "r") as file:
            citas = file.readlines()
            for cita in citas:
                data = json.loads(cita)
                citas_text.insert(tk.END, f"Nombre: {data['nombre']}\nTeléfono: {data['telefono']}\nDPI: {data['dpi']}\nCorreo: {data['correo']}\nEdad: {data['edad']}\nMotivo: {data['motivo']}\n\n")
    except FileNotFoundError:
        citas_text.insert(tk.END, "No hay citas programadas para esta fecha.")

def borrar_citas():
    fecha = fecha_entry.get()
    fecha_formateada = formatear_fecha(fecha)
    try:
        os.remove(f"{citas_directory}/{fecha_formateada}.json")
        citas_text.delete(1.0, tk.END)
        citas_text.insert(tk.END, "Citas eliminadas correctamente.")
    except FileNotFoundError:
        citas_text.insert(tk.END, "No hay citas programadas para esta fecha.")

def cargar_paciente():
    fecha = fecha_entry.get()
    fecha_formateada = formatear_fecha(fecha)
    nombre_paciente = nombre_entry.get()
    temp_file_path = f"{citas_directory}/{fecha_formateada}_temp.json"

    try:
        with open(f"{citas_directory}/{fecha_formateada}.json", "r") as original_file, open(temp_file_path, "w") as temp_file:
            citas = original_file.readlines()
            encontrado = False

            for cita in citas:
                data = json.loads(cita)
                if data['nombre'] == nombre_paciente:
                    telefono_entry.delete(0, tk.END)
                    telefono_entry.insert(0, data['telefono'])
                    dpi_entry.delete(0, tk.END)
                    dpi_entry.insert(0, data['dpi'])
                    correo_entry.delete(0, tk.END)
                    correo_entry.insert(0, data['correo'])
                    edad_entry.delete(0, tk.END)
                    edad_entry.insert(0, data['edad'])
                    motivo_entry.delete(0, tk.END)
                    motivo_entry.insert(0, data['motivo'])
                    encontrado = True
                else:
                    json.dump(data, temp_file)
                    temp_file.write("\n")

            if encontrado:
                os.remove(f"{citas_directory}/{fecha_formateada}.json")
                os.rename(temp_file_path, f"{citas_directory}/{fecha_formateada}.json")
            else:
                citas_text.insert(tk.END, "Paciente no encontrado in la fecha seleccionada.")
    except FileNotFoundError:
        citas_text.insert(tk.END, "No hay citas programadas para esta fecha.")

def editar_paciente():
    fecha = fecha_entry.get()
    fecha_formateada = formatear_fecha(fecha)
    nombre_paciente = nombre_entry.get()
    nueva_info = {
        "nombre": nombre_paciente,
        "telefono": telefono_entry.get(),
        "dpi": dpi_entry.get(),
        "correo": correo_entry.get(),
        "edad": edad_entry.get(),
        "motivo": motivo_entry.get()
    }
    try:
        with open(f"{citas_directory}/{fecha_formateada}.json", "r") as file:
            citas = file.readlines()
        with open(f"{citas_directory}/{fecha_formateada}.json", "w") as file:
            paciente_encontrado = False
            for cita in citas:
                data = json.loads(cita)
                if data['nombre'] == nombre_paciente:
                    json.dump(nueva_info, file)
                    file.write("\n")
                    paciente_encontrado = True
                else:
                    json.dump(data, file)
                    file.write("\n")

            if paciente_encontrado:
                citas_text.delete(1.0, tk.END)
                citas_text.insert(tk.END, "Paciente editado correctamente.")
            else:
                citas_text.delete(1.0, tk.END)
                citas_text.insert(tk.END, "Paciente no encontrado in la fecha seleccionada.")
    except FileNotFoundError:
        citas_text.delete(1.0, tk.END)
        citas_text.insert(tk.END, "No hay citas programadas para esta fecha.")

def ver_citas():
    citas_window = tk.Toplevel(root)
    citas_window.title("Citas Generadas")

    # Crear una lista en filas para mostrar los datos
    lista_frame = ttk.Frame(citas_window)
    lista_frame.pack(padx=10, pady=10)

    lista_header = ["Fecha", "Nombre", "Teléfono", "DPI", "Correo", "Edad", "Motivo"]
    for col, header in enumerate(lista_header):
        ttk.Label(lista_frame, text=header).grid(row=0, column=col, padx=5, pady=5)

    # Obtener y mostrar los datos de todas las citas
    row = 1
    for filename in os.listdir(citas_directory):
        if filename.endswith(".json"):
            fecha_formateada = filename.split(".")[0]
            with open(os.path.join(citas_directory, filename), "r") as file:
                citas = file.readlines()
                for cita in citas:
                    data = json.loads(cita)
                    ttk.Label(lista_frame, text=fecha_formateada).grid(row=row, column=0, padx=5, pady=5)
                    ttk.Label(lista_frame, text=data['nombre']).grid(row=row, column=1, padx=5, pady=5)
                    ttk.Label(lista_frame, text=data['telefono']).grid(row=row, column=2, padx=5, pady=5)
                    ttk.Label(lista_frame, text=data['dpi']).grid(row=row, column=3, padx=5, pady=5)
                    ttk.Label(lista_frame, text=data['correo']).grid(row=row, column=4, padx=5, pady=5)
                    ttk.Label(lista_frame, text=data['edad']).grid(row=row, column=5, padx=5, pady=5)
                    ttk.Label(lista_frame, text=data['motivo']).grid(row=row, column=6, padx=5, pady=5)
                    row += 1

# Crear la ventana principal
root = tk.Tk()
root.title("Consultorio de Citas")

# Estilo para los botones
style = ttk.Style()
style.configure('TButton', background='lightblue', foreground='black', padding=(10, 5))

# Crear el marco principal
frame = ttk.Frame(root)
frame.grid(padx=10, pady=10)

# Etiquetas y campos de entrada
fecha_label = ttk.Label(frame, text="Fecha de la cita (dd/mm/yyyy):")
fecha_label.grid(column=0, row=0, padx=5, pady=5)
fecha_entry = ttk.Entry(frame)
fecha_entry.grid(column=1, row=0, padx=5, pady=5)

nombre_label = ttk.Label(frame, text="Nombre del paciente:")
nombre_label.grid(column=0, row=1, padx=5, pady=5)
nombre_entry = ttk.Entry(frame)
nombre_entry.grid(column=1, row=1, padx=5, pady=5)

telefono_label = ttk.Label(frame, text="Teléfono:")
telefono_label.grid(column=0, row=2, padx=5, pady=5)
telefono_entry = ttk.Entry(frame)
telefono_entry.grid(column=1, row=2, padx=5, pady=5)

dpi_label = ttk.Label(frame, text="DPI del paciente:")
dpi_label.grid(column=0, row=3, padx=5, pady=5)
dpi_entry = ttk.Entry(frame)
dpi_entry.grid(column=1, row=3, padx=5, pady=5)

correo_label = ttk.Label(frame, text="Correo Electrónico:")
correo_label.grid(column=0, row=4, padx=5, pady=5)
correo_entry = ttk.Entry(frame)
correo_entry.grid(column=1, row=4, padx=5, pady=5)

edad_label = ttk.Label(frame, text="Edad del paciente:")
edad_label.grid(column=0, row=5, padx=5, pady=5)
edad_entry = ttk.Entry(frame)
edad_entry.grid(column=1, row=5, padx=5, pady=5)

motivo_label = ttk.Label(frame, text="Motivo de la cita:")
motivo_label.grid(column=0, row=6, padx=5, pady=5)
motivo_entry = ttk.Entry(frame)
motivo_entry.grid(column=1, row=6, padx=5, pady=5)

# Cuadro de texto para mostrar las citas
citas_text = tk.Text(root, width=40, height=10)
citas_text.grid(row=0, column=1, padx=10, pady=10)

# Botones
botones_frame = ttk.Frame(frame)
botones_frame.grid(column=0, row=7, columnspan=2, pady=10)

guardar_button = ttk.Button(botones_frame, text="Guardar Cita", command=guardar_cita)
guardar_button.grid(column=0, row=0, padx=5, pady=5)

editar_button = ttk.Button(botones_frame, text="Editar Paciente", command=editar_paciente)
editar_button.grid(column=1, row=0, padx=5, pady=5)

eliminar_button = ttk.Button(botones_frame, text="Eliminar Citas", command=borrar_citas)
eliminar_button.grid(column=2, row=0, padx=5, pady=5)

cargar_button = ttk.Button(botones_frame, text="Cargar Paciente", command=cargar_paciente)
cargar_button.grid(column=3, row=0, padx=5, pady=5)

ver_citas_button = ttk.Button(frame, text="Ver Citas", command=ver_citas)
ver_citas_button.grid(column=0, row=8, columnspan=2, pady=10)

# Crear el directorio de citas si no existe
create_citas_directory()

# Iniciar la ventana principal
root.mainloop()