import requests
import json
import sys

def download_and_filter_json(url, user_name):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica si hubo algún error en la solicitud

        # Decodifica el contenido JSON
        data = response.json()

        # Procesa el contenido JSON filtrando por nombre de usuario
        filtered_data = [entry for entry in data if entry.get('userName').lower() == (user_name).lower()]
        path = f"data/{user_name}/times/"
        # Guarda el contenido filtrado en un archivo JSON
        with open(path+user_name+"_posts_times.json", 'w', encoding='utf-8') as file:
            json.dump(filtered_data, file, ensure_ascii=False, indent=4)
        
        print(f"Filtered file saved as {user_name}")
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python request.py <user_name>")
    else:
        user_name = sys.argv[1]
        url = 'http://localhost:3001/download/answersPostsAndSurvey'
        download_and_filter_json(url, user_name)
