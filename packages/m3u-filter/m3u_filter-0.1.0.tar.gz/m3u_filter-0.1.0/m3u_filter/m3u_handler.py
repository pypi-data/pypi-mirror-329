import requests
import re

def download_m3u_xtream(base_url, username, password):
    """Download M3U content from Xtream provider."""
    url = f"{base_url}/get.php?username={username}&password={password}&type=m3u&output=mpegts"
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_attribute_line(line):
    """Parse a single EXTINF line for attributes."""
    attrs = dict(re.findall(r'([\w-]+)="(.*?)"', line))
    channel_name = line.split(",", 1)[1].strip() if "," in line else ""
    return attrs, channel_name

def parse_m3u(content, progress_callback=None):
    """Parse M3U content and return a list of channel entries."""
    lines = content.splitlines()
    total = len(lines)
    entries = []
    i = 0
    
    while i < total:
        line = lines[i].strip()
        if line.startswith("#EXTINF:"):
            attrs, channel_name = parse_attribute_line(line)
            url = lines[i+1].strip() if i+1 < len(lines) else ""
            
            entries.append({
                "name": attrs.get("tvg-name", channel_name),
                "logo": attrs.get("tvg-logo", ""),
                "group": attrs.get("group-title", ""),
                "url": url
            })
            i += 2
        else:
            i += 1
        
        if progress_callback:
            percent = int((i / total) * 100)
            progress_callback(percent)
            
    if progress_callback:
        progress_callback(100)
            
    return entries

def create_m3u_content(entries):
    """Create M3U file content from a list of channel entries."""
    lines = ['#EXTM3U']
    for entry in entries:
        attrs = []
        if entry.get("logo"):
            attrs.append(f'tvg-logo="{entry["logo"]}"')
        if entry.get("group"):
            attrs.append(f'group-title="{entry["group"]}"')
        if entry.get("name"):
            attrs.append(f'tvg-name="{entry["name"]}"')
            
        attrs_str = " ".join(attrs)
        lines.append(f'#EXTINF:-1 {attrs_str},{entry["name"]}')
        lines.append(entry["url"])
    
    return "\n".join(lines)
