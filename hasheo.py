from hashlib import sha256

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

#si quieres cambiar algo del chain solo se utiliza la variable
