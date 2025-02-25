import platform
import subprocess
import time
import pyautogui
import psutil
import logging
pyautogui.USE_MOUSEINFO = False
log = logging.getLogger('__main__')

def obter_ip_conexao_rdp():
    """Retorna o ip da conexão RDP

    Returns:
        str: ip
    """
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    
        if proc.info['name'] == 'mstsc.exe' and proc.info['cmdline']:
    
            for arg in proc.info['cmdline']:
    
                if arg.startswith("/v:"):  # O argumento '/v:' contém o IP
    
                    return arg.replace("/v:", "").strip()
    
    return None

def conectar_rdp(host, usuario, senha):
    """Conecta via RDP em uma máquina remota
    
    Args:
    
            host (str): ip/host destino
        usuario (str): usuário
        senha (str): senha
    
    Returns:
        bool: True/False
    """
    
    sistema = platform.system()

    if sistema == "Windows":

        try:
            
            # Inicia o mstsc
            cmd_conexao = f"start mstsc /v:{host} /f"
            subprocess.run(cmd_conexao, shell=True)

            # Aguarda um tempo para verificar se a conexão foi feita
            time.sleep(3)  # Dá tempo para o usuário tentar logar
            pyautogui.typewrite(senha)
            pyautogui.press('enter')
            time.sleep(2)
            pyautogui.press('left')
            pyautogui.press('enter')
            time.sleep(5)
            return True
        
        except Exception as e:
            
            log.error(f"Falha ao tentar logar via RDP (Windows)\nErro: {str(e)}")
            return False
    
    elif sistema == "Linux":
        
        # Comando para executar a conexao com o xfreerdp
        # Para instalar: sudo apt install freerdp2-x11
        comando_rdp = f"""xfreerdp /u:{usuario} /p:{senha} /v:{host} /size:1920x1080"""

        # Executar o comando e capturar saída
        try:
            
            processo_rdp = subprocess.Popen(
                comando_rdp,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        
        except Exception as e:
        
            raise Exception(f"Falha ao executar o comando de conexão RDP no Linux. Você possui o xfreerdp instalado? (sudo apt install freerdp2-x11)\nErro: {str(e)}")
        
        # Aguarda 10 segundos, para aparecer o banner azul
        time.sleep(10)

        # Se a conexão foi bem-sucedida, retornar True
        if processo_rdp.poll() is None:
            
            # Clica no 'enter', no banner azul
            pyautogui.press('enter')
            return True

        else:

            return False
        
    else:

        raise Exception("Sistema operacional não suportado (Somente 'Windows' ou 'Linux').")

