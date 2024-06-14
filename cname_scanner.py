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

def output(cname_records,output=None):

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

def report(all_subs,unique_cname=None,duration_process=None):
  print("\n")
  print(Fore.GREEN + 'Summery Report:\n' + Style.RESET_ALL)

  table = [["Duration", duration_process, "Duration of process"],["","" , ""],["All Subdomains", all_subs, "Number of subdomains in input file."],
  ["Unique CNAME", unique_cname, "Number of Unique CNAME in result."]]

  print(tabulate(table, headers=["Name", "Quantity", "Description"],tablefmt="github"))

def check_cname(subdomain, nameserver=None):
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

def main():
  start = time.time()
  parser = argparse.ArgumentParser(description='This Python script helps you check subdomains for CNAME records and identify the targets they point to.')
  parser.add_argument('-f','--file', type=str, required=False, help='Path to the text file containing subdomains')
  parser.add_argument('-ns','--nameserver', type=str, default=None, help='Optional, nameserver to use for DNS queries (defaults to 8.8.8.8)')
  parser.add_argument('-o','--output', type=str, choices=['text', 'json'], default='text', help='Optional, Output format (JSON, or text(default))')
  parser.add_argument("-r", "--report", help="Optional, Show a summary report about process", action="store_true")
  parser.add_argument("-c", "--cname", help="Optional, Show only cnames ", action="store_true")
  args = parser.parse_args()

  cname_records = {}

  try:
    # Read from stdin
    if not sys.stdin.isatty():

      lines = sys.stdin
      all_subs = 0

      for subdomain in sys.stdin:
        all_subs += 1
        if subdomain.startswith("http://") or subdomain.startswith("https://"):
            subdomain = urlparse(subdomain).hostname

        cname_target = check_cname(subdomain, args.nameserver)
        if cname_target:
            if cname_target not in cname_records:
                cname_records[cname_target] = []
            cname_records[cname_target].append(subdomain)


    else:
    # Read from the specified file
      with open(args.file, 'r') as f:

        lines = f.readlines()
        all_subs = len(lines) # find number of subs in input file

        for line in lines:
          subdomain = line.strip()
          if subdomain.startswith("http://") or subdomain.startswith("https://"):
            subdomain = urlparse(subdomain).hostname

          cname_target = check_cname(subdomain, args.nameserver)
          if cname_target:
            if cname_target not in cname_records:
              cname_records[cname_target] = []
            cname_records[cname_target].append(subdomain)

    cname_keys = list(cname_records.keys())
    unique_cname = len(cname_keys)

    if args.cname == True:
      for cname in cname_keys:
        print(cname)
    else:
      output(cname_records,args.output)

    end = time.time()
    duration = end - start
    duration_process = convert_duration(duration)

    if args.report == True:
      report(all_subs,unique_cname,duration_process)
  except ValueError:
     print(f"Invalid URL: {subdomain}")
     sys.exit(1)

   

if __name__ == '__main__':
 
  main()
