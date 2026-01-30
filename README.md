# dns-ly

```
 ██████╗ ███╗   ██╗███████╗      ██╗  ██╗   ██╗
 ██╔══██╗████╗  ██║██╔════╝      ██║  ╚██╗ ██╔╝
 ██║  ██║██╔██╗ ██║███████╗█████╗██║   ╚████╔╝ 
 ██║  ██║██║╚██╗██║╚════██║╚════╝██║    ╚██╔╝  
 ██████╔╝██║ ╚████║███████║      ███████╗██║   
 ╚═════╝ ╚═╝  ╚═══╝╚══════╝      ╚══════╝╚═╝   
```

**DNS Insight Made Simple**

A professional DNS reconnaissance tool designed for cybersecurity professionals and penetration testers. Perform comprehensive DNS lookups with beautiful, colored output and multiple export formats.

## Features

- **Multiple Record Types**: Query A, AAAA, CNAME, MX, NS, TXT, SOA, and PTR records
- **Beautiful Output**: Rich, colored terminal output with tables and progress indicators
- **Multiple Formats**: Export results as human-readable text or JSON
- **Fast & Reliable**: Built on dnspython for robust DNS resolution
- **Flexible Queries**: Query single or multiple record types in one command
- **Professional**: Designed to look and feel like real pentesting tools
- **Verbose Mode**: Detailed output for debugging and analysis
- **Quiet Mode**: Minimal output for scripting and automation

## Installation

### Method 1: Using pipx (Recommended)

**pipx** installs Python CLI tools in isolated environments, preventing conflicts.

```bash
# Install pipx (if not already installed)
sudo apt install pipx        # Debian/Ubuntu/Kali
brew install pipx            # macOS

# Ensure pipx is in PATH
pipx ensurepath

# Install dns-ly
git clone https://github.com/Roman1-debug/dns-ly.git
cd dns-ly
pipx install .
```

### Method 2: From Source (Virtual Environment)

```bash
# Clone the repository
git clone https://github.com/Roman1-debug/dns-ly.git
cd dns-ly

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install with pip
pip install .
```

### Requirements

- Python 3.8 or higher
- dnspython >= 2.4.0
- rich >= 13.0.0

## Usage

### Basic Usage

```bash
# Query A records (default)
dns-ly example.com

# Query specific record type
dns-ly example.com -t MX

# Query multiple record types
dns-ly example.com -t A,AAAA,MX,TXT

# Query all common record types
dns-ly example.com -t ALL
```

### Output Formats

```bash
# Human-readable output (default)
dns-ly example.com -t MX

# JSON output for scripting
dns-ly example.com -t A -o json
```

### Advanced Options

```bash
# Verbose mode
dns-ly example.com -v

# Quiet mode (no banner)
dns-ly example.com -q

# Combine options
dns-ly example.com -t ALL -o json -q
```

### Examples

**Query MX records:**
```bash
$ dns-ly google.com -t MX
```

**Query all record types:**
```bash
$ dns-ly github.com -t ALL
```

**Export to JSON:**
```bash
$ dns-ly example.com -t A,AAAA -o json > results.json
```

**Quiet mode for scripting:**
```bash
$ dns-ly example.com -q -o json | jq '.records[]'
```

## Command-Line Options

```
usage: dns-ly [-h] [-t RECORD_TYPE] [-o {text,json}] [-v] [-q] [--version] domain

positional arguments:
  domain                Domain name to query

optional arguments:
  -h, --help            show this help message and exit
  -t RECORD_TYPE, --type RECORD_TYPE
                        DNS record type(s) to query (comma-separated or ALL) [default: A]
  -o {text,json}, --output {text,json}
                        Output format [default: text]
  -v, --verbose         Enable verbose output
  -q, --quiet           Quiet mode (no banner)
  --version             show program's version number and exit
```

## Supported Record Types

| Type | Description |
|------|-------------|
| A | IPv4 address records |
| AAAA | IPv6 address records |
| CNAME | Canonical name records |
| MX | Mail exchange records |
| NS | Name server records |
| TXT | Text records |
| SOA | Start of authority records |
| PTR | Pointer records (reverse DNS) |

## Output Examples

### Text Output (Default)
```
✓ DNS Query Results for example.com
Record Type: A
Records Found: 1

╭────────────────╮
│ Record         │
├────────────────┤
│ 93.184.216.34  │
╰────────────────╯
```

### JSON Output
```json
{
  "success": true,
  "domain": "example.com",
  "record_type": "A",
  "records": [
    "93.184.216.34"
  ],
  "count": 1
}
```

## Development

### Project Structure

```
dns-ly/
├── dns-ly/
│   ├── __init__.py      # Package metadata
│   ├── cli.py           # CLI interface
│   └── core.py          # Core DNS lookup logic
├── requirements.txt     # Dependencies
├── setup.py            # Installation script
├── README.md           # This file
├── LICENSE             # MIT License
└── .gitignore          # Git ignore rules
```

### Running Tests

```bash
# Test basic functionality
dns-ly google.com

# Test multiple record types
dns-ly github.com -t ALL

# Test JSON output
dns-ly example.com -o json
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Roman**
- GitHub: [@Roman1-debug](https://github.com/Roman1-debug)

## Contributing

Contributions, issues, and feature requests are welcome!

## Show Your Support

Give a ⭐️ if this project helped you!

---

**Note**: This tool is designed for legitimate security research and network administration. Always ensure you have permission before performing DNS reconnaissance on domains you don't own.


