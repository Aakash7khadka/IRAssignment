import re
import concurrent.futures
import requests
import os


directory = "documents"
if not os.path.exists(directory):
    os.makedirs(directory)

def fetch_and_write(topic):
    try:
        text_config = {
            'action': 'query',
            'format': 'json',
            'titles': topic,
            'prop': 'extracts',
            'exintro': True,
            'explaintext': True,
        }

        text_response = requests.get('https://en.wikipedia.org/w/api.php',params=text_config).json()
        text_page = next(iter(text_response['query']['pages'].values()))
        # filename = re.sub(r'[<>:"/\\|?*\n]', '_', text_page['title'])
        if 'extract' in text_page and len(text_page['extract']) > 0:

            file_name = topic + ".txt"

            directory = "documents"
            directory = os.path.join(directory, file_name)
            with open(directory ,"w", encoding='utf-8') as write_file:
                write_file.write(text_page['extract'])

            print(f"Response  writing to {file_name}")
        else:
            print(f"Failed to fetch api: {text_response.status_code}")
    except Exception as e:
        print(f"Error fetching api: {e}")



f = open ("topics2.txt", "r", encoding="utf-8")



with concurrent.futures.ThreadPoolExecutor() as executor:

    futures = [executor.submit(fetch_and_write, re.sub(r'[<>:"/\\|?*\n]', '', topic)) for topic in f.readlines()]
    for future in concurrent.futures.as_completed(futures):
        future.result()

print("All API requests completed.")

