# shared/turn.py
"""
Módulo: shared/turn.py
Responsável por gerenciar a lógica de cada turno do jogo.
Atualmente:
- Atualiza a produtividade dos assentamentos
- Aplica crescimento populacional

Futuramente: pode incluir produção, eventos, IA, etc.
"""


class Turno:
    def __init__(self):
        self.numero = 0  # Turno atual (0 = pré-jogo)
        self.historico = []  # Histórico de eventos por turno

    def avancar(self, mundo):
        """
        Avança um turno no mundo.
        Aplica:
        1. Atualização da produtividade dos assentamentos
        2. Crescimento populacional
        3. Registro de estatísticas

        :param mundo: Instância de Mundo
        """
        self.numero += 1
        total_nascimentos = 0

        # --- 1. ATUALIZAR PRODUTIVIDADE DE TODOS OS ASSENTAMENTOS ---
        # Útil se houver mudanças ambientais, expansão, etc.
        for civ in mundo.civs:
            for assentamento in civ.assentamentos:
                assentamento.atualizar_produtividade(mundo)

        # --- 2. APLICAR CRESCIMENTO POPULACIONAL ---
        for civ in mundo.civs:
            for assentamento in civ.assentamentos:
                antes = assentamento.get_populacao_total()
                assentamento.aumentar_populacao()
                depois = assentamento.get_populacao_total()
                total_nascimentos += max(0, depois - antes)  # Evita valores negativos

        # --- 3. REGISTRAR NO HISTÓRICO ---
        populacao_total = mundo.get_populacao_global()[2]
        registro = {
            "turno": self.numero,
            "nascimentos": total_nascimentos,
            "populacao_total": populacao_total
        }
        self.historico.append(registro)

        # --- 4. LOG VISUAL ---
        print(f"\n--- Turno {self.numero} concluído ---")
        print(f"📊 +{total_nascimentos} nascimentos | População total: {populacao_total}")

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