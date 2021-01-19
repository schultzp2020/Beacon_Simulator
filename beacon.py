import argparse
import requests
import time
import numpy as np

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 *(iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)

    if iteration == total:
        print()

def check_status_code(r):
    if r.status_code == 200:
        if args.random:
            mean = args.interval
            scale = mean * 0.16
            interval = int(np.abs(round(np.random.normal(mean, scale), 0)))
        else: 
            interval = args.interval
        if args.verbose:
            print("Successfully sent the payload!\n")
            print(f"Waiting for {interval} seconds...")
            print_progress_bar(0, interval)
        for i in range(interval):
            time.sleep(1)
            if args.verbose:
                print_progress_bar(i+1, interval)
        if args.verbose:
            print(f"Done waiting!\n")
    else:
        print("Domain did not return a successful response!")
        exit(1)


def validate_domain():
    if args.verbose:
        print("Validating domain...")
    if not ("https://" in args.domain or "http://" in args.domain):
        try:
            if args.verbose:
                print("Checking https connection...")
            r = requests.get("https://" + args.domain)
            args.domain = "https://" + args.domain
            if args.verbose:
                print(f"Connected using {args.domain}!")
        except:
            try:
                if args.verbose:
                    print("Checking http connection...")
                r = requests.get("http://" + args.domain)
                args.domain = "http://" + args.domain
                if args.verbose:
                    print(f"Connected using {args.domain}!")
            except:
                print("Failed to establish a connection!")
                exit(1)
        finally:
            check_status_code(r)
    else:
        try:
            if args.verbose:
                print(f"Testing connection...")
            r = requests.get(args.domain)
            if args.verbose:
                print(f"Connected using {args.domain}!")
        except:
            print("Failed to establish a connection!")
            exit(1)
        else:
            check_status_code(r)
    if args.verbose:
        print("Completed validation!\n")

def create_beacon():
    while True:
        try:
            if args.verbose:
                print("Sending payload!")
            r = requests.get(args.domain)
        except:
            print("Failed to establish a connection!")
            exit(1)
        else:
            check_status_code(r)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Beacon Simulator")
    parser.add_argument("domain", nargs='?', help="Enter a domain to act as a C2.", type=str)
    parser.add_argument("-i", "--interval", help="Enter a time interval in seconds.", type=int)
    parser.add_argument("-v", "--verbose", help="Verbose mode: displays when the next packet will be sent.", action="store_true", default=False)
    parser.add_argument("-V", "--version", help="Print out version and exit.", action="store_true", default=False)
    parser.add_argument("-r", "--random", help="Randomizes the sleep interval for the beacon using normal distribution.", action="store_true", default=False)
    args = parser.parse_args()
    if args.version:
        print("Beacon Sumulator version 1.0")
        exit(0)
    if not args.domain:
        print("Please enter a domain to act as a C2.")
        exit(1)
    if args.interval < 1: 
        print("Please enter a time interval greater than zero.")
    if not args.interval:
        args.interval = 60

    validate_domain()

    create_beacon()