from jinja2 import Template
import os

template_path = os.path.join(os.path.dirname(__file__), 'ERC721_template.sol')
with open(template_path, 'r') as f:
    template = Template(f.read())

name = 'MyNFT'
symbol = 'MNFT'

contract_source_code = template.render(name=name, symbol=symbol)

print(contract_source_code)
# with open('MyNFT_{0}.sol'.format(name), 'w') as f:
#     f.write(contract_source_code)
