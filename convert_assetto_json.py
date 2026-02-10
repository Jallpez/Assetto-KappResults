import json
import os
import sys

def convert_assetto_json(input_path, output_path):
    """Convierte JSON original de Assetto Corsa Server al formato de la web"""
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Construir mapa de CarId -> Driver info desde Cars
    car_map = {}
    for car in data.get('Cars', []):
        car_map[car['CarId']] = {
            'name': car['Driver']['Name'],
            'team': car['Driver'].get('Team', ''),
            'car': car.get('Model', ''),
            'skin': car.get('Skin', '')
        }
    
    # Procesar Results
    results = []
    for pos, r in enumerate(data.get('Result', []), 1):
        driver_name = r.get('DriverName', '')
        car_info = car_map.get(r.get('CarId', -1), {})
        
        results.append({
            'Position': pos,
            'DriverName': driver_name,
            'Team': car_info.get('team', ''),
            'Car': r.get('CarModel', car_info.get('car', '')),
            'BestLap': r.get('BestLap', 0),
            'TotalTime': r.get('TotalTime', 0),
            'NumLaps': r.get('NumLaps', 0),
            'HasPenalty': r.get('HasPenalty', False),
            'PenaltyTime': r.get('PenaltyTime', 0),
            'Disqualified': r.get('Disqualified', False),
            'GridPosition': r.get('GridPosition', 0)
        })
    
    # Procesar Laps
    laps = []
    for lap in data.get('Laps', []):
        laps.append({
            'DriverName': lap.get('DriverName', ''),
            'LapTime': lap.get('LapTime', 0),
            'Sectors': lap.get('Sectors', []),
            'Cuts': lap.get('Cuts', 0),
            'Tyre': lap.get('Tyre', ''),
            'Timestamp': lap.get('Timestamp', 0)
        })
    
    # Procesar Events (colisiones)
    events = []
    for event in data.get('Events', []):
        ev = {
            'Type': event.get('Type', ''),
            'CarId': event.get('CarId', 0),
            'ImpactSpeed': event.get('ImpactSpeed', 0),
            'Timestamp': event.get('Timestamp', 0)
        }
        driver_info = event.get('Driver', {})
        if driver_info:
            ev['DriverName'] = driver_info.get('Name', '')
            ev['Team'] = driver_info.get('Team', '')
        
        other_driver = event.get('OtherDriver', {})
        if other_driver:
            ev['OtherDriverName'] = other_driver.get('Name', '')
            ev['OtherTeam'] = other_driver.get('Team', '')
        
        events.append(ev)
    
    # Construir JSON final
    output = {
        'Results': results,
        'Laps': laps,
        'Events': events
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Convertido: {input_path} -> {output_path}")
    print(f"  Pilotos: {len(results)}, Vueltas: {len(laps)}, Eventos: {len(events)}")


def process_folder(folder):
    """Procesa todos los JSON originales de una carpeta"""
    for filename in os.listdir(folder):
        if filename.endswith('.json') and 'Race' not in filename:
            input_path = os.path.join(folder, filename)
            
            with open(input_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except:
                    print(f"Error leyendo {input_path}")
                    continue
            
            if 'Cars' in data and 'Result' in data:
                clean_name = filename.strip().replace('.json', '')
                output_path = os.path.join(folder, f"{clean_name} - Race.json")
                convert_assetto_json(input_path, output_path)
            else:
                print(f"Saltando {filename} (no es formato Assetto original)")


if __name__ == '__main__':
    folder = sys.argv[1] if len(sys.argv) > 1 else 'Copa_Clio'
    process_folder(folder)
