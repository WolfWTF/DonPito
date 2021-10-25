import json
#################-ACTUALIZAR PADAWANS-#################
#Esta función guarda el objeto JSON "padawans" en el archivo "DonPito/padawans.json".
def actualizar_padawans(padawans):
  out_file = open("DonPito/padawans.json", "w") 
  json.dump(padawans, out_file, indent = 4) 
  out_file.close()    

#################-ABRIR JSON-#################
#Esta función abre un archivo json y carga su contenido en la variable que devuelve.
def abrir_json(nombre_archivo):
  with open(nombre_archivo,"r", encoding= "latin-1") as jsonFile:#="utf-8") as jsonFile: #,encoding='latin-1'
  #with open(nombre_archivo,"rb") as jsonFile:
    objeto_json = json.load(jsonFile)
    jsonFile.close()
  return objeto_json