class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        out_string = ""
        for key, value in self.props.items():
            out_string += f' {key}="{value}"'
        return out_string
    
    def __repr__(self):
        return f"Tag={self.tag}\nValue={self.value}\nChildren={self.children}\nProps={self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Error: Leaf nodes must have a value!")
        if self.tag is None:
            return self.value
        else:
            out_string = ""
            out_string += f"<{self.tag}"
            if self.props is not None:
                out_string += self.props_to_html()
            out_string += f">{self.value}</{self.tag}>"
            return out_string