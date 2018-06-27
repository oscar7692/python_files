import sys

def main():
 #leo la longitud de n (para que calcule de cualquiera)
 print "teclea la longitud del tablero"
 n = int(sys.stdin.readline())

 nr = n #nr son las reinas pero estas son las que ire metiendo a la matriz


 #inicializo la matriz
 mat = []
 for i in range(n):
     mat.append([])
     for j in range(n):
         mat[i].append(0)

 play(n, mat, nr) #este metodo ejecuta el algoritmo


#algoritmo de busqueda en profundidad para la solucion del
#problema de las N-Reinas con Fuerza Bruta
def play(n, m, nr):
 pila = []
 nr -= 1 #retrocedo una porque se supone que voy a poner siempre
 # la primer reina en la primer posicion
 solFound = False
 pila.append((0, 0)) #le meto la primer posicion de siempre
 # para fines de cumplir con la condicion de abajo
 # porque que python.. no tiene do while!
 soluciones = 0
 running = False
 while len(pila)>0: #mientras tenga elementos (posiciones) que visitar
     ij = pila.pop()
     m[ij[0]][ij[1]] = 0
     nr += 1
 #retiro la reina que habia puesto.. esto es para que cuando regrese
 # a algun punto de la pila regrese la reina que haya puesto

 i = ij[0] #inicializo i en el punto que este en la pila
 # meto un arreglo coordenado en la pila (i, j)

 sizee = len(pila)

 if(sizee > 0 or (sizee== 0 and running)):
     j = ij[1] + 1
 else:
     j = 0
     running = True #para decirle que ya entro a la rama (a la que sea)

 that = True #este es para que j se quede o no en la posicion tomada


 while(i < n):
     if not(that): #si es la posicion que habia sacado de la pila
         j = 0 # o si es el recorrido en la matriz, si es lo segundo lo hago 0
 else: #si no, lo dejo en la misma posicion que estaba pero le digo que
     that = False #la siguiente sera parte del recorrido (para que regrese a 0)
 while (j < n):

     if(m[i][j]==0 and nr > 0): #si quedan reinas y entre alguna
         if(canMove(m, i, j, n)): #mientras no se ataquen
             pila.append((i, j)) #meto la posicion actual a la pila
             m[i][j] = nr #le paso la reina correspondiente
             if(nr == 1): #si estoy poniendo la ultima reina
 #::::::::: significa que ya no tengo
 # mas reinas pendientes
                 soluciones += 1 #cuento una solucion mas
                 print "********************************"
                 print "Solucion numero", str(soluciones)
                 print(m, n) #imprimo la solucion
                 nr -= 1 #le quito la reina que le puse

                 solFound = True #para indicarle que ya no siga buscando
                 break
 nr -= 1
 j += 1
 if(solFound): #si le dije que no busque
     solFound = False #que rompa y se vaya con la ultima     #posicion pendiente (ir a la parte superior del ciclo)     #ya que no tiene sentido buscar si ya tengo las n-reinas
break
    i += 1
    print "se encontraron un total de:", str(soluciones), "soluciones"



#le indico si puede colocar la reina en la posicion i, j
# dependiendo si se atacan o no
def canMove(m, i, j, n):
 return (checkDiagonal1(m, i, j, n) and checkDiagonal2(m, i, j, n) and checkVertical(m, j, n) and checkOrizontal(m, i, n))


#imprimir la matriz
def printM(t, n):
 for i in range(n):
     print t[i]


#toda esta seccion es para checar que pedo con las diagonales y eso
def checkDiagonal1(t, i, j, n): #checar una de las diagonales (1)
 a = i - 1
 b = j - 1
 while (a >= 0 and b >= 0):
     if(t[a][b] != 0):
         return False
     a -= 1
     b -= 1
     a = i + 1
     b = j + 1
 while (a < n and b < n):
     if(t[a][b] != 0):
         return False
         a += 1
         b += 1
 return True

def checkDiagonal2(t, i, j, n): #checar una de las diagonales (2)
 a = i - 1
 b = j + 1
 while (a >= 0 and b < n):
     if(t[a][b] != 0):
         return False
         a -= 1
         b += 1
         a = i + 1
         b = j - 1
 while (a < n and b >= 0):
     if(t[a][b] != 0):
         return False
         a += 1
         b -= 1
return True


def checkVertical(t, j, n): # linea vertical
 a = 0
 while a < n:
     if(t[a][j] != 0):
         return False
 a += 1
 return True

def checkOrizontal(t, i, n): # linea orizontal
 b = n - 1
 while b >= 0:
     if(t[i][b] != 0):
         return False
 b -= 1
 return True



main() #mando a ejecutar el programa completo