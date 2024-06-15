import pytest
import re
from main import Node
from main import generateNewText

nodes = {}
with open('test.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    # 进行匹配的正则表达式
    words = re.findall(r'\b[A-Za-z]+\b', content)
    nodelast = Node()
    nodenow = Node()
    for word in words:
        # print("本轮开始last=",nodelast.label,",now=",nodenow.label)
        if word not in nodes:
            nodes[word] = Node(word)
            nodenow = nodes[word]
            if nodelast is not None:
                # print("last=", nodelast.label, ",now=", nodenow.label)
                if nodenow not in nodelast.outgoing_edges:
                    nodelast.add_edge_to(nodenow)
                else:
                    nodelast.update_edge_weight(nodenow)
        else:
            nodenow = nodes[word]
            if nodelast is not None:
                # print("last=", nodelast.label, ",now=", nodenow.label)
                if nodenow not in nodelast.outgoing_edges:
                    nodelast.add_edge_to(nodenow)
                else:
                    nodelast.update_edge_weight(nodenow)
        nodelast = nodenow
        # print("本轮结束last=",nodelast.label,",now=",nodenow.label,"\n")

# 查看已生成节点的信息
# for word, node in nodes.items():
#     print(f"节点: {word}")
#     print("出边:")
#     for edge,weight in node.outgoing_edges.items():
#         print(f" - {edge.label}:{weight}")

@pytest.mark.parametrize("text, expected_output",[
    ("Hello world", "Hello world"),
    ("Seek to explore new and exciting synergies", "Seek to explore strange new life and exciting synergies"),
    ("Zebra jumps", "Zebra jumps"),
    ("Seek to explore unknown territories", "Seek to explore unknown territories"),
    ("hello", "hello"),
    ("new and new and new","new life and new life and new")
])

def test_generateNewText(text, expected_output):
    result = generateNewText(text,nodes)
    result_str = ' '.join(result) 
    assert result_str == expected_output

