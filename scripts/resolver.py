import requests
import os

def update_m3u_selective():
    json_url = "https://raw.githubusercontent.com/ZapprTV/channels/refs/heads/main/it/dtt/national.json"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    m3u_file = os.path.join(script_dir, "..", "iptvmia.m3u")
    
    # 1. Scarichiamo il JSON
    try:
        response = requests.get(json_url)
        json_data = response.json()
        json_channels = {item["name"]: item for item in json_data}
    except Exception as e:
        print(f"Errore download JSON: {e}")
        return

    # Lista dei nomi da escludere (Rai e Mediaset)
    esclusioni = ["Rai", "Mediaset", "Canale 5", "Italia 1", "Rete 4"]
    
    # 2. Leggiamo il file M3U
    with open(m3u_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Verifichiamo se è un canale da aggiornare (presente nel JSON e NON è Rai/Mediaset)
        da_aggiornare = False
        target_info = None
        
        for name, info in json_channels.items():
            if name in line and not any(escl in name for escl in esclusioni):
                da_aggiornare = True
                target_info = info
                break
        
        if da_aggiornare:
            # Scriviamo i nuovi dati dal JSON
            new_lines.append(f'#EXTINF:-1 tvg-id="{target_info.get("tvg_id", "")}" tvg-name="{target_info.get("name", "")}" tvg-logo="{target_info.get("logo", "")}", {target_info.get("name", "")}\n')
            new_lines.append("#EXTVLCOPT:http-user-agent=HbbTV/1.6.1\n")
            new_lines.append(target_info.get("url", "") + "\n")
            
            # Saltiamo le vecchie righe del canale originale
            i += 1
            while i < len(lines) and not lines[i].startswith("#EXTINF"):
                i += 1
            i -= 1 # Torniamo indietro per riprendere il ciclo correttamente
        else:
            new_lines.append(line)
        i += 1

    # 3. Scriviamo il file finale
    with open(m3u_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    update_m3u_selective()
