import json
import csv
import os
import platform
import re

# --------------------------Carga y Escritura de archivos---------------------------
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
        marca = insumo[2].title()
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


def mostrar_insumo_fila(insumo: dict) -> None:
    """
    Funcion que muestra un unico insumo en una sola linea.

    Args:
        insumo: El insumo que quiere imprimirse
    """
    print(f"""{insumo['ID']:4s}  {insumo['Nombre']:35}       {insumo['Marca']:22}      ${insumo['Precio']:10}     {insumo['Caracteristicas']}""")

def mostrar_insumo_titulo ()-> None:
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





# --------------------------------------------

def esta_en_lista(lista: list, item: str) -> bool:
    esta = False
    for elemento in lista:
        if (elemento.lower() == item.lower()):
            esta = True
            break
    return esta

def proyectar_insumo(lista: list, key: str, repe: bool = False) -> list:
    """_summary_
    Se filtra el valor que tiene un insumo dentro de una key particular 
    Args:
        lista (list): Lista que desea filtrarse
        key (str): Campo del insumo que va a filtrarse
        repe (bool, optional):True (Lista con repetidos) False(Lista sin repetidos)

    Returns:
        list: Devuelve la lista filtrada
    """

    lista_filtrada = []
    for insumo in lista:
        lista_filtrada.append(insumo[key])

    if (not repe):
        lista_aux = []
        for item in lista_filtrada:
            if (not esta_en_lista(lista_aux, item)):
                lista_aux.append(item)

        lista_filtrada = lista_aux

    return lista_filtrada


def contar_coincidencias_lista(lista_filtrada:list, lista_repetidos:list)->None:
    """Cuenta cada vez que los elementos repetidos de una lista
    coindicen con los elementos de la otra lista (filtrada)

    Args:
        lista_filtrada (_type_): Lista que no tendrá elementos repetidos
        lista_repetidos (_type_): Lista con elementos repetidos
    """
    for elemento in lista_filtrada:
        contador = 0

        for item in lista_repetidos:

            if (item.lower() == elemento.lower()):
                contador += 1

        print(f"{elemento}: ({contador})")

# -----------------------Punto 3---------------------------------
def obtener_nombre(insumo: dict) -> str:
    """_summary_
        Se obtiene el nombre de un insumo  y se devuelve el string
    Args:
        insumo (dict): Insumo del cual quiere obtenerse el nombre

    Returns:
        str: Nombre obtenido del insumo
    """
    string = (f'Nombre: {insumo["Nombre"]}')

    return string

def obtener_nombre_y_dato(insumo: dict, key: str,simbolo:str = "") -> str:
    """_summary_
    Obtiene el nombre y el atributo de un insumo
    Args:
        insumo (dict): insumo del que se va a obtener el nombre
        key (str): el atributo que ira acompañado del nombre
        simbolo:(str)(opcional): Puede agregarse un simbolo al lado del dato que se va a imprimir
    Returns:
        str: Devuelve el nombre + el atributo del insumo
    """

    string = (f"{obtener_nombre(insumo):30s} | {key}: {simbolo}{insumo[key]}")

    return string

def imprimir_nombre_dato_coincidencia(lista: list, key: str, coincidencia):
    """_summary_
    Se imprime el nombre y el dato siempre que el elemento de la lista coincida con otro elemento (coincidencia) 
    Args:
        lista (list): Lista (completa)
        key (str): key con la que se va a realizar la comparacion
        coincidencia (_type_): elemento de una lista (filtrada)
    """
    
    for insumo in lista:
        if (insumo[key] == coincidencia):
            print(obtener_nombre_y_dato(insumo,"Precio","$"))

def pet_marca_nombre_precio (lista:list):

    lista_marca = proyectar_insumo(lista,"Marca")
    print (lista_marca)

    for marca in lista_marca:
        print (f"------------------\n({marca}):")
        imprimir_nombre_dato_coincidencia(lista,"Marca",marca)



# -------------------------Punto 4 -------------------------------
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



# ---------------------------Punto 5----------------------------------
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

# ------------------------Punto 7------------------------------------

def pet_alimento_json(lista:list)->None:
    with open ('Alimento.json', 'w', encoding='utf-8') as file:
        for insumo in lista:
            if (buscar_coincidencia_string("Alimento",insumo['Nombre'])):
                json.dump(insumo, file, ensure_ascii=False, indent =2)
    print ("Lista creada.")

# --------------------Menu---------------------------------------
def validar_entero(numero: str) -> bool:
    """ Valida si el string ingresado es un número

    Args:
        numero (str): dato que se va a analizar

    Returns:
        bool: Retorna True si es un numero, caso contrario un False
    """

    flag_es_numero = False

    if numero.isdigit():
        flag_es_numero = True

    return flag_es_numero

def imprimir_menu() -> None:
    print("""
            INSUMOS APP
-----------------------------------------    
1)Cargar datos.
2)Listar cantidad de insumos por marca.
3)Listar insumos por marca.
4)Buscar insumo por caracteristica.
5)Listar insumos ordenados.
6)Realizar compras.
7)Guardar Productos "alimento"(JSON).
8)Listado de Productos "alimento"(JSON).
9)Actualizar Precios.
10)Salir.
----------------------------------------- """)


def pet_menu_principal() -> int:
    """Valida si el tipo de dato ingresado por el usuario es un entero
    De no cumplirse retorna un -1

    Returns:
        int: retorna el numero ingresado o -1(si no ingresó numero)
    """
    imprimir_menu()
    opcion = input("Ingrese opción: ")
    if validar_entero(opcion):
        opcion = int(opcion)
    else:
        opcion = -1

    return opcion


def pet_app() -> None:

    flag_carga = False

    while True:
    #    Menu
        os.system("cls")
        opcion = pet_menu_principal()
        os.system("cls")
        match(opcion):

            case -1:
                print("Opcion invalida.")

            case 1:
                # Cargar datos dsde archivo csv
                lista_insumos = pet_parser_csv()
                flag_carga = True
                pet_listar_insumos(lista_insumos)
            
            case 2:
                lista_marcas = proyectar_insumo(lista_insumos,"Marca")
                lista_marcas_repetidos = proyectar_insumo(lista_insumos,"Marca",True)
                contar_coincidencias_lista(lista_marcas,lista_marcas_repetidos)
            case 3:
                pet_marca_nombre_precio(lista_insumos)
            case 4:
                pet_insumo_por_caracteristica(lista_insumos)
            case 5:
                lista_ordenada_ascendente = ordenar_marca_precio(lista_insumos)
                pet_listar_insumos(lista_ordenada_ascendente)
            case 7: 
                pet_alimento_json(lista_insumos)
            case 10:
                print("HA SALIDO.")
                break

        os.system("pause")
