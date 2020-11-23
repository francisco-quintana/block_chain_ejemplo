from hashlib import sha256
"""
users=[]
mel= dict()
jos=dict()
vic=dict()
adr=dict()
fco=dict()

users=[mel,jos,vic,adr,fco]

chain=[]

mel["user"]="Melissa"
jos["user"]="Joshua"
vic["user"]="Victor"
adr["user"]="Adrian"
fco["user"]="Francisco"

mel["pass"]="mel1"
jos["pass"]="jos2"
vic["pass"]="vic3"
adr["pass"]="adr4"
fco["pass"]="fco5"

mel["chain"]=chain
jos["chain"]=chain
vic["chain"]=chain
adr["chain"]=chain
fco["chain"]=chain



def agregar(time,hs,nonce,msg):
    block=dict()
    block["indice"]=len(chain)
    block["hora"]=time
    block["hash"]=hs
    block["nonce"]=nonce
    if len(chain)!=0:
        block["hash_a"]=chain[len(chain)-1]["hash"]
    block["mensaje"]=msg
    chain.append(block)

    """

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
