#!/usr/bin/python3

import mysql.connector, os

try:
    conn = mysql.connector.connect(user='root', password='Bonsai#7692', host='localhost', database='AccessControlDB')
    cursor = conn.cursor()
except Exception as error:
    print(error)

cursor.execute("show tables")
print(cursor.fetchall())

class DBaccessResidentes:

    # def __init__(self, nombreR, correoR, fotoR, estatusR):
    #     self.nombreR = nombreR
    #     self.correoR = correoR
    #     self.fotoR = True
    #     self.estatusR = True

    def agregar(self):

        print("\n\testa es la estructura de los campos de la tabla:", cursor.execute("describe residente"))
        print(cursor.fetchall())
        print("\n\n\tingrese los datos que desea agregar:\n\t\t")
        nombreR = str(input())
        print("ingrese correo :\t\t")
        correoR = str(input())
        fotoR = True
        estatusR = True
        cursor.execute("insert into residente values(", nombreR, ",", correoR, ",", fotoR, ",",  estatusR, ")")
        cursor.fetchall()
        cursor.execute("commit")
        print("se han insertado los registros correctamente, presione enter para continuar...")
        input()
        os.system('clear')

    def borrar(self):
        pass

    def consultar(self):
        print("\n\teste es el contenido de residentes:\n\n")

        pass

residentes = DBaccessResidentes
# visitantes = DBaccess
# guardias = DBaccess
# puertas = DBaccess
# actividades = DBaccess


cursor.execute("show tables")

print(cursor.fetchall())

cursor.execute("describe puerta")

print(cursor.fetchall())