
def not_found_message(resource_name: str, resource_id: int) -> str:
    return f"Não foi encontrado {resource_name} com o ID {resource_id}"

def invalid_type(resource_name: str, expected_type: str, received_type: str) -> str:
    return f"Campo {resource_name} com tipo inválido. Esperado: {expected_type}, recebido: {received_type}"
