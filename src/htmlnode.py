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