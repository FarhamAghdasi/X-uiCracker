import requests
import threading
import concurrent.futures
import random
from os import system, name

class Checker:
    def __init__(self, ip_file, port, workers, timeout):
        self.ip_file = ip_file
        self.port = port
        self.workers = workers
        self.timeout = timeout
        self.lock = threading.Lock()
        self.ips = []

    def load_ips(self):
        try:
            with open(self.ip_file, "r") as f:
                self.ips = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("IP file not found!")
            exit(1)

    def user_agent(self):
        agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0)",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X)"
        ]
        return random.choice(agents)

    def check_ip(self, ip):
        for proto in ["http://", "https://"]:
            url = f"{proto}{ip}:{self.port}"
            headers = {"User-Agent": self.user_agent()}
            try:
                r = requests.get(url, headers=headers, timeout=self.timeout)
                if r.status_code != 503:
                    with self.lock:
                        with open("good-sites.txt", "a") as f:
                            f.write(url + "\n")
                    print(f"[Good] {url}")
                    return
            except requests.RequestException:
                continue
        print(f"[Not Good] {ip}")

    def run(self):
        self.load_ips()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            executor.map(self.check_ip, self.ips)
        print("\nDone!")

if __name__ == "__main__":
    system("cls" if name == "nt" else "clear")
    ip_file = input("IP list file > ").strip()
    port = input("Port > ").strip()
    try:
        workers = int(input("Max workers > ").strip())
        timeout = float(input("Timeout > ").strip())
    except:
        print("Invalid input")
        exit(1)

    checker = Checker(ip_file, port, workers, timeout)
    checker.run()
