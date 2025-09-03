# shared/turn.py
"""
Módulo: shared/turn.py
Responsável por gerenciar a lógica de cada turno do jogo.
Atualmente: crescimento populacional por província.
Futuramente: pode incluir produção, eventos, IA, etc.
"""


class Turno:
    def __init__(self):
        self.numero = 0  # Turno atual (0 = pré-jogo)
        self.historico = []  # Histórico de eventos por turno

    def avancar(self, mundo):
        """
        Avança um turno no mundo.
        Aplica todas as regras do jogo: crescimento populacional, etc.

        :param mundo: Instância de Mundo
        """
        self.numero += 1
        total_nascimentos = 0

        # Aplicar crescimento populacional em todas as províncias
        for civ in mundo.civs:
            for provincia in civ.provincias:
                antes = provincia.get_populacao_total()
                provincia.aumentar_populacao()
                depois = provincia.get_populacao_total()
                total_nascimentos += (depois - antes)

        # Registrar no histórico
        registro = {
            "turno": self.numero,
            "nascimentos": total_nascimentos,
            "populacao_total": mundo.get_populacao_global()[2]
        }
        self.historico.append(registro)

        # Log opcional (pode ser removido ou controlado por DEBUG)
        # from shared.debug import DEBUG  # opcional
        # if DEBUG:
        print(f"\n--- Turno {self.numero} concluído ---")
        print(f"📊 +{total_nascimentos} nascimentos | População total: {registro['populacao_total']}")

    def resetar(self):
        """Reseta o contador de turnos (sem afetar o mundo)."""
        self.numero = 0
        self.historico.clear()
        print("🔁 Turnos resetados.")

    def get_ultimo_registro(self):
        """Retorna o último registro do histórico, ou None."""
        return self.historico[-1] if self.historico else None

    def __repr__(self):
        return f"<Turno {self.numero} | Histórico: {len(self.historico)} turnos>"