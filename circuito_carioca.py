import random
import matplotlib.pyplot as plt
import networkx as nx

COORDENADAS = {
    "Cristo Redentor": (-22.951997, -43.210698),
    "Pão de Açúcar": (-22.949680, -43.152977),
    "Mirante da Dona Marta": (-22.945264, -43.196467),
    "Parque Nacional da Tijuca": (-22.965760, -43.239848),
    "Parque Lage": (-22.960040, -43.212276),
    "Maracanã": (-22.9125, -43.2302),
    "Jardim Botânico": (-22.968845, -43.226084),
    "Lagoa Rodrigo de Freitas": (-22.971907, -43.212372),
    "Praia de Copacabana": (-22.975542, -43.186558),
    "Praia da Urca": (-22.947944, -43.163339),
    "Praia do Leme": (-22.964419, -43.166817),
    "Mirante do Leblon": (-22.990694, -43.237328),
    "Quinta da Boa Vista": (-22.9085, -43.2203),
    "Bioparque": (-22.904918, -43.231469),
    "AquaRio": (-22.880481, -43.191537),
    "Museu do Amanhã": (-22.890409, -43.178898),
    "Boulevard Olímpico": (-22.898573, -43.177743),
    "Ilha Fiscal": (-22.8837, -43.1596),
    "Botafogo": (-22.945491, -43.180636),
    "Aterro do Flamengo": (-22.92741, -43.16115),
    "Escadaria Selarón": (-22.929583, -43.179504),
    "Arcos da Lapa": (-22.912973, -43.180363),
    "Gabinete Real": (-22.905097, -43.182293),
    "Teatro Municipal": (-22.910704, -43.173008),
    "Forte de Copacabana": (-22.985874, -43.184048),
    "Praia do Arpoador": (-22.988620, -43.193047),
    "Praia de Ipanema": (-22.987316, -43.202029),
    "Praia do Leblon": (-22.987059, -43.224882),
    "Cachoeira do Horto": (-22.955012, -43.247434),
    "Vista Chinesa": (-22.973092, -43.259537),
}

ARESTAS = [
    ("Cristo Redentor", "Pão de Açúcar"),
    ("Cristo Redentor", "Mirante da Dona Marta"),
    ("Cristo Redentor", "Parque Nacional da Tijuca"),
    ("Cristo Redentor", "Parque Lage"),
    ("Mirante da Dona Marta", "Maracanã"),
    ("Parque Lage", "Jardim Botânico"),
    ("Parque Lage", "Lagoa Rodrigo de Freitas"),
    ("Parque Lage", "Praia de Copacabana"),
    ("Pão de Açúcar", "Praia da Urca"),
    ("Pão de Açúcar", "Praia de Copacabana"),
    ("Pão de Açúcar", "Praia do Leme"),
    ("Jardim Botânico", "Mirante do Leblon"),
    ("Jardim Botânico", "Maracanã"),
    ("Jardim Botânico", "Parque Nacional da Tijuca"),
    ("Jardim Botânico", "Lagoa Rodrigo de Freitas"),
    ("Jardim Botânico", "Praia de Ipanema"),
    ("Maracanã", "Quinta da Boa Vista"),
    ("Maracanã", "Bioparque"),
    ("Quinta da Boa Vista", "Bioparque"),
    ("Bioparque", "AquaRio"),
    ("Bioparque", "Museu do Amanhã"),
    ("AquaRio", "Museu do Amanhã"),
    ("Museu do Amanhã", "Boulevard Olímpico"),
    ("Museu do Amanhã", "Ilha Fiscal"),
    ("Boulevard Olímpico", "Ilha Fiscal"),
    ("Praia da Urca", "Botafogo"),
    ("Botafogo", "Aterro do Flamengo"),
    ("Aterro do Flamengo", "Escadaria Selarón"),
    ("Escadaria Selarón", "Arcos da Lapa"),
    ("Arcos da Lapa", "Gabinete Real"),
    ("Arcos da Lapa", "Teatro Municipal"),
    ("Arcos da Lapa", "Praia de Ipanema"),
    ("Gabinete Real", "Teatro Municipal"),
    ("Praia de Copacabana", "Forte de Copacabana"),
    ("Forte de Copacabana", "Praia do Arpoador"),
    ("Praia do Arpoador", "Praia de Ipanema"),
    ("Praia de Ipanema", "Praia do Leblon"),
    ("Praia do Leblon", "Mirante do Leblon"),
    ("Praia do Leme", "Praia de Copacabana"),
    ("Cachoeira do Horto", "Parque Nacional da Tijuca"),
    ("Cachoeira do Horto", "Vista Chinesa"),
    ("Vista Chinesa", "Parque Nacional da Tijuca"),
]


def criar_grafo(coordenadas=None, arestas=None):
    """Cria e retorna o grafo de pontos turísticos e arestas."""
    if coordenadas is None:
        coordenadas = COORDENADAS
    if arestas is None:
        arestas = ARESTAS

    G = nx.Graph()
    G.add_nodes_from(coordenadas.keys())
    G.add_edges_from(arestas)
    return G


def obter_posicoes(coordenadas=None):
    """Retorna dicionário de posições (lon, lat) para visualização."""
    if coordenadas is None:
        coordenadas = COORDENADAS
    return {local: (lon, lat) for local, (lat, lon) in coordenadas.items()}


def adicionar_desafios(G, prob_desafio=0.4, seed=None):
    """Define quais arestas contêm casas de desafio (ponto de interrogação)."""
    if seed is not None:
        random.seed(seed)

    desafios = []
    for u, v in G.edges():
        if random.random() < prob_desafio:
            desafios.append((u, v))
    return desafios


def gerar_legenda(coordenadas=None):
    """Gera o dicionário de mapeamento local -> número."""
    if coordenadas is None:
        coordenadas = COORDENADAS
    return {local: str(i + 1) for i, local in enumerate(coordenadas.keys())}


def verificar_circuito_euleriano(G):
    """
    Verifica propriedades eulerianas do grafo.
    Retorna um dicionário com:
      - 'is_eulerian': True se possui circuito euleriano (conectado e todos os vértices com grau par)
      - 'has_eulerian_path': True se possui caminho euleriano
      - 'odd_degree_nodes': Lista de nós com grau ímpar
      - 'is_connected': True se o grafo é conectado
    """
    is_conn = nx.is_connected(G) if len(G) > 0 else True
    odd_nodes = [node for node, degree in G.degree() if degree % 2 != 0]

    is_eul = is_conn and len(odd_nodes) == 0
    has_eul_path = is_conn and (len(odd_nodes) == 0 or len(odd_nodes) == 2)

    return {
        "is_eulerian": is_eul,
        "has_eulerian_path": has_eul_path,
        "odd_degree_nodes": odd_nodes,
        "is_connected": is_conn,
    }


def desenhar_tabuleiro(
    G=None,
    pos=None,
    desafios=None,
    coordenadas=None,
    salvar_caminho=None,
    show=False,
):
    """Desenha a imagem do tabuleiro do jogo."""
    if coordenadas is None:
        coordenadas = COORDENADAS
    if G is None:
        G = criar_grafo(coordenadas)
    if pos is None:
        pos = obter_posicoes(coordenadas)
    if desafios is None:
        desafios = []

    fig, ax = plt.subplots(figsize=(16.5, 11.7), facecolor="none")

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=400,
        node_color="#2F2F2F",
        alpha=0.9,
        edgecolors="black",
        ax=ax,
    )
    nx.draw_networkx_edges(
        G, pos, edge_color="gray", style="dashed", width=5.5, ax=ax
    )

    numeros_rotulos = gerar_legenda(coordenadas)
    nx.draw_networkx_labels(
        G,
        pos,
        labels=numeros_rotulos,
        font_size=12,
        font_color="white",
        verticalalignment="center",
        horizontalalignment="center",
        ax=ax,
    )

    desafios_set = {
        (u, v) if (u, v) in G.edges() else (v, u) for u, v in desafios
    }
    for u, v in G.edges():
        if (u, v) in desafios_set or (v, u) in desafios_set:
            x = (pos[u][0] + pos[v][0]) / 2
            y = (pos[u][1] + pos[v][1]) / 2
            ax.text(
                x,
                y,
                "?",
                fontsize=12,
                color="black",
                ha="center",
                va="center",
                bbox=dict(
                    facecolor="white", edgecolor="black", boxstyle="round,pad=0.2"
                ),
            )

    ax.axis("off")
    plt.title(
        "Circuito Carioca", fontsize=20, color="black", loc="center", pad=20
    )

    if salvar_caminho:
        plt.savefig(salvar_caminho, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


def gerar_figura_legenda(
    coordenadas=None, num_colunas=3, salvar_caminho=None, show=False
):
    """Gera a figura com a legenda dos pontos turísticos."""
    if coordenadas is None:
        coordenadas = COORDENADAS

    numeros_rotulos = gerar_legenda(coordenadas)

    fig, ax = plt.subplots(figsize=(10, 6), facecolor="white")
    plt.title(
        "Legenda dos Pontos Turísticos",
        fontsize=16,
        color="black",
        loc="center",
        pad=20,
    )

    itens_por_coluna = len(numeros_rotulos) // num_colunas + 1
    colunas = [
        list(numeros_rotulos.items())[i : i + itens_por_coluna]
        for i in range(0, len(numeros_rotulos), itens_por_coluna)
    ]

    for col_index, coluna in enumerate(colunas):
        for linha_index, (local, numero) in enumerate(coluna):
            legenda_x = 0.1 + col_index * 0.3
            legenda_y = 0.9 - linha_index * 0.05
            ax.text(
                legenda_x,
                legenda_y,
                f"{numero} - {local}",
                fontsize=10,
                color="black",
                ha="left",
            )

    ax.axis("off")

    if salvar_caminho:
        plt.savefig(salvar_caminho, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig
