import requests

def get_google_custom_search_results(query, num_results=10, location='us', language='en'):
    api_key = 'AIzaSyAU2xTU6jE1n785RZPxZ_Npz9Vl4jRLdyA'
    search_engine_id = '17271f76bff4b4b74'
    search_url = 'https://www.googleapis.com/customsearch/v1'
    
    params = {
        'key': api_key,
        'cx': search_engine_id,
        'q': query,
        'num': min(num_results, 10),  # Google API returns a maximum of 10 results per request
        'gl': location,               # Country code
        'hl': language                # Language
    }

    results = []
    start_index = 1

    while len(results) < num_results:
        params['start'] = start_index
        response = requests.get(search_url, params=params)
        if response.status_code != 200:
            return {"error": "Failed to retrieve search results"}
        
        data = response.json()
        items = data.get('items', [])
        
        for item in items:
            results.append({
                'title': item.get('title'),
                'link': item.get('link')
            })
        
        if 'nextPage' not in data['queries']:
            break
        
        start_index += 10

    return results[:num_results]

# Example usage
query = "python programming"
results = get_google_custom_search_results(query, num_results=20, location='us', language='en')
for i, result in enumerate(results):
    print(f"{i + 1}. {result['title']} - {result['link']}")
