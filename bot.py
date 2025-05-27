import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
    async def on_voice_state_update(self, member, before, after):
        if not before.channel == None:
            c = f'Goodbye {member.display_name}'
            await before.channel.send(content=c, tts=True)
        if not after.channel == None:
            c = f'I SEE YOU {member.display_name}'
            await after.channel.send(content=c, tts=True)



app_intents = discord.Intents.default()
app_intents.message_content = True 
app_intents.voice_states = True 
client = MyClient(intents = app_intents)
#client = MyClient()

f = open("super-secret-pw", "r")
client.run(f.read())
f.close()
