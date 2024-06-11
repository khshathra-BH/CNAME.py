import dns.resolver
import dns.exception
import json
import argparse
from colorama import Fore, Style

def check_cname(subdomain, nameserver=None):

  resolver = dns.resolver.Resolver()

  # Set default nameserver to 8.8.8.8
  resolver.nameservers = ['8.8.8.8']

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
  parser = argparse.ArgumentParser(description='Check subdomains for CNAME records')
  parser.add_argument('--file', type=str, required=True, help='Path to the text file containing subdomains')
  parser.add_argument('--nameserver', type=str, default=None, help='Optional nameserver to use for DNS queries (defaults to 8.8.8.8)')
  parser.add_argument('--output', type=str, choices=['text', 'json'], default='json', help='Output format (JSON - default, or text)')
  args = parser.parse_args()

  cname_records = {}
  with open(args.file, 'r') as f:
    for line in f:
      subdomain = line.strip()
      cname_target = check_cname(subdomain, args.nameserver)
      if cname_target:
        if cname_target not in cname_records:
          cname_records[cname_target] = []
        cname_records[cname_target].append(subdomain)

  if args.output == 'text':
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

if __name__ == '__main__':
  main()
