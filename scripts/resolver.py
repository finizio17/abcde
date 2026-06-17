import requests
import os

def update_m3u_with_json():
    json_url = "https://raw.githubusercontent.com/ZapprTV/channels/refs/heads/main/it/dtt/national.json"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    m3u_file = os.path.join(script_dir, "..", "iptvmia.m3u")
    
    # 1. Scarichiamo il JSON
    try:
        response = requests.get(json_url)
        data = response.json()
        # Creiamo un dizionario per ricerca rapida: {nome_canale: dati_canale}
        json_channels = {item["name"]: item for item in data}
    except Exception as e:
        print(f"Errore download JSON: {e}")
        return

    # 2. Leggiamo il file M3U esistente
    with open(m3u_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    processed_json_channels = set()
    i = 0
    
    # 3. Processiamo riga per riga
    while i < len(lines):
        line = lines[i]
        
        # Se troviamo un canale che esiste nel JSON, lo aggiorniamo
        found = False
        for name, info in json_channels.items():
            if f'tvg-name="{name}"' in line or f', {name}' in line:
                # Scriviamo i nuovi dati
                new_lines.append(f'#EXTINF:-1 tvg-id="{info.get("tvg_id", "")}" tvg-name="{name}" tvg-logo="{info.get("logo", "")}", {name}\n')
                new_lines.append("#EXTVLCOPT:http-user-agent=HbbTV/1.6.1\n")
                new_lines.append(info.get("url", "") + "\n")
                
                # Saltiamo le vecchie righe del canale nel file originale
                i += 1
                while i < len(lines) and not lines[i].startswith("#EXTINF"):
                    i += 1
                i -= 1 # Indietreggiamo per riprendere il ciclo
                
                processed_json_channels.add(name)
                found = True
                break
        
        if not found:
            new_lines.append(line)
        i += 1

    # 4. Aggiungiamo eventuali canali del JSON che non c'erano nel file originale
    for name, info in json_channels.items():
        if name not in processed_json_channels:
            new_lines.append(f'\n#EXTINF:-1 tvg-id="{info.get("tvg_id", "")}" tvg-name="{name}" tvg-logo="{info.get("logo", "")}", {name}\n')
            new_lines.append("#EXTVLCOPT:http-user-agent=HbbTV/1.6.1\n")
            new_lines.append(info.get("url", "") + "\n")

    # 5. Scriviamo il file finale
    with open(m3u_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    update_m3u_with_json()
