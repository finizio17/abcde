import requests

# Il link del tuo Relinker
url_relinker = "https://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=2606803&output=16"

def risolvi_link():
    try:
        # Chiediamo al server Rai dove punta il link
        r = requests.get(url_relinker, allow_redirects=True)
        # Il link reale dello stream solitamente è nell'URL finale dopo i redirect
        stream_url = r.url
        
        # Scriviamo il file M3U
        with open("lista_finale.m3u", "w") as f:
            f.write("#EXTM3U\n")
            f.write("#EXTINF:-1, Rai 1\n")
            f.write(stream_url + "\n")
            
        print("Successo! Lista aggiornata.")
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    risolvi_link()
