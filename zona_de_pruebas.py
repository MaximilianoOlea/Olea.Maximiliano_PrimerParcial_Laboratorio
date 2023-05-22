# open("Primer_Parcial.py\\insumos.csv")
import csv
import re
def pet_parser_csv() -> list:

    """_summary_
        Se ocupa de cargar los datos del archivo insumos.csv
    Returns:
        _type_: Returna una lista de diccionario con los insumos
    """
    lista_insumos = []
    lineas = parser_csv("Primer_Parcial.py\\insumos.csv", ",")
    for insumo in lineas:
        id = insumo[0]
        nombre = insumo[1]
        marca = insumo[2]
        precio = insumo[3].replace("$","")
        caracteristicas = insumo[4].title()

        lista_insumos.append({
            "ID": id,
            "Nombre": nombre,
            "Marca": marca,
            "Precio": precio,
            "Caracteristicas": caracteristicas,
        })

    return lista_insumos

def parser_csv(path: str, separador: str, saltar_primer_linea: bool = True) -> list:
    """_summary_
        Abre un archivo tipo csv y lo convierte en una lista
    Args:
        path (str): Lugar donde se encuentra el archivo csv
        separador (str): caracter separador de los datos
        saltar_primer_linea (bool, optional): True si se quiere OMITIR la primer linea
        (Encabezado) o False para escribirla

    Returns:
        list: Lista con los datos obtenidos en cada linea del archivo csv
    """
    lista = []
    with open(path, "r", encoding="utf-8") as file:
        # if saltar_primer_linea:
        #     next(file)  # Omite la primera linea del archivo (que son los titulos)

        contenido = file.readlines()

        for i in range(len(contenido)):
            # Para no guardar el salto de linea "invisible" del archivo
            # linea = linea.rstrip("\n")
            contenido[i] = contenido[i].replace("\n", "")
            lista.append(contenido[i].split(separador))

        if saltar_primer_linea:
            elemento = lista.pop(0)
    return lista

def mostrar_insumo_fila(insumo: dict) -> None:
    """
    Funcion que muestra un unico insumo en una sola linea.

    Args:
        insumo: El insumo que quiere imprimirse
    """
    print(f"""{insumo['ID']:4s}  {insumo['Nombre']}       {insumo['Marca']}      {insumo['Precio']}     {insumo['Caracteristicas']}""")


def obtener_primer_caracteristica (insumo:dict)->str:
    """_summary_
    De un insumo[caracteristicas] se obtiene la primer coincidencia hasta encontrar un simbolo
    Args:   
        insumo (dict): Insumo del que se va a obtener la primer caracteristica

    Returns:
        str: Devuelve la primera caracteristica obtenida en forma de string
    """
    string = ""
    patron = re.compile("[a-zA-Z-\s]+")
    match = patron.match (f"{insumo['Caracteristicas']}")
    
    if (match):
        string = match.group()+"."

    return string

def buscar_coincidencia_string (string_a_buscar:str,string_coincidencia:str)->bool:
    """_summary_
    Recibe un string (primer parametro) para buscar y el string en donde debe buscarse el primer parametro
    Args:
        string_a_buscar (str): String que va a buscarse
        string_coincidencia (str): String donde debe buscarse el primer parametro

    Returns:
        bool: Devuelve True si encontró y False si no encontró
    """
    
    flag_encontro = False
    
    patron = re.compile (string_a_buscar.title())
    match = patron.search (string_coincidencia.title())

    if (match):
        flag_encontro = True
    return flag_encontro

def imprimir_insumo_por_caracteristica (lista:list,string_a_buscar)->bool:

    flag_encontro = False

    for insumo in lista:
        if (buscar_coincidencia_string(string_a_buscar,insumo['Caracteristicas'])):
            mostrar_insumo_fila(insumo)
            flag_encontro = True

    return flag_encontro 
def pet_insumo_por_caracteristica(lista:list)->bool:

    flag_encontro = False
    string_a_buscar = input ("Ingrese caracteristica del insumo: ").title()

    if (not imprimir_insumo_por_caracteristica(lista,string_a_buscar)):
        print ("La característica no se ha encontrado.")
    else:
        flag_encontro = True

    return flag_encontro

def validar_si_no (mensaje:str,intentos:int)->bool:

    flag_validacion = False
    respuesta = input(f"\n{mensaje.lower()} (S|N) \n")
    while (respuesta != "s" and respuesta != "n" and intentos>0):
        intentos -= 1
        print ("Opcion invalida.")
        respuesta = input(f"\n{mensaje.lower()} (S|N) \n")

    if intentos > 0:
        flag_validacion = True
    return flag_validacion
lista = pet_parser_csv()

mostrar_insumo_fila(lista[4])
# print(obtener_primer_caracteristica(lista[4]))
# print (buscar_coincidencia_string("Sin granos","Con lupulos y Sin Granos"))


    
# pet_listar_insumos(lista)



