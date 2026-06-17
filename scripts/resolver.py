import requests
import os

def update_m3u():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "..", "config.txt")
    m3u_file = os.path.join(script_dir, "..", "iptvmia.m3u")
    
    headers = {
        "User-Agent": "HbbTV/1.6.1 (+PVR; LG; TV; 2026; SmartTV)"
    }
    
    # Leggiamo la configurazione pulendo ogni possibile spazio extra
    with open(config_file, "r") as f:
        configs = []
        for line in f:
            if '|' in line:
                parts = line.strip().split('|')
                # .strip() rimuove spazi prima e dopo il nome del canale
                configs.append((parts[0].strip(), parts[1].strip()))
    
    with open(m3u_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        for name, relinker in configs:
            # Confronto flessibile: cerchiamo il nome del canale nella riga
            if name in line:
                i += 1
                while i < len(lines) and (lines[i].strip().startswith("http") or lines[i].strip().startswith("#")):
                    if lines[i].strip().startswith("#EXTINF"):
                        break
                    i += 1
                
                try:
                    session = requests.Session()
                    response = session.get(relinker, headers=headers, allow_redirects=True)
                    
                    if "playlist.m3u8" in response.text:
                        # Estrazione robusta
                        for link in response.text.split('"'):
                            if "m3u8" in link and "http" in link:
                                new_lines.append(link + "\n")
                                break
                    else:
                        new_lines.append(response.url + "\n")
                        
                except Exception as e:
                    print(f"Errore nella risoluzione di {name}: {e}")
                    
                i -= 1
                break
        i += 1
                
    with open(m3u_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    update_m3u()
