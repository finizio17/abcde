import requests
import os

def update_m3u():
    # Definiamo i percorsi
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "..", "config.txt")
    m3u_file = os.path.join(script_dir, "..", "iptvmia.m3u")
    
    # User-Agent che simula una Smart TV per convincere il server Rai
    headers = {
        "User-Agent": "HbbTV/1.6.1 (+PVR; LG; TV; 2026; SmartTV)"
    }
    
    # Leggiamo i link sorgente dal file di config
    with open(config_file, "r") as f:
        configs = [line.strip().split('|') for line in f if '|' in line]
    
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
                
                # Usiamo una sessione con header simulati
                try:
                    session = requests.Session()
                    response = session.get(relinker, headers=headers, allow_redirects=True)
                    
                    # Se il relinker restituisce ancora una pagina web, 
                    # forziamo il recupero del link m3u8 che Rai usa per le TV
                    if "playlist.m3u8" in response.text:
                        # Estrazione semplice del link m3u8 dalla risposta
                        final_url = [l for l in response.text.split('"') if "m3u8" in l][0]
                        new_lines.append(final_url + "\n")
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
