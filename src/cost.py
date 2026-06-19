def calculate_tco(route, distance_matrix, package_weights, fuel_price, exec_time_ms):
    """
    Menghitung Total Cost of Ownership (TCO) berdasarkan rute.
    TCO = Biaya BBM + Biaya Komputasi Server
    """
    total_load = sum(package_weights)
    
    empty_ratio = 0.02
    max_ratio = 0.05
    
    if total_load > 0:
        factor_per_kg = (max_ratio - empty_ratio) / total_load
    else:
        factor_per_kg = 0

    current_load = total_load
    total_fuel_cost = 0.0
    
    for i in range(len(route) - 1):
        u = route[i]
        v = route[i+1]
        dist = distance_matrix[u][v]
        
        current_ratio = empty_ratio + (current_load * factor_per_kg)
        
        fuel_cost_segment = dist * current_ratio * fuel_price
        total_fuel_cost += fuel_cost_segment
        
        current_load -= package_weights[v]
        
    compute_cost = exec_time_ms * 50.0
    
    tco = total_fuel_cost + compute_cost
    
    return tco, total_fuel_cost, compute_cost
