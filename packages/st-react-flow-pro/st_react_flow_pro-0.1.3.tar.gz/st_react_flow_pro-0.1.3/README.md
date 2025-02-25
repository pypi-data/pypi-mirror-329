# st-react-flow-pro

Streamlit component that allows you to draw a DAG / Directed Acyclic Graph with abilitty to highlight active node. It's highly customizable since it's been written in React.js with ReactFlow package. 

## Installation instructions 

```sh
pip install st-react-flow-pro
```

or use 

```sh
pip install --index-url https://test.pypi.org/simple/ st-react-flow-pro==0.1.0
```

if above command doesn't work. 

## Usage instructions

```python
import streamlit as st
import time
from st_react_flow_pro import st_react_flow_pro

def main():
    st.title("ST React Flow Pro - Hierarchical Graph Traversal")

    initial_nodes = [
        {"id": "1", "data": {"label": "Start"}, "position": {"x": 100, "y": 0}},
        {"id": "2", "data": {"label": "Level 1 - A"}, "position": {"x": 300, "y": 100}},
        {"id": "3", "data": {"label": "Level 1 - B"}, "position": {"x": 100, "y": 200}},
        {"id": "4", "data": {"label": "Level 2 - A1"}, "position": {"x": 300, "y": 300}},
        {"id": "5", "data": {"label": "Level 2 - B1"}, "position": {"x": 500, "y": 200}},
        {"id": "6", "data": {"label": "Level 3 - A2"}, "position": {"x": 700, "y": 100}},
    ]

    initial_edges = [
        {"id": "e1-2", "source": "1", "target": "2"},
        {"id": "e1-3", "source": "1", "target": "3"},
        {"id": "e2-4", "source": "2", "target": "4"},
        {"id": "e3-5", "source": "3", "target": "5"},
        {"id": "e4-6", "source": "4", "target": "6"},
    ]

    if st.button("Reset Highlight Sequence"):
        st.session_state.node_index = 0
        st.rerun()

    if "node_index" not in st.session_state:
        st.session_state.node_index = 0

    if st.session_state.node_index < len(initial_nodes):
        current_node = initial_nodes[st.session_state.node_index]["id"]
        st.session_state.borderNodeId = current_node

        st.write(f"Highlighting node: {current_node}")

        st_react_flow_pro(
            initial_nodes,
            initial_edges,
            borderNodeId=st.session_state.borderNodeId,
            key="react_flow_instance"
        )

        if st.session_state.node_index < len(initial_nodes) - 1:
            time.sleep(2)
            st.session_state.node_index += 1
            st.rerun()
        else:
            st.write("Completed highlighting nodes.")
    else:
        st.write("Completed highlighting nodes.")

if __name__ == "__main__":
    main()

