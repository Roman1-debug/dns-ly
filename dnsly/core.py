"""
Core DNS lookup functionality for dnsly.
"""

import dns.resolver
import dns.reversename
from typing import Dict, Any


def validate_domain(domain: str) -> bool:
    """
    Validate if a string is a valid domain name.
    
    Args:
        domain: String to validate
    
    Returns:
        True if valid domain, False otherwise
    """
    import re
    
    if not domain or len(domain) > 253:
        return False
    
    # Regular expression for domain validation
    domain_regex = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    )
    
    return bool(domain_regex.match(domain))


def dns_lookup(domain: str, record_type: str = "A") -> Dict[str, Any]:
    """
    Perform DNS lookup for a domain.
    
    Args:
        domain: Domain name to lookup
        record_type: DNS record type (A, AAAA, MX, TXT, CNAME, NS, SOA, PTR)
    
    Returns:
        Dictionary with DNS lookup results
    """
    # Validate domain
    if not validate_domain(domain):
        return {
            "success": False,
            "error": "Invalid domain format",
            "domain": domain,
            "record_type": record_type
        }
    
    # For PTR records, we need an IP address
    if record_type.upper() == "PTR":
        try:
            # Convert IP to in-addr.arpa format
            reversed_name = dns.reversename.from_address(domain)
            domain = str(reversed_name)
        except Exception:
            return {
                "success": False,
                "error": "Invalid IP address for PTR lookup",
                "domain": domain,
                "record_type": record_type
            }
    
    try:
        # Create resolver
        resolver = dns.resolver.Resolver()
        
        # Perform query
        answers = resolver.resolve(domain, record_type)
        
        # Process results based on record type
        results = []
        for rdata in answers:
            if record_type.upper() == "MX":
                results.append({
                    "preference": rdata.preference,
                    "exchange": str(rdata.exchange)
                })
            elif record_type.upper() == "TXT":
                results.append(str(rdata).strip('"'))
            elif record_type.upper() == "SOA":
                results.append({
                    "mname": str(rdata.mname),
                    "rname": str(rdata.rname),
                    "serial": rdata.serial,
                    "refresh": rdata.refresh,
                    "retry": rdata.retry,
                    "expire": rdata.expire,
                    "minimum": rdata.minimum
                })
            else:
                results.append(str(rdata))
        
        return {
            "success": True,
            "domain": domain,
            "record_type": record_type,
            "records": results,
            "count": len(results)
        }
    
    except dns.resolver.NXDOMAIN:
        return {
            "success": False,
            "error": "Domain does not exist",
            "domain": domain,
            "record_type": record_type
        }
    except dns.resolver.NoAnswer:
        return {
            "success": False,
            "error": f"No {record_type} records found",
            "domain": domain,
            "record_type": record_type
        }
    except dns.resolver.Timeout:
        return {
            "success": False,
            "error": "DNS query timed out",
            "domain": domain,
            "record_type": record_type
        }
    except dns.exception.DNSException as e:
        return {
            "success": False,
            "error": f"DNS error: {str(e)}",
            "domain": domain,
            "record_type": record_type
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "domain": domain,
            "record_type": record_type
        }


