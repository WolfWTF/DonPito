#IMPORTS
from ffprobe import FFProbe
import os
import random
import discord
from datetime import datetime
import pydub
import asyncio

#Custom imports
import actjson as aj
from tdform import timedeltaformatter as tdf
import wave_gen as wg

from discord_components import ComponentsBot, Button#, Select, SelectOption #DiscordComponents,  

Bot = ComponentsBot(command_prefix="!",intents=discord.Intents.all())
start = datetime.now()
channel_whitelist =[320694020328390666,840366998315991061]

@Bot.check_once
def whitelist(ctx):
    return ctx.message.channel.id in channel_whitelist

hora_antigua = datetime.now()

@Bot.event
async def on_ready():
  print('Sesión iniciada como {0.user}'.format(Bot))
  channel = Bot.get_channel(840366998315991061) #Parche
  await channel.send("¡Don Pito reconectado!")
  Bot.loop.create_task(hora())


async def hora():
  canal = Bot.get_channel(840366998315991061)
  while True:
      quehora = quehoraes()
      global hora_antigua
      han_pasado = quehora - hora_antigua
      tiempo = tdf(han_pasado)
      hora_antigua = quehora
      respuesta = str(round(tiempo[2])) + " minutos"
      await canal.send(respuesta)
      await asyncio.sleep(180)
      await hora()

def quehoraes():
  hora = datetime.now()
  return hora

def get_comandos():
    comandos = aj.abrir_json('comandos.json')

    str_entrenamiento = comandos["entrenamiento"]
    str_entrenamiento = str_entrenamiento.replace(",","`\n`!")
    str_entrenamiento = "`!" + str_entrenamiento + "`"

    string_completa = str_entrenamiento

    return string_completa
'''
@Bot.command()
async def r(ctx):
  info = aj.abrir_json("piano/info.json")
  keys = info['keys']
  print(len(keys))
  for s in keys:
    f_name = "piano/" + s + ".mp3"
    sound = pydub.AudioSegment.from_mp3(f_name)
    faded = sound.fade_out(25)
    f_name2 = "piano2/" + s + ".mp3"
    faded.export(f_name2, format="mp3")
'''
@Bot.command()
async def uptime(ctx):
  global start
  now = datetime.now()
  elapsed = now - start
  [dias, horas, minutos, segundos] = tdf(elapsed)
  respuesta = "Llevo conectado "
  if dias != 0:
    respuesta += str(dias) + " días, " 
  if horas!= 0:
    respuesta += str(horas) + " horas, " 
  if minutos != 0:
    respuesta += str(minutos) + " minutos, " 
  if segundos != 0:
    seg = segundos - dias*24*3600 - horas*3600 - minutos*60
    respuesta += str(round(seg)) + " segundos."
  await ctx.reply(respuesta)
  
  
@Bot.command()
async def id_canal(ctx):
  respuesta = ctx.channel.id
  await ctx.reply(respuesta)

intervalos = [
              "Unísono",
              "2ª menor",
              "2ª Mayor",
              "3ª menor",
              "3ª Mayor",
              "4ª",
              "Tritono",
              "5ª",
              "6ª menor",
              "6ª mayor",
              "7ª menor",
              "7ª Mayor",
              "Octava"]
Botones_Intervalos = [
              Button(label = intervalos[0],style = 1),
              Button(label = intervalos[1],style = 1),
              Button(label = intervalos[2],style = 1),
              Button(label = intervalos[3],style = 1),
              Button(label = intervalos[4],style = 1),
              Button(label = intervalos[5],style = 1),
              Button(label = intervalos[6],style = 1),
              Button(label = intervalos[7],style = 1),
              Button(label = intervalos[8],style = 1),
              Button(label = intervalos[9],style = 1),
              Button(label = intervalos[10],style = 1),
              Button(label = intervalos[11],style = 1),
              Button(label = intervalos[12],style = 1)]
ActionRow1 = Botones_Intervalos[0:4]
ActionRow2 = Botones_Intervalos[4:9]
ActionRow3 = Botones_Intervalos[9:]



def corregir(ctx,selec_usuario,respuesta_correcta,elapsed):
  correcto = selec_usuario == respuesta_correcta
  usuario = ctx.author.name
  tiempo = tdf(elapsed)
  segundos_totales = round(tiempo[0]*3600*24 + tiempo[1]*3600 + tiempo[2]*60 + tiempo[3], 2)

  if correcto:
    respuesta = ":white_check_mark:  **" + selec_usuario + "**  :white_check_mark:  ¡Muy bien, " + usuario +"!" + " Tiempo: " + str(segundos_totales) + " s."
  else:
    respuesta =":x:  **" + selec_usuario +"**  :x:  Respuesta correcta: **" + respuesta_correcta +"**."
  return respuesta, correcto

piano = False

def esunnumero(mensaje):
  loes=True
  for caracter in mensaje:
    if not caracter.isdigit():
      loes = False
  return loes

@Bot.command()
async def pito(ctx):
  sonido = []
  await ctx.send("Preparando pito... :smirk:",delete_after = 7)
  exponente = random.uniform(1.7,3.6989)#3.69897
  f = round(10**exponente)
  lim = 1.2
  tolerancia = [round(f/lim), round(f*lim)]
  audio = wg.append_sinewave(freq = f,duration_milliseconds = 1000,volume = 0.3, audio = sonido)
  wg.save_wav('tono_puro.wav', audio)
  start=datetime.now()
  informacion = "Adivina el número de Hz del tono puro. Rango: 50 - 5000 Hz."  
  audio = await ctx.send(informacion, file=discord.File(r'tono_puro.wav'))
  def check(frecuencia_msg):
      return frecuencia_msg.author == ctx.author and frecuencia_msg.channel == ctx.channel and esunnumero(frecuencia_msg.content)
  frecuencia_msg = await Bot.wait_for("message", check = check)
  end=datetime.now()
  elapsed = end-start
  frecuencia = int(frecuencia_msg.content)
  if frecuencia <= tolerancia[0] or frecuencia >= tolerancia[1]: 
    respuesta1 = ":x: *No pasas la prueba. Tu respuesta: " + str(frecuencia) + " Hz.*" 
    color = 0xff0000
  else:
    respuesta1 = ":white_check_mark: *¡Prueba superada! Tu respuesta: " + str(frecuencia) + " Hz.*" 
    color = 0x00c907
  tiempo = tdf(elapsed)
  segundos_totales = round(tiempo[0]*3600*24 + tiempo[1]*3600 + tiempo[2]*60 + tiempo[3], 2)
  contenido = ":thought_balloon: Respuesta de "+ ctx.author.name + ": "
  contenido += ":loud_sound: Respuesta correcta: " + str(f) +  " Hz.\n"
  contenido += ":straight_ruler: Intervalo tolerancia: " + str(tolerancia) + " Hz.\n"
  contenido += ":bar_chart: Te has equivocado en " + str(abs(frecuencia - f)) +" Hz."
  footer = "Tiempo empleado por "+ ctx.author.name+ ": " + str(segundos_totales) +  " s."
    
  os.remove('tono_puro.wav')
  mensaje = discord.Embed(title = respuesta1, description = contenido, colour = color)
  mensaje.set_footer(text = footer,icon_url = "https://images.emojiterra.com/google/android-pie/512px/23f1.png")
  await ctx.send(embed = mensaje, reference = audio)

@Bot.command()
async def piano(ctx):
  global piano
  piano = True
  await ctx.send("Sonido: Piano.")
@Bot.command()
async def tono(ctx):
  global piano
  piano = False
  await ctx.send("Sonido: Tonos puros.")


entrenador_ocupado = False
def get_audio(modo,semitones):
      global piano
      if piano:
        lim_asc =[0,75]
        lim_des =[11,87]
      else:
        lim_asc =[1,37]
        lim_des =[12,49]
      #start=datetime.now()

      if(modo == 'ascendente' or modo == 'simultaneo'):
        n1 = random.randint(lim_asc[0],lim_asc[1])
        n2 = n1 + semitones
        
      elif(modo =='descendente'):
        n1 = random.randint(lim_des[0],lim_des[1])
        n2 = n1 - semitones

      #if(modo == 'ascendente' or modo == 'descendente'):
      if piano:
        info = aj.abrir_json("piano/info.json")
        notas = info['keys']
        nota1_nombre = "piano/" + notas[n1] +".mp3"
        nota2_nombre = "piano/" + notas[n2] +".mp3"
      else:
        nota1_nombre = "mp3s/" +str(n1) +".mp3"
        nota2_nombre = "mp3s/" +str(n2) +".mp3"

      fnota1 = open(nota1_nombre,'rb')
      nota1 = pydub.AudioSegment.from_file(nota1_nombre)
      fnota1.close()

      fnota2 = open(nota2_nombre,'rb')
      nota2 = pydub.AudioSegment.from_file(nota2_nombre)
      fnota2.close()

      if modo == 'simultaneo':
        nota1 = nota1.apply_gain(-13)
        juntas = nota2.overlay(nota1, gain_during_overlay = -13)
      else:
        juntas = nota1.append(nota2, crossfade = 25)

      juntas.export("test.mp3", format="mp3")
      
media = 0
n = 0
aciertos = 0
fallos = 0
@Bot.command()
async def continuo(ctx,modo = 'aleatorio'):

  modos = ['ascendente','descendente','simultaneo']
  if modo == 'aleatorio':
    modo_elegido = random.choice(modos)
  else:
    modo_elegido = modo
  continuar=True
  stop_button = Button(label="Stop",style=4)
  global ActionRow3
  ActionRow3.append(stop_button)
  continuar, elapsed, correcto = await entrenar(ctx,modo_elegido)
  ActionRow3 = Botones_Intervalos[9:]

  global media
  global n
  n += 1
  global aciertos
  global fallos
  ##Cambiar esta locura por un diccionario y añadir donde se falla

  if media == 0:
    media = elapsed
  else:
    media = (media*(n-1) + elapsed)/n


  if continuar:
    if correcto:
      aciertos += 1
    else: 
      fallos += 1
    await continuo(ctx,modo)
  else:
    m = round(tdf(media)[3],2)
    respuesta = discord.Embed(title = "*Resultados:*",color= 0x2a59a1)
    nombre = str(n-1) + " pruebas:"
    valor = ":white_check_mark: Aciertos: " + str(aciertos) + ". \n"
    valor += ":x: Fallos: " + str(fallos) + ". \n"
    valor += ":timer: Media: " + str(m) + " segundos."

    respuesta.add_field(name = nombre, value= valor)
     
    await ctx.reply(embed=respuesta)
    media = 0
    n = 1
    aciertos = 0 
    fallos = 0
    

@Bot.command()
async def entrenar(ctx,modo = 'ascendente'):
  if modo == 'aleatorio':
    modo = random.choice(['ascendente','descendente','simultaneo'])
  global entrenador_ocupado
  if(not entrenador_ocupado):
    entrenador_ocupado = True
    #PREPARAMOS EL AUDIO
    with ctx.channel.typing():
      await ctx.send("Preparando entrenamiento...",delete_after = 5)
      semitones = random.randint(0,12)
      get_audio(modo,semitones)
      #### SE ENVIA EL AUDIO
      audio = await ctx.send(file=discord.File(r'test.mp3'))

    #NI BIEN SE ENVIA, SE BORRA
    os.remove("test.mp3")
    global intervalos
    respuesta_correcta = intervalos[semitones]

    #MANDAMOS LOS BOTONES Y ESPERAMOS A QUE SE PULSEN
    start=datetime.now()
    Botones = await ctx.send("Opciones:", components = [ActionRow1,ActionRow2,ActionRow3])

    def check(interaction):
      return interaction.author == ctx.author

    interaction = await Bot.wait_for("button_click",check=check)
    end=datetime.now()
    elapsed = end-start
    await Botones.delete()
    selec_usuario = interaction.component.label

    #CORREGIMOS
    if selec_usuario != "Stop":
      respuesta, correcto = corregir(ctx,selec_usuario, respuesta_correcta,elapsed)
      await ctx.send(respuesta, reference = audio)
      entrenador_ocupado = False
      return True, elapsed, correcto
    else:
      respuesta = "Deteniendo..."
      await ctx.send(respuesta)
      return False, elapsed, False
  else:
    respuesta = "Estoy entrenando a otro usuario."
    await ctx.send(respuesta)


@Bot.command()
async def comandos(ctx):
  respuesta = discord.Embed(title="__**COMANDOS**__" , color= 0x2a59a1)
  comandos = get_comandos()
  respuesta.add_field(name="Entrenamiento:", value = comandos)
  await ctx.reply(embed=respuesta)
  
Bot.run('insertar token') #token
