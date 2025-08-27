import networkx as nx

def name_numbers(numbers:list[int])->str:
    return "-".join(map(str,map(int,sorted(numbers))))

def get_roots(number_graph: nx.DiGraph, name:str)->list[str]:
    if name not in number_graph.nodes:
        return []
    roots = [node for node in nx.ancestors(number_graph, name) if number_graph.in_degree(node)==0]
    return roots

def get_last_steps(number_graph:nx.DiGraph, name:str, target:int)->list[str]:
    return [node for node in nx.descendants(number_graph,name) if number_graph.nodes[node]["rank"] == 2 and number_graph.nodes[node]["solutions"][target] > 0]

def get_parents(number_graph: nx.DiGraph, name:str)->list[str]:
    if name not in number_graph.nodes:
        return []
    return list(number_graph.predecessors(name))

def describe_node(number_graph: nx.DiGraph, name:str) -> None:
    if name not in number_graph.nodes:
        print(f"Node {name} not found")
        return
    
    node = number_graph.nodes[name]
    roots = get_roots(number_graph, name)
    parents = get_parents(number_graph, name)
    print(f"Node: {name}")
    print(f"  Rank: {node['rank']}")
    print(f"  Roots: {', '.join(sorted(list(roots)))}")
    print(f"  Root Count: {len(roots)}")
    print(f"  Parents: {', '.join(sorted(list(parents)))}")
    print(f"  Parent Count: {len(parents)}")
    print(f"  Solutions: {node['solutions']}")
    print(f"  Outgoing edges:")
    for edge in number_graph.out_edges(name, data=True):
        equations = ", ".join(edge[2]["equation"])
        print(f"    To {edge[1]} via {equations}")
    print(f"  Incoming edges:")
    for edge in number_graph.in_edges(name, data=True):
        equations = ", ".join(edge[2]["equation"])
        print(f"    From {edge[0]} via {equations}")