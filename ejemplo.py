from hashlib import sha256
from datetime import datetime
import time
import os

def hashear(message):
	#se decodifica el mensaje creado
	message = message.encode()
	#se convierte a hexadecimal y se hashea
	hs=""
	nonce=0
	while not hs.startswith('00'):
		nonce=nonce+1
		nonce2=str(nonce)
		nonce2=nonce2.encode()
		hs=sha256(nonce2+message).hexdigest()
	return [hs,nonce]

def hashearnonce(message,nonce):
	#se decodifica el mensaje creado
	message = message.encode()
	#se convierte a hexadecimal y se hashea
	nonce2=str(nonce)
	nonce2=nonce2.encode()
	hs=sha256(nonce2+message).hexdigest()
	return [hs,nonce]

def add(msg):
	#si el archivo existe no se hace nada pero si no se crea
	if not os.path.isfile("blockchain.txt"):
		f = open("blockchain.txt", "x")
		f.close()
	#si el txt no tiene nada o es el bloque genesis se ejecuta lo siguiente
	if os.stat("blockchain.txt").st_size==0:
		with open("blockchain.txt","a") as f:
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			arr=[]
			indice=0
			arr.append(indice)
			arr.append(current_time)
		#se llama la funcion que nos devuelve el hash
			arr2=hashear(msg)
			arr.append(arr2[0])
			arr.append(arr2[1])
		#si no es bloque genesis se agrega el hash anterior
			arr.append(msg)
		#se crea el archivo con el bloque genesis
			for i in arr:
				f.write("%s " % i)
			f.write("\n")
			f.close()
	else:
		with open("blockchain.txt","r+") as f:
			lines=[]
			lines = [(line.strip()).split() for line in f]
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			arr=[]
			indice=len(lines)
			arr.append(indice)
			arr.append(current_time)
		#se llama la funcion que nos devuelve el hash
			arr2=hashear(msg)
			arr.append(arr2[0])
			arr.append(arr2[1])
		#si no es bloque genesis se agrega el hash anterior
			a_hash=lines[indice-1][2]
			arr.append(a_hash)
			arr.append(msg)
		#se anexa el bloque en el archivo llamado blockchain.txt
			for i in arr:
				f.write("%s " % i)
			f.write("\n")
			f.close()
		#mensaje bonito
	return "Se va a agregar "+msg



def edit(msg,nonce):
	chain=[]
	with open("blockchain.txt") as f:
		chain = [(line.strip()).split() for line in f]
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	arr=[]
	indice=len(chain)
	indice=indice-1
	chain[indice][1]=current_time
	arr2=hashearnonce(msg,nonce)
	chain[indice][2]=arr2[0]
	chain[indice][3]=arr2[1]
	if(len(chain)==1):
		chain[indice][4]=msg
	else:
		chain[indice][5]=msg
		a_hash=chain[indice-1][2]

	file_out = open("blockchain.txt", "w")
	for block in chain:
		for i in block:
		    file_out.write("%s " % i)
		file_out.write("\n")
	file_out.close()
	return "Se va a cambiar "+msg

def check(text):
	message="no hubo errores"
	lineList=[]
	lineList2=[]
	with open("blockchain.txt") as f:
		lineList = [(line.strip()).split() for line in f]
	with open(text+".txt") as f:
		lineList2 = [(line.strip()).split() for line in f]
	i=0
	for line in lineList:
		hs=line[2]
		if(hs==lineList2[i][2]):
			if (line[0]==str(len(lineList)-1)):
				if not hs.startswith('00'):
					message="error en la cadena. hash no empieza con cero en el indice "+line[0]
					break
				else:
					break
			else:
				if(hs!=lineList[i+1][4] and not hs.startswith('00')):
					message="error en la cadena. mal enlazamiento de bloques en los indices "+line[0]+" y "+lineList[i][0] 
					break
				else:
					i=i+1
		else:
			message="error en la cadena. los hash no concuerdan con el indice "+line[0]
			break
	
	return message

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
	[2] Editar con Fallo
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
