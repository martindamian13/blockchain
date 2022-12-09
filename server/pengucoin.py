from flask import Flask, jsonify, request
from time import time

class Bloque:
    def __init__(self, index, transacciones,timestamp):
        self.index = index
        self.transacciones = transacciones
        self.timestamp = timestamp

class Blockchain: 
    def __init__(self):
        self.transacciones_pendientes = []
        self.chain = []
        # Una vez creada la funcion pasamos a crear el bloque genesis.
        self.crear_bloque_genesis()
    
    #Lo siguiente seria crear una funcion que nos permita crear el bloque genesis. 
    #Para llamarlo al iniciar la blockchain.
    def crear_bloque_genesis(self):
        genesis_block = Bloque(0, ["Genesis"], time())
        self.chain.append(genesis_block)
    
    # Agregamos una propiedad a la cadena. 
    # Esta propiedad nos permite acceder al ultimo bloque
    @property
    def last_block(self):
        return self.chain[-1]
    
    # Luego creamos una funcion que nos permita agregar bloques a la cadena
    def agregar_bloque(self, block):
        self.chain.append(block)
        return True
    
    # Una funcion que agregue las transacciones al bloque que queremos agregar
    def agregar_transaccion(self, transaction):
                self.transacciones_pendientes.append(transaction)
    
    # Por ultimo lo que debemos hacer es cerrar un bloque, para ello creamos una funcion
    # que cree un bloque con las transacciones pendientes y luego los agregue a la cadena de bloques.
    def cerrar_bloque(self):
        if not self.transacciones_pendientes:
            return False
        ultimo_bloque = self.last_block
        nuevo_bloque = Bloque(ultimo_bloque.index + 1, self.transacciones_pendientes, time())
        self.agregar_bloque(nuevo_bloque)
        self.transacciones_pendientes = []
        return nuevo_bloque


app = Flask(__name__)

cadena = Blockchain()

@app.route('/cerrar', methods=['GET'])
def mine():
    bloque = cadena.cerrar_bloque()
    response = {
        'message': "Nuevo Bloque Cerrado",
        'index': bloque.index,
        'transactions': bloque.transacciones,
        'timestamp': bloque.timestamp,
    }
    return jsonify(response), 200


@app.route('/transaccion/new', methods=['POST'])
def nueva_transaccion():
    values = request.get_json()

    # Create a new Transaction
    index = cadena.agregar_transaccion(values['transaccion'])

    response = {'message': f'La transaccion se a agregado correctamente.'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    chain = []
    for i in cadena.chain:
        chain.append(i.__dict__)
    response = {
        'chain': chain,
        'length': len(chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
