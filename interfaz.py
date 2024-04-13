import tkinter as tk
import http.client
import json

# Función para hacer la solicitud a la API y mostrar los resultados
def obtener_recomendaciones():
    tipo = tipo_var.get()
    duracion_min = int(duracion_min_entry.get()) * 60
    duracion_max = int(duracion_max_entry.get()) * 60
    genero = genero_listbox.get(tk.ACTIVE)
    fecha = fecha_entry.get()
    fechav = fechav_entry.get()
    
    # Hacer la solicitud a la API de IMDb
    conn = http.client.HTTPSConnection("ott-details.p.rapidapi.com")
    headers = {
        'content-type': "application/json",
        'X-RapidAPI-Key': "20dbd951b8msh1dd90e5029c8d9bp145fc5jsnb2a18480915b",
        'X-RapidAPI-Host': "ott-details.p.rapidapi.com"
    }

    conn_imdb = http.client.HTTPSConnection("imdb146.p.rapidapi.com")
    headers_imdb = {
        'X-RapidAPI-Key': "20dbd951b8msh1dd90e5029c8d9bp145fc5jsnb2a18480915b",
        'X-RapidAPI-Host': "imdb146.p.rapidapi.com"
    }

    conn.request("GET", f"/advancedsearch?start_year={fecha}&end_year={fechav}&min_imdb=6&max_imdb=7.8&genre={genero}&language=english&type={'movie' if tipo == 1 else 'show'}&sort=latest&page=1", headers=headers)
    res = conn.getresponse()
    data = res.read()
    
    movie_data = json.loads(data.decode("utf-8"))

    # Mostrar los resultados en la interfaz
    result_text.delete(1.0, tk.END)
    for movie in movie_data['results']:
        movie_id = movie['imdbid']
        conn_imdb.request("GET", f"/v1/title/?id={movie_id}", headers=headers_imdb)
        res_imdb = conn_imdb.getresponse()
        data_imdb = res_imdb.read()
        movie_info = json.loads(data_imdb.decode("utf-8"))
        if 'runtime' in movie_info and movie_info['runtime'] is not None and 'seconds' in movie_info['runtime']:
            movie_duration = int(movie_info['runtime']['seconds']) / 60
            if duracion_min <= movie_duration * 60 <= duracion_max:
                result_text.insert(tk.END, f"Título: {movie_info['titleText']['text']}\n")
        else:
            result_text.insert(tk.END, f"Título: {movie_info['titleText']['text']}\n")

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Recomendación de Películas y Series")

# Crear variables de control
tipo_var = tk.IntVar()

# Crear widgets
titulo_label = tk.Label(root, text="BIENVENIDO AL SISTEMA INTELIGENTE DE RECOMENDACIÓN DE PELÍCULAS Y SERIES")
titulo_label.pack()

tipo_label = tk.Label(root, text="¿Qué estás buscando?")
tipo_label.pack()

tipo_movie_radio = tk.Radiobutton(root, text="Película", variable=tipo_var, value=1)
tipo_movie_radio.pack()

tipo_show_radio = tk.Radiobutton(root, text="Serie de televisión", variable=tipo_var, value=2)
tipo_show_radio.pack()

duracion_min_label = tk.Label(root, text="Duración mínima (en minutos):")
duracion_min_label.pack()

duracion_min_entry = tk.Entry(root)
duracion_min_entry.pack()

duracion_max_label = tk.Label(root, text="Duración máxima (en minutos):")
duracion_max_label.pack()

duracion_max_entry = tk.Entry(root)
duracion_max_entry.pack()

genero_label = tk.Label(root, text="Género:")
genero_label.pack()

generos = [
    "Comedy", "Horror", "Romance", "Thriller", "Sci-Fi", "Drama", "Action",
    "Adventure", "Animation", "Biography", "Crime", "Documentary", "Family",
    "Fantasy", "Film-Noir", "Game-Show", "History", "Music", "Musical",
    "Mystery", "Mews", "Sport", "War", "Western"
]
genero_listbox = tk.Listbox(root, selectmode=tk.SINGLE, exportselection=0)
for genero in generos:
    genero_listbox.insert(tk.END, genero)
genero_listbox.pack()

fecha_label = tk.Label(root, text="Año de lanzamiento:")
fecha_label.pack()

fecha_entry = tk.Entry(root)
fecha_entry.pack()

fechav_label = tk.Label(root, text="Año de lanzamiento límite:")
fechav_label.pack()

fechav_entry = tk.Entry(root)
fechav_entry.pack()

buscar_button = tk.Button(root, text="Buscar", command=obtener_recomendaciones)
buscar_button.pack()

result_label = tk.Label(root, text="Resultados:")
result_label.pack()

result_text = tk.Text(root, height=10, width=50)
result_text.pack()

# Ejecutar la aplicación
root.mainloop()