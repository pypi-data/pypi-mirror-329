import json
from typing import List, Union

from .node import Node
from .edge import Edge


class Workflow:
    def __init__(self) -> None:
        self.nodes: List[Node] = []
        self.edges: List[Edge] = []

    def add_node(self, node: Node):
        self.nodes.append(node)

    def add_nodes(self, nodes: List[Node]):
        self.nodes.extend(nodes)

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

    def connect(
        self,
        source_node: Union[str, Node],
        source_port: str,
        target_node: Union[str, Node],
        target_port: str,
    ):
        # 获取源节点ID
        if isinstance(source_node, Node):
            source_node_id = source_node.id
        else:
            source_node_id = source_node

        # 获取目标节点ID
        if isinstance(target_node, Node):
            target_node_id = target_node.id
        else:
            target_node_id = target_node

        # 检查源节点是否存在
        source_node_exists = any(node.id == source_node_id for node in self.nodes)
        if not source_node_exists:
            raise ValueError(f"源节点不存在: {source_node_id}")

        # 检查目标节点是否存在
        target_node_exists = any(node.id == target_node_id for node in self.nodes)
        if not target_node_exists:
            raise ValueError(f"目标节点不存在: {target_node_id}")

        # 检查源节点的端口是否存在
        source_node_obj = next(node for node in self.nodes if node.id == source_node_id)
        if not source_node_obj.has_output_port(source_port):
            raise ValueError(f"源节点 {source_node_id} 不存在输出端口: {source_port}")

        # 检查目标节点的端口是否存在
        target_node_obj = next(node for node in self.nodes if node.id == target_node_id)
        if not target_node_obj.has_input_port(target_port):
            raise ValueError(f"目标节点 {target_node_id} 不存在输入端口: {target_port}")

        # 创建并添加边
        edge_id = f"vueflow__edge-{source_node_id}{source_port}-{target_node_id}{target_port}"
        edge = Edge(edge_id, source_node_id, source_port, target_node_id, target_port)
        self.add_edge(edge)

    def to_dict(self):
        return {
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
            "viewport": {"x": 0, "y": 0, "zoom": 1},
        }

    def to_json(self, ensure_ascii=False):
        return json.dumps(self.to_dict(), ensure_ascii=ensure_ascii)

    def to_mermaid(self) -> str:
        """生成 Mermaid 格式的流程图。

        Returns:
            str: Mermaid 格式的流程图文本
        """
        lines = ["flowchart TD"]

        # 创建节点类型到序号的映射
        type_counters = {}
        node_id_to_label = {}

        # 首先为所有节点生成标签
        for node in self.nodes:
            node_type = node.type.lower()
            if node_type not in type_counters:
                type_counters[node_type] = 0
            node_label = f"{node_type}_{type_counters[node_type]}"
            node_id_to_label[node.id] = node_label
            type_counters[node_type] += 1

        # 添加节点定义
        for node in self.nodes:
            node_label = node_id_to_label[node.id]
            lines.append(f'    {node_label}["{node_label} ({node.type})"]')

        lines.append("")  # 添加一个空行分隔节点和边的定义

        # 添加边的定义
        for edge in self.edges:
            source_label = node_id_to_label[edge.source]
            target_label = node_id_to_label[edge.target]
            label = f"{edge.sourceHandle} → {edge.targetHandle}"
            lines.append(f"    {source_label} -->|{label}| {target_label}")

        return "\n".join(lines)
