from discord.ext import commands
Bot= commands.Bot(command_prefix="-")

@Bot.event
async def on_ready():
  channel = Bot.get_channel(630135300131127324) 
  await channel.send("Conection.")

@Bot.command()
async def hola(ctx):
  await ctx.reply("Hola mundo!")

Bot.run("ODg3ODQxNjUzMDc3OTk1NTYx.YUKA-Q.Icdd2tLOqkHaL2V45ztBNH44rJc")
#Invitación: https://discord.com/api/oauth2/authorize?client_id=887841653077995561&scope=bot&permissions=8