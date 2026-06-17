import requests
import os

def update_m3u():
    # Definiamo i percorsi in modo assoluto per evitare errori di directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "..", "config.txt")
    m3u_file = os.path.join(script_dir, "..", "iptvmia.m3u")
    
    # Leggiamo i link sorgente dal file di config
    with open(config_file, "r") as f:
        configs = [line.strip().split('|') for line in f if '|' in line]
    
    # Leggiamo la lista m3u
    with open(m3u_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # Se troviamo un canale configurato
        for name, relinker in configs:
            if name in line:
                i += 1
                # Saltiamo le righe "vecchie" (il relinker o il link scaduto)
                while i < len(lines) and (lines[i].strip().startswith("http") or lines[i].strip().startswith("#")):
                    # Se incontriamo un altro tag #EXT, ci fermiamo
                    if lines[i].strip().startswith("#EXTINF"):
                        break
                    i += 1
                
                # Inseriamo il nuovo link risolto
                try:
                    r = requests.get(relinker, allow_redirects=True)
                    new_lines.append(r.url + "\n")
                except Exception as e:
                    print(f"Errore nella risoluzione di {name}: {e}")
                    
                i -= 1 # Torniamo indietro di uno per non perdere la riga corrente
                break
        i += 1
                
    with open(m3u_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    update_m3u()
