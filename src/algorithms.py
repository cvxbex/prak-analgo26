def greedy_tsp(distance_matrix, start_node=0):
    n = len(distance_matrix)
    visited = [False] * n
    route = [start_node]
    visited[start_node] = True
    
    current_node = start_node
    
    for _ in range(n - 1):
        next_node = -1
        min_dist = float('inf')
        
        for i in range(n):
            if not visited[i] and distance_matrix[current_node][i] < min_dist:
                min_dist = distance_matrix[current_node][i]
                next_node = i
                
        route.append(next_node)
        visited[next_node] = True
        current_node = next_node
        
    route.append(start_node)
    
    total_dist = 0
    for i in range(len(route) - 1):
        total_dist += distance_matrix[route[i]][route[i+1]]
        
    return route, total_dist


def exact_tsp_branch_and_bound(distance_matrix, package_weights, start_node=0):
    n = len(distance_matrix)
    
    total_load = sum(package_weights)
    empty_ratio = 0.02
    max_ratio = 0.05
    factor_per_kg = (max_ratio - empty_ratio) / total_load if total_load > 0 else 0
    
    best_route, best_dist = greedy_tsp(distance_matrix, start_node)
    
    best_fuel_cost = 0.0
    curr_load = total_load
    for i in range(len(best_route) - 1):
        u = best_route[i]
        v = best_route[i+1]
        dist = distance_matrix[u][v]
        curr_ratio = empty_ratio + (curr_load * factor_per_kg)
        best_fuel_cost += dist * curr_ratio
        curr_load -= package_weights[v]
        
    best_route_final = list(best_route)
    best_pure_dist = best_dist
    
    def dfs(current_node, visited_count, current_fuel_cost, current_pure_dist, current_route, visited, current_load):
        nonlocal best_fuel_cost, best_route_final, best_pure_dist
        
        if current_fuel_cost >= best_fuel_cost:
            return
            
        if visited_count == n:
            dist_to_start = distance_matrix[current_node][start_node]
            curr_ratio = empty_ratio + (current_load * factor_per_kg)
            final_fuel_cost = current_fuel_cost + (dist_to_start * curr_ratio)
            
            if final_fuel_cost < best_fuel_cost:
                best_fuel_cost = final_fuel_cost
                best_route_final = current_route + [start_node]
                best_pure_dist = current_pure_dist + dist_to_start
            return
            
        for i in range(n):
            if not visited[i]:
                visited[i] = True
                current_route.append(i)
                
                dist = distance_matrix[current_node][i]
                curr_ratio = empty_ratio + (current_load * factor_per_kg)
                segment_fuel = dist * curr_ratio
                
                next_load = current_load - package_weights[i]
                
                dfs(i, visited_count + 1, current_fuel_cost + segment_fuel, current_pure_dist + dist, current_route, visited, next_load)
                
                current_route.pop()
                visited[i] = False
                
    visited = [False] * n
    visited[start_node] = True
    
    dfs(start_node, 1, 0.0, 0.0, [start_node], visited, total_load)
    
    return best_route_final, best_pure_dist
