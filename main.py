import re
import graphviz
import random

class Node:
    def __init__(self, label = None):
        self.label = label #id
        self.outgoing_edges = {} #出边终点（Node,weight）
        # 有向边列表，指向其他节点


    def add_edge_to(self, destination_node):
        #添加一个从当前节点到指定节点的有向边
        self.outgoing_edges.setdefault(destination_node,1)

    def update_edge_weight(self, destination_node):
        # 更新与指定节点的边的权重
        self.outgoing_edges[destination_node]+=1

# 输出有向图
def showDirectedGraph(graph,color='black', outputPath= './output/graph', Pathlist=None, Nodelist=None):
    # 创建 Graphviz 的 DiGraph 对象
    dot = graphviz.Digraph(comment='The Graph')

    # 遍历你的 nodes 字典，为每个节点添加到图中的节点和边

    for word, node in graph.items():
        dot.node(word, label=word)
        for edge,weight in node.outgoing_edges.items():
            dot.edge(word, edge.label, label='%s' % weight, color='black')
    if Pathlist != None:
        for i in range(0,len(Pathlist)-1):
            dot.edge(Pathlist[i].label, Pathlist[i+1].label, color='red')
    # 生成图片
    dot.render(outputPath, view=True, format = 'png')

# 查询桥接词
def queryBridgeWords(word1,word2,graph):
    bridgewords = []
    node1 = None
    node2 = None
    flag = 0
    for word, node in graph.items():
        if word1 == word:
            node1 = node
        if word2 == word:
            node2 = node
    if node1 == None:
        #print("no such a word as",word1)
        flag = 1
    if node2 == None:
        #print("no such a word as",word2)
        flag = 1
    if flag == 1:
        return None
    for edge1,weight1 in node1.outgoing_edges.items():
        for edge2,weight2 in edge1.outgoing_edges.items():
            if edge2 == node2:
                bridgewords.append(edge1)
    if(bridgewords):
        for bridegword in bridgewords:
            print(bridegword.label,"between",word1,"and",word2)
        return bridgewords
    else:
        print("no bridgeword between",word1,"and",word2)
        return None

def generateNewText(inputText,graph):
    words_new = re.findall(r'\b[A-Za-z]+\b', inputText)
    words_final = []
    for i in range( 0, len(words_new)-1,1 ):
        words_final.append(words_new[i])
        #words_new[i/i+1]为当前词和下一个词
        bridgewords = queryBridgeWords(words_new[i],words_new[i+1],graph)
        if ( bridgewords != None ):
            random_word = random.choice(bridgewords).label
            words_final.append(random_word)
    words_final.append(words_new[len(words_new)-1])
    for word in words_final:
        print(word,"",end='')
    return words_final

def calcShortest_path(graph, word1, word2 = None):
    node1 = graph[word1]
    distances = calcPathFrom(word1,graph)
    if word2 == None:
        for target,value in distances.items():
            print(node1.label,"到",target.label,"的距离为",value[0],"上一步为",value[1].label)
    else:
        node2 = graph[word2]
        Pathlist = []
        nodenow = node2
        while nodenow.label != None :
            Pathlist.insert(0,nodenow)
            nodenow = distances[nodenow][1]
        print("路径为:")
        print(node1.label,end='')
        for i in Pathlist[1:]:
            print("->",i.label,end='')
        print("距离为",distances[node2][0])
        showDirectedGraph(graph, 'red', './output/graph_path', Pathlist)

    return distances

def calcPathFrom(word,graph):
    start = graph[word]
    distances = {}  # 目标点，距离，上一步
    for worrd, node in graph.items():
        distances[node] = (float('infinity'), Node())
    distances[start] = (0, Node())

    # 创建一个优先队列，以便寻找下一个节点
    priority_queue = [(start, 0, Node())]  # 目标点，距离，上一步
    for target in priority_queue:
        current_node = target[0]
        current_distance = target[1]
        last_node = target[2]
        print("当前点:", current_node.label)
        for edge, weight in current_node.outgoing_edges.items():
            print(edge.label, ":", weight)
        if current_distance > distances[current_node][0]:
            continue
        # 遍历邻居
        for neighbor, weight in current_node.outgoing_edges.items():
            distance = current_distance + weight
            # 是否是更短路径？
            if distance < distances[neighbor][0]:
                distances[neighbor] = (distance, current_node)
                priority_queue.append((neighbor, distance, current_node))
                print("新节点", neighbor.label, ":", distance)
    return distances

def randomWalk(graph):
    random_node_label = random.choice(list(graph.keys()))
    node = graph[random_node_label]
    Pathlist = []
    print(node.label,end='')#保留
    while True:
        if node.outgoing_edges:
            neighbor = random.choice(list(node.outgoing_edges.keys()))
        else:
            break
        path = (node.label, neighbor.label)
        if path in Pathlist:
            break
        else:
            Pathlist.append(path)
            node = neighbor
        print("->", node.label, end='')#保留


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    nodes = {}
    with open('test.txt', 'r', encoding='utf-8') as file:
        content = file.read()
        # 进行匹配的正则表达式
        words = re.findall(r'\b[A-Za-z]+\b', content)
        nodelast = Node()
        nodenow = Node()
        for word in words:
            #print("本轮开始last=",nodelast.label,",now=",nodenow.label)
            if word not in nodes:
                nodes[word] = Node(word)
                nodenow = nodes[word]
                if (nodelast is not None) :
                    #print("last=", nodelast.label, ",now=", nodenow.label)
                    if (nodenow not in nodelast.outgoing_edges):
                        nodelast.add_edge_to(nodenow)
                    else:
                        nodelast.update_edge_weight(nodenow)
            else :
                nodenow = nodes[word]
                if (nodelast is not None) :
                    #print("last=", nodelast.label, ",now=", nodenow.label)
                    if (nodenow not in nodelast.outgoing_edges):
                        nodelast.add_edge_to(nodenow)
                    else:
                        nodelast.update_edge_weight(nodenow)
            nodelast = nodenow
            #print("本轮结束last=",nodelast.label,",now=",nodenow.label,"\n")

    # 查看已生成节点的信息
    # for word, node in nodes.items():
    #     print(f"节点: {word}")
    #     print("出边:")
    #     for edge,weight in node.outgoing_edges.items():
    #         print(f" - {edge.label}:{weight}")

    #showDirectedGraph(nodes)
    #queryBridgeWords('book',"without",nodes)
    inputText = "To out"
    generateNewText(inputText,nodes)
    #Path_dictionary = calcShortest_path(nodes, 'To')
    #Path_dictionary = calcShortest_path(nodes,'bank','pleasure')
    #randomWalk(nodes)
