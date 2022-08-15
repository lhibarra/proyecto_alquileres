import requests
import json
def fetch(provincia):
    #Filtro los alquileres por provincia
    url = 'https://api.mercadolibre.com/sites/MLA/search?category=MLA1459&q=Departamentos%20Alquilers%20{}%20&limit=50'.format(provincia)
    response = requests.get(url)
    json_data = response.json()['results']
    return json_data
  
    
def cant_tipo_moneda(lista_datos):   
    lista_en_pesos =  [i  for i in lista_datos if i["currency_id"] == "ARS"]
    lista_en_dolares  = [i  for i in lista_datos if i["currency_id"] == "USD"]
    #print(len(lista_en_dolares))
    total_alquileres = len(lista_datos)
    cant_moneda = []
    cant_moneda.append({"total":len(lista_datos), "pesos":len(lista_en_pesos),"dolar":len(lista_en_dolares)})
    #print(f"El total de alquileres encontrados son: {total_alquileres}")
    #print("Cantidad de alquileres en $: ",len(lista_en_peso))
    #print("Cantidad de alquileres en USD: ",len(lista_en_dolar))
    return cant_moneda

def seleccionar_datos(lista_datos, moneda,minimo,maximo):
       
    lista_segun_moneda  = [i  for i in lista_datos if i["currency_id"] == moneda]
    lista_datos = lista_segun_moneda
    lista = []
    for i in lista_datos:       
        #Obtener precio      
        if i.get('price') and i.get('currency_id') is None:
            print("Datos no cargados") 
        else:
            precio = int(i.get('price'))
        
            #Obtener metros2 del dpto
                
        for k in i['attributes']:
            if k.get("value_struct") is None:
                    print("datos no encontrados")
            else:
                mt = k.get("value_struct").get("number") 
            #obtengo nro de ambientes del dpto
            
        if (i['attributes'][5]['value_name']).isdigit():
            ambiente = (i['attributes'][5]['value_name'])              
            #Armo la lista de diccionario con los datos obtenidos
            if precio >= minimo and precio <= maximo:
                lista.append({"Precio":precio, "Moneda":moneda, "Mts2": mt,"Ambientes": ambiente})       
    
    return lista
'''
    lista = []
    #Busco y muestro m2 de cada dpto
    for k in json_data:
       # try:
            for i in k['attributes']:
                if i.get("value_struct") is None:
                    print("datos no encontrados")
                else:
                    lista.append({"Mts2",i.get("value_struct").get("number")})
    print(f"Metros2 de cada Dpto{lista}")
        # except:
       
    #return lista
                   
           # print("estructura incompleta")
    
    #busco y muestro cantidad de ambientes de cada dpto
    for d in json_data:
        for k,v in d['attributes'][3].items():
                if k == "value_name" and v.isdigit():
                    print(f'cantidad de ambientes: {v}')
   
if __name__ == '__main__':
   
    lista_provincia = fetch("Cordoba")
    x = seleccionar_datos(lista_provincia,"USD",10,50000)
    print(x)
    #n = cant_tipo_moneda(lista_provincia)
    #print(n)
 ''' 
  
       