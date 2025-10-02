import discord
import datetime

import logging

MAX_LENGTH = 5
names = []
name_dic = {}

THRESHOLD_DURATION = datetime.timedelta(minutes=1)

def less_than_threshold_duration(name):
    clean_up_dictionary()
    if not name in name_dic:
        return False
    return datetime.datetime.now() - name_dic[name] < THRESHOLD_DURATION
    
def clean_up_dictionary():
    #print(name_dic)
    mark_for_removal = []
    for k, v in name_dic.items():
        if datetime.datetime.now() - v > THRESHOLD_DURATION:
            mark_for_removal.append(k)
    for item in mark_for_removal:
        name_dic.pop(item)

    

class MyBot(discord.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    #async def on_message(self, message):
    #    print(f'Message from {message.author}: {message.content}')

    async def on_voice_state_update(self, member, before, after):
        if before.channel == after.channel:
            return
        # Joining channel
        if not after.channel == None:
            name_dic[member.display_name] = datetime.datetime.now()
            return
        if not before.channel == None:
            if less_than_threshold_duration(member.display_name):
                c = f'Goodbye {member.display_name}'
                await before.channel.send(content=c, tts=True)

            names.append(f'{member.display_name} from {before.channel} at {datetime.datetime.now()}')
            if len(names) > MAX_LENGTH:
                names.pop(0)


required_intents = discord.Intents.default()
required_intents.message_content = True

bot = MyBot(intents = required_intents)

@bot.slash_command(description="Drops some names.") # this decorator makes a slash command
async def who(ctx): # a slash command will be created with the name "ping"
    name_list = ""
    if len(names) == 0:
        await ctx.respond("No one (yet)")
        return
    for name in names:
        name_list = name_list + name + "\n"
    await ctx.respond(name_list)

f = open("super-secret-pw", "r")
token = f.read()
f.close()

logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.ERROR) 
try:
    bot.run(token)
except Exception as err:
    logger.error(f"Unexpected {err=}, {type(err)=}")
