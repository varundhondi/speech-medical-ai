import networkx as nx
from pyvis.network import Network


def build_graph(symptoms, icd, cpt):

    G = nx.DiGraph()

    for s in symptoms:

        G.add_node(s, color="red")

        if icd[s]:

            disease = icd[s][0]["Title"]
            G.add_node(disease, color="orange")
            G.add_edge(s, disease)

            code = icd[s][0]["Code"]
            G.add_node(code, color="blue")
            G.add_edge(disease, code)

        if cpt[s]:

            procedure = cpt[s][0]["Description"]
            G.add_node(procedure, color="green")
            G.add_edge(code, procedure)

    net = Network(height="500px", width="100%", bgcolor="#0f172a", font_color="white")

    net.from_nx(G)

    net.save_graph("graph.html")

    return "graph.html"