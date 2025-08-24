# consolidar.py
import os
from pathlib import Path

# ⚙️ CONFIGURAÇÕES
PROJECT_ROOT = "."                   # Diretório raiz do projeto
OUTPUT_FILE = "scripts.txt"          # Nome do arquivo de saída
FILE_EXTENSIONS = {".py"}            # Extensões incluídas no conteúdo
INCLUDE_DIRS = [
    "server",
    "client",
    "shared"
]  # Diretórios principais a varrer
EXCLUDE_FILES = {
    "consolidar.py",
    "merge_to_txt.py",
    "__pycache__",
    ".pyc",
    ".git",
    ".txt",
    ".pyo",
    ".pyd",
    ".egg-info",
    "dist",
    "build",
    "flags",
    "naming",
    "__init__",
    ".png",
    ".json"
}  # Nomes ou substrings para ignorar

# Cabeçalho do arquivo gerado
HEADER = f"""\
ARQUIVO DE CÓDIGO CONSOLIDADO
Gerado em: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Diretório: {os.path.abspath(PROJECT_ROOT)}
Conteúdo dos scripts principais reunidos.

{'='*80}
"""

def should_include(path: Path) -> bool:
    """Verifica se o caminho (arquivo ou pasta) deve ser incluído na estrutura ou leitura."""
    path_str = str(path)
    if any(ex in path_str for ex in EXCLUDE_FILES):
        return False
    return True

def build_project_tree(root_dir: Path, prefix: str = "") -> list:
    """
    Gera uma representação em árvore dos diretórios e arquivos.
    Retorna uma lista de strings (linhas).
    """
    lines = []
    try:
        entries = sorted([e for e in root_dir.iterdir() if should_include(e)],
                         key=lambda e: (e.is_file(), e.name.lower()))

        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            branch = "└── " if is_last else "├── "
            lines.append(f"{prefix}{branch}{entry.name}")

            if entry.is_dir():
                extension = "    " if is_last else "│   "
                lines.extend(build_project_tree(entry, prefix + extension))
    except PermissionError:
        lines.append(f"{prefix}├── [Sem permissão para ler]")
    except Exception as e:
        lines.append(f"{prefix}├── [Erro: {e}]")
    return lines

def merge_scripts():
    project_path = Path(PROJECT_ROOT).resolve()

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as output:
        # Escreve o cabeçalho
        output.write(HEADER)

        # === ESTRUTURA DO PROJETO ===
        separator = "=" * 80
        output.write(f"\n{separator}\n")
        output.write("📁 ESTRUTURA DO PROJETO\n")
        output.write(f"{separator}\n\n")

        tree_lines = ["📁 ."]
        for directory in INCLUDE_DIRS:
            dir_path = project_path / directory
            if dir_path.exists() and should_include(dir_path):
                # Adiciona diretório principal
                tree_lines.append(f"├── {directory}")
                # Adiciona conteúdo do diretório
                subdir_lines = build_project_tree(dir_path, "│   ")
                tree_lines.extend(subdir_lines)
            else:
                tree_lines.append(f"├── {directory}/ (não encontrado ou ignorado)")

        output.write("\n".join(tree_lines))
        output.write(f"\n\n{separator}\n")

        # === CONTEÚDO DOS ARQUIVOS ===
        output.write("📄 CONTEÚDO DOS ARQUIVOS\n")
        output.write(f"{separator}\n")

        count = 0
        for directory in INCLUDE_DIRS:
            dir_path = project_path / directory
            if not dir_path.exists():
                warning = f"\n❌ Diretório não encontrado: {dir_path}"
                output.write(warning)
                print(f"⚠️ Diretório não encontrado: {dir_path}")
                continue

            for file_path in dir_path.rglob("*"):
                if file_path.is_file() and should_include(file_path) and file_path.suffix in FILE_EXTENSIONS:
                    rel_path = file_path.relative_to(project_path)
                    file_header = f"\n{separator}\n📄 {rel_path}\n{separator}\n"

                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        output.write(file_header)
                        output.write(content)
                        output.write("\n")
                        print(f"✅ Adicionado: {rel_path}")
                        count += 1
                    except Exception as e:
                        error_msg = f"\n❌ Erro ao ler {rel_path}: {e}\n"
                        output.write(error_msg)
                        print(error_msg.strip())

        # Resumo final
        final_summary = f"\n{separator}\n✅ Total de {count} arquivos incluídos.\n{separator}"
        output.write(final_summary)
        print(f"\n🎉 Arquivo consolidado criado: ./{OUTPUT_FILE}")

if __name__ == "__main__":
    merge_scripts()