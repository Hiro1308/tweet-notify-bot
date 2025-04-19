import tweepy
import requests

# ==== TU TOKEN DE ACCESO (Bearer Token de Twitter API v2) ====
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAG7d0gEAAAAACSOGtZ5s4cys03UJUEX2uApQXwM%3Dk7o3MExSFTnAsW41CYJj9YyXpiPS5pktH1Yg5LhU9206FDZ6ma"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1363050567579992256/O98OA_tjgCEt2zft-w0ElALkhI2qKcVw23H7CBgZpk2EH9mdPdAFIj2-LVYUJbzkSBNh"

# ==== Palabra clave a buscar ====
PALABRA_CLAVE = "SUNSHIIIIIIIAAAAAAIIIIIN"

# === Función para enviar mensaje a Discord ===
def enviar_a_discord(mensaje):
    payload = {
        "content": mensaje,
        "allowed_mentions": {"parse": ["everyone"]},
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code != 204:
        print("Error al enviar a Discord:", response.text)

# === Stream de Twitter ===
class MyStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        if tweet.text.lower().startswith("rt"):
            return
        mensaje = f"📣 @everyone ENTRADAS PARA OASIS YA YA YA!:\n{tweet.text}\nhttps://twitter.com/i/web/status/{tweet.id}"
        print(mensaje)
        enviar_a_discord(mensaje)

# ==== Configurar el stream ====
def main():
    stream = MyStream(bearer_token=BEARER_TOKEN)

    # Limpiar reglas anteriores
    reglas = stream.get_rules().data
    if reglas:
        ids = [r.id for r in reglas]
        stream.delete_rules(ids)

    # Agregar nueva regla
    stream.add_rules(tweepy.StreamRule(PALABRA_CLAVE))

    print("✅ Bot escuchando tweets con:", PALABRA_CLAVE)
    stream.filter(tweet_fields=["text"])

if __name__ == "__main__":
    main()
