import graphviz
graphviz.version()
import pydot
import requests
from bs4 import BeautifulSoup
import json
import time
# 하..... 이거 어려운 문제 주셨네. 일단 봉인된 코파일럿 켭니다.
class Graph :
    def __init__(self) :
        self.graph = {}
        
    def addEdge(self, u, v) :
        if u not in self.graph :
            self.graph[u] = []
        self.graph[u].append(v)
    
    def printGraph(self) :
        for u in self.graph :
            print(u, end=" : ")
            for v in self.graph[u] :
                print(v, end=" ")
            print()
            

transactionsUrl = "https://api.blockchain.info/haskoin-store/btc/transactions?txids="

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json",
    "Accept": "application"
}
baseUrl = "https://api.blockchain.info/haskoin-store/btc/address/%s/transactions?limit=10000&offset=0"
graph = Graph()
addressList = set()
addressList.add("394utAB8437aTjzfYJrtGcuj8cyNtGc57A")

def visit(index : int, depth : int) :
    if(len(addressList) == index) :
        return
    if depth == 0 :
        return
    address = list(addressList)[index]
    url = baseUrl %(address)
    
    

    response = requests.get(url, headers=headers).json()
    txidList = []
    for res in response :
        txidList.append(res["txid"])
    
    for txid in txidList :
        url = transactionsUrl + txid + ","
    url = url[:-1]
    # print(url)
    response = requests.get(url, headers=headers).json()
    for res in response :
        for input in res["inputs"] :
            addressList.add(input["address"])
            graph.addEdge(input["address"], address)
        for output in res["outputs"] :
            addressList.add(output["address"])
            graph.addEdge(address, output["address"])
            
    visit(index + 1, depth - 1)
    # print(graph.graph)
    
    # graph.printGraph()
    

visit(0, 5)
# graph.printGraph()
dot = pydot.Dot( graph_type="digraph", rankdir="LR")

# 그래프 생성
for (u, vList) in graph.graph.items() :
    if u == "394utAB8437aTjzfYJrtGcuj8cyNtGc57A" :
        pydot.Node(u, fillcolor='#FF0000')
    else : 
        pydot.Node(u)
    for v in vList :
        edge = pydot.Edge(u, v, arrowhead='vee')
        dot.add_edge(edge)
dot.write_png('graph_example_pydot.png')

