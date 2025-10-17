import serial
import csv
import time
from datetime import datetime

# ==== CONFIGURAÇÕES ====
PORTA = "COM8"      # Porta Serial
BAUDRATE = 9600      # Velocidade da porta
TIMEOUT_PARADA = 2.0  # Tempo em segundos sem dados para encerrar
ARQUIVO_CSV = "dados_serial.csv"
# =======================

def main():
    try:
        ser = serial.Serial(PORTA, BAUDRATE, timeout=0.1)
        print(f"Aguardando dados na porta {PORTA}...")

        # Espera até chegar o primeiro dado
        while True:
            if ser.in_waiting > 0:
                print("Dados detectados, iniciando coleta!")
                break

        ultimo_dado = time.time()
        ARQUIVO_CSV = 'SensorData' + datetime.now().strftime("%m_%d_%H_%M_%S") + '.csv'
        with open(ARQUIVO_CSV, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Dado"])

            while True:
                if ser.in_waiting > 0:
                    linha = ser.readline().decode(errors="ignore").strip()
                    if linha:
                        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                        writer.writerow([agora, linha])
                        print(f"{agora} - {linha}")
                        ultimo_dado = time.time()  # atualiza o tempo do último dado
                else:
                    # Se não chegou nada por um tempo, encerra
                    if time.time() - ultimo_dado > TIMEOUT_PARADA:
                        print("Nenhum dado recebido recentemente. Encerrando coleta.")
                        break

        print(f"Coleta finalizada. Dados salvos em {ARQUIVO_CSV}")

    except serial.SerialException as e:
        print(f"Erro ao acessar a porta serial: {e}")
    except KeyboardInterrupt:
        print("Execução interrompida pelo usuário.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Porta serial fechada.")

if __name__ == "__main__":
    main()
