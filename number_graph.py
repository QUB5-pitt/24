from utils import name_numbers
import networkx as nx
import itertools

def add_numbers_to_number_graph(number_graph: nx.DiGraph, numbers:list[int])->None:
    #Determine the name of the node and add it if it doesn't exist
    name = name_numbers(numbers)

    #Return if we've already added this node
    if name in number_graph.nodes:
        return
    
    #Add the node
    number_graph.add_node(name)
    
    #Initialize the rank and solutions of this node
    number_graph.nodes[name]["solutions"] = {}
    number_graph.nodes[name]["rank"] = len(numbers)

    #Try all pairs of numbers and all operations on them to determine if we can reach 24
    for two in itertools.combinations(numbers, 2):
        remaining = list(numbers)
        remaining.remove(two[0])
        remaining.remove(two[1])

        val_lower = min(two)
        val_higher = max(two)

        equations = [f"{two[0]}+{two[1]}", f"{val_higher}-{val_lower}", f"{two[0]}*{two[1]}"]

        if val_lower!=0 and val_higher%val_lower==0:
            equations.append(f"{val_higher}/{val_lower}")

        for equation in equations:
            result = eval(equation)
            new_numbers = sorted(remaining+[result])
            new_name = name_numbers(new_numbers)
            add_numbers_to_number_graph(number_graph, new_numbers)
            number_graph.add_edge(name, new_name)
            number_graph.edges[(name,new_name)]["equation"] = equation

def build_number_graph(number_graph: nx.DiGraph, include_zero:bool=True):
    start = 0 if include_zero else 1
    for combination in itertools.combinations_with_replacement(range(start, 10), 4):
        add_numbers_to_number_graph(number_graph, list(combination))

def add_solutions_to_node(number_graph: nx.DiGraph, node_name:str, target:int=24)->int:
    #Have we already solved this one?
    if target in number_graph.nodes[node_name]["solutions"]:
        return number_graph.nodes[node_name]["solutions"][target]
    
    #If this is a rank 1 node, it can only solve itself
    if number_graph.nodes[node_name]["rank"] == 1:
        solutions = 1 if int(node_name) == target else 0
        number_graph.nodes[node_name]["solutions"][target] = solutions
        return solutions
    
    #Try all successors and sum their solutions
    solutions = 0
    for successor in number_graph.successors(node_name):
        solutions += add_solutions_to_node(number_graph, successor, target)
    number_graph.nodes[node_name]["solutions"][target] = solutions
    return solutions

def add_solutions_to_all_nodes(number_graph: nx.DiGraph, target:int=24):
    #Iterate over all nodes and add solutions for the target
    for node in number_graph.nodes:
        add_solutions_to_node(number_graph, node, target)

def add_all_solutions(number_graph: nx.DiGraph, targets:list[int]):
    #Iterate over all targets and add solutions for each
    for target in targets:
        add_solutions_to_all_nodes(number_graph, target)