import snscrape.modules.twitter as sntwitter
import requests
import time

# Configuración
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1363050567579992256/O98OA_tjgCEt2zft-w0ElALkhI2qKcVw23H7CBgZpk2EH9mdPdAFIj2-LVYUJbzkSBNh"
PALABRA_CLAVE = "lol"
INTERVALO_SEGUNDOS = 10

ultimo_id = None

def enviar_a_discord(mensaje):
    payload = {
        "content": mensaje,
        "allowed_mentions": {"parse": ["everyone"]},
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code != 204:
        print("Error al enviar a Discord:", response.text)

def buscar_tweets():
    global ultimo_id
    try:
        nuevos = []
        for tweet in sntwitter.TwitterSearchScraper(f'{PALABRA_CLAVE} since:2023-01-01').get_items():
            tweet_id = int(tweet.id)
            if ultimo_id is None or tweet_id > ultimo_id:
                nuevos.append(tweet)
            else:
                break  # ya vimos todos los nuevos, no seguir

        nuevos.sort(key=lambda t: int(t.id))

        for tweet in nuevos:
            mensaje = f"@everyone ENTRADAS PARA OASIS YA YA YA:\n{tweet.content}\nhttps://twitter.com/i/web/status/{tweet.id}"
            print(mensaje)
            enviar_a_discord(mensaje)
            ultimo_id = int(tweet.id)

    except Exception as e:
        print("Error buscando tweets:", e)

if __name__ == "__main__":
    print(f"Bot activo con snscrape. Buscando '{PALABRA_CLAVE}' cada {INTERVALO_SEGUNDOS} segundos.")
    while True:
        buscar_tweets()
        time.sleep(INTERVALO_SEGUNDOS)
