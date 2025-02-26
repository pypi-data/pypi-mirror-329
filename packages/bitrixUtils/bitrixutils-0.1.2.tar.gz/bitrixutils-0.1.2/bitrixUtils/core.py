import requests
import logging
import json
import time

# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format="\n%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Exibe logs no console
    ]
)

# ==========================
# FUNÇÕES GERAIS
# ==========================

def log_detalhado(mensagem, tag_log=False):
    """
    Função para gerar logs detalhados se a tag LOG estiver ativa.

    :param mensagem: Mensagem a ser logada.
    :param tag_log: Se True, exibe/loga a mensagem.
    """
    if tag_log:
        logging.info(mensagem)

def _bitrix_request(api_method, params, bitrix_webhook_url, LOG=False, max_retries=5):
    """
    Função centralizada para requisições ao Bitrix24 com tratamento de erros e retry.

    :param api_method: Método da API do Bitrix24 (ex: "crm.contact.list").
    :param params: Dicionário com os parâmetros da requisição.
    :param bitrix_webhook_url: URL base do webhook do Bitrix24.
    :param LOG: Se True, ativa logs detalhados.
    :param max_retries: Número máximo de tentativas em caso de erro 503.
    :return: Resposta JSON da API ou None em caso de falha.
    """
    endpoint = f"{bitrix_webhook_url}{api_method}"
    delay = 2  # Tempo inicial de espera em segundos

    for tentativa in range(max_retries):
        try:
            if LOG:
                log_detalhado(f"[BITRIX REQUEST] Tentativa {tentativa + 1}/{max_retries} para {api_method}", LOG)
                log_detalhado(f"[BITRIX REQUEST] Payload: {json.dumps(params, indent=2, ensure_ascii=False)}", LOG)

            response = requests.post(endpoint, json=params, timeout=10)

            if LOG:
                log_detalhado(f"[BITRIX REQUEST] Resposta: {response.status_code} - {response.text}", LOG)

            if response.status_code == 200:
                return response.json()

            elif response.status_code == 503:  # Too Many Requests
                log_detalhado(f"[BITRIX REQUEST] Erro 503: Too Many Requests. Retentando em {delay} segundos...", LOG)
                time.sleep(delay)
                delay *= 2  # Aumenta o tempo de espera exponencialmente

            else:
                log_detalhado(f"[BITRIX REQUEST] Erro na requisição: {response.status_code} - {response.text}", LOG)
                return None

        except requests.Timeout:
            log_detalhado(f"[BITRIX REQUEST] Timeout na requisição. Tentativa {tentativa + 1}/{max_retries}. Retentando em {delay} segundos...", LOG)
            time.sleep(delay)
            delay *= 2  # Backoff exponencial
        except requests.RequestException as e:
            log_detalhado(f"[BITRIX REQUEST] Erro ao conectar com Bitrix24: {str(e)}", LOG)
            return None

    log_detalhado("[BITRIX REQUEST] Número máximo de tentativas atingido. Requisição falhou.", LOG)
    return None

# ==========================
# FUNÇÕES DE CONTATOS
# ==========================

def verificarContato(key, keyField, bitrix_webhook_url, LOG=False):
    """
    Verifica se um contato com um campo único (ex: CPF, e-mail) já existe no Bitrix24.

    :param key: Valor único que será usado para buscar o contato.
    :param keyField: Nome do campo no Bitrix24 que contém esse valor.
    :param bitrix_webhook_url: URL do webhook do Bitrix24.
    :param LOG: Se True, ativa logs detalhados.
    :return: ID do contato se existir, None caso contrário.
    """
    params = {
        "filter": {keyField: key},
        "select": ["ID"]
    }

    response = _bitrix_request("crm.contact.list", params, bitrix_webhook_url, LOG)

    if response and "result" in response and response["result"]:
        contact_id = response["result"][0]["ID"]
        log_detalhado(f"[VERIFICAR CONTATO] Contato encontrado. ID: {contact_id}", LOG)
        return contact_id

    log_detalhado("[VERIFICAR CONTATO] Nenhum contato encontrado.", LOG)
    return None

def criarContato(contact_data, cpf_field, bitrix_webhook_url, extra_fields=None, LOG=False):
    """
    Cria um novo contato no Bitrix24.

    Esta função cria um contato no Bitrix24 utilizando os dados fornecidos e pode incluir
    campos personalizados, se necessário.

    :param contact_data: Dicionário contendo as informações do contato, com as seguintes chaves:
        - cpf (str): CPF do contato no formato "123.456.789-00".
        - name (str): Nome do contato.
        - email (str): Endereço de e-mail do contato.
        - celular (str): Número de telefone no formato "(11) 98765-4321".
    :param cpf_field: Nome do campo personalizado no Bitrix24 que armazena o CPF.
    :param bitrix_webhook_url: URL base do webhook do Bitrix24.
    :param extra_fields: (Opcional) Dicionário contendo campos adicionais para o contato.
    :param LOG: Se True, ativa logs detalhados para depuração.

    :return: ID do contato criado em caso de sucesso, ou None se falhar.
    """

    # Construindo payload com os dados obrigatórios do contato
    params = {
        "fields": {
            cpf_field: contact_data.get("cpf"),
            "NAME": contact_data.get("name"),
            "EMAIL": [{"VALUE": contact_data.get("email"), "VALUE_TYPE": "WORK"}],
            "PHONE": [{"VALUE": contact_data.get("celular"), "VALUE_TYPE": "WORK"}]
        }
    }

    # Se houver campos extras, adicioná-los ao payload
    if extra_fields and isinstance(extra_fields, dict):
        params["fields"].update(extra_fields)

    # Chamada à API centralizada usando `_bitrix_request`
    response = _bitrix_request("crm.contact.add", params, bitrix_webhook_url, LOG)

    # Verifica resposta e retorna o ID do contato criado
    if response and "result" in response:
        contact_id = response["result"]
        log_detalhado(f"[CRIAR CONTATO] Contato criado com sucesso. ID: {contact_id}", LOG)
        return contact_id

    log_detalhado("[CRIAR CONTATO] Falha ao obter o ID do contato criado.", LOG)
    return None

def criarEndereco(contact_id, address_data, bitrix_webhook_url, extra_fields=None, LOG=False):
    """
    Cria um endereço no Bitrix24 e vincula ao contato especificado.

    Esta função cria um novo endereço para um contato existente no Bitrix24.

    :param contact_id: ID do contato ao qual o endereço será vinculado (int ou string).
    :param address_data: Dicionário contendo os dados do endereço:
        - rua (str): Nome da rua.
        - numero (str): Número do endereço.
        - cidade (str): Nome da cidade.
        - cep (str): CEP do endereço no formato "01234-567".
        - estado (str): Sigla do estado (ex: "SP").
        - bairro (str): Nome do bairro.
        - complemento (str): Complemento do endereço.
    :param bitrix_webhook_url: URL base do webhook do Bitrix24.
    :param extra_fields: (Opcional) Dicionário contendo campos adicionais do endereço.
    :param LOG: Se True, ativa logs detalhados.

    :return: ID do endereço criado em caso de sucesso, ou None se falhar.
    """

    # Construção do payload com os campos obrigatórios
    params = {
        "fields": {
            "ENTITY_ID": contact_id,  # ID do contato vinculado
            "ENTITY_TYPE_ID": 3,  # Tipo de entidade para contatos
            "TYPE_ID": 1,  # Tipo de endereço (Padrão: Comercial)
            "ADDRESS_1": f"{address_data.get('rua', '')}, {address_data.get('numero', '')}",
            "CITY": address_data.get("cidade", ""),
            "POSTAL_CODE": address_data.get("cep", ""),
            "COUNTRY": "Brasil",
            "PROVINCE": address_data.get("estado", ""),
            "ADDRESS_2": f"{address_data.get('bairro', '')}, {address_data.get('complemento', '')}"
        }
    }

    # Se houver campos extras, adicioná-los ao payload
    if extra_fields and isinstance(extra_fields, dict):
        params["fields"].update(extra_fields)

    # Chamada à API centralizada usando `_bitrix_request`
    response = _bitrix_request("crm.address.add", params, bitrix_webhook_url, LOG)

    # Verifica resposta e retorna o ID do endereço criado
    if response and "result" in response:
        address_id = response["result"]
        log_detalhado(f"[CRIAR ENDEREÇO] Endereço criado com sucesso. ID: {address_id}", LOG)
        return address_id

    log_detalhado("[CRIAR ENDEREÇO] Falha ao obter o ID do endereço criado.", LOG)
    return None

def obterEndereco(contact_id, bitrix_webhook_url, LOG=False):
    """
    Obtém o endereço vinculado a um contato no Bitrix24.

    Essa função retorna o primeiro endereço encontrado associado a um contato no Bitrix24.

    :param contact_id: ID do contato no Bitrix24.
    :param bitrix_webhook_url: URL base do webhook do Bitrix24.
    :param LOG: Se True, ativa logs detalhados para depuração.

    :return: Dicionário com os dados do endereço ou None se não existir.
    """

    params = {
        "filter": {
            "ENTITY_ID": contact_id,
            "ENTITY_TYPE_ID": 3  # Tipo de entidade para contatos no Bitrix24
        }
    }

    response = _bitrix_request("crm.address.list", params, bitrix_webhook_url, LOG)

    if response and "result" in response and response["result"]:
        endereco = response["result"][0]  # Retorna o primeiro endereço encontrado
        log_detalhado(f"[OBTER ENDEREÇO] Endereço encontrado para contato ID {contact_id}: {endereco}", LOG)
        return endereco

    log_detalhado(f"[OBTER ENDEREÇO] Nenhum endereço encontrado para contato ID {contact_id}.", LOG)
    return None

def obterCamposContato(contact_id, bitrix_webhook_url, LOG=False):
    """
    Obtém todos os campos de um contato específico no Bitrix24.

    :param contact_id: ID do contato a ser consultado.
    :param bitrix_webhook_url: URL base do webhook do Bitrix24.
    :param LOG: Se True, ativa logs detalhados.

    :return: Dicionário com os campos do contato ou None em caso de erro.
    """
    params = {"id": contact_id}
    response = _bitrix_request("crm.contact.get", params, bitrix_webhook_url, LOG)

    if response and "result" in response:
        contato = response["result"]
        log_detalhado(f"[OBTER CAMPOS CONTATO] Campos obtidos com sucesso para contato ID {contact_id}.", LOG)
        return contato

    log_detalhado(f"[OBTER CAMPOS CONTATO] Nenhum contato encontrado para ID {contact_id}.", LOG)
    return None

def obterCampoEspecificoContato(campo_personalizado, bitrix_webhook_url, LOG=False):
    """
    Obtém os metadados de um campo personalizado específico de um contato no Bitrix24 e,
    se presente, retorna a propriedade "items" desse campo.

    :param campo_personalizado: Nome exato do campo personalizado (ex: ufCrm41_1737980514688).
    :param bitrix_webhook_url: URL base do webhook do Bitrix24.
    :param LOG: Se True, ativa logs detalhados.

    :return: Lista com os itens do campo, ou o dicionário do campo se não possuir "items".
    """
    # Faz a requisição para obter todos os campos dos contatos
    response = _bitrix_request("crm.contact.fields", {}, bitrix_webhook_url, LOG)

    if response and "result" in response:
        campos = response["result"]

        # Debug: log das chaves encontradas para ajudar na depuração
        for key in campos:
            log_detalhado(f"[DEBUG] Chave encontrada: {repr(key)}", LOG)

        # Normaliza a comparação removendo espaços e convertendo para minúsculas
        campo_procura = campo_personalizado.strip().lower()

        for key in campos:
            if key.strip().lower() == campo_procura:
                log_detalhado(f"[OBTER CAMPO ESPECÍFICO CONTATO] Campo encontrado: {key}", LOG)
                field_data = campos[key]
                if "items" in field_data:
                    return field_data["items"]
                else:
                    log_detalhado(f"[OBTER CAMPO ESPECÍFICO CONTATO] O campo {key} não possui a propriedade 'items'.", LOG)
                    return field_data

    log_detalhado(f"[OBTER CAMPO ESPECÍFICO CONTATO] Campo {campo_personalizado} não encontrado nos contatos.", LOG)
    return None

# ==========================
# FUNÇÕES DE SMART PROCESS AUTOMATION (SPA)
# ==========================

def criarCardSPA(title, stage_id, category_id, assigned_by_id, bitrix_webhook_url, contact_id=None, extra_fields=None, LOG=False):
    """
    Cria um novo card no pipeline do Bitrix24.

    Essa função adiciona um novo card dentro de um Smart Process Automation (SPA) no Bitrix24.

    :param title: Título do card (string).
    :param stage_id: ID do estágio inicial do card (string).
    :param category_id: ID da categoria do card (int ou string).
    :param assigned_by_id: ID do responsável pelo card (int ou string).
    :param bitrix_webhook_url: URL base do webhook do Bitrix24.
    :param contact_id: (Opcional) ID do contato a ser vinculado ao card.
    :param extra_fields: (Opcional) Dicionário contendo campos extras para o card.
    :param LOG: Se True, ativa logs detalhados para depuração.

    :return: ID do card criado em caso de sucesso, ou None se falhar.
    """

    # Construção do payload com os campos obrigatórios
    params = {
        "entityTypeId": 128,  # ID padrão para SPA, pode ser ajustado conforme necessário
        "fields": {
            "title": title,
            "stageId": stage_id,
            "categoryId": category_id,
            "assignedById": assigned_by_id,
            "contactId": contact_id
        }
    }

    # Se houver campos extras, adicioná-los ao payload
    if extra_fields and isinstance(extra_fields, dict):
        params["fields"].update(extra_fields)

    # Chamada à API centralizada usando `_bitrix_request`
    response = _bitrix_request("crm.item.add", params, bitrix_webhook_url, LOG)

    # Verifica resposta e retorna o ID do card criado
    if response and "result" in response and "item" in response["result"]:
        card_id = response["result"]["item"].get("id")
        log_detalhado(f"[CRIAR CARD SPA] Card criado com sucesso. ID: {card_id}", LOG)
        return card_id

    log_detalhado("[CRIAR CARD SPA] Falha ao obter o ID do card criado.", LOG)
    return None

def obterCamposPersonalizadosCardSPA(entity_type_id, bitrix_webhook_url, LOG=False):
    """
    Obtém os metadados de todos os campos personalizados de uma entidade SPA no Bitrix24.

    :param entity_type_id: ID da entidade no Bitrix24.
    :param bitrix_webhook_url: URL base do webhook do Bitrix24.
    :param LOG: Se True, ativa logs detalhados.

    :return: Dicionário com os metadados de todos os campos personalizados ou None em caso de erro.
    """
    params = {"entityTypeId": entity_type_id}
    response = _bitrix_request("crm.item.fields", params, bitrix_webhook_url, LOG)

    if response and "result" in response:
        log_detalhado(f"[OBTER CAMPOS PERSONALIZADOS] Metadados obtidos para entityTypeId {entity_type_id}.", LOG)
        return response["result"]

    log_detalhado(f"[OBTER CAMPOS PERSONALIZADOS] Falha ao obter metadados para entityTypeId {entity_type_id}.", LOG)
    return None

def obterCampoEspecificoCardSPA(campo_personalizado, entity_type_id, bitrix_webhook_url, LOG=False):
    """
    Obtém os metadados de um campo personalizado específico no Bitrix24 e, se presente,
    retorna a propriedade "items" desse campo.

    :param campo_personalizado: Nome do campo personalizado (ex: ufCrm41_1737980514688).
    :param entity_type_id: ID da entidade SPA no Bitrix24.
    :param bitrix_webhook_url: URL base do webhook do Bitrix24.
    :param LOG: Se True, ativa logs detalhados.
    :return: Lista com os itens do campo ou o dicionário do campo se não possuir "items".
    """
    params = {"entityTypeId": entity_type_id}

    # Faz a requisição centralizada
    response = _bitrix_request("crm.item.fields", params, bitrix_webhook_url, LOG)

    if response and "result" in response and "fields" in response["result"]:
        campos = response["result"]["fields"]

        # Debug: log das chaves com repr para verificar espaços ou caracteres ocultos
        for key in campos:
            log_detalhado(f"[DEBUG] Chave encontrada: {repr(key)}", LOG)

        # Normaliza a comparação removendo espaços e convertendo para minúsculas
        campo_procura = campo_personalizado.strip().lower()

        for key in campos:
            if key.strip().lower() == campo_procura:
                log_detalhado(f"[OBTER CAMPO ESPECÍFICO] Campo encontrado: {key}", LOG)
                field_data = campos[key]
                if "items" in field_data:
                    return field_data["items"]
                else:
                    log_detalhado(f"[OBTER CAMPO ESPECÍFICO] O campo {key} não possui a propriedade 'items'.", LOG)
                    return field_data

    log_detalhado(f"[OBTER CAMPO ESPECÍFICO] Campo {campo_personalizado} não encontrado na entidade {entity_type_id}.", LOG)
    return None

def mapearCampos(campos, metadados):
    """
    Mapeia valores de IDs para os valores reais de campos personalizados do Bitrix24.

    Alguns campos personalizados no Bitrix24 armazenam valores como números (IDs) que representam textos.
    Essa função substitui esses IDs pelos valores reais.

    :param campos: Dicionário com os campos do item obtido do Bitrix24.
    :param metadados: Dicionário com os metadados dos campos personalizados.

    :return: Dicionário com os valores traduzidos (quando aplicável).
    """
    if not isinstance(campos, dict) or not isinstance(metadados, dict):
        return campos  # Retorna inalterado se os parâmetros não forem dicionários válidos

    for campo, valor in campos.items():
        # Verifica se o campo está nos metadados e se é do tipo "enumeration" (lista de seleção)
        if campo in metadados and metadados[campo].get("type") == "enumeration":
            opcoes = {str(item["ID"]): item["VALUE"] for item in metadados[campo].get("items", [])}

            if isinstance(valor, list):  # Se for uma seleção múltipla
                campos[campo] = [opcoes.get(str(v), v) for v in valor if v is not None]
            else:
                campos[campo] = opcoes.get(str(valor), valor) if valor is not None else valor

    return campos

def obterCamposCardSPA(entity_type_id, item_id, bitrix_webhook_url, LOG=False):
    """
    Obtém todos os campos de um item SPA específico no Bitrix24 e traduz os valores de listas de seleção.

    :param entity_type_id: ID da entidade SPA no Bitrix24 (ex: 128 para AdvEasy, 158 para Sittax, etc.).
    :param item_id: ID do item a ser consultado.
    :param bitrix_webhook_url: URL base do webhook do Bitrix24.
    :param LOG: Se True, ativa logs detalhados.

    :return: Dicionário com os campos formatados ou None em caso de erro.
    """
    params = {"entityTypeId": entity_type_id, "id": item_id}
    response = _bitrix_request("crm.item.get", params, bitrix_webhook_url, LOG)

    if response and "result" in response and "item" in response["result"]:
        campos = response["result"]["item"]
        log_detalhado(f"[OBTER CAMPOS] Campos obtidos com sucesso para item ID {item_id}.", LOG)

        # Obtém metadados para converter IDs para valores reais
        metadados = obterCamposPersonalizadosCardSPA(entity_type_id, bitrix_webhook_url, LOG)
        if metadados:
            campos = mapearCampos(campos, metadados)

        return campos

    log_detalhado(f"[OBTER CAMPOS] Nenhum campo encontrado para item ID {item_id}.", LOG)
    return None

def obterCardSPAPorContato(contact_id, entity_type_id, bitrix_webhook_url, LOG=False):
    """
    Verifica se existe um Card SPA associado ao contato informado.

    Essa função busca um card (negócio, oportunidade, etc.) que esteja vinculado a um contato específico
    dentro de um Smart Process Automation (SPA) no Bitrix24.

    :param contact_id: ID do contato no Bitrix24.
    :param entity_type_id: Tipo da entidade no Bitrix24 (ex: 128 para AdvEasy, 158 para outra entidade).
    :param bitrix_webhook_url: URL base do webhook do Bitrix24.
    :param LOG: Se True, ativa logs detalhados para depuração.

    :return: ID do primeiro card associado ao contato ou None se não houver cards vinculados.
    """

    params = {
        "entityTypeId": entity_type_id,
        "filter": {"contactId": contact_id},
        "select": ["id"]
    }

    response = _bitrix_request("crm.item.list", params, bitrix_webhook_url, LOG)

    if response and "result" in response and "items" in response["result"]:
        items = response["result"]["items"]
        if items:
            card_id = items[0]["id"]  # Pega o primeiro card encontrado
            log_detalhado(f"[OBTER CARD SPA] Card encontrado para contato ID {contact_id}: {card_id}", LOG)
            return card_id

    log_detalhado(f"[OBTER CARD SPA] Nenhum card encontrado para contato ID {contact_id}.", LOG)
    return None

def moverEtapaCardSPA(stage_id, card_id, entity_type_id, bitrix_webhook_url, LOG=False):
    """
    Move um Card SPA para uma nova etapa no Bitrix24.

    Essa função altera o estágio de um card dentro de um Smart Process Automation (SPA) no Bitrix24.

    :param stage_id: Novo stageId para onde o card será movido.
    :param card_id: ID do card que será movido.
    :param entity_type_id: Tipo da entidade no Bitrix24 (ex: 128 para negócios).
    :param bitrix_webhook_url: URL base do webhook do Bitrix24.
    :param LOG: Se True, ativa logs detalhados para depuração.

    :return: True se a movimentação for bem-sucedida, False caso contrário.
    """

    params = {
        "entityTypeId": entity_type_id,
        "id": card_id,
        "fields": {"stageId": stage_id}
    }

    response = _bitrix_request("crm.item.update", params, bitrix_webhook_url, LOG)

    if response and "result" in response:
        log_detalhado(f"[MOVER ETAPA SPA] Card ID {card_id} movido com sucesso para stageId {stage_id}.", LOG)
        return True

    log_detalhado(f"[MOVER ETAPA SPA] Falha ao mover o Card ID {card_id} para stageId {stage_id}.", LOG)
    return False

def listarCardsSPA(bitrix_webhook_url, entity_type_id, category_id=None, stage_id=None, LOG=False):
    """
    Lista todos os cards de um SPA no Bitrix24, aplicando filtros opcionais e lidando corretamente com paginação.

    :param bitrix_webhook_url: URL do webhook do Bitrix24.
    :param entity_type_id: ID do tipo de entidade (SPA).
    :param category_id: (Opcional) ID da categoria para filtrar os cards.
    :param stage_id: (Opcional) ID do estágio para filtrar os cards.
    :param LOG: Se True, ativa logs detalhados.

    :return: Lista de dicionários contendo ID e title de cada card encontrado.
    """

    # Filtros opcionais
    filtro = {}
    if category_id:
        filtro["categoryId"] = category_id
    if stage_id:
        filtro["stageId"] = stage_id

    cards = []
    start = 0  # Controle de paginação

    while True:
        params = {
            "entityTypeId": entity_type_id,
            "filter": filtro,
            "select": ["id", "title"],
            "start": start
        }

        response = _bitrix_request("crm.item.list", params, bitrix_webhook_url, LOG)

        if response and "result" in response and "items" in response["result"]:
            items = response["result"]["items"]

            if not items:
                log_detalhado("[LISTAR CARDS SPA] Nenhum card encontrado.", LOG)
                return cards  # Retorna lista vazia se não houver registros

            cards.extend(items)

            # Atualiza paginação
            next_start = response["result"].get("next")
            if next_start is None:
                break  # Sai do loop se não houver mais páginas
            start = next_start  # Define o próximo ponto de início da paginação

            log_detalhado(f"[LISTAR CARDS SPA] Total de cards coletados até agora: {len(cards)}", LOG)

        else:
            log_detalhado("[LISTAR CARDS SPA] Falha ao obter os cards ou resposta vazia.", LOG)
            return cards  # Retorna os cards coletados até o momento

    return cards

def listAllSPA(bitrix_webhook_url, LOG=False):
    """
    Obtém a lista de entidades do CRM do Bitrix24.

    :param bitrix_webhook_url: URL base do webhook do Bitrix24.
    :param LOG: Se True, ativa logs detalhados.

    :return: Lista de dicionários contendo 'title' e 'entityTypeId' das entidades.
    """
    method = "crm.type.list"  # Método para listar os tipos de entidades
    response = _bitrix_request(method, {}, bitrix_webhook_url, LOG)

    # Verificando se a resposta é válida e contém os dados esperados
    if response and "result" in response and "types" in response["result"]:
        entidades = []

        for entity in response["result"]["types"]:
            entidade_info = {
                "title": entity.get("title"),
                "entityTypeId": entity.get("entityTypeId")
            }
            entidades.append(entidade_info)

        log_detalhado(f"[FIND ENTERPRISE] {len(entidades)} entidades encontradas.", LOG)
        return entidades  # Retorna a lista formatada

    log_detalhado("[FIND ENTERPRISE] Nenhuma entidade encontrada ou formato inesperado da resposta.", LOG)
    return None  # Retorna None em caso de erro

def obterTypeId(bitrixWebhookUrl, LOG=False):
    """
    Obtém todos os valores distintos do campo TYPE_ID dos contatos no Bitrix24 e seus significados.

    Essa função consulta a API `crm.status.list` para mapear os IDs dos TYPE_IDs aos seus respectivos valores.

    :param bitrixWebhookUrl: URL base do webhook do Bitrix24.
    :param LOG: Se True, ativa logs detalhados para depuração.

    :return: Dicionário { ID: "Descrição" } contendo todos os valores possíveis do TYPE_ID.
    """
    params = {"FILTER": {"ENTITY_ID": "CONTACT_TYPE"}}

    response = _bitrix_request("crm.status.list", params, bitrixWebhookUrl, LOG)

    if response and "result" in response:
        typeIdMap = {item["STATUS_ID"]: item["NAME"] for item in response["result"]}
        log_detalhado(f"[OBTER TYPE_ID] Mapeamento obtido: {typeIdMap}", LOG)
        return typeIdMap

    log_detalhado("[OBTER TYPE_ID] Erro ao buscar os metadados do campo TYPE_ID via crm.status.list.", LOG)
    return {}
