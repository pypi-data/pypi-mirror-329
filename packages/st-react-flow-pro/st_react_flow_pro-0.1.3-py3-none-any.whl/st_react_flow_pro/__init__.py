from pathlib import Path
import time
import streamlit as st
import streamlit.components.v1 as components
import os

_RELEASE = True

def st_react_flow_pro(nodes, edges, borderNodeId=None, key=None):
    """
    A component that renders a React Flow visualization.
    """
    component_key = key if key is not None else f"react_flow_pro_{id(nodes)}"
    component_value = _st_react_flow_pro(
        nodes=nodes,
        edges=edges,
        borderNodeId=borderNodeId,
        key=component_key,
    )
    return component_value

root_dir = os.path.dirname(__file__)
build_dir = (Path(__file__).parent / "frontend/dist").absolute()

if _RELEASE:
    print(build_dir)
    _st_react_flow_pro = components.declare_component(
        "st_react_flow_pro",
        path=build_dir
    )


else:
    _st_react_flow_pro = components.declare_component(
        "discrete_slider",
        path=build_dir
    )



if not _RELEASE:
    st.title("ST React Flow Pro - Automated Highlight")

    initial_nodes = [
        {"id": "1", "data": {"label": "Start"}, "position": {"x": 100, "y": 0}},
        {"id": "2", "data": {"label": "Hamza LLM"}, "position": {"x": 100, "y": 100}},
        {"id": "3", "data": {"label": "Tool"}, "position": {"x": 100, "y": 200}},
        {"id": "4", "data": {"label": "The End"}, "position": {"x": 100, "y": 300}},
    ]


    initial_edges = [
        {"id": "e1-2", "source": "1", "target": "2"},
        {"id": "e2-3", "source": "2", "target": "3"},
        {"id": "e3-4", "source": "3", "target": "4"},
    ]

    # Optionally, add a reset button to force starting from the first node.
    if st.button("Reset Highlight Sequence"):
        st.session_state.node_index = 0
        st.rerun()

    # Initialize the current node index in session state if it doesn't exist.
    if "node_index" not in st.session_state:
        st.session_state.node_index = 0

    # Only proceed if we still have nodes left to highlight.
    if st.session_state.node_index < len(initial_nodes):
        # Use the current node index to set the borderNodeId.
        current_node = initial_nodes[st.session_state.node_index]["id"]
        st.session_state.borderNodeId = current_node

        st.write(f"Highlighting node: {current_node}")

        # Render the component with the current borderNodeId.
        st_react_flow_pro(
            initial_nodes,
            initial_edges,
            borderNodeId=st.session_state.borderNodeId,
            key="react_flow_instance"
        )

        # Only auto-update if this isn't the last node.
        if st.session_state.node_index < len(initial_nodes) - 1:
            time.sleep(2)
            st.session_state.node_index += 1
            st.rerun()
        else:
            st.write("Completed highlighting nodes.")
    else:
        st.write("Completed highlighting nodes.")
