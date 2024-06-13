# CNAME Record Checker

This Python script helps you check subdomains for CNAME records and identify the targets they point to.

## Features

* Checks subdomains from a text file.
* Uses Google Public DNS (8.8.8.8) by default for lookups (configurable).
* Outputs results in JSON format (default) or text format.
* Add option for summery report
* Add option for show only unique cname records
* Get subdomains in pipe (cat subdomains | python3 cname-mapper.py )

### Options:

```bash
  -f FILE, --file FILE  Path to the text file containing subdomains
  -ns NAMESERVER, --nameserver NAMESERVER
                        Optional, nameserver to use for DNS queries (defaults
                        to 8.8.8.8)
  -o {text,json}, --output {text,json}
                        Optional, Output format (JSON, or text(default))
  -r, --report          Optional, Show a summary report about process
  -c, --cname           Optional, Show only cnames
```

## Installation

**Requirements:**

* Python 3

## Usage

1. Clone the project.
2. `cd cname-mapper`
3. `pip3 install -r requirements.txt`
5. Run the script from the command line:

```bash
python3 cname-mapper.py --file subdomains.txt 
```

### Output 

![cname_mapper-simple](https://github.com/miladkeivanfar/cname-mapper/assets/129506375/b7557b21-b5a3-4fec-a5a4-47218caeb7ea)


### Some Examples:

```bash
python3 cname-mapper.py -f subdomains.txt
cat subdomains.txt | python3 cname-mapper.py
python3 cname-mapper.py -f subdomains.txt -r # show summery report
python3 cname-mapper.py -f subdomains.txt -c # only show unique CNAME
python3 cname-mapper.py -f subdomains.txt -ns # use custom name server for DNS queries 
```



## How it Works

The script iterates through the subdomains in the provided file and performs DNS queries using the dnspython library. It checks for CNAME records and returns the target domain if found. The results are then stored in a dictionary and finally converted to JSON (or printed in text format depending on the chosen output).


