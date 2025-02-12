import requests
import dns.resolver
from colorama import Fore, Style
import sys
import time

idk = f"""
             \033[92m██╗░░░██╗░█████╗░██████╗░░██████╗░██╗
             ╚██╗░██╔╝██╔══██╗██╔══██╗██╔════╝░██║
             ░╚████╔╝░███████║██████╔╝██║░░██╗░██║
             ░░╚██╔╝░░██╔══██║██╔══██╗██║░░╚██╗██║
             ░░░██║░░░██║░░██║██║░░██║╚██████╔╝██║
             ░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝░╚═════╝░╚═╝
             \033[31m                                         \033[0m
"""
print(idk)

def main1(domain):
    crt_sh_url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        response = requests.get(crt_sh_url)
        if response.status_code == 200:
            subdomains = set()
            crt_data = response.json()
            for entry in crt_data:
                subdomain = entry['name_value']
                subdomains.update(subdomain.split("\n"))
            return subdomains
        else:
            print(Fore.RED + f"ERROR FETCHING DOMAINS... {domain}: {response.status_code}" + Style.RESET_ALL)
            return None
    except requests.RequestException as e:
        print(Fore.RED + f"ERROR FETCHING SUBDOMAINS FROM crt.sh: {e}" + Style.RESET_ALL)
        return None

def main2(domain):
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = ['8.8.8.8', '8.8.4.4']
    try:
        result = resolver.resolve(domain, 'A')
        return result[0].to_text()
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
        print(Fore.RED + f"ORIGIN IP NOT FOUND FOR: {domain}" + Style.RESET_ALL)
        return None

def main3(ip):
    cloudflare_ip_ranges = [
        "104.16.", "104.17.", "104.18.", "104.19.", "104.20.", "104.21.", "104.22.", "104.23.",
        "172.64.", "172.65.", "172.66.", "172.67.", "173.245.", "188.114.", "190.93.", "197.234.",
        "198.41.", "199.27."
    ]
    if not ip:
        return False
    for range_prefix in cloudflare_ip_ranges:
        if ip.startswith(range_prefix):
            return False
    return True

def main4(prompt, typing_speed=0.1):
    for char in prompt:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(typing_speed)
    return input()

def main5(domain):
    subdomains = main1(domain)
    if not subdomains:
        print(Fore.RED + "SUBDOMAINS NOT FOUND." + Style.RESET_ALL)
        return
    print(Fore.LIGHTGREEN_EX + f"FOUND {len(subdomains)} SUBDOMAINS. CHECKING FOR IPs..." + Style.RESET_ALL)
    for subdomain in subdomains:
        ip = main2(subdomain)
        if ip:
            if main3(ip):
                print(Fore.LIGHTGREEN_EX + f"POTENTIAL ORIGIN FOUND FOR: {subdomain} IP: {ip}" + Style.RESET_ALL)
            else:
                print(f"\033[38;5;214mFOUND CLOUDFARE IP FOR: {subdomain} IP: {ip} BUT NO ORIGIN \033[38;5;214m")

if __name__ == "__main__":
    domain = main4("Enter the domain: ", typing_speed=0.05)
    print("")
    main5(domain)
