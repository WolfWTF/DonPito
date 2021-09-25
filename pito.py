#IMPORTS
from ffprobe import FFProbe
import os
import random
import discord
from datetime import datetime
import pydub
import asyncio
from discord_components import ComponentsBot, Button#, Select, SelectOption #DiscordComponents,  

#Custom imports
import actjson as aj
from tdform import timedeltaformatter as tdf
import wave_gen as wg


####################################################################################################
################################# CONFIGURACIÓN E INICIALIZACIONES #################################
####################################################################################################


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

intervalos = ["Unísono", "2ª menor", "2ª Mayor","3ª menor", "3ª Mayor",
              "4ª", "Tritono", "5ª", "6ª menor", "6ª mayor","7ª menor",
              "7ª Mayor", "Octava", "9ª menor", "9ª Mayor"]
Botones_Intervalos = []
'''              Button(label = intervalos[0],style = 1),
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
              Button(label = intervalos[12],style = 1)]''' #SI NO HA DADO ERROR, QUITAR ESTO

for inter in intervalos:
  new_boton = Button(label = inter,style = 1)
  Botones_Intervalos.append(new_boton)

ActionRow1 = Botones_Intervalos[0:4]
ActionRow2 = Botones_Intervalos[4:9]
ActionRow3 = Botones_Intervalos[9:13]

####################################################################################################
################# FUNCIONES AUXILIARES QUE EN EL FUTURO METERÉ EN UN ARCHIVO APARTE ################
####################################################################################################

def get_comandos():
    comandos = aj.abrir_json('DonPito/comandos.json')
    str_entrenamiento = comandos["entrenamiento"]
    str_entrenamiento = str_entrenamiento.replace(",","`\n`!")
    str_entrenamiento = "`!" + str_entrenamiento + "`"
    string_completa = str_entrenamiento

    return string_completa

def inscribir(ctx):
  padawans = aj.abrir_json("DonPito/padawans.json")
  usr_id = str(ctx.author.id)
  usr_name = ctx.author.name
  padawans[usr_id] = {"name": usr_name, "exp": 0, "nivel_intervalos": 0}
  aj.actualizar_padawans(padawans)
  return padawans

def corregir(ctx,selec_usuario,respuesta_correcta,elapsed):
  correcto = selec_usuario == respuesta_correcta
  usuario = ctx.author
  tiempo = tdf(elapsed)
  segundos_totales = round(tiempo[0]*3600*24 + tiempo[1]*3600 + tiempo[2]*60 + tiempo[3], 2)

  if correcto:
    respuesta = ":white_check_mark:  **" + selec_usuario + "**  :white_check_mark:  ¡Muy bien, " + usuario.name +"!" + " Tiempo: " + str(segundos_totales) + " s.\n +1 punto de experiencia."
    dar_exp(ctx,1)
  else:
    respuesta =":x:  **" + selec_usuario +"**  :x:  Respuesta correcta: **" + respuesta_correcta +"**."
  return respuesta, correcto

piano = True

def esunnumero(mensaje):
  loes=True
  for caracter in mensaje:
    if not caracter.isdigit():
      loes = False
  return loes

def dar_exp(ctx,puntos):
  padawans = aj.abrir_json("DonPito/padawans.json")
  usr_id = str(ctx.author.id)
  exp = padawans[usr_id]['exp']
  exp += puntos
  padawans[usr_id]['exp'] = exp
  aj.actualizar_padawans(padawans)

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
        info = aj.abrir_json("DonPito/piano/info.json")
        notas = info['keys']
        nota1_nombre = "DonPito/piano/" + notas[n1] +".mp3"
        nota2_nombre = "DonPito/piano/" + notas[n2] +".mp3"
      else:
        nota1_nombre = "DonPito/mp3s/" +str(n1) +".mp3"
        nota2_nombre = "DonPito/mp3s/" +str(n2) +".mp3"

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

      juntas.export("DonPito/test.mp3", format="mp3")


##############################################################################################################################
####################################################### COMANDOS #############################################################
##############################################################################################################################

###################### COMANDOS #######################

@Bot.command()
async def comandos(ctx):
  respuesta = discord.Embed(title="__**COMANDOS**__" , color= 0x2a59a1)
  comandos = get_comandos()
  respuesta.add_field(name="Entrenamiento:", value = comandos)
  await ctx.reply(embed=respuesta)

####################### UPTIME ########################################################################

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

###################### NIVELES ########################################################################

@Bot.command()
async def niveles(ctx):
  niveles = aj.abrir_json("DonPito/niveles.json")
  i=1
  respuesta = u"**NIVELES:** \n"
  for nivel in niveles:
    nivel_string = u"{}. {}\n".format(i,niveles[nivel]["nombre"]).encode("latin-1").decode("utf-8")
    respuesta += nivel_string
    i+=1
  await ctx.reply(respuesta)
###################### AVENTURA #######################################################################

@Bot.command()
async def aventura(ctx):
  usr_id = str(ctx.author.id)
  padawans = aj.abrir_json("DonPito/padawans.json")
  try:
    nivel = padawans[usr_id]['nivel_intervalos']
  except:
    padawans[usr_id]['nivel_intervalos'] = 1
    aj.actualizar_padawans(padawans)
    nivel = padawans[usr_id]['nivel_intervalos']
  ActionRowSiNo = [Button(label = "Sí",style = 3), Button(label = "No" ,style = 4)]
  mensaje = "¿Quieres continuar la avenutra?"
  Botones = await ctx.send(mensaje, components = [ActionRowSiNo])

  def check(interaction):
    return interaction.author == ctx.author
  interaction = await Bot.wait_for("button_click",check=check)
  await Botones.delete()
  selec_usuario = interaction.component.label
  if selec_usuario == "No":
    await ctx.reply("Saliendo...", delete_after = 5)
  elif selec_usuario == "Sí":
    niveles = aj.abrir_json("DonPito/niveles.json")
    usr_name = padawans[usr_id]['name']
    await ctx.reply("Comenzando aventura. Usuario: {}.\nNivel {}: {}".format(usr_name,nivel,niveles[str(nivel)]['nombre']).encode("latin-1").decode("utf-8"))
    interv = niveles[str(nivel)]['intervalos']
    modo = niveles[str(nivel)]['modo']
    aciertos = 0
    media = 0
    for i in range(1,11):
      continuar, elapsed, correcto = await entrenar(ctx,modo,interv)
      tiempo = tdf(elapsed)
      segundos_totales = round(tiempo[0]*3600*24 + tiempo[1]*3600 + tiempo[2]*60 + tiempo[3], 2)
      media += media*(i-1) + segundos_totales/i 
      if correcto:
        aciertos += 1

####################### PITO ##########################################################################

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

  #AQUI PREMIAR O CASTIGAR
  tiempo = tdf(elapsed)
  segundos_totales = round(tiempo[0]*3600*24 + tiempo[1]*3600 + tiempo[2]*60 + tiempo[3], 2)
  contenido = ":thought_balloon: Respuesta de "+ ctx.author.name + ": "
  contenido += ":loud_sound: Respuesta correcta: " + str(f) +  " Hz.\n"
  contenido += ":straight_ruler: Intervalo tolerancia: " + str(tolerancia) + " Hz.\n"
  contenido += ":bar_chart: Te has equivocado en " + str(abs(frecuencia - f)) +" Hz."
  footer = "Tiempo empleado por "+ ctx.author.name+ ": " + str(segundos_totales) +  " s."
  if frecuencia <= tolerancia[0] or frecuencia >= tolerancia[1]: 
    respuesta1 = ":x: *No pasas la prueba. Tu respuesta: " + str(frecuencia) + " Hz.*" 
    color = 0xff0000
  else:
    respuesta1 = ":white_check_mark: *¡Prueba superada! Tu respuesta: " + str(frecuencia) + " Hz.*" 
    color = 0x00c907
    contenido +=  "+1 punto de experiencia. :chart_with_upwards_trend:"
    dar_exp(ctx,1)

  os.remove('tono_puro.wav')
  mensaje = discord.Embed(title = respuesta1, description = contenido, colour = color)
  mensaje.set_footer(text = footer,icon_url = "https://images.emojiterra.com/google/android-pie/512px/23f1.png")
  await ctx.send(embed = mensaje, reference = audio)


#####################SONIDO#############################################################################################
################################################
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
################################################
################################################

###################### EXPERIENCIA ############################################################################################

@Bot.command()
async def exp(ctx):
  usr_id = str(ctx.author.id)
  usr_name = ctx.author.name
  padawans = aj.abrir_json("DonPito/padawans.json")
  if usr_id in padawans:
    exp= padawans[usr_id]['exp']
  else:
    padawans = inscribir(ctx)
    exp = padawans[usr_id]['exp']
  respuesta = "El padawan **" + usr_name + "** tiene **" + str(exp) + "** puntos de experiencia :chart_with_upwards_trend:."
  await ctx.reply(respuesta)
      
##################### CONTINUO ################################################################################################

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
    
##################### ENTRENAR ################################################################################################

@Bot.command()
async def entrenar(ctx,modo = 'ascendente', inter = range(0,13)):
  if modo == 'aleatorio':
    modo = random.choice(['ascendente','descendente','simultaneo'])
  global entrenador_ocupado
  if(not entrenador_ocupado):
    entrenador_ocupado = True
    #PREPARAMOS EL AUDIO
    with ctx.channel.typing():
      await ctx.send("Preparando entrenamiento...",delete_after = 5)
      semitones = random.choice(inter)
      get_audio(modo,semitones)
      #### SE ENVIA EL AUDIO
      audio = await ctx.send(file=discord.File(r'DonPito/test.mp3'))

    #NI BIEN SE ENVIA, SE BORRA
    os.remove("DonPito/test.mp3")
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
      ### aqui habría que premiar o castigar en funcion del boolean "correcto". aqui o en corregir?
      entrenador_ocupado = False
      return True, elapsed, correcto
    else:
      respuesta = "Deteniendo..."
      await ctx.send(respuesta)
      return False, elapsed, False
  else:
    respuesta = "Estoy entrenando a otro usuario."
    await ctx.send(respuesta)


################################################################################################
################################# PASARLE EL TOKEN AL BOT ######################################
################################################################################################

token = aj.abrir_json('DonPito/token_pito.json')["token"]
Bot.run(token) #token
