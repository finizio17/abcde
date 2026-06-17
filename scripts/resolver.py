import requests

def update_m3u():
    # URL di test per Rai 1
    url_relinker = "https://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=2606803&output=16"
    file_path = "iptvmia.m3u"
    
    # Risolviamo il nuovo URL
    r = requests.get(url_relinker, allow_redirects=True)
    new_url = r.url
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    new_lines = []
    skip_next = False
    
    for i in range(len(lines)):
        line = lines[i]
        
        # Se dobbiamo saltare la riga precedente (il vecchio link), lo facciamo
        if skip_next:
            new_lines.append(new_url + "\n")
            skip_next = False
            continue
            
        new_lines.append(line)
        
        # Cerchiamo la riga che identifica Rai 1
        if "Rai 1" in line:
            skip_next = True
            
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    update_m3u()
