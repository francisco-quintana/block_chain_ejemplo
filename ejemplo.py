from hashlib import sha256
import time

def hashear(message):
	#se decodifica el mensaje creado
	message = message.encode()
	#se convierte a hexadecimal y se hashea
	hs=sha256(message).hexdigest()
	return hs

def add(msg,chain):
	#si es el bloque genesis se agregan todos los campos excepto el hash anterior
	if not chain:
		arr=[]
		arr.append(0)
		arr.append(time.asctime())
		arr.append(hashear(msg))
		arr.append(msg)
		#se agrega el bloque a la cadena
		chain.append(arr)
	#si no es bloque genesis se agregan todos los campos
	else:
		arr=[]
		indice=len(chain)
		a_hash=chain[indice-1][2]
		arr.append(indice)
		arr.append(time.asctime())
		arr.append(hashear(msg+a_hash))
		arr.append(a_hash)
		arr.append(msg)
		#se agrega el bloque a la cadena
		chain.append(arr)
	
	#mensaje bonito
	return "Se va a agregar "+msg



def edit(msg,chain):
	
	return "Se va a cambiar "+msg


def see(chain):
	for sblock in chain:
		#si es el bloque es el genesis se imprime un dato menos ya que no tiene hash anterior
		if (sblock[0]==0):
			print("indice: "+str(sblock[0]))
			print("fecha y hora: "+sblock[1])
			print("hash: "+sblock[2])
			print("mensaje: "+sblock[3])
			print("")
		#si no es el bloque genesis se imprimen todos los datos
		else:
			print("indice: "+str(sblock[0]))
			print("fecha y hora: "+sblock[1])
			print("hash: "+sblock[2])
			print("hash anterior: "+sblock[3])
			print("mensaje: "+sblock[4])
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
		print(edit(msg,block))
		time.sleep(2)
	#si escogio tres se ejecuta la funcion de ver
	elif op==3:
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
	[2] Verificar
	[3] Ver mensaje
	[4] Salir

	"""))
		if(op==4):
			print("Bye")
			break
		else:
			#manda a llamar al metodo main pasandole la opcion escogida "op"
			main(op,blockchain)

