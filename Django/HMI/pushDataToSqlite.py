import pandas as pd
import os
import sys
import django
from django.utils import timezone
import datetime

# Adicione o caminho do diretório-mãe ao sys.path
# Isso permite que o Python encontre o seu projeto Django 'HMI'
# O caminho é: 'D:\Users\Bolinfel\Documents\0-PRJ Sistema Bola Barra\Sistema-Bola-Barra\Django\HMI'
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'HMI')))
# O método abaixo é mais confiável pois não depende do caminho absoluto, mas sim do projeto raiz
# Suba dois níveis a partir de 'TestDataUpload' para chegar na pasta 'Django'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# Adicione o diretório raiz do projeto ao Python path para encontrar o 'HMI'
sys.path.append(project_root)

# Configurar o ambiente Django
# Agora o Python sabe onde encontrar 'HMI'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMI.settings')
django.setup()

from dashboard.models import Datalog

# O caminho para o banco de dados não é mais necessário, o Django cuida disso
# conn = sqlite3.connect(...) # Esta linha não é mais necessária

# get data from
df = pd.read_csv('Datalog - Folha2.csv')

# Padronizar os nomes das colunas para evitar erros de digitação ou capitalização
df.columns = df.columns.str.strip().str.upper()

# Limpar colunas não nomeadas
df = df.loc[:, ~df.columns.str.contains('^UNNAMED')]

# Opcional: Imprima as colunas para verificar se estão corretas
print("Colunas do DataFrame:", df.columns.tolist())

# Limpar a tabela antes de popular (opcional)
Datalog.objects.all().delete()

# Iterar sobre o DataFrame e criar objetos Datalog
for index, row in df.iterrows():
    try:
        timestamp_str = row['TIMESTAMP']
        timestamp_dt = datetime.datetime.strptime(timestamp_str, '%Y/%m/%d %H:%M:%S')
        timestamp_tz = timezone.make_aware(timestamp_dt)

        # Tratar vírgulas e converter para float antes de converter para int,
        # para evitar o erro de conversão
        servo_motor_raw_val = float(str(row['SERVO_MOTOR_RAW']).replace(',', '.'))
        servo_raw_val = float(str(row['SERVO_RAW']).replace(',', '.'))

        Datalog.objects.create(
            TIMESTAMP=timestamp_tz,
            SERVO_MOTOR_RAW=int(servo_motor_raw_val),
            SERVO_MOTOR_SCA=float(str(row['SERVO_MOTOR_SCA']).replace(',', '.')),
            SERVO_RAW=int(servo_raw_val),
            SERVO_SCA=float(str(row['SERVO_SCA']).replace(',', '.')),
            ARDUINO_RPI_STATUS=bool(int(row['ARDUINO_RPI_STATUS'])),
            ARDUINO_STATUS=bool(int(row['ARDUINO_STATUS'])),
            RPI_STATUS=bool(int(row['RPI_STATUS']))
        )
    except (ValueError, TypeError) as e:
        print(f"Erro ao processar a linha {index}: {e}")
        continue
    
print("Importação concluída com sucesso! 🎉")
