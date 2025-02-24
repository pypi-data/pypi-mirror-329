import requests

def watch(service, alert_callback):
    if service.startswith("http"):
        try:
            response = requests.get(service, timeout=5)
            if response.status_code == 200:
                print(f"Service {service} is healthy!")
            else:
                alert_callback(f"Service {service} returned status code {response.status_code}")
        except Exception as e:
            alert_callback(f"Service {service} is down! Error: {e}")
    else:
        print(f"Monitoring service '{service}' (simulated)...")
        print(f"Service {service} is healthy!")
