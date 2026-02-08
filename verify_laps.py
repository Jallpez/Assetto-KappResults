import json

with open('SuperGT/Ronda 4.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

drivers = ['bertillo30', 'Jose Miguel Romay', 'Kappy Astur']

for driver_name in drivers:
    laps = [lap['LapTime'] for lap in data['Laps'] if lap['DriverName'] == driver_name]
    total = sum(laps)
    
    print(f"\n{driver_name}:")
    print(f"  Vueltas: {len(laps)}")
    print(f"  Total: {total} ms = {total/1000:.3f} seg")
    print(f"  Formato: {int(total/60000)}:{(total%60000)/1000:06.3f}")
    
    # Mostrar primeras 5 vueltas
    print(f"  Primeras 5 vueltas: {[f'{t/1000:.3f}' for t in laps[:5]]}")
