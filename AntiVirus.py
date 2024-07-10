import os
import requests
import time

API_KEY = '96afc8b2ca7cd09e9bb7f03c242e5dd2bbeb287b5f03884b2b4c8859bb4758f8'


def scan_file(api_key, file_path):
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'
    params = {'apikey': api_key}
    files = {'file': (file_path, open(file_path, 'rb'))}
    
    response = requests.post(url, files=files, params=params)
    response.raise_for_status()
    return response.json()


def get_report(api_key, resource):
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    params = {'apikey': api_key, 'resource': resource}
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def scan_for_virus(directory, infected_files):
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isfile(path):
            try:
                print("scanning...")
                scan_response = scan_file(API_KEY, path)
                resource = scan_response['resource']

                # Wait for a while to ensure the scan is completed
                time.sleep(20)

                report_response = get_report(API_KEY, resource)
                print(f"got response.")
                if 'positives' in report_response:
                    if report_response['positives'] > 0:
                        infected_files.append(path)
                        print(f"Malicious file detected: {path}")
                else:
                    print(f"Unexpected response format for file {path}: {report_response}")

            except requests.exceptions.RequestException as e:
                print(f"Error scanning file {path}: {e}")
        elif os.path.isdir(path):
            scan_for_virus(path, infected_files)


if __name__ == "__main__":
    while True:
        directory = 'C:'
        if os.path.isdir(directory):
            infected_files = []
            scan_for_virus(directory, infected_files)
            if not infected_files:
                print("No malicious files detected.")
            else:
                print("List of malicious files:")
                for infected_file in infected_files:
                    print(infected_file)
        else:
            print(f"{directory} is not a valid directory")