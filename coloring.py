from simpleai.search import CspProblem, backtrack

def constraint_func(names, values):
    return values[0] != values[1]

def solve_coloring_problem(provinces, adjacency_list):
    domains = {province: ['Light Green', 'Light Blue', 'Light Yellow', 'Light Orange', 'Light Pink'] for province in provinces}
    # Thiết lập các ràng buộc màu cho các cặp tỉnh liền kề nhau
    constraints = [(pair, constraint_func) for pair in adjacency_list]
    problem = CspProblem(provinces, domains, constraints)
    return backtrack(problem)
