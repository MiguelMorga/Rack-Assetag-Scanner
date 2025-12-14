#!/usr/bin/env python3

# ======================================
# IMPORTS
# ======================================
import paramiko
import time
import os


# ======================================
# CONFIGURACIÓN SSH
# ======================================
PROMPT = "RScmCli#"
USER = os.getenv("SSH_USERNAME")
PASS = os.getenv("SSH_PASSWORD")


# ======================================
# ESPERA DE PROMPT
# ======================================
def esperar_prompt(shell, prompt, timeout=10):
    shell.settimeout(timeout)
    buffer = ""
    start_time = time.time()

    while True:
        if shell.recv_ready():
            buffer += shell.recv(1024).decode("utf-8", errors="ignore")
            if prompt in buffer:
                return buffer

        if time.time() - start_time > timeout:
            raise TimeoutError(
                f"No se recibió el prompt '{prompt}' en {timeout} segundos."
            )

        time.sleep(0.01)


# ======================================
#  ESCANEO DE ASSET TAGS (CT 2–9, 25–34)
# ======================================
def main():
    ip = input("Introduce la IP de una RSCM: ").strip()
    indices = [
        2, 3, 4, 5, 6, 7, 8, 9,
        25, 26, 27, 28, 29, 30, 31, 32, 33, 34
    ]
    asset_tags = []

    if not USER or not PASS:
        print("Error: variables SSH_USERNAME o SSH_PASSWORD no definidas")
        return

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print(f"Conectando a {ip}...\n")
        ssh.connect(ip, username=USER, password=PASS, timeout=8)

        shell = ssh.invoke_shell()
        esperar_prompt(shell, PROMPT, timeout=10)

        for i_num in indices:
            comando = f"show system fru -i {i_num}\n"
            shell.send(comando)
            output = esperar_prompt(shell, PROMPT, timeout=10)

            asset_tag_line = ""
            for linea in output.splitlines():
                if "AssetTag:" in linea:
                    asset_tag_line = linea.strip()
                    break

            print(f"CT {i_num} {asset_tag_line}")

            valor = (
                asset_tag_line.split("AssetTag:")[-1].strip()
                if "AssetTag:" in asset_tag_line
                else ""
            )
            asset_tags.append(valor)

        print("\nImprimiendo para copiar y pegar:")
        for tag in asset_tags:
            print(tag)

        shell.close()
        ssh.close()

    except Exception as e:
        print(f"\nError: {e}")


# ======================================
# MAIN
# ======================================
if __name__ == "__main__":
    main()
