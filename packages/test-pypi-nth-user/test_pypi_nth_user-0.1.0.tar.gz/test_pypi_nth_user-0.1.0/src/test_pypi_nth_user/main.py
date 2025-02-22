import requests

def get_nth_user_name(n):
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    return response.json()[n-1]['name']
