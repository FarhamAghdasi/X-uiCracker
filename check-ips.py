import aiohttp
import asyncio
import random
from os import system, name
from pystyle import Colors, Colorate, Center
from tqdm import tqdm
import logging
import json
import argparse

logging.basicConfig(
    filename="scan_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

b = '''
 ▄▀ ▗▖  ▗▖▗▖ ▗▖▗▄▄▄▖    ▗▖  ▗▖ ▗▄▖ ▗▖   ▗▄▄▄▖▗▄▄▄   ▗▄▖▗▄▄▄▖▗▄▖ ▗▄▄▖ 
 █   ▝▚▞▘ ▐▌ ▐▌  █      ▐▌  ▐▌▐▌ ▐▌▐▌     █  ▐▌  █ ▐▌ ▐▌ █ ▐▌ ▐▌▐▌ ▐▌
▄▀    ▐▌  ▐▌ ▐▌  █      ▐▌  ▐▌▐▛▀▜▌▐▌     █  ▐▌  █ ▐▛▀▜▌ █ ▐▌ ▐▌▐▛▀▚▖
    ▗▞▘▝▚▖▝▚▄▞▘▗▄█▄▖     ▝▚▞▘ ▐▌ ▐▌▐▙▄▄▖▗▄█▄▖▐▙▄▄▀ ▐▌ ▐▌ █ ▝▚▄▞▘▐▌ ▐▌    
                          t.me/secabuser
'''

class IPChecker:
    def __init__(self, ip_file, workers, timeout, proxy_file=None):
        self.ip_file = ip_file
        self.workers = workers
        self.timeout = timeout
        self.proxy_file = proxy_file
        self.targets = []
        self.proxies = []
        self.good_sites = []

    def load_ips(self):
        try:
            with open(self.ip_file, "r") as f:
                for line in f:
                    clean = line.strip()
                    if clean and ':' in clean:
                        self.targets.append(clean)
            logging.info(f"Loaded {len(self.targets)} IPs from {self.ip_file}")
        except FileNotFoundError:
            logging.error(f"IP file {self.ip_file} not found!")
            print("IP file not found!")
            exit(1)

    def load_proxies(self):
        if self.proxy_file:
            try:
                with open(self.proxy_file, "r") as f:
                    self.proxies = [line.strip() for line in f if line.strip()]
                logging.info(f"Loaded {len(self.proxies)} proxies from {self.proxy_file}")
            except FileNotFoundError:
                logging.error(f"Proxy file {self.proxy_file} not found!")
                print("Proxy file not found!")
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

    async def check_ip(self, session, target, progress):
        for proto in ["http://", "https://"]:
            url = f"{proto}{target}/xui"
            headers = {"User-Agent": self.user_agent()}
            proxy = random.choice(self.proxies) if self.proxies else None
            try:
                async with session.get(url, headers=headers, timeout=self.timeout, proxy=proxy) as r:
                    if r.status not in [400, 404, 407, 503]:
                        self.good_sites.append({"url": target, "status": r.status})
                        logging.info(f"[Good] {target} ({r.status})")
                        print(f"[Good] {target} ({r.status})")
                        return
            except Exception as e:
                logging.warning(f"[Not Good] {target} - Error: {str(e)}")
                continue
        print(f"[Not Good] {target}")
        progress.update(1)

    async def run(self):
        self.load_ips()
        self.load_proxies()
        if not self.targets:
            print("No valid IPs loaded.")
            logging.error("No valid IPs loaded.")
            return

        async with aiohttp.ClientSession() as session:
            with tqdm(total=len(self.targets), desc="Scanning IPs") as progress:
                tasks = [self.check_ip(session, target, progress) for target in self.targets]
                await asyncio.gather(*tasks, return_exceptions=True)

        if self.good_sites:
            with open("good-sites.json", "w") as f:
                json.dump(self.good_sites, f, indent=4)
            print(f"\nResults saved to good-sites.json")
            logging.info(f"Saved {len(self.good_sites)} good sites to good-sites.json")
        print("\nDone!")

def clear_screen():
    try:
        system("cls" if name == "nt" else "clear")
    except:
        pass

def main():
    parser = argparse.ArgumentParser(description="X-uiCracker IP Scanner")
    parser.add_argument("--ip-file", default="urls.txt", help="File containing IP addresses")
    parser.add_argument("--workers", type=int, default=50, help="Maximum number of concurrent workers")
    parser.add_argument("--timeout", type=float, default=5.0, help="Timeout for HTTP requests (seconds)")
    parser.add_argument("--proxy-file", help="File containing proxy addresses")
    args = parser.parse_args()

    clear_screen()
    print(Colorate.Diagonal(Colors.red_to_blue, Center.XCenter(b)))

    checker = IPChecker(args.ip_file, args.workers, args.timeout, args.proxy_file)
    asyncio.run(checker.run())

if __name__ == "__main__":
    main()