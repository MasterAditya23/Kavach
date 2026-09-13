from urllib.parse import urlparse


def analyze_url(url):
    findings = []

    parsed = urlparse(url)

    if parsed.scheme not in ["http", "https"]:
        findings.append("Unusual or unsupported URL scheme")

    if parsed.scheme == "http":
        findings.append("URL does not use HTTPS")

    if parsed.hostname:
        hostname = parsed.hostname.lower()

        if hostname.replace(".", "").isdigit():
            findings.append("URL uses an IP address instead of a domain name")

        if "@" in url:
            findings.append("URL contains an @ symbol")

        if hostname.startswith("xn--") or ".xn--" in hostname:
            findings.append("Domain may use punycode")

        if len(hostname.split(".")) > 4:
            findings.append("URL contains many subdomains")

    if not findings:
        findings.append("No obvious suspicious URL indicators detected")

    return {
        "url": url,
        "findings": findings
    }