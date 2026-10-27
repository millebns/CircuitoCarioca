import os
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for testing
import matplotlib.pyplot as plt
import networkx as nx
import pytest

from circuito_carioca import (
    ARESTAS,
    COORDENADAS,
    adicionar_desafios,
    criar_grafo,
    desenhar_tabuleiro,
    gerar_figura_legenda,
    gerar_legenda,
    obter_posicoes,
    verificar_circuito_euleriano,
)


def test_coordenadas_e_arestas_validas():
    """Verifica se todas as arestas se referem a vértices existentes nas coordenadas."""
    assert len(COORDENADAS) == 30
    assert len(ARESTAS) > 0

    locais = set(COORDENADAS.keys())
    for u, v in ARESTAS:
        assert u in locais, f"Local '{u}' não encontrado em COORDENADAS"
        assert v in locais, f"Local '{v}' não encontrado em COORDENADAS"


def test_criar_grafo():
    """Testa a criação do grafo."""
    G = criar_grafo()
    assert isinstance(G, nx.Graph)
    assert len(G.nodes) == len(COORDENADAS)
    assert len(G.edges) == len(ARESTAS)

    # Test custom coordinates and edges
    custom_coords = {"A": (0, 0), "B": (1, 1)}
    custom_edges = [("A", "B")]
    G_custom = criar_grafo(coordenadas=custom_coords, arestas=custom_edges)
    assert len(G_custom.nodes) == 2
    assert len(G_custom.edges) == 1


def test_obter_posicoes():
    """Testa a extração de posições (lon, lat)."""
    pos = obter_posicoes()
    assert len(pos) == len(COORDENADAS)
    for local, (lat, lon) in COORDENADAS.items():
        assert pos[local] == (lon, lat)


def test_adicionar_desafios():
    """Testa a seleção aleatória de desafios com semente determinística."""
    G = criar_grafo()

    # Probabilidade 0 -> nenhum desafio
    desafios_0 = adicionar_desafios(G, prob_desafio=0.0)
    assert len(desafios_0) == 0

    # Probabilidade 1 -> todas as arestas viram desafios
    desafios_1 = adicionar_desafios(G, prob_desafio=1.0)
    assert len(desafios_1) == len(G.edges)

    # Com semente
    d1 = adicionar_desafios(G, prob_desafio=0.4, seed=42)
    d2 = adicionar_desafios(G, prob_desafio=0.4, seed=42)
    assert d1 == d2


def test_gerar_legenda():
    """Testa o mapeamento da legenda de 1 a N."""
    legenda = gerar_legenda()
    assert len(legenda) == len(COORDENADAS)
    assert legenda["Cristo Redentor"] == "1"
    assert legenda["Pão de Açúcar"] == "2"

    for i, local in enumerate(COORDENADAS.keys()):
        assert legenda[local] == str(i + 1)


def test_verificar_circuito_euleriano():
    """Testa a análise de propriedades eulerianas."""
    G = criar_grafo()
    res = verificar_circuito_euleriano(G)

    assert "is_eulerian" in res
    assert "has_eulerian_path" in res
    assert "odd_degree_nodes" in res
    assert "is_connected" in res
    assert isinstance(res["odd_degree_nodes"], list)

    # Test with a known Eulerian graph (a cycle graph C4)
    c4 = nx.cycle_graph(4)
    res_c4 = verificar_circuito_euleriano(c4)
    assert res_c4["is_eulerian"] is True
    assert res_c4["has_eulerian_path"] is True
    assert len(res_c4["odd_degree_nodes"]) == 0

    # Test with a path graph P3 (0 - 1 - 2) which has an Eulerian path but not Eulerian circuit
    p3 = nx.path_graph(3)
    res_p3 = verificar_circuito_euleriano(p3)
    assert res_p3["is_eulerian"] is False
    assert res_p3["has_eulerian_path"] is True
    assert len(res_p3["odd_degree_nodes"]) == 2


def test_desenhar_tabuleiro(tmp_path):
    """Testa a função de renderização do tabuleiro e salvamento em arquivo."""
    G = criar_grafo()
    desafios = [("Cristo Redentor", "Pão de Açúcar")]
    out_file = tmp_path / "tabuleiro.png"

    fig = desenhar_tabuleiro(
        G=G, desafios=desafios, salvar_caminho=str(out_file), show=False
    )
    assert fig is not None
    assert os.path.exists(out_file)
    assert os.path.getsize(out_file) > 0


def test_gerar_figura_legenda(tmp_path):
    """Testa a função de renderização da legenda e salvamento em arquivo."""
    out_file = tmp_path / "legenda.png"

    fig = gerar_figura_legenda(salvar_caminho=str(out_file), show=False)
    assert fig is not None
    assert os.path.exists(out_file)
    assert os.path.getsize(out_file) > 0
