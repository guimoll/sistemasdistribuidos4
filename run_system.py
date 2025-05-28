import subprocess
import sys
import time
import os

def run_in_terminal(command, title):
    if sys.platform == "darwin":
        osascript = f'''
        tell application "Terminal"
            do script "cd {os.getcwd()} && {command}"
            set current settings of selected tab of front window to settings set "Pro"
            set custom title of selected tab of front window to "{title}"
        end tell
        '''
        subprocess.run(['osascript', '-e', osascript])
    elif sys.platform == "linux":
        subprocess.Popen(['gnome-terminal', '--title', title, '--', 'bash', '-c', f'cd {os.getcwd()} && {command}'])
    elif sys.platform == "win32":
        subprocess.Popen(['start', 'cmd', '/k', f'title {title} && cd {os.getcwd()} && {command}'], shell=True)

def main():
    # Lista de componentes para executar
    components = [
        ("python hospital_trauma.py", "Hospital de Trauma"),
        ("python hospital_medio.py", "Hospital Médio"),
        ("python upa.py", "UPA"),
        ("python ambulancia.py", "Ambulância")
    ]

    print("Iniciando o sistema de emergência...")
    print("Abrindo terminais para cada componente...")

    for command, title in components:
        run_in_terminal(command, title)
        time.sleep(1)
    
    print("\nSistema iniciado! Todos os componentes estão rodando.")
    print("\nInstruções:")
    print("1. Use o terminal da Ambulância para enviar mensagens")
    print("2. Formato das mensagens: prioridade;nome;observação")
    print("   Exemplo: vermelho;João Silva;Acidente de carro")
    print("3. Para encerrar, feche os terminais ou pressione Ctrl+C em cada um")
    print("\nPrioridades disponíveis:")
    print("- vermelho: casos graves (Hospital de Trauma)")
    print("- amarelo: casos médios (Hospital Médio)")
    print("- verde: casos leves (UPA)")

if __name__ == "__main__":
    main() 