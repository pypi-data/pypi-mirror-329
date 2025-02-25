# bitrixUtils

**bitrixUtils** é uma biblioteca Python para facilitar a integração com a API do Bitrix24.
Ela encapsula funções comuns para facilitar o uso dos endpoints da API, lidando com autenticação, manipulação de contatos, cards, endereços e mais.

## 👉 Instalação

```bash
pip install bitrixUtils
```

## 🚀 Como Usar

Antes de usar a biblioteca, defina a URL do Webhook do Bitrix24:

```python
from bitrixUtils import core

BITRIX_WEBHOOK_URL = "https://seu-webhook-bitrix24.com/rest/XXX/YYYYY/"
```

---

## 👥 Contatos

### **Verificar se um Contato Existe**
```python
contact_id = core.verificarContato("123.456.789-00", "UF_CRM_CPF", BITRIX_WEBHOOK_URL)
print(f"Contato encontrado: {contact_id}")
```

### **Criar um Novo Contato**
```python
contact_data = {
    "cpf": "123.456.789-00",
    "name": "João Silva",
    "email": "joao@email.com",
    "celular": "(11) 98765-4321"
}
contact_id = core.criarContato(contact_data, "UF_CRM_CPF", BITRIX_WEBHOOK_URL)
print(f"Novo contato criado: {contact_id}")
```

### **Criar um Endereço para um Contato**
```python
address_data = {
    "rua": "Avenida Paulista",
    "numero": "1000",
    "cidade": "São Paulo",
    "cep": "01311-000",
    "estado": "SP",
    "bairro": "Bela Vista",
    "complemento": "Apto 101"
}
address_id = core.criarEndereco(contact_id, address_data, BITRIX_WEBHOOK_URL)
print(f"Endereço criado: {address_id}")
```

### **Obter Endereço de um Contato**
```python
endereco = core.obterEndereco(contact_id, BITRIX_WEBHOOK_URL)
print(f"Endereço encontrado: {endereco}")
```

---

## 🌍 Smart Process Automation (SPA) - Cards

### **Criar um Novo Card no Pipeline**
```python
card_id = core.criarCardSPA("Novo Card", "STAGE_1", 203, 1, BITRIX_WEBHOOK_URL)
print(f"Card criado: {card_id}")
```

### **Listar Todos os Cards**
```python
cards = core.listarCardsSPA(BITRIX_WEBHOOK_URL, entity_type_id=128)
print(f"Cards encontrados: {cards}")
```

### **Mover um Card para Outra Etapa**
```python
sucesso = core.moverEtapaCardSPA("STAGE_2", card_id, 128, BITRIX_WEBHOOK_URL)
print(f"Movimentado com sucesso? {sucesso}")
```

---

## 📂 Campos Personalizados

### **Obter Metadados de Campos Personalizados**
```python
metadados = core.obterCamposPersonalizadosCardSPA(128, BITRIX_WEBHOOK_URL)
print(metadados)
```

### **Obter Informação de um Campo Específico**
```python
campo_info = core.obterCampoEspecificoCardSPA("UF_CRM_CAMPO_TESTE", 128, BITRIX_WEBHOOK_URL)
print(campo_info)
```

---

## 🛠️ Erros e Depuração
Se precisar de logs detalhados, adicione `LOG=True` nas chamadas:
```python
contact_id = core.verificarContato("123.456.789-00", "UF_CRM_CPF", BITRIX_WEBHOOK_URL, LOG=True)
```
