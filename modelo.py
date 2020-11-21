users=[]
mel= dict()
jos=dict()
vic=dict()
adr=dict()
fco=dict()

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

users=[mel,jos,vic,adr,fco]

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

#si quieres cambiar algo del chain solo se utiliza la variable
