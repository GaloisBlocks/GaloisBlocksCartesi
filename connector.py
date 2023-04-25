from flask import Flask, request
import importlib
import json
from GB_NFTgenerator import compileNFT

app = Flask(__name__)

@app.route('/', methods=['POST'])
def execute_module():
    data = request.get_json()

    module_args = [data['name'],data['symbol'], data['address'], int(data['maxSupply']) ] # Arguments to pass to the module
    print(module_args)
    try:
        # module = importlib.import_module(module_name)
        # compiler = getattr(module.compileNFT, 'main')
        result = compileNFT.main(*module_args)
        return {'result': result}
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    app.run()
