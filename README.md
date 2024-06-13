# CNAME Record Checker

This Python script helps you check subdomains for CNAME records and identify the targets they point to.

## Features

* Checks subdomains from a text file.
* Uses Google Public DNS (8.8.8.8) by default for lookups (configurable).
* Outputs results in JSON format (default) or text format.
* Add option for summery report
* Add option for show only unique cname records
* Get subdomains in pip (cat subdomains | python3 cname-mapper.py )

## Installation

**Requirements:**

* Python 3
* `dnspython` library (install using `pip install dnspython`)

## Usage

1. Save the script as `cname.py`.
2. Create a text file containing the subdomains you want to check (one subdomain per line).
3. Run the script from the command line:

```bash
python3 cname-mapper.py --file subdomains.txt
```
### Example Output (JSON format by default)

![image](https://github.com/khshathra-BH/cname-scanner/assets/129506375/74a573e1-cd21-4644-8771-afab3c9d37c6)



This will output the results in JSON format by default.

Options:

--file: Path to the text file containing subdomains (required).

--nameserver: Optional nameserver to use for DNS queries (defaults to 8.8.8.8).

--output: Output format (json - default, or text).

Example (using custom nameserver and text output):

```bash
python3 cname-mapper.py --file subdomains.txt --nameserver 8.4.4.8 --output text
```
### Example Output (text)

![image](https://github.com/khshathra-BH/cname-scanner/assets/129506375/8a5f66da-fb50-4f5e-a472-9dc8acabae9e)


## How it Works

The script iterates through the subdomains in the provided file and performs DNS queries using the dnspython library. It checks for CNAME records and returns the target domain if found. The results are then stored in a dictionary and finally converted to JSON (or printed in text format depending on the chosen output).


