import requests

def update_m3u():
    url_relinker = "https://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=2606803&output=16"
    file_path = "iptvmia.m3u" # Il nome del tuo file esistente
    
    # 1. Risolviamo il nuovo link
    r = requests.get(url_relinker, allow_redirects=True)
    new_stream_url = r.url
    
    # 2. Leggiamo il tuo file originale
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    # 3. Aggiorniamo la riga dopo quella che contiene "Rai 1"
    new_lines = []
    found_rai1 = False
    for line in lines:
        if found_rai1:
            new_lines.append(new_stream_url + "\n")
            found_rai1 = False # Abbiamo aggiornato, ora continuiamo a copiare il resto
        else:
            new_lines.append(line)
            if "Rai 1" in line:
                found_rai1 = True
                
    # 4. Sovrascriviamo il file
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    update_m3u()
