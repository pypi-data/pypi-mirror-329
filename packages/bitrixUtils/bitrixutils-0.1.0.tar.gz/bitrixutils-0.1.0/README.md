# bitrixUtils

**bitrixUtils** é uma biblioteca Python para facilitar a integração com a API do Bitrix24.
Ela encapsula funções comuns para facilitar o uso dos endpoints da API, lidando com autenticação, manipulação de contatos, cards, endereços e mais.

## 📌 Instalação
```Bash
pip install bitrixUtils
```

## 🚀 Como Usar
```python
from bitrixUtils import core

BITRIX_WEBHOOK_URL = "https://setup.bitrix24.com.br/rest/629/c0q6gqm7og1bs91k/"
cpf = "123.456.789-00"

contact_id = core.verificarContato(cpf, BITRIX_WEBHOOK_URL)
print(contact_id)
```

## 🔧 Funcionalidades
- Verificar se um contato existe no Bitrix24
- Criar e atualizar contatos
- Criar e gerenciar cards no pipeline
- Manipular endereços
- Gerenciar etapas de pipeline