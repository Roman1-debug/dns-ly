#!/usr/bin/env python3
"""
dnsly CLI - Professional DNS reconnaissance tool
"""

import sys
import argparse
import json
from typing import List
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box
import time

from dnsly.core import dns_lookup
from dnsly import __version__


console = Console()


BANNER = """
[cyan]
 ██████╗ ███╗   ██╗███████╗      ██╗  ██╗   ██╗
 ██╔══██╗████╗  ██║██╔════╝      ██║  ╚██╗ ██╔╝
 ██║  ██║██╔██╗ ██║███████╗█████╗██║   ╚████╔╝ 
 ██║  ██║██║╚██╗██║╚════██║╚════╝██║    ╚██╔╝  
 ██████╔╝██║ ╚████║███████║      ███████╗██║   
 ╚═════╝ ╚═╝  ╚═══╝╚══════╝      ╚══════╝╚═╝   
[/cyan]
[dim]DNS Insight Made Simple | v{version}[/dim]
"""


def print_banner(quiet: bool = False):
    """Print the tool banner."""
    if not quiet:
        console.print(BANNER.format(version=__version__))


def format_text_output(result: dict, verbose: bool = False) -> None:
    """Format and print results as text."""
    if not result["success"]:
        console.print(f"[red]✗[/red] Error: {result['error']}")
        return
    
    console.print(f"\n[green]✓[/green] DNS Query Results for [cyan]{result['domain']}[/cyan]")
    console.print(f"[dim]Record Type:[/dim] [yellow]{result['record_type']}[/yellow]")
    console.print(f"[dim]Records Found:[/dim] [yellow]{result['count']}[/yellow]\n")
    
    # Create table for results
    table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")
    
    if result['record_type'].upper() == "MX":
        table.add_column("Priority", style="yellow")
        table.add_column("Mail Server", style="green")
        for record in result['records']:
            table.add_row(str(record['preference']), record['exchange'])
    
    elif result['record_type'].upper() == "SOA":
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        for record in result['records']:
            for key, value in record.items():
                table.add_row(key.upper(), str(value))
    
    else:
        table.add_column("Record", style="green")
        for record in result['records']:
            table.add_row(str(record))
    
    console.print(table)
    
    if verbose:
        console.print(f"\n[dim]Query completed successfully[/dim]")


def format_json_output(result: dict) -> None:
    """Format and print results as JSON."""
    console.print(json.dumps(result, indent=2))


def perform_lookup(domain: str, record_types: List[str], output_format: str, 
                   verbose: bool, quiet: bool) -> int:
    """
    Perform DNS lookups and display results.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    exit_code = 0
    
    for record_type in record_types:
        if not quiet and len(record_types) > 1:
            console.print(f"\n[cyan]→[/cyan] Querying {record_type} records...")
        
        # Show progress for single queries
        if not quiet and len(record_types) == 1:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task(f"Querying {record_type} records...", total=None)
                result = dns_lookup(domain, record_type)
                progress.update(task, completed=True)
        else:
            result = dns_lookup(domain, record_type)
        
        # Format output
        if output_format == "json":
            format_json_output(result)
        else:
            format_text_output(result, verbose)
        
        # Set exit code if any query fails
        if not result["success"]:
            exit_code = 1
    
    return exit_code


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="dnsly - Professional DNS reconnaissance tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  dnsly example.com                    # Query A records
  dnsly example.com -t MX              # Query MX records
  dnsly example.com -t A,AAAA,MX       # Query multiple record types
  dnsly example.com -t ALL             # Query all common record types
  dnsly example.com -o json            # Output as JSON
  dnsly example.com -v                 # Verbose output
  dnsly example.com -q                 # Quiet mode (no banner)

Supported Record Types:
  A, AAAA, CNAME, MX, NS, TXT, SOA, PTR
        """
    )
    
    parser.add_argument(
        "domain",
        help="Domain name to query"
    )
    
    parser.add_argument(
        "-t", "--type",
        dest="record_type",
        default="A",
        help="DNS record type(s) to query (comma-separated or ALL) [default: A]"
    )
    
    parser.add_argument(
        "-o", "--output",
        choices=["text", "json"],
        default="text",
        help="Output format [default: text]"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Quiet mode (no banner)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"dnsly v{__version__}"
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner(args.quiet or args.output == "json")
    
    # Parse record types
    if args.record_type.upper() == "ALL":
        record_types = ["A", "AAAA", "CNAME", "MX", "NS", "TXT", "SOA"]
    else:
        record_types = [rt.strip().upper() for rt in args.record_type.split(",")]
    
    # Validate record types
    valid_types = ["A", "AAAA", "CNAME", "MX", "NS", "TXT", "SOA", "PTR"]
    for rt in record_types:
        if rt not in valid_types:
            console.print(f"[red]✗[/red] Invalid record type: {rt}")
            console.print(f"[yellow]Valid types:[/yellow] {', '.join(valid_types)}")
            return 1
    
    # Perform lookup
    try:
        exit_code = perform_lookup(
            args.domain,
            record_types,
            args.output,
            args.verbose,
            args.quiet
        )
        return exit_code
    
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠[/yellow] Operation cancelled by user")
        return 1
    
    except Exception as e:
        console.print(f"[red]✗[/red] Unexpected error: {str(e)}")
        if args.verbose:
            import traceback
            console.print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main())



