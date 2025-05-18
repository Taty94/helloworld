import time
import requests

def check_service(name, url):
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"{name} is up and running with status code: 200")
                return True
            else:
                print(f"{name} responded with status code: {response.status_code}")
        except requests.ConnectionError:
            print(f"{name} not ready yet. Retrying in 5 seconds...")
        time.sleep(5)

if __name__ == "__main__":
    print("Checking WireMock...")
    check_service("WireMock", "http://127.0.0.1:9090/__admin")

    print("Checking Flask app...")
    check_service("Flask", "http://127.0.0.1:5000")