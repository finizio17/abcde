import requests
import os

def update_m3u():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "..", "config.txt")
    m3u_file = os.path.join(script_dir, "..", "iptvmia.m3u")
    
    # Questo User-Agent fa credere al server Rai di essere una TV LG in Italia
    headers = {
        "User-Agent": "Mozilla/5.0 (WebOS; SmartTV; U; it) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36",
        "Referer": "https://www.raiplay.it/",
        "Origin": "https://www.raiplay.it"
    }
    
    with open(config_file, "r") as f:
        configs = [(line.strip().split('|')[0].strip(), line.strip().split('|')[1].strip()) for line in f if '|' in line]
    
    with open(m3u_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        for name, relinker in configs:
            if name in line:
                i += 1
                while i < len(lines) and (lines[i].strip().startswith("http") or lines[i].strip().startswith("#")):
                    if lines[i].strip().startswith("#EXTINF"):
                        break
                    i += 1
                
                try:
                    # Usiamo una sessione per mantenere i cookie
                    session = requests.Session()
                    # Primo step: otteniamo il token di sessione
                    session.get("https://www.raiplay.it/", headers=headers)
                    # Secondo step: chiamiamo il relinker con gli stessi header
                    response = session.get(relinker, headers=headers, allow_redirects=True)
                    
                    if "m3u8" in response.text:
                        for link in response.text.split('"'):
                            if "m3u8" in link and "http" in link:
                                new_lines.append(link + "\n")
                                break
                    else:
                        new_lines.append(response.url + "\n")
                        
                except Exception as e:
                    print(f"Errore: {e}")
                    
                i -= 1
                break
        i += 1
                
    with open(m3u_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    update_m3u()
