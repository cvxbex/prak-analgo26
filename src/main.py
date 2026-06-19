import json
import os
import time
import argparse
from algorithms import greedy_tsp, exact_tsp_branch_and_bound
from cost import calculate_tco

def load_data(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} tidak ditemukan.")
        exit(1)
        
    with open(filepath, 'r') as f:
        data = json.load(f)
        
    desc = data.get('description', 'Dataset Default')
        
    return (data['locations'], 
            data['package_weights'], 
            data['distance_matrix'], 
            data['scenarios'],
            desc)

def print_route(locations, route):
    route_names = [locations[i] for i in route]
    print(" -> ".join(route_names))

def run_simulation(scenario_name, fuel_price, locations, package_weights, distance_matrix, desc):
    print(f"\n{'='*60}")
    print(f"MENJALANKAN SKENARIO: {scenario_name.upper()} (Harga BBM: Rp {fuel_price}/liter)")
    print(f"DATASET: {desc}")
    print(f"{'='*60}")
    
    print("\n[ALGORITMA A - HEURISTIK (GREEDY)]")
    start_time_a = time.perf_counter()
    route_a, dist_a = greedy_tsp(distance_matrix, start_node=0)
    end_time_a = time.perf_counter()
    exec_time_ms_a = (end_time_a - start_time_a) * 1000
    
    tco_a, fuel_a, comp_a = calculate_tco(route_a, distance_matrix, package_weights, fuel_price, exec_time_ms_a)
    
    print("Urutan Rute:")
    print_route(locations, route_a)
    print(f"Jarak Tempuh Murni    : {dist_a:.2f} km")
    print(f"Waktu Eksekusi        : {exec_time_ms_a:.4f} ms")
    print(f"Biaya BBM             : Rp {fuel_a:,.2f}")
    print(f"Biaya Komputasi       : Rp {comp_a:,.2f}")
    print(f"TCO (Total Cost)      : Rp {tco_a:,.2f}")
    
    print("\n[ALGORITMA B - EKSAK (DFS PRUNING)]")
    start_time_b = time.perf_counter()
    route_b, dist_b = exact_tsp_branch_and_bound(distance_matrix, package_weights, start_node=0)
    end_time_b = time.perf_counter()
    exec_time_ms_b = (end_time_b - start_time_b) * 1000
    
    tco_b, fuel_b, comp_b = calculate_tco(route_b, distance_matrix, package_weights, fuel_price, exec_time_ms_b)
    
    print("Urutan Rute:")
    print_route(locations, route_b)
    print(f"Jarak Tempuh Murni    : {dist_b:.2f} km")
    print(f"Waktu Eksekusi        : {exec_time_ms_b:.4f} ms")
    print(f"Biaya BBM             : Rp {fuel_b:,.2f}")
    print(f"Biaya Komputasi       : Rp {comp_b:,.2f}")
    print(f"TCO (Total Cost)      : Rp {tco_b:,.2f}")
    
    print(f"\n{'='*60}")
    print("KESIMPULAN SKENARIO")
    print(f"Selisih TCO: Rp {abs(tco_a - tco_b):,.2f}")
    if tco_a < tco_b:
        print(f"-> REKOMENDASI: Gunakan Algoritma Heuristik (Lebih hemat Rp {abs(tco_a - tco_b):,.2f})")
    elif tco_b < tco_a:
        print(f"-> REKOMENDASI: Gunakan Algoritma Eksak (Lebih hemat Rp {abs(tco_b - tco_a):,.2f})")
    else:
        print("-> REKOMENDASI: Keduanya menghasilkan TCO yang sama.")

def main():
    parser = argparse.ArgumentParser(description="Simulasi TCO Last-Mile Delivery")
    parser.add_argument('--scenario', type=str, choices=['subsidi', 'krisis', 'all'], default='all')
    parser.add_argument('--dataset', type=str, default='all', help='Nama file dataset (atau "all" untuk semua file)')
    args = parser.parse_args()
    
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    if args.dataset == 'all':
        dataset_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
        # Urutkan berdasarkan nama agar output lebih rapi
        dataset_files.sort()
    else:
        dataset_files = [args.dataset]
        
    if not dataset_files:
        print(f"Error: Tidak ada file JSON ditemukan di {data_dir}")
        return
        
    for idx, dataset_file in enumerate(dataset_files):
        if idx > 0:
            print("\n" + "*"*80 + "\n") # Separator antar dataset
            
        data_path = os.path.join(data_dir, dataset_file)
        
        try:
            locations, package_weights, distance_matrix, scenarios, desc = load_data(data_path)
        except Exception as e:
            print(f"Gagal memuat dataset {dataset_file}: {e}")
            continue
            
        print(f">>> MEMPROSES DATASET: {dataset_file} <<<")
        
        if args.scenario == 'all' or args.scenario == 'subsidi':
            run_simulation('subsidi', scenarios['subsidi'], locations, package_weights, distance_matrix, desc)
            
        if args.scenario == 'all' or args.scenario == 'krisis':
            run_simulation('krisis', scenarios['krisis'], locations, package_weights, distance_matrix, desc)

if __name__ == "__main__":
    main()
