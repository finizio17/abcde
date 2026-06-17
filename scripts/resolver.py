import requests

def update_m3u():
    config_file = "config.txt"
    m3u_file = "iptvmia.m3u"
    
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
                # Trovato! Ora saltiamo le righe "vecchie" (il relinker o il link scaduto)
                # finché non arriviamo a una riga che non è un link http
                while i < len(lines) and (lines[i].strip().startswith("http") or lines[i].strip().startswith("#")):
                    i += 1
                
                # Inseriamo il nuovo link risolto
                r = requests.get(relinker, allow_redirects=True)
                new_lines.append(r.url + "\n")
                i -= 1 # Torniamo indietro di uno per non perdere la riga successiva
                break
        i += 1
                
    with open(m3u_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    update_m3u()
