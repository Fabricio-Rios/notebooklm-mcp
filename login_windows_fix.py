"""
Login do notebooklm com correção do event loop no Windows.

Problema: importar a CLL do notebooklm troca a política do asyncio para
WindowsSelectorEventLoopPolicy (provavelmente via o SDK do MCP). O SelectorEventLoop
NÃO cria subprocessos no Windows, então o Playwright falha ao iniciar o driver do
navegador com NotImplementedError em _make_subprocess_transport.

Correção: depois que a CLL é importada (o que troca a política), forçamos de volta
o WindowsProactorEventLoopPolicy — que suporta subprocessos — antes de rodar o login.

Uso:
    uv run python login_windows_fix.py
"""
import asyncio
import sys

# 1. Importa a CLL — este import é o que troca a política para Selector.
import notebooklm.notebooklm_cli as cli_mod

# 2. Reverte para Proactor (necessário para o Playwright abrir o navegador no Windows).
asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# 3. Executa o comando de login como se fosse a CLL normal.
sys.argv = ["notebooklm", "login"]
cli_mod.main()
