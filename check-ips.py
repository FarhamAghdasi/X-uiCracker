import requests
import threading
import concurrent.futures
import random
from os import system, name
from pystyle import Colors, Colorate, Center

b = '''
 ▄▀ ▗▖  ▗▖▗▖ ▗▖▗▄▄▄▖    ▗▖  ▗▖ ▗▄▖ ▗▖   ▗▄▄▄▖▗▄▄▄   ▗▄▖▗▄▄▄▖▗▄▖ ▗▄▄▖ 
 █   ▝▚▞▘ ▐▌ ▐▌  █      ▐▌  ▐▌▐▌ ▐▌▐▌     █  ▐▌  █ ▐▌ ▐▌ █ ▐▌ ▐▌▐▌ ▐▌
▄▀    ▐▌  ▐▌ ▐▌  █      ▐▌  ▐▌▐▛▀▜▌▐▌     █  ▐▌  █ ▐▛▀▜▌ █ ▐▌ ▐▌▐▛▀▚▖
    ▗▞▘▝▚▖▝▚▄▞▘▗▄█▄▖     ▝▚▞▘ ▐▌ ▐▌▐▙▄▄▖▗▄█▄▖▐▙▄▄▀ ▐▌ ▐▌ █ ▝▚▄▞▘▐▌ ▐▌    

                          t.me/secabuser
'''

class Checker:
    def __init__(self, ip_file, workers, timeout):
        self.ip_file = ip_file
        self.workers = workers
        self.timeout = timeout
        self.lock = threading.Lock()
        self.targets = []

    def load_ips(self):
        try:
            with open(self.ip_file, "r") as f:
                for line in f:
                    clean = line.strip()
                    if clean and ':' in clean:
                        self.targets.append(clean)
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

    def check_ip(self, target):
        for proto in ["http://", "https://"]:
            url = f"{proto}{target}/xui"
            headers = {"User-Agent": self.user_agent()}
            try:
                r = requests.get(url, headers=headers, timeout=self.timeout)
                if r.status_code not in [400, 404, 407, 503]:
                    with self.lock:
                        with open("good-sites.txt", "a") as f:
                            f.write(target + "\n")
                    print(f"[Good] {target} ({r.status_code})")
                    return
            except requests.RequestException:
                continue
        print(f"[Not Good] {target}")

    def run(self):
        self.load_ips()
        if not self.targets:
            print("No valid IPs loaded.")
            return
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            executor.map(self.check_ip, self.targets)
        print("\nDone!")

if __name__ == "__main__":
    try:
        system("cls" if name == "nt" else "clear")
    except:
        pass
    print(Colorate.Diagonal(Colors.red_to_blue, Center.XCenter(b)))
    ip_file = input("IP list file > ").strip()
    try:
        workers = int(input("Max workers > ").strip())
        timeout = float(input("Timeout > ").strip())
    except ValueError:
        print("Invalid input!")
        exit(1)

    checker = Checker(ip_file, workers, timeout)
    checker.run()
