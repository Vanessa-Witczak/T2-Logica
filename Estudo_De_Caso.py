# Simulação do estudo de caso: ordenar clientes por valor de compra (maior -> menor)

from dataclasses import dataclass
from typing import List

@dataclass
class Cliente:
    nome: str
    valor: float

def validar_clientes(raw_list):
    clientes = []
    erros = []
    for i, item in enumerate(raw_list):
        try:
            nome = str(item['nome']).strip()
            valor = float(item['valor'])
            if nome == "":
                erros.append((i, "nome vazio"))
                continue
            if valor < 0:
                erros.append((i, "valor negativo"))
                continue
            clientes.append(Cliente(nome, valor))
        except Exception as e:
            erros.append((i, f"erro conversao: {e}"))
    return clientes, erros

def gerar_relatorio_ordenado(clientes: List[Cliente]):

    clientes_sorted = sorted(clientes, key=lambda c: (-c.valor, c.nome))
    return clientes_sorted

def exemplo_execucao():
    # dados de entrada (poderiam vir de CSV ou banco)
    raw = [
        {'nome': 'Ana', 'valor': 250.0},
        {'nome': 'Carlos', 'valor': 150.0},
        {'nome': 'Bianca', 'valor': 250.0},
        {'nome': 'Davi', 'valor': -20},
        {'nome': '', 'valor': 100},
        {'nome': 'Eduardo', 'valor': '300.5'}
    ]

    clientes, erros = validar_clientes(raw)
    print("Erros encontrados (linha, motivo):", erros)
    ordenados = gerar_relatorio_ordenado(clientes)
    print("Relatório (maior -> menor):")
    for c in ordenados:
        print(f"{c.nome}: R$ {c.valor:.2f}")

if __name__ == "__main__":
    exemplo_execucao()