import json
import csv
import os
import platform
import re


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
        nombre = insumo[1]
        marca = insumo[2]
        precio = insumo[3]
        caracteristicas = insumo[4]

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
    print(f"""{insumo['ID']:<4d}  {insumo['Nombre']:35}       {insumo['Marca']:22}      ${insumo['Precio']:>7.2f}     {insumo['Caracteristicas']}""")


def mostrar_insumo_titulo() -> None:
    print("ID    Nombre                                    Marca                       Precio       Caracteristicas")


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
    patron = re.compile("[\w\s]+")
    match = patron.match (f"{insumo['Caracteristicas']}")

    if (match):
        string = match.group()+"."

    return string

def cargar_lista_primer_caracteristica(lista)->list:
    lista_copia = lista.copy()

    for insumo in lista_copia:
        insumo["Caracteristicas"] = obtener_primer_caracteristica(insumo)

    return lista_copia

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

def buscar_coincidencia_string(string_a_buscar: str, string_coincidencia: str) -> bool:
    """_summary_
    Recibe un string (primer parametro) para buscar y el string en donde debe buscarse el primer parametro
    Args:
        string_a_buscar (str): String que va a buscarse
        string_coincidencia (str): String donde debe buscarse el primer parametro

    Returns:
        bool: Devuelve True si encontró y False si no encontró
    """

    flag_encontro = False

    patron = re.compile(string_a_buscar.title())
    match = patron.search(string_coincidencia.title())

    if (match):
        flag_encontro = True
    return flag_encontro

# def comprar(lista: list) -> None:

#     while True:
#         marca_a_buscar = input("Ingrese una marca: ")
#         lista_marca_coincidencia = []

#         # Obtengo la marca
#         for insumo in lista:
#             # Si coincide la guardo en una lista aparte para despues mostrarla
#             if buscar_coincidencia_string(marca_a_buscar,insumo["Marca"]):
#                 lista_marca_coincidencia.append(insumo)

#         if lista_marca_coincidencia:
#             acumulador_subtotal = 0.0
#             print("Lista de productos de esa marca:\n")
#             pet_listar_insumos(lista_marca_coincidencia)
#             while(True):
#                 producto = input("Ingrese un producto: ").title()
#                 lista_nombre_coincidencia = []
#                 for insumo in lista_marca_coincidencia:
#                     if (insumo['Nombre']) == producto:#Si el producto tiene mismo nombre, preguntar por precio
#                         lista_nombre_coincidencia.append (insumo)
#                 print (len(lista_nombre_coincidencia))
#                 if(len(lista_nombre_coincidencia)>1):
#                     producto_precio = input("Hay más de un producto con ese nombre. Especique su precio: ")
#                     for producto in lista_nombre_coincidencia:
#                         if (producto["Precio"]) == producto_precio:
#                             cantidad = int(input("Ingrese cuantas unidades quiere: "))
#                             acumulador_subtotal += cantidad * float(producto["Precio"])
#                 elif(len(lista_nombre_coincidencia)==1):
#                     cantidad = int(input("Ingrese cuantas unidades quiere: "))
#                     acumulador_subtotal += cantidad * float(insumo["Precio"])

#                 print ("Subtotal :$",acumulador_subtotal)
#                 respuesta = input("Quiere comprar otro producto de esta marca? (s)").lower()
#                 if (respuesta != "s"):
#                     # Salgo de la lista
#                     print (f"La cantidad total de su compra es : ${acumulador_subtotal:.2f}")
#                     break
#             break
#         else:
#             print("No se encontró la marca")


def filtrar_lista_lambda(lista: list, condicion) -> list:
    """_summary_
    Filtra una lista dependiendo de la condicion lambda que se pase
    Args:
        lista (list): Lista que se va a filtrar
        condicion (_type_): Desarrollo de una funcion lambda (que filtre la lista)

    Returns:
        list: Devuelve una lista filtrada
    """
    lista_filtrada = list(filter(condicion, lista))

    return lista_filtrada


def comprar(lista: list) -> list:
    factura = []

    lista_copia = cargar_lista_primer_caracteristica(lista)
    pet_listar_insumos(lista_copia)
    acumulador_total = 0
    while True:
        marca_a_buscar = input(
            "Ingrese una marca: ('Salir para finalizar')").title()

        if marca_a_buscar == "Salir":
            break

        lista_marca_coincidencia = filtrar_lista_lambda(
            lista_copia, lambda insumo: insumo if buscar_coincidencia_string(marca_a_buscar, insumo['Marca']) else None)
        os.system("cls")
        if lista_marca_coincidencia:
            acumulador_subtotal = 0.0
            print("Lista de productos de esa marca:\n")
            pet_listar_insumos(lista_marca_coincidencia)
            while (True):
                producto = input(
                    "Ingrese nombre del producto: ('Salir para finalizar')").title()
                if producto == "Salir":
                    print(
                        f"La cantidad total de su compra es : ${acumulador_subtotal:.2f}")
                    break

                lista_nombre_coincidencia = filtrar_lista_lambda(
                    lista_marca_coincidencia, lambda insumo: insumo if buscar_coincidencia_string(producto, insumo['Nombre']) else None)

                pet_listar_insumos(lista_nombre_coincidencia)
                if (len(lista_nombre_coincidencia) > 1):

                    producto_caracteristica = input(
                        "Hay más de un producto con ese nombre. Especique su caracteristica: ")
                    for producto in lista_nombre_coincidencia:
                        if buscar_coincidencia_string(producto_caracteristica, producto["Caracteristicas"]):                            
                            cantidad = int(
                                input("Ingrese cuantas unidades quiere: "))
                            factura.append (f"Nombre del producto: {producto['Nombre']}")
                            factura.append (f"{cantidad}u  x  ${lista_nombre_coincidencia[0]['Precio']:.2f}              ${acumulador_subtotal}")
                            acumulador_subtotal += cantidad * \
                                producto["Precio"]                   

                elif (len(lista_nombre_coincidencia) == 1):
                    cantidad = int(input("Ingrese cuantas unidades quiere: "))
                    acumulador_subtotal += cantidad * \
                        lista_nombre_coincidencia[0]["Precio"]
                    factura.append (f"Nombre del producto: {lista_nombre_coincidencia[0]['Nombre']}")
                    factura.append (f"{cantidad}u  x  ${lista_nombre_coincidencia[0]['Precio']:.2f}              ${acumulador_subtotal}")                    

                print("Subtotal :$", acumulador_subtotal)


                acumulador_total += acumulador_subtotal
        else:
            print("No se encontró la marca")
    print("Total :$", acumulador_total)
    factura.append (f"Total :                   ${acumulador_total:.2f}") 

    return factura

def crear_txt(lista:list) -> None:

    archivo = open("factura.txt", "w")
    with open("factura.txt", "w") as archivo:
        for linea in lista:
            archivo.write(linea + "\n")

    print("Factura guardada en factura.txt")


# ---------------------------Punto 7------------------------------------
def filtrar_lista_lambda(lista: list, condicion) -> list:
    lista_filtrada = list(filter(condicion, lista))

    return lista_filtrada


def pet_alimento_json(lista: list, nombre_archivo_json: str) -> None:
    # Filtré la lista
    lista_alimentos = filtrar_lista_lambda(
        lista, lambda insumo: insumo if buscar_coincidencia_string("Alimento", insumo['Nombre']) else None)

    convertir_lista_pretty_a_json(
        lista_alimentos, f"{nombre_archivo_json}.json")
    print(f"Se cargó el archivo '{nombre_archivo_json}' a un .json")


def convertir_lista_pretty_a_json(lista: list, path: str) -> None:

    with open(path, 'w', encoding='utf-8') as file:
        json.dump(lista, file, ensure_ascii=False, indent=2)


def pet_cargar_lista_desde_json(ruta_archivo: str) -> list:
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        contenido = file.read()
        lista = json.loads(contenido)

    return lista


def aplicar_aumento(lista: list) -> list:
    lista_copia = lista.copy()
    for insumo in lista_copia:
        insumo["Precio"] += insumo["Precio"] * 0.84

    return lista_copia


def pet_normalizar_datos(lista: list) -> list:

    for insumo in lista:
        insumo["ID"] = int(insumo["ID"])
        insumo["Nombre"] = insumo["Nombre"].title()
        insumo["Marca"] = insumo["Marca"].title()
        insumo["Precio"] = float(insumo["Precio"].replace("$", ""))
        insumo["Caracteristicas"] = insumo["Caracteristicas"].title()


def guardar_lista_csv(lista, nombre_archivo):
    # Obtenemos los nombres de las columnas del primer diccionario
    columnas = lista[0].keys()

    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=columnas)

        # Escribimos los nombres de las columnas en la primera fila
        writer.writeheader()

        # Escribimos cada diccionario como una fila en el archivo CSV
        for item in lista:
            writer.writerow(item)

def cargar_lista_desde_txt(path:str)->list:

    with open(path, 'r') as file:
        contenido = file.read()
        lista = contenido.split('\n')
    return lista

def mostrar_lista_fila (lista:list,title:str)->None:

    print (f"\n-------------------{title}-------------------\n")

    for insumo in lista:
        print (insumo)

def validar_marca (lista_marcas:list)->str:
    flag_encontro = False

    lista_marcas_coincidencias = []
    while True:
        mostrar_lista_fila (lista_marcas,"Marcas disponibles:")

        marca = input("Ingrese marca que desea agregar ('Salir' para cancelar): ").title()
        if (marca) == "Salir":
            return ""

        for insumo in lista_marcas:
            if insumo == marca:
                flag_encontro = True
                break

        if flag_encontro:
            if(input(f"Presiona 's' para confirmar la marca: ({insumo})\n").lower() == "s"):
                return insumo
            else:
                print("Se cancelo la acción.")
        else:
            print("La marca ingresada no está disponible")

def validar_producto (lista_marcas)->list:
    marca_validada = validar_marca(lista_marcas)
    especificaciones = []
    if marca_validada:
        especificaciones.append (marca_validada)
        nombre = input ("Ingrese nombre del producto: ").title()
        especificaciones.append(nombre)
        
        while True:
            try:
                precio = float(input("Ingrese precio del producto: "))
                especificaciones.append(precio)
                break
            except ValueError:
                print ("Eso no es un numero")

        contador = 3
        while (contador>1):
            contador -= 1
            
            if (contador == 2):
                caracteristicas = input("Ingrese caracteristicas del producto: ").title()
                if caracteristicas:
                    especificaciones.append(caracteristicas)
                    respuesta = input("Presione 's' para agregar otra caracteristica.").lower()
                else:
                    print ("Debe ingresar al menos una caracteristica")
                if (respuesta != "s" or respuesta == " "):
                    break                    
            else :
                caracteristicas = input("Ingrese caracteristicas del producto: ").title()
                if caracteristicas:
                    especificaciones.insert(-1, caracteristicas)
                    respuesta = input("Presione 's' para agregar otra caracteristica.").lower()                
                else:
                    break        
            if (respuesta != "s" or respuesta == ""):
                break
       
    return especificaciones
    
def buscar_ultima_id (lista:list)->int:
    return lista[-1]["ID"]

def crear_insumo_dict (marca:str,nombre:str,precio:float,caracteristicas:str,lista_id:list)->dict:
    
    insumo_dict ={
            "ID": buscar_ultima_id(lista_id)+1,
            "Nombre": nombre,
            "Marca": marca,
            "Precio": precio,
            "Caracteristicas": caracteristicas,
        }
    
    return insumo_dict

def pet_agregar_insumo_a_lista (lista_marcas:list,lista:list)->None:
    especificaciones_del_producto = validar_producto(lista_marcas)
    if especificaciones_del_producto:
        lista.append(crear_insumo_dict(especificaciones_del_producto[0],especificaciones_del_producto[1],especificaciones_del_producto[2],especificaciones_del_producto[3],lista))
    



# -----------------------------------------------------------------------
lista = pet_parser_csv()
print("--------------------LISTA NORMALIZADA--------------------")

pet_normalizar_datos(lista)
# pet_listar_insumos(lista)

# pet_alimento_json(lista,"Alimento")
# lista_cargada = pet_cargar_lista_desde_json("Alimento.json")

# pet_listar_insumos(lista_cargada)

# lista_aumento = aplicar_aumento(lista)

# guardar_lista_csv(lista_aumento,"insumos_aumento.csv")

lista_marcas = (cargar_lista_desde_txt ("marcas.txt"))



pet_listar_insumos(lista)