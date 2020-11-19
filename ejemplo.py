from hashlib import sha256
import time

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

def add(msg,chain):
	#si es el bloque genesis se agregan todos los campos excepto el hash anterior
		arr=[]
		indice=len(chain)
		arr.append(indice)
		arr.append(time.asctime())
		#se llama la funcion que nos devuelve el hash
		arr2=hashear(msg)
		arr.append(arr2[0])
		arr.append(arr2[1])
		#si no es bloque genesis se agrega el hash anterior
		if chain:
			a_hash=chain[indice-1][2]
			arr.append(a_hash)
		arr.append(msg)
		#se agrega el bloque a la cadena
		chain.append(arr)
		#mensaje bonito
		return "Se va a agregar "+msg



def edit(msg,chain,nonce):
	arr=[]
	indice=len(chain)
	indice=indice-1
	a_hash=chain[indice-1][2]
	chain[indice][1]=time.asctime()
	arr2=hashearnonce(msg,nonce)
	chain[indice][2]=arr2[0]
	chain[indice][3]=arr2[1]
	if(len(chain)==1):
		chain[indice][4]=msg
	else:
		chain[indice][5]=msg
	
	return "Se va a cambiar "+msg

def check(chain):
	
	return "Se va a checar"


def see(chain):
	for sblock in chain:
		#si es el bloque es el genesis se imprime un dato menos ya que no tiene hash anterior
		if (sblock[0]==0):
			print("indice: "+str(sblock[0]))
			print("fecha y hora: "+sblock[1])
			print("hash: "+sblock[2])
			print("nonce: "+str(sblock[3]))
			print("mensaje: "+sblock[4])
			print("")
		#si no es el bloque genesis se imprimen todos los datos
		else:
			print("indice: "+str(sblock[0]))
			print("fecha y hora: "+sblock[1])
			print("hash: "+sblock[2])
			print("nonce: "+str(sblock[3]))
			print("hash anterior: "+sblock[4])
			print("mensaje: "+sblock[5])
			print("")



def main(op,block):
	#si escogio uno se ejecuta la funcion add
	if op == 1:
		msg = input('Introduce un mensaje para codificar: ')
		print(add(msg,block))
		time.sleep(2)
	#si escogio dos se ejecuta la funcion editar
	elif op==2:
		msg= input('Introduce el nuevo mensaje: ')
		nonce=input('Introduce el nonce: ')
		print(edit(msg,block,nonce))
		time.sleep(2)
	elif op==3:
		check(block)
		time.sleep(2)
	#si escogio tres se ejecuta la funcion de ver
	elif op==4:
		see(block)
		time.sleep(2)
	else:
		print('ERROR')
		time.sleep(2)
		

if __name__ == '__main__':
	blockchain=[]
	while(True):
		op = int(input("""
	Select an option:

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
			main(op,blockchain)
			#se crea un archivo donde se guardan los datos
			file_out = open("blockchain.bin", "w")
			for block in blockchain:
				for i in block:
		        		file_out.write("%s\n" % i)
			file_out.close()
