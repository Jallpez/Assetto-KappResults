import json

with open('SuperGT/Ronda 4.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("VERIFICACIÓN TIEMPOS RONDA 4")
print("="*50)

for result in data['Result']:
    if result['NumLaps'] == 25:
        total_ms = result['TotalTime']
        total_seg = total_ms / 1000
        minutos = int(total_seg // 60)
        segundos = total_seg % 60
        
        print(f"{result['DriverName']:25} | {total_ms:8} ms | {minutos}:{segundos:06.3f}")
