import requests

def fact_check_with_api(claim):
    url = "https://factcheck-api.com/validate"
    params = {"query": claim}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Unable to verify claim. Status code: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
