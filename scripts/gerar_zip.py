"""
Gera o arquivo ZIP de entrega do projeto EasySplit.
Uso: python scripts/gerar_zip.py [nome_grupo]
Exemplo: python scripts/gerar_zip.py Grupo1
"""

import os
import sys
import zipfile
from pathlib import Path

# Padrões a excluir do ZIP (matches de nome de arquivo/pasta)
EXCLUDE_DIRS = {
    "venv",
    "__pycache__",
    ".git",
    ".pytest_cache",
    ".mypy_cache",
    ".vscode",
    ".idea",
    ".copilot",
    ".cursor",
    ".windsurf",
    ".cline",
    "dist",
    "build",
    "htmlcov",
    ".aider.tags.cache.v3",
}

EXCLUDE_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".db",
    ".sqlite3",
    ".coverage",
    ".egg-info",
}

EXCLUDE_FILES = {
    ".env",
    "easysplit.db",
}


def should_exclude(path: Path) -> bool:
    """Retorna True se o caminho deve ser excluído do ZIP."""
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
        if part.startswith(".aider"):
            return True

    if path.suffix in EXCLUDE_EXTENSIONS:
        return True

    if path.name in EXCLUDE_FILES:
        return True

    if path.suffix in (".egg-info",) or ".egg-info" in path.name:
        return True

    return False


def criar_zip(nome_grupo: str) -> Path:
    raiz = Path(__file__).resolve().parent.parent
    nome_arquivo = f"{nome_grupo}_EasySplit.zip"
    destino = raiz / nome_arquivo

    arquivos_incluidos = 0
    with zipfile.ZipFile(destino, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for caminho in sorted(raiz.rglob("*")):
            # Ignorar o próprio ZIP de saída
            if caminho == destino:
                continue

            relativo = caminho.relative_to(raiz)

            if should_exclude(relativo):
                continue

            if caminho.is_file():
                zf.write(caminho, relativo)
                arquivos_incluidos += 1
                print(f"  + {relativo}")

    print(f"\nZIP gerado: {destino}")
    print(f"Total de arquivos incluídos: {arquivos_incluidos}")
    return destino


def validar_zip(caminho_zip: Path) -> None:
    """Valida que arquivos obrigatórios estão presentes no ZIP."""
    obrigatorios = [
        "app.py",
        "requirements.txt",
        ".env.example",
    ]
    pastas_obrigatorias = [
        "models/",
        "routes/",
        "services/",
        "forms/",
        "templates/",
        "static/",
        "tests/",
    ]

    with zipfile.ZipFile(caminho_zip) as zf:
        nomes = set(zf.namelist())

    print("\nValidação do ZIP:")
    ok = True

    for arq in obrigatorios:
        encontrado = arq in nomes
        status = "OK" if encontrado else "FALTANDO"
        print(f"  [{status}] {arq}")
        if not encontrado:
            ok = False

    for pasta in pastas_obrigatorias:
        encontrado = any(n.startswith(pasta) for n in nomes)
        status = "OK" if encontrado else "FALTANDO"
        print(f"  [{status}] {pasta}")
        if not encontrado:
            ok = False

    if ok:
        print("\nZIP validado com sucesso!")
    else:
        print("\nATENÇÃO: Alguns arquivos obrigatórios estão faltando no ZIP.")


if __name__ == "__main__":
    nome_grupo = sys.argv[1] if len(sys.argv) > 1 else "Grupo1"
    caminho = criar_zip(nome_grupo)
    validar_zip(caminho)
