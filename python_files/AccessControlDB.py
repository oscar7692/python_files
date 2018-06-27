#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import pymysql
import time

class project():
	def __init__(self):
		try:
			self.conn = pymysql.connect(user='root', password='Bonsai#7692', host='127.0.0.1', database='AccessControlDB')
			self.dbac = self.conn.cursor()
		except Exception as e:
			print(e)		

	def main(self):
		ans = True
		opc = True

		while ans:

			print("""
		    selecione la opcion que desea usar '1..5', escriba exit o precione '6' para salir del sistema.\n\n\a
		    1-\t consultar residentes
		    2-\t consultar visitantes
		    3-\t consultar guardias
		    4-\t consultar puertas
		    5-\t consultar actividad
		    6-\t salir/exit \n\n""")

			ans = str(input())

			if ans == "1":
				os.system('clear')
				while opc:
					print("""
		            \n\t Seccion de residentes\n\tingrese la opcion que desea '1..4'\n\n
		            1-\t agregar registro
		            2-\t borrar registro
		            3-\t consultar regitros
		            4-\t salir al menu anterior""")

					opc = str(input())
					if opc == "1":
						print("\n\testa es la estructura de los campos de la tabla:")
						self.dbac.execute("SHOW TABLES")
						print(self.dbac.fetchall())
						print("\n\n\tingrese los datos que desea agregar:\n\t\t")
						nombreR = raw_input('ingrese nombre :')
						correoR = raw_input('ingrese correo :')
						fotoR = True
						estatusR = True
						sql = "INSERT INTO residente(nombre,correo,foto,estatus_act,placas) VALUES('%s','%s','%s',%d,'JCIL')"%(nombreR,correoR,fotoR,estatusR)
						self.dbac.execute(sql)
						print("Se han insertado los registros correctamente!")
						self.conn.commit()
						time.sleep(2.5)
						os.system('clear')

		            elif opc == "2":
		                pass

		            elif opc == "3":
		                os.system('clear')
		                print("\n\teste es el contenido de residentes:\n\n")
		                self.dbac.execute("select * from residente")
		                print(self.dbac.fetchall())
		                time.sleep(2.5)
		                os.system('clear')

		            elif opc == "4":
		                print("\n\tregresando al menu anterior presione enter para continuar...")
		                time.sleep(2.5)
		                os.system('clear')
		                break
		            else:
		                print("ingrese una opcion valida, presione enter para continuar...")
		                time.sleep(2.5)
		                os.system('clear')

		    elif ans == "2":

		        os.system('clear')

		        while opc:

		            print("""
		            \n\t Seccion de visitantes\n\tingrese la opcion que desea '1..4'\n\n
		            1-\t agregar registro
		            2-\t borrar registro
		            3-\t consultar regitros
		            4-\t salir al menu anterior""")

		            opc = str(input())

		            if opc == "1":
		                pass
		            elif opc == "2":
		                pass
		            elif opc == "3":
		                pass
		            elif opc == "4":
		                print("\n\tregresando al menu anterior presione enter para continuar...")
		                time.sleep(2.5)
		                os.system('clear')
		                break
		            else:
		                print("ingrese una opcion valida, presione enter para continuar...")
		                time.sleep(2.5)
		                os.system('clear')

		    elif ans == "3":

		        os.system('clear')

		        while opc:

		            print("""
		            \n\t Seccion de guardias\n\tingrese la opcion que desea '1..4'\n\n
		            1-\t agregar registro
		            2-\t borrar registro
		            3-\t consultar regitros
		            4-\t salir al menu anterior""")

		            opc = str(input())

		            if opc == "1":
		                pass
		            elif opc == "2":
		                pass
		            elif opc == "3":
		                pass
		            elif opc == "4":
		                print("\n\tregresando al menu anterior presione enter para continuar...")
		                time.sleep(2.5)
		                os.system('clear')
		                break
		            else:
		                print("ingrese una opcion valida, presione enter para continuar...")
		                time.sleep(2.5)
		                os.system('clear')

		    elif ans == "4":

		        os.system('clear')

		        while opc:

		            print("""
		            \n\t Seccion de puertas\n\tingrese la opcion que desea '1..4'\n\n
		            1-\t agregar registro
		            2-\t borrar registro
		            3-\t consultar regitros
		            4-\t salir al menu anterior""")

		            opc = str(input())

		            if opc == "1":
		                pass
		            elif opc == "2":
		                pass
		            elif opc == "3":
		                pass
		            elif opc == "4":
		                print("\n\tregresando al menu anterior presione enter para continuar...")
		                time.sleep(2.5)
		                os.system('clear')
		                break
		            else:
		                print("ingrese una opcion valida, presione enter para continuar...")
		                time.sleep(2.5)
		                os.system('clear')

		    elif ans == "5":

		        os.system('clear')

		        while opc:

		            print("""
		            \n\t Seccion de actividades\n\tingrese la opcion que desea '1..4'\n\n
		            1-\t agregar registro
		            2-\t borrar registro
		            3-\t consultar regitros
		            4-\t salir al menu anterior""")

		            opc = str(input())

		            if opc == "1":
		                pass
		            elif opc == "2":
		                pass
		            elif opc == "3":
		                pass
		            elif opc == "4":
		                print("\n\tregresando al menu anterior presione enter para continuar...")
		                time.sleep(2.5)
		                os.system('clear')
		                break
		            else:
		                print("ingrese una opcion valida, presione enter para continuar...")
		                time.sleep(2.5)
		                os.system('clear')

		    elif ans == "6" or "exit":

		        print("\n\thasta luego, presione enter para salir...")
		        time.sleep(2.5)
		        os.system('clear')
		        raise SystemExit

		    else:
		        print("\a\nIngrese una opcion valida porfavor, presione enter para continuar...")
		        time.sleep(2.5)
				

init = project()
init.main()