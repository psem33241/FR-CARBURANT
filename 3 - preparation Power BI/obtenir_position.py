'''
import geocoder

def obtenir_position_utilisateur():
    """Obtient les coordonnées GPS de l'utilisateur."""
    g = geocoder.ip('me')  # Utilise l'IP pour déterminer la localisation  
    if g.ok:
        return g.latlng  # retourne [latitude, longitude]
    else:
        print("Impossible d'obtenir la localisation.")
        return None

# Exemple d'utilisation  
position = obtenir_position_utilisateur()
if position:
    latitude, longitude = position  
    print(f"Latitude: {latitude}, Longitude: {longitude}")
    '''


import geocoder  
import mysql.connector  
from mysql.connector import Error

def obtenir_position_utilisateur():
    """Obtient les coordonnées GPS de l'utilisateur."""
    g = geocoder.ip('me')  # Utilise l'IP pour déterminer la localisation  
    if g.ok:
        return g.latlng  # Retourne [latitude, longitude]
    else:
        print("Impossible d'obtenir la localisation.")
        return None

def trouver_stations_service(latitude, longitude, rayon):
    """Trouve les stations de service à proximité en fonction de la latitude et de la longitude."""
    try:
        # Connexion à la base de données MySQL  
        conn = mysql.connector.connect(
            host='localhost',  # Remplacez par votre hôte (ex: 'localhost')
            user='root',  # Remplacez par votre nom d'utilisateur  
            password='14061971',  # Remplacez par votre mot de passe  
            database='projet_carburants_france'  # Remplacez par le nom de votre base de données  
        )

        if conn.is_connected():
            cursor = conn.cursor()

            # Requête SQL  
            query = """
            SELECT 
                adresse_complete,
                ROUND((6371 * ACOS(
                    COS(RADIANS(%s)) * COS(RADIANS(latitude)) * 
                    COS(RADIANS(longitude) - RADIANS(%s)) + 
                    SIN(RADIANS(%s)) * SIN(RADIANS(latitude))
                )), 2) AS distance_km  
            FROM 
                stations_service  
            HAVING 
                distance_km < %s  
            ORDER BY  
                distance_km ASC;
            """

            # Exécution de la requête avec les paramètres  
            cursor.execute(query, (latitude, longitude, latitude, rayon))
            resultats = cursor.fetchall()

            # Affichage des résultats  
            for adresse, distance in resultats:
                print(f"Adresse: {adresse}, Distance: {distance} km")

    except Error as e:
        print(f"Une erreur est survenue : {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Exemple d'utilisation  
position = obtenir_position_utilisateur()
if position:
    latitude, longitude = position  
    rayon = 10  # Définir le rayon de recherche, par exemple 10 km  
    trouver_stations_service(latitude, longitude, rayon)