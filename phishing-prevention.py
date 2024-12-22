# Prevent access to known phishing sites
def detect_phishing_link(url):
    phishing_domains = ["127.0.0.1:5555"]
    for domain in phishing_domains:
        if domain in url:
            return True
    return False

url = "127.0.0.1:5555"

if detect_phishing_link(url):
    print("Phishing link detected! Block access.")
else:
    print("URL is safe.")
