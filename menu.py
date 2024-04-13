import os
import http.client
import json


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

x = 0

while (x != 2):
    print("-"*15,"BIENVENIDO AL SISTEMA INTELIGENTE DE RECOMENDACIÓN DE PELÍCULAS Y SERIES","-"*15)
    print("1. Continuar")
    print("2. Salir")
    x = int(input("Ingrese un número: "))
    os.system('cls')
    if (x == 1):
        tipo = -1
        while (tipo < 1 or tipo > 2):
            print("*"*10,"SISTEMA DE RECOMENDACION DE PELICULAS Y SERIES","*"*10)
            print("Que es lo que estas buscando?")
            print("1. Película")
            print("2. Serie de televisión")
            tipo = int(input("Ingrese un número: "))
            #os.system('cls')
        print("*"*10,"SISTEMA DE RECOMENDACION DE PELICULAS Y SERIES","*"*10)
        if (tipo == 1):
            tip = "movie"
            duracion_min = -1
            while (duracion_min < 1):
                print("Cuál es el tiempo mínimo de duración de lo que estás buscando?")
                duracion_min = int(input("Ingrese la duración mínima en minutos: "))
                duracion_min *= 60
                #os.system('cls')
            duracion_max = -1
            while (duracion_max < duracion_min):
                print("Cuál es el tiempo máximo de duración de lo que estás buscando?")
                duracion_max = int(input(f"Ingrese la duración máxima en minutos (mayor o igual a {duracion_min/60}): "))
                duracion_max *= 60
                if duracion_max < duracion_min:
                    print(f"La duración máxima debe ser mayor o igual a {duracion_min}.")
                #os.system('cls')
        else:
            tip = "show"
            capitulo = -1
            while (capitulo < 1):
                print("Cuál es la cantidad mínima de capítulos que buscas?")
                capitulo = int(input("Ingrese la cantidad mínima de capítulos: "))
                #os.system('cls')
        print("*"*10,"SISTEMA DE RECOMENDACION DE PELICULAS Y SERIES","*"*10)
        genero = -1
        while (genero < 1 or genero > 24):
            print("De qué clase de género estás buscando?")
            print("1. Comedia")
            print("2. Horror")
            print("3. Romance")
            print("4. Suspenso")
            print("5. Ciencia ficción")
            print("6. Drama")
            print("7. Acción")
            print("8. Aventura")
            print("9. Animación")
            print("10. Biografía")
            print("11. Crimen")
            print("12. Documental")
            print("13. Familia")
            print("14. Fantasía")
            print("15. Cine negro")
            print("16. Programa de juegos")
            print("17. Historia")
            print("18. Música")
            print("19. Musical")
            print("20. Misterio")
            print("21. Mews")
            print("22. Deporte")
            print("23. Guerra")
            print("24. Occidental")
            genero = int(input("Ingresa un número: "))
            if (genero == 1):
                gen = "Comedy"
            elif (genero == 2):
                gen = "Horror"
            elif (genero == 3):
                gen = "Romance"
            elif (genero == 4):
                gen = "Thriller"
            elif (genero == 5):
                gen = "Sci-Fi"
            elif (genero == 6):
                gen = "Drama"
            elif (genero == 7):
                gen = "Action"
            elif (genero == 8):
                gen = "Adventure"
            elif (genero == 9):
                gen = "Animation"
            elif (genero == 10):
                gen = "Biography"
            elif (genero == 11):
                gen = "Crime"
            elif (genero == 12):
                gen = "Documentary"
            elif (genero == 13):
                gen = "Family"
            elif (genero == 14):
                gen = "Fantasy"
            elif (genero == 15):
                gen = "Film-Noir"
            elif (genero == 16):
                gen = "Game-Show"
            elif (genero == 17):
                gen = "History"
            elif (genero == 18):
                gen = "Music"
            elif (genero == 19):
                gen = "Musical"
            elif (genero == 20):
                gen = "Mystery"
            elif (genero == 21):
                gen = "Mews"
            elif (genero == 22):
                gen = "Sport"
            elif (genero == 23):
                gen = "War"
            elif (genero == 24):
                gen = "Western"
            #os.system('cls')
        print("*"*10,"SISTEMA DE RECOMENDACION DE PELÍCULAS Y SERIES","*"*10)
        print("Por qué año crees que se realizó el lanzamiento?")
        fecha = input("Ingrese una posible fecha (AAAA): ")
        
        print("*"*10,"SISTEMA DE RECOMENDACION DE PELÍCULAS Y SERIES","*"*10)
        print("Ingrese una posible fecha límite?")
        fechav = input("Ingrese una posible fecha límite (AAAA): ")

        conn.request("GET", f"/advancedsearch?start_year={fecha}&end_year={fechav}&min_imdb=6&max_imdb=7.8&genre={gen}&language=english&type={tip}&sort=latest&page=1", headers=headers)
        res = conn.getresponse()
        data = res.read()
        
        movie_data = json.loads(data.decode("utf-8"))

#---------------------------------------------------------------------------

        #os.system('pause')
        movie_ids = [movie['imdbid'] for movie in movie_data['results']]
        #os.system('cls')
        print("RESULTADOS")
        for movie_id in movie_ids:
            conn_imdb.request("GET", f"/v1/title/?id={movie_id}", headers=headers_imdb)
            res_imdb = conn_imdb.getresponse()
            data_imdb = res_imdb.read()
            movie_info = json.loads(data_imdb.decode("utf-8"))
            if 'runtime' in movie_info and movie_info['runtime'] is not None and 'seconds' in movie_info['runtime']:
                movie_duration = int(movie_info['runtime']['seconds']) / 60
                if duracion_min <= movie_duration * 60 <= duracion_max:
                    print(f"Título: {movie_info['titleText']['text']}")
            else:
                print(f"Titulo: {movie_info['titleText']['text']}")

        #os.system('pause')



