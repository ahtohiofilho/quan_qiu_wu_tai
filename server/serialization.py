# server/serialization.py
import json
import networkx as nx
import numpy as np
from pathlib import Path
from typing import Any, Dict, Optional
from shared.world import Mundo
from shared.references import Referencias


class Serializador:
    """
    Classe responsável por serializar e desserializar o estado completo de um Mundo.
    Converte para dict serializável em JSON, salva em disco e recarrega.
    """

    @staticmethod
    def _convert(value: Any) -> Any:
        """
        Converte valores não serializáveis em tipos compatíveis com JSON.
        """
        if isinstance(value, np.integer):
            return int(value)
        if isinstance(value, np.floating):
            return float(value)
        if isinstance(value, np.ndarray):
            return value.tolist()
        if isinstance(value, tuple):
            return list(value)
        if hasattr(value, '__dict__'):
            return {k: Serializador._convert(v) for k, v in value.__dict__.items() if not k.startswith('_')}
        return value

    @classmethod
    def to_serializable_dict(cls, mundo: Mundo) -> Dict[str, Any]:
        """
        Converte um objeto Mundo em um dicionário compatível com JSON.
        Remove atributos deriváveis para reduzir tamanho.
        """
        if not hasattr(mundo, 'planeta') or not hasattr(mundo, 'civs'):
            raise ValueError("Objeto mundo inválido: falta atributos 'planeta' ou 'civs'")

        G = mundo.planeta.geografia.copy()

        # Atributos que podem ser recalculados, então não precisam ser salvos
        node_attrs_to_remove = {
            'cor_placa', 'cor_bioma', 'letra_grega', 'cust_mob', 'tipo', 'altitude', 'umidade', 'temperatura',
        }
        for node in G.nodes:
            for attr in node_attrs_to_remove:
                G.nodes[node].pop(attr, None)  # Remove silenciosamente

        # Remover arestas (serão recalculadas com custo de mobilidade)
        G.remove_edges_from(list(G.edges))

        # Converter atributos dos nós
        for node in G.nodes:
            attrs = G.nodes[node]
            for key in list(attrs.keys()):
                attrs[key] = cls._convert(attrs[key])

        G_data = nx.node_link_data(G)
        G_data.pop("directed", None)
        G_data.pop("multigraph", None)
        G_data.pop("graph", None)

        # Serializar civilizações
        civilizacoes_data = []
        for civ in mundo.civs:
            civ_data = {
                'nome': civ.nome,
                'cultura': civ.cultura,
                'cor': cls._convert(civ.cor),
                'modalidade_bandeira': civ.modalidade_bandeira,
                'cores_bandeira': cls._convert(civ.cores_bandeira),
                'player': civ.player,
                'provincias': [
                    {
                        'coordenadas': cls._convert(p.coordenadas),
                        'nome': p.nome
                    }
                    for p in civ.provincias
                ]
            }
            civilizacoes_data.append(civ_data)

        return {
            "id_mundo": mundo.id_mundo,
            "fator": mundo.planeta.fator,
            "bioma_inicial": mundo.planeta.bioma_inicial,
            "vagas": mundo.planeta.numero_de_jogadores,
            "geografia": G_data,
            "civilizacoes": civilizacoes_data
        }

    @classmethod
    def from_serializable_dict(cls, data: Dict[str, Any], ref: Optional[Referencias] = None):
        """
        Reconstroi um objeto Mundo a partir de um dicionário.
        Requer uma instância de Referencias para inicialização.
        """
        """
        Ainda a ser implementado
        retorna Mundo
        """

    @classmethod
    def save_to_json(cls, mundo: Mundo, filepath: str) -> bool:
        try:
            data = cls.to_serializable_dict(mundo)
            path = Path(filepath)
            path.parent.mkdir(exist_ok=True, parents=True)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ Mundo salvo em JSON: {filepath}")
            return True
        except Exception as e:
            print(f"❌ Falha ao salvar mundo: {e}")
            return False

    @classmethod
    def save_mundo(cls, mundo: Mundo, filepath: str = None) -> str:
        """
        Salva um objeto Mundo em JSON.
        Se filepath não for fornecido, gera um nome automático em 'saves/'.
        :param mundo: Instância de Mundo
        :param filepath: Caminho opcional para salvar
        :return: Caminho final usado, ou string vazia se falhar
        """
        from pathlib import Path

        if filepath is None:
            # Gera caminho padrão: saves/mundo_{id}.json
            saves_dir = Path("saves")
            saves_dir.mkdir(exist_ok=True)
            filepath = saves_dir / f"mundo_{mundo.id_mundo}.json"
        else:
            # Garante que o diretório pai exista
            path = Path(filepath)
            path.parent.mkdir(exist_ok=True, parents=True)

        sucesso = cls.save_to_json(mundo, filepath)
        return str(filepath) if sucesso else ""