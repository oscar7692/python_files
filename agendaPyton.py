def menu():

    print('******Directorio de Contactos******')

    print('1- Crear nombre de la lista')

    print('2- Agregar Contacto')

    print('3- Buscar en directorio')

    print('4- Editar contactos')

    print('5- Mostrar contactos')

    print('6- Cerrar directorio')

    print()

def menu2():

    print('a- Buscar por nombre')

    print('b- Buscar por telefono')

    print('c- Buscar por direccion')

def menu3():

    print("Editar lista")

    print('1.- Eliminar un contacto')

    print('2.- Editar un contacto')


directorio = []

telefonos = {}

nombres = {}

direcciones = {}

apodos = {}

opcionmenu = 0

menu()

x=0

while opcionmenu != 6:

    opcionmenu = int(input("Inserta un numero para elegir una opcion: "))

    if opcionmenu == 1:

        print('Ingrese el nombre de la lista:')

        nombre_de_lista=input()

        menu()


    elif opcionmenu == 2:

        print("Agregar Nombre, telefono, direccion y apodo")

        nombre = input("Nombre: ")

        telefono = input("Telefono: ")

        direccion = input("Direccion: ")

        apodo = input("Apodo: ")

        telefonos[nombre] = telefono

        nombres[telefono] = nombre

        direcciones[direccion] = nombre

        directorio.append([nombre, telefono, direccion, apodo])

        menu()

    elif opcionmenu == 3:

        print("Busqueda")

        menu2()

        opcionmenu2 = input("Inserta una letra para elegir una opcion: ")

        if opcionmenu2=="a":

            nombre = input("Nombre: ")

            if nombre in telefonos:

                print("El telefono es", telefonos[nombre])

            else:

                print(nombre, "no se encuentra")


        if opcionmenu2=="b":

            telefono = input("Telefono: ")

            if telefono in nombres:

                print("El Nombre es", nombres[telefono])

            else:

                print(telefono, "no se encuentra")


        if opcionmenu2=="c":

            direccion = input("direccion: ")

            for linea in direcciones:

                linea = linea.rstrip()

                if not linea.startswith(direccion) : continue

                palabras = linea.split()

                print()

            else:

                print(direccion, "no se encuentra")

        menu()

    elif opcionmenu == 4:

        menu3()

        opcionmenu3 = input("Inserta un numero para elegir una opcion: ")

        if opcionmenu3=="1":

            nombre = input("Nombre: ")

            if nombre in directorio[0:10]:

                print('borrado')

            else:

                print(nombre, "no encontrado")

        else:

            menu()

        menu()

    elif opcionmenu == 5:



        print("\nNombre de la lista: ",nombre_de_lista)

        for e in directorio:

            print("\nLa lista es: ",directorio)

        menu()

    elif opcionmenu != 6:

        menu()
