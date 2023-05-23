# open("Primer_Parcial.py\\insumos.csv")
import csv
import re
import json


def pet_parser_csv() -> list:
    """_summary_
        Se ocupa de cargar los datos del archivo insumos.csv
    Returns:
        _type_: Returna una lista de diccionario con los insumos
    """
    lista_insumos = []
    lineas = parser_csv("insumos.csv", ",")
    for insumo in lineas:
        id = insumo[0]
        nombre = insumo[1].title()
        marca = insumo[2].title()
        precio = insumo[3].replace("$", "")
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
            lista.pop(0)
    return lista


def mostrar_insumo_fila(insumo: dict) -> None:
    """
    Funcion que muestra un unico insumo en una sola linea.

    Args:
        insumo: El insumo que quiere imprimirse
    """
    print(f"""{insumo['ID']:4s}  {insumo['Nombre']:35}       {insumo['Marca']:22}      ${insumo['Precio']:10}     {insumo['Caracteristicas']}""")


def mostrar_insumo_titulo() -> None:
    print("ID    Nombre                                    Marca                       Precio          Caracteristicas")


def pet_listar_insumos(lista: list) -> None:
    """_summary_
    Se ingresa una lista de insumos y se imprime todos sus datos
    Args:
        lista (list):  La lista que se va a imprimir
    """

    # Este print no se limpia con el os.system (Preguntar por qué)
    # print ("Lista de insumos:")
    mostrar_insumo_titulo()
    for insumo in lista:
        mostrar_insumo_fila(insumo)


# -----------------------------------------------------------------------------------

def obtener_primer_caracteristica(insumo: dict) -> str:
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


def validar_si_no(mensaje: str, intentos: int) -> bool:

    flag_validacion = False
    respuesta = input(f"\n{mensaje.lower()} (S|N) \n")
    while (respuesta != "s" and respuesta != "n" and intentos > 0):
        intentos -= 1
        print("Opcion invalida.")
        respuesta = input(f"\n{mensaje.lower()} (S|N) \n")

    if intentos > 0:
        flag_validacion = True
    return flag_validacion


lista = pet_parser_csv()


def ordenar_marca_precio(lista_a_ordenar: list) -> list:

    lista = lista_a_ordenar.copy()
    tam = len(lista)
    for i in range(tam-1):
        for j in range(i+1, tam):
            # ordenar de manera ascendente (menor a mayor )
            if (lista[i]["Marca"] == lista[j]["Marca"]) and (float(lista[i]["Precio"]) < float(lista[j]["Precio"])) or (lista[i]["Marca"] > lista[j]["Marca"]):
                aux = lista[i]
                lista[i] = lista[j]
                lista[j] = aux

    return lista


# -------------------------------Punto 6------------------------------

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

def comprar(lista: list) -> None:

    while True:
        marca_a_buscar = input("Ingrese una marca: ")
        lista_marca_coincidencia = []

        # Obtengo la marca
        for insumo in lista:
            # Si coincide la guardo en una lista aparte para despues mostrarla
            if buscar_coincidencia_string(marca_a_buscar,insumo["Marca"]):
                lista_marca_coincidencia.append(insumo)

        if lista_marca_coincidencia:
            acumulador_subtotal = 0.0
            print("Lista de productos de esa marca:\n")
            pet_listar_insumos(lista_marca_coincidencia)
            while(True):
                producto = input("Ingrese un producto: ").title()
                lista_nombre_coincidencia = []
                for insumo in lista_marca_coincidencia:
                    if (insumo['Nombre']) == producto:#Si el producto tiene mismo nombre, preguntar por precio
                        lista_nombre_coincidencia.append (insumo)
                print (len(lista_nombre_coincidencia))
                if(len(lista_nombre_coincidencia)>1):
                    producto_precio = input("Hay más de un producto con ese nombre. Especique su precio: ")
                    for producto in lista_nombre_coincidencia:
                        if (producto["Precio"]) == producto_precio:
                            cantidad = int(input("Ingrese cuantas unidades quiere: "))
                            acumulador_subtotal += cantidad * float(producto["Precio"])
                else:
                    cantidad = int(input("Ingrese cuantas unidades quiere: "))
                    acumulador_subtotal += cantidad * float(insumo["Precio"])
                
                print ("Subtotal :$",acumulador_subtotal)
                respuesta = input("Quiere comprar otro producto de esta marca? (s)").lower()
                if (respuesta != "s"):
                    # Salgo de la lista
                    print (f"La cantidad total de su compra es : ${acumulador_subtotal:.2f}")
                    break
            break
        else:
            print("No se encontró la marca")


# ---------------------------Punto 7------------------------------------

def convertir_dicc_a_json(diccionario:dict,archivo:str)->None:
    diccionario = str(diccionario)
    diccionario_json = json.dump (diccionario,archivo,ensure_ascii=False, indent =2)
    return diccionario_json



def pet_alimento_json(lista:list)->None:

    lista_alimentos= []

    for insumo in lista:
        if (buscar_coincidencia_string("Alimento",insumo['Nombre'])):
            lista_alimentos.append(insumo)

    with open ('Alimento.json', 'w', encoding='utf-8') as file:
        json.dump(lista_alimentos, file, ensure_ascii=False, indent =2)

def cargar_lista_desde_json(ruta_archivo:str)->list:
    with open (ruta_archivo, 'r',encoding='utf-8') as file:
        contenido = file.read()
        lista = json.loads(contenido)
    
    return lista

# -----------------------------------------------------------------------
lista = pet_parser_csv()

# pet_listar_insumos(lista)

# pasar_a_json(lista)
# comprar(lista)
pet_alimento_json(lista)
lista_cargada = cargar_lista_desde_json('Alimento.json')
pet_listar_insumos(lista_cargada)
# pet_listar_alimento_json()
