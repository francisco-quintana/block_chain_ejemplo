#import del hash
from hashlib import sha256
#import de utilidades
from datetime import datetime
import time
import os

#función para hashear un mensaje
def hashear(message):
	#se convierte a binarios el mensaje que se llama
	message = message.encode()
	#se crean variables para el ciclo
	hs=""
	nonce=0
	#el ciclo no acaba hasta que el hash empiece con dos ceros
	while not hs.startswith('00'):
		#se agrega uno al nonce
		nonce=nonce+1
		#se convierte a string debido a que los ints no tiene el metodo encode
		nonce2=str(nonce)
		#se convierte a binarios
		nonce2=nonce2.encode()
		#se agrega el nonce al principio del mensaje y se hashea
		hs=sha256(nonce2+message).hexdigest()
	#nos devuelve el hash y el nonce
	return [hs,nonce]

def hashearnonce(message,nonce):
	#se convierte a binarios el mensaje que se llama
	message = message.encode()
	#se convierte a string debido a que los ints no tiene el metodo encode
	nonce2=str(nonce)
	#se convierte a binarios
	nonce2=nonce2.encode()
	#se agrega el nonce introducido al principio del mensaje y se hashea
	hs=sha256(nonce2+message).hexdigest()
	#nos devuelve el hash y el nonce
	return [hs,nonce]

def add(msg):
	#si el archivo existe se saltea este paso y si no crea el archivo vacio
	if not os.path.isfile("blockchain.txt"):
		f = open("blockchain.txt", "x")
		f.close()
	#si el txt no tiene nada o es el bloque genesis que se esta creando se ejecuta lo siguiente
	if os.stat("blockchain.txt").st_size==0:
		#se abre el archivo
		with open("blockchain.txt","a") as f:
			#se obtiene la hora actual
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			arr=[]
			#se asigna el indice cero ya que sabemos que es el bloque genesis
			indice=0
			#se agrega el indice y el tiempo
			arr.append(indice)
			arr.append(current_time)
		#se llama la funcion que nos devuelve el hash y se agregan los valores que nos arroja
			arr2=hashear(msg)
			arr.append(arr2[0])
			arr.append(arr2[1])
		#se agrega el mensaje del usuario
			arr.append(msg)
		#se llena en una sola linea el arreglo dividido por espacios
			for i in arr:
				f.write("%s " % i)
		#se hace un enter para el siguiente bloque
			f.write("\n")
			f.close()
	#si no es el bloque genesis
	else:
		#se abre el archivo
		with open("blockchain.txt","r+") as f:			
			lines=[]
		#se lee el archivo y separa cada linea en un arreglo y cada "palabra" en un campo del arreglo
			lines = [(line.strip()).split() for line in f]
		#se obtiene el tiempo actual
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			arr=[]
		#el indice es la longitud del arreglo actual
			indice=len(lines)
		#se busca el hash anterior;el ultimo bloque actual
			a_hash=lines[indice-1][2]
			#se agregan los campos
			arr.append(indice)
			arr.append(current_time)
		#se llama la funcion que nos devuelve el hash con el mensaje mas el hash anterior
		#y se agregan los valores que nos arroja
			arr2=hashear(a_hash+msg)
			arr.append(arr2[0])
			arr.append(arr2[1])
			#se guarda en este bloque el hash anterior
			arr.append(a_hash)
			arr.append(msg)
		#se anexa el bloque en el archivo llamado blockchain.txt separado por espacios
			for i in arr:
				f.write("%s " % i)
			f.write("\n")
			f.close()
		#mensaje bonito
	return "Se va a agregar "+msg


#el edit requiere que el usuario sepa el nonce y lo ingrese
def edit(msg,nonce):
	chain=[]
	#se guarda en el arreglo vacio toda la cadena
	with open("blockchain.txt") as f:
		chain = [(line.strip()).split() for line in f]
	#se obtiene la hora actual
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	#se obtiene el indice del ultimo bloque
	indice=len(chain)
	indice=indice-1
	#se sobrescribe la hora del mensaje
	chain[indice][1]=current_time
	#si el bloque que estamos editando es el genesis esta en la posicion 4 ya no tiene hash anterior
	if(len(chain)==1):
		arr=hashearnonce(msg,nonce)
		chain[indice][2]=arr[0]
		chain[indice][3]=arr[1]
		chain[indice][4]=msg
	else:
		a_hash=chain[indice-1][2]
		#se llama al metodo que nos pide darle el nonce y se sobreescribe el hash y el nonce del ultimo bloque
		arr=hashearnonce(a_hash+msg,nonce)
		chain[indice][2]=arr[0]
		chain[indice][3]=arr[1]
	#si el bloque es cualquier otro se sobrescribe en la posicion 5
		chain[indice][5]=msg
	#se sobrescribe todo el archivo con la cadena de este metodo y con el ultimo bloque cambiado
	file_out = open("blockchain.txt", "w")
	for block in chain:
		for i in block:
		    file_out.write("%s " % i)
		file_out.write("\n")
	file_out.close()
	return "Se va a cambiar "+msg

#funcion para checar dos archivos
def check(text):
	#se crea el mensaje correcto y dos listas una para el archivo local y otro para la copia
	message="no hubo errores"
	lineList=[]
	lineList2=[]
	#se separan en arreglos las lineas del archivo
	with open("blockchain.txt") as f:
		lineList = [(line.strip()).split() for line in f]
	with open(text+".txt") as f:
		lineList2 = [(line.strip()).split() for line in f]
	#contador para que las dos listas vayan juntas
	i=0
	#for que itera cada bloque
	for line in lineList:
		#se obtiene el hash actual
		hs=line[2]
		#si el hash es igual que el de la copia continua si no se rompe el for y obtenemos un mensaje de error
		if(hs==lineList2[i][2]):
			#si es el ultimo bloque que no busque un hash anterior en el siguiente bloque
			if (line[0]==str(len(lineList)-1)):
				#si el hash no empieza con cero obtenemos un mensaje de error y de igual forma se quiebra el for ya que es el ultimo bloque
				if not hs.startswith('00'):
					message="error en la cadena. hash no empieza con cero en el indice "+line[0]
					break
				else:
					break
			#si es cualquier otro bloque que no sea el ultimo
			else:
				#si el hash anterior del siguiente bloque no es igual al hash actual nos manda mensaje de error
				if(hs!=lineList[i+1][4]):
					message="error en la cadena. mal enlazamiento de bloques en los indices "+line[0]+" y "+lineList[i][0]
					break
				#si el hash no empieza con dos ceros nos manda mensaje de error
				elif not hs.startswith('00'):
					message="error en la cadena. hash no empieza con cero en el indice "+line[0]
					break
				#si no se encuentra ningun error en la iteración actual se continua
				else:
					i=i+1
		else:
			message="error en la cadena. los hash no concuerdan con el indice "+line[0]
			break
	
	return message

#imprimir los contenidos del archivo
def see():
	chain=[]
	with open("blockchain.txt") as f:
		chain = [(line.strip()).split() for line in f]
	
	for sblock in chain:
		#si es el bloque es el genesis se imprime un dato menos ya que no tiene hash anterior
		if (sblock[0]=="0"):
			print("indice: "+str(sblock[0]))
			print("hora: "+sblock[1])
			print("hash: "+sblock[2])
			print("nonce: "+str(sblock[3]))
			print("mensaje: "+sblock[4])
			print("")
		#si no es el bloque genesis se imprimen todos los datos
		else:
			print("indice: "+str(sblock[0]))
			print("hora: "+sblock[1])
			print("hash: "+sblock[2])
			print("nonce: "+str(sblock[3]))
			print("hash anterior: "+sblock[4])
			print("mensaje: "+sblock[5])
			print("")



def main(op):
	#si escogio uno se ejecuta la funcion add
	if op == 1:
		msg = input('Introduce un mensaje para codificar: ')
		print(add(msg))
		time.sleep(2)
	#si escogio dos se ejecuta la funcion editar
	elif op==2:
		msg= input('Introduce el nuevo mensaje: ')
		nonce=input('Introduce el nonce: ')
		print(edit(msg,nonce))
		time.sleep(2)
	#si escogio tres se ejecuta la funcion de chequeo
	elif op==3:
		txt= input('Cual es el nombre de tu copia? ')
		print(check(txt))
		time.sleep(2)
	#si escogio tres se ejecuta la funcion de ver
	elif op==4:
		see()
		time.sleep(2)
	else:
		print('ERROR')
		time.sleep(2)
		

if __name__ == '__main__':
	while(True):
		op = int(input("""
	Selecciona una opción:

	[1] Crear mensaje
	[2] Editar
	[3] Checar
	[4] Ver mensaje
	[5] Salir
	"""))

		if(op==5):
			print("Bye")
			break
		else:
			#manda a llamar al metodo main pasandole la opcion escogida "op"
			main(op)
