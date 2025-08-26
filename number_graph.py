from utils import name_numbers
import networkx as nx
import itertools

def add_numbers_to_number_graph(number_graph: nx.DiGraph, numbers:list[int], target:int=24)->int:
    #Determine the name of the node and add it if it doesn't exist
    name = name_numbers(numbers)
    number_graph.add_node(name)

    #Have we already solved this one?
    if "solutions" in number_graph.nodes[name]:
        return number_graph.nodes[name]["solutions"]
    
    #Store the rank and root of this node
    number_graph.nodes[name]["rank"] = len(numbers)

    #If there's only one number, check if it's 24
    if len(numbers)==1:
        val = 1 if numbers[0]==target else 0
        number_graph.nodes[name_numbers(numbers)]["solutions"] = val
        return val

    #Try all pairs of numbers and all operations on them to determine if we can reach 24
    solutions = 0
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
            new_solutions = add_numbers_to_number_graph(number_graph, new_numbers, target)
            
            number_graph.add_edge(name, new_name)
            if "equation" not in number_graph.edges[(name,new_name)]:
                number_graph.edges[(name,new_name)]["equation"] = set()
            number_graph.edges[(name,new_name)]["equation"].add(equation)
            solutions += new_solutions
    
    #Store the number of solutions found
    number_graph.nodes[name]["solutions"] = solutions
    return solutions

def build_number_graph(number_graph: nx.DiGraph, target:int=24):
    for combination in itertools.combinations_with_replacement(range(10), 4):
        name = name_numbers(combination)
        number_graph.add_node(name)
        add_numbers_to_number_graph(number_graph, list(combination), target)