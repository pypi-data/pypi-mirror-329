from typing import Dict, Any, Union


class Edge:
    def __init__(
        self,
        id: str,
        source: str,
        sourceHandle: str,
        target: str,
        targetHandle: str,
        animated: bool = True,
        type: str = "default",
    ) -> None:
        self.id: str = id
        self.source: str = source
        self.sourceHandle: str = sourceHandle
        self.target: str = target
        self.targetHandle: str = targetHandle
        self.animated: bool = animated
        self.type: str = type
        self.style: Dict[str, Union[str, int]] = {"stroke": "#28c5e5", "strokeWidth": 3}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "source": self.source,
            "sourceHandle": self.sourceHandle,
            "target": self.target,
            "targetHandle": self.targetHandle,
            "animated": self.animated,
            "type": self.type,
            "style": self.style,
            "data": {},
            "label": "",
        }
