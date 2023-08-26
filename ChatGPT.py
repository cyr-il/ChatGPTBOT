import openai
import os
import dotenv
import discord


config = dotenv.dotenv_values(".env")
openai.api_key = config['OPENAI_API_KEY']
TOKEN_DISCORD = config['TOKEN_DISCORD']

last_messages = []
max_chat_history = 20
role_message = {"role": "system", "content": "Tu es un développeur informatique très doué"}

intents = discord.Intents.default()

client = discord.Client(intents=intents)

async def get_reply_for_question(question):
    
    last_messages.append({"role": "user", "content": question})
    response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",  # Le nom du moteur, ici le modèle GPT-3.5
            messages = [role_message] + last_messages,  # Les messages de la conversation
        ).choices[0].message
    
    last_messages.append(response)
    
    while len(last_messages) > max_chat_history:
        last_messages.pop(0)
        
    with open("result.txt", "a") as file:
        file.write(response.content+ "\n")
        
    return response.content


@client.event
async def on_ready():
    print(f'Connecté en tant que {client.user.name} ({client.user.id})')
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return 

    if len(message.content) > 0:
        await message.channel.typing()
        response = await get_reply_for_question(message.content)
        await message.channel.send(response)
               
# Connexion au serveur Discord
client.run(TOKEN_DISCORD)
