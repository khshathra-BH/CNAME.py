import dns.resolver
import dns.exception
import json
import time
import argparse
import sys
from tabulate import tabulate
from colorama import Fore, Style
from urllib.parse import urlparse

def convert_duration(duration):
    # Convert the duration to seconds
    total_seconds = duration

    # Calculate hours, minutes, and seconds
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)

    # Format the duration
    if hours > 0:
        formatted_duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    elif minutes > 0:
        formatted_duration = f"{minutes:02d}:{seconds:02d}"
    else:
        formatted_duration = f"00:00:{seconds:02d}"

    return formatted_duration


def output(cname_records, output=None):
    # Make Output
    if output == 'text':
        # Print results in text format
        for cname, subdomains in cname_records.items():
            print(f"\n{Fore.CYAN + cname + Style.RESET_ALL}")
            print('-' * len(cname))

            for subdomain in subdomains:
                print(subdomain)
            print()

    else:
        # Prepare JSON data structure
        results = []
        for cname, subdomains in cname_records.items():
            result = {
                "cname": cname,
                "subdomains": subdomains
            }
            results.append(result)

        # Convert to JSON string and print
        json_data = json.dumps(results, indent=4)
        print(json_data)


def report(all_subs, unique_cname=None, duration_process=None):
    # Make summery report
    print("\n")
    print(Fore.GREEN + 'Summery Report:\n' + Style.RESET_ALL)

    table = [["Duration", duration_process, "Duration of process"], ["", "", ""],
             ["All Subdomains", all_subs, "Number of subdomains in input file."],
             ["Unique CNAME", unique_cname, "Number of Unique CNAME in result."]]

    print(tabulate(table, headers=["Name", "Quantity", "Description"], tablefmt="github"))


def check_cname(subdomain, nameserver=None):
    # check CNAME porcess
    resolver = dns.resolver.Resolver()

    # Set default nameserver to 8.8.8.8
    resolver.nameservers = ['8.8.8.8', '1.1.1.1']

    # Override with a custom nameserver if provided
    if nameserver:
        resolver.nameservers = [nameserver]

    try:
        answer = resolver.resolve(subdomain, 'CNAME')
        for record in answer:
            return record.target.to_text()  # Extract CNAME target as a string
    except dns.exception.DNSException:
        pass  # Handle DNS resolution error gracefully
    return None

def process_subdomain(subdomain, cname_records, args):
    # Map CNAMEs to each subdomains
    cname_target = check_cname(subdomain, args.nameserver)
    if cname_target:
        if cname_target not in cname_records:
            cname_records[cname_target] = []
        cname_records[cname_target].append(subdomain)

def verify_input(subdomain):
    # validation input
    if subdomain.startswith("http://") or subdomain.startswith("https://"):
        subdomain = urlparse(subdomain).hostname
        return subdomain

def main():
    start = time.time()
    parser = argparse.ArgumentParser(
        description='This Python script helps you check subdomains for CNAME records and identify the targets they point to.')
    parser.add_argument('-f', '--file', type=str, required=False, help='Path to the text file containing subdomains')
    parser.add_argument('-ns', '--nameserver', type=str, default=None,
                        help='Optional, nameserver to use for DNS queries (defaults to 8.8.8.8)')
    parser.add_argument('-o', '--output', type=str, choices=['text', 'json'], default='text',
                        help='Optional, Output format (JSON, or text(default))')
    parser.add_argument("-c", "--cname", help="Optional, Show only cnames ", action="store_true")
    parser.add_argument("-d", "--delete", help="Optional, Show all subdomains whitout CNAMEs", action="store_true")
    parser.add_argument("-s","--silent", action="store_true", help="Do not show the report")
    args = parser.parse_args()

    cname_records = {}
    all_subdomains = []
    try:
        # Read from stdin
        if not sys.stdin.isatty():

            lines = sys.stdin
            all_subs = 0

            for subdomain in sys.stdin:
                all_subs += 1
                subdomain = verify_input(subdomain)
                all_subdomains.append(subdomain)
                process_subdomain(subdomain, cname_records, args)

        else:
            # Read from the specified file
            with open(args.file, 'r') as f:

                lines = f.readlines()
                all_subs = len(lines)  # find number of subs in input file

                for line in lines:
                    subdomain = line.strip()
                    subdomain = verify_input(subdomain)
                    all_subdomains.append(subdomain)
                    process_subdomain(subdomain, cname_records, args)

        cname_keys = list(cname_records.keys())
        cname_values = list(cname_records.values())
        unique_cname = len(cname_keys)

        if args.cname:
            print(Fore.GREEN + 'Result with unique CNAME:\n' + Style.RESET_ALL)
            for cname in cname_keys:
                print(cname)
        elif args.delete:
            print(Fore.GREEN + 'Result with remove CNAMEs:\n' + Style.RESET_ALL)
            all_cnames = []
            without_cname = 0
            for a in cname_values:
                for b in a:
                    all_cnames.append(b)
            for sub in all_subdomains:
                if sub not in all_cnames:
                    without_cname += 1
                    print(sub)
        else:
            output(cname_records, args.output)

        end = time.time()
        duration = end - start
        duration_process = convert_duration(duration)

        if args.silent != True:
            report(all_subs, unique_cname, duration_process)
    except ValueError:
        print(f"Invalid URL: {subdomain}")
        sys.exit(1)

if __name__ == '__main__':
    main()
