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
  #await channel.send("¡Don Pito reconectado!")

intervalos = ["Unísono", "2ª menor", "2ª Mayor","3ª menor", "3ª Mayor",
              "4ª", "Tritono", "5ª", "6ª menor", "6ª mayor","7ª menor",
              "7ª Mayor", "Octava", "9ª menor", "9ª Mayor"]
Botones_Intervalos = []

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
  padawans[usr_id] = {"name": usr_name, "exp": 0, "nivel_intervalos": 1}
  aj.actualizar_padawans(padawans)
  return padawans

def corregir(ctx,usuario,selec_usuario,respuesta_correcta,elapsed):
  correcto = selec_usuario == respuesta_correcta
  tiempo = tdf(elapsed)
  segundos_totales = round(tiempo[0]*3600*24 + tiempo[1]*3600 + tiempo[2]*60 + tiempo[3], 2)

  if correcto:
    #DEPENDE LA EXPERIENCIA DE LA OCTAVA OCTAVA CENTRAL +1, EN ESPEJO +2 Y +3
    experiencia = dar_exp(ctx,1)# por qué a Alex no le ha dado la experiencia?
    respuesta = ":white_check_mark:  **{}**  :white_check_mark:  ¡Muy bien, {}!Tiempo: {} s.\n +1 punto de exp. Puntos totales: {}".format(selec_usuario,usuario.name,str(segundos_totales),experiencia)
  else:
    respuesta =":x: {}:  **{}**  :x:  Respuesta correcta: **{}**.".format(usuario.name, selec_usuario, respuesta_correcta)
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
  if not(usr_id in padawans):
    padawans = inscribir(ctx)
  exp = padawans[usr_id]['exp']
  exp += puntos

  padawans[usr_id]['exp'] = exp
  aj.actualizar_padawans(padawans)
  return exp

def get_escala(escala,direccion="ascendente"):
  #Falta implementar las direcciones
  lim_asc =[20,60]
  start = random.randint(lim_asc[0],lim_asc[1])
  info = aj.abrir_json("DonPito/piano/info.json")
  notas = info['keys']
  audio = pydub.AudioSegment.silent(duration=25)
  for i in escala:
    #notas.append(start + i)
    n_nota = start + int(i)
    nombre_nota = "DonPito/piano/" + notas[n_nota] +".mp3"
    #fnota1 = open(nota1_nombre,'rb')
    nota = pydub.AudioSegment.from_file(nombre_nota)
    #fnota1.close()
    audio = audio.append(nota, crossfade = 25)
    audio.export("DonPito/modo.mp3", format="mp3")


entrenador_ocupado = False
def get_audio(modo,semitones):
      global piano
      if piano:
        lim_asc = [0,75]
        lim_des = [11,87]
      else:
        lim_asc = [1,37]
        lim_des = [12,49]
      #start=datetime.now()

      if(modo == 'ascendente'):
        n1 = random.randint(lim_asc[0],lim_asc[1])
        n2 = n1 + semitones

      elif(modo == 'simultaneo'):
        n1 = random.randint(28,75)
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

###################### COMANDOS ############################################################################################

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
  d = (dias != 0)*"{} días ,".format(dias)
  h = (horas!= 0)*"{} horas ,".format(horas)
  m = (minutos != 0)*"{} minutos, ".format(minutos)
  segundos = round(segundos - dias*24*3600 - horas*3600 - minutos*60)
  s = (segundos != 0)*"{} segundos.".format(segundos)
  respuesta = "Llevo conectado {}{}{}{}".format(d,h,m,s)
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
  usr_name = padawans[usr_id]['name']
  #try:
  if usr_id in padawans:
    nivel = padawans[usr_id]['nivel_intervalos']
  #except:
  else:
    padawans[usr_id]['nivel_intervalos'] = 1
    aj.actualizar_padawans(padawans)
    nivel = padawans[usr_id]['nivel_intervalos']
  ActionRowSiNo = [Button(label = "Sí",style = 3), Button(label = "No" ,style = 4), Button(label = "Repetir nivel" ,style = 3)]
  mensaje = "Nivel {} ¿Continuar avenutra interválica?".format(nivel)
  Botones = await ctx.send(mensaje, components = [ActionRowSiNo])

  async def func_nivel(nivel,usr_name):
    niveles = aj.abrir_json("DonPito/niveles.json")
    
    interv = niveles[str(nivel)]['intervalos']
    modo = niveles[str(nivel)]['modo']
    aciertos = 0
    media = 0
    for i in range(1,11):
      continuar, elapsed, correcto, usuario = await entrenar(ctx,modo,interv)
      if not continuar:
        return
      tiempo = tdf(elapsed)
      segundos_totales = round(tiempo[0]*3600*24 + tiempo[1]*3600 + tiempo[2]*60 + tiempo[3], 2)
      media += media*(i-1) + segundos_totales/i 
      if correcto:
        aciertos += 1
    return aciertos

  def check(interaction):
    return interaction.author == ctx.author


  interaction = await Bot.wait_for("button_click",check=check)
  await Botones.delete()
  selec_usuario = interaction.component.label
  if selec_usuario == "No":
    pass
    #await ctx.reply("Saliendo...", delete_after = 5)

  elif selec_usuario == "Sí":
    await ctx.reply("Comenzando aventura. Usuario: {}.\nNivel {}: {}".format(usr_name,nivel,niveles[str(nivel)]['nombre']).encode("latin-1").decode("utf-8"))
    aciertos = func_nivel(nivel,usr_name)

    #ACTUALIZAMOS PADAWANS
    #padawans = aj.abrir_json("DonPito/padawans.json")
    resultados = "Aciertos: {}/10. ".format(aciertos)
    if aciertos >= 7:
      resultados += ":white_check_mark: Has superado la prueba, pasas al nivel {}.".format(nivel+1)
      padawans[usr_id]["nivel_intervalos"] += 1
      aj.actualizar_padawans(padawans)
    else:
      resultados += ":x: No has superado la prueba. Inténtalo de nuevo."
    respuesta = discord.Embed(title = "Resultados:", description = resultados)
    await ctx.send(embed=respuesta)

  elif selec_usuario == "Repetir nivel":
    #habrá que seleccionar el nivel, digo yo
    query = await ctx.reply("Introduce el número de nivel que quieres repetir.") #hay que deletear luego
    selec_usuario = (await Bot.wait_for("message", check=check)).content.lower()
    num = esunnumero(selec_usuario)
    if not num:
      resultados = ":x: Error. Selecciona nivel con su número. "
      await ctx.send(resultados)
    if int(selec_usuario) < int(nivel):
      aciertos = await func_nivel(selec_usuario,usr_name)

      if aciertos == 10:
        resultados = ":muscle_tone2: 10/10 ¡Te has marcado un perfect!"
        await ctx.send(resultados)
      else:
        resultados = ":woozy_face: {}/10 Aún no te sale perfecto. ".format(aciertos)
        await ctx.send(resultados)
    else:
      resultados = "Sólo puedes repetir niveles que ya hayas superado."
      await ctx.send(resultados)



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
  contenido =  """:thought_balloon: {}: {} Hz.
                  :loud_sound: Respuesta correcta: {} Hz.
                  :straight_ruler: Tolerancia: {} Hz.
                  :bar_chart: Error de {} Hz.""".format(ctx.author.name, f, tolerancia, abs(frecuencia - f), segundos_totales)
  '''contenido = ":thought_balloon: Respuesta de "+ ctx.author.name + ": "
        contenido += ":loud_sound: Respuesta correcta: " + str(f) +  " Hz.\n"
        contenido += ":straight_ruler: Intervalo tolerancia: " + str(tolerancia) + " Hz.\n"
        contenido += ":bar_chart: Te has equivocado en " + str(abs(frecuencia - f)) +" Hz."'''
  footer = "Tiempo: {}s.".format(segundos_totales)
  if frecuencia <= tolerancia[0] or frecuencia >= tolerancia[1]: 
    respuesta1 = ":x: *No pasas la prueba.*"
    color = 0xff0000
  else:
    respuesta1 = ":white_check_mark: *¡Prueba superada!*"
    color = 0x00c907
    contenido +=  " +1 punto de exp. :chart_with_upwards_trend:"
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
  respuesta = "El padawan **{}** tiene **{}** puntos de exp :chart_with_upwards_trend:.".format(usr_name, exp)
  await ctx.reply(respuesta)
      
##################### CONTINUO ################################################################################################
#ADAPTAR AL NIVEL DEL USUARIO

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
  ActionRow3.append(stop_button) #ESTO ME LO HE CARGAO EN LA FUNCION ENTRENAR
  continuar, elapsed, correcto = await entrenar(ctx,modo_elegido)
  ActionRow3 = Botones_Intervalos[9:13]

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
    nombre = "{} pruebas:".format(n-1)
    valor =  """:white_check_mark: Aciertos: {}.
                :x: Fallos: {}.
                :timer: Media: {} segundos.""".format(aciertos,fallos,m)
    respuesta.add_field(name = nombre, value= valor)
     
    await ctx.reply(embed=respuesta)
    media = 0
    n = 1
    aciertos = 0 
    fallos = 0
    
##################### ENTRENAR ################################################################################################
#ADAPTAR AL NIVEL DEL USUARIO
@Bot.command()
async def entrenar(ctx,modo = 'ascendente', inter = range(0,13),usr2=None):
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

    stop_button = Button(label="Stop",style=4)
    ar1=[]  
    a=1
    if (len(inter) <= 5):
      for i in inter:
        ar1.append(Botones_Intervalos[i])
      componentes = [ar1,[stop_button]]
      
    elif (len(inter) <= 10):
      ar2 = []
      for i in inter():
        if a <= 5:
          ar1.append(Botones_Intervalos[i])
        else:
          ar2.append(Botones_Intervalos[i])
      componentes = [ar1,ar2,[stop_button]]
      a+=1

    else:
      ar2 = []
      ar3 = []
      for i in inter:
        if (a <= 5):
          ar1.append(Botones_Intervalos[i])
        elif (a <= 10):
          ar2.append(Botones_Intervalos[i])
        else:
          ar3.append(Botones_Intervalos[i])
        a += 1

      
      componentes = [ar1,ar2,ar3,[stop_button]]  

    Botones = await ctx.send("Opciones:", components = componentes)

    def check(interaction):
      return interaction.author == ctx.author or interaction.author == usr2

    interaction = await Bot.wait_for("button_click",check=check)
    end=datetime.now()
    elapsed = end-start
    await Botones.delete()
    selec_usuario = interaction.component.label
    usuario = interaction.author

    #¿qué pasa si el más rápido FALLA?

    #CORREGIMOS
    if selec_usuario != "Stop":
      respuesta, correcto = corregir(ctx,usuario,selec_usuario, respuesta_correcta,elapsed)
      await ctx.send(respuesta, reference = audio)
      entrenador_ocupado = False
      return True, elapsed, correcto, usuario
    else:
      respuesta = "Deteniendo..."
      entrenador_ocupado = False
      await ctx.send(respuesta, delete_after=5)
      return False, elapsed, False, usuario
  else:
    respuesta = "Estoy entrenando a otro usuario."
    await ctx.send(respuesta, delete_after=5)

#################### DUELO #####################
@Bot.command()
async def duelo(ctx,usr2: discord.member.Member):
  usr1 = ctx.author
  continuar = True
  punt_usr1 = 0
  punt_usr2 = 0
  for i in range(5):
    if continuar:

      continuar, elapsed, correcto, usuario = await entrenar(ctx,'aleatorio',range(0,13),usr2)
      if usuario == usr1 and correcto:
        punt_usr1 += 1
      elif usuario == usr2 and correcto:
        punt_usr2 += 1

    else:
      await ctx.reply("Duelo interrumpido por {}.".format(usuario), delete_after = 5)
      return
  if punt_usr1 > punt_usr2:
    ganador = usr1.name
  elif punt_usr1 < punt_usr2:
    ganador = usr2.name
  else:
    ganador = "Empate."

  puntuaciones = """Resultados:
    {}: {} puntos.
    {}: {} puntos.
    El ganador del duelo es...
    ***{}***
    """.format(usr1,punt_usr1,usr2,punt_usr2,ganador)
  await ctx.reply(puntuaciones)


  #Es un modo que tiene como entrada dos usuarios, igual que los que están en /dar de Montse
  #En principio va a ser un duelo al mejor de 5 intervalos, quiero que marque por cuántos va. 
  #En el duelo, se llama a !entrenar pero se autoriza a dos usuarios para la interacción.
  #Se debe acumular el número de aciertos y al final, el que más tenga, gana.


#################### MODOS #########################
@Bot.command()
async def modos(ctx):
  lista = aj.abrir_json("DonPito/modos.json")
  mayor = lista["mayor"]
  modos_mayor = list(mayor.keys())

  botoncitos = []
  for modo in modos_mayor:
    new_boton = Button(label = modo, style = 1)
    botoncitos.append(new_boton)
  row1 = botoncitos[0:3]
  row2 = botoncitos[3:]

  respuesta_correcta = random.choice(modos_mayor)
  escala = lista["mayor"][respuesta_correcta]
  await ctx.send("Preparando entrenamiento...",delete_after=5)
  get_escala(escala)
  audio = await ctx.send(file=discord.File(r'DonPito/modo.mp3'))
  start=datetime.now()    
  componentes = [row1,row2]  
  Botones = await ctx.send("Opciones:", components = componentes)
  def check(interaction):
    return interaction.author == ctx.author
  interaction = await Bot.wait_for("button_click",check=check)
  end=datetime.now()
  elapsed = end-start
  await Botones.delete()
  selec_usuario = interaction.component.label
  if selec_usuario == respuesta_correcta:
    respuesta = ":white_check_mark: Correcto! {}.".format(respuesta_correcta)
    dar_exp(ctx,1)
  else:
    respuesta = ":x: Incorrecto. El modo era {}, no {}.".format(respuesta_correcta, selec_usuario)
  await ctx.send(respuesta,reference = audio)

################################################################################################
################################# PASARLE EL TOKEN AL BOT ######################################
################################################################################################

token = aj.abrir_json('DonPito/token_pito.json')["token"]
Bot.run(token) #token
