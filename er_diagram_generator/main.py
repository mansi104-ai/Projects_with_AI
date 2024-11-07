import streamlit as st
import graphviz
import base64
from io import BytesIO

# Define Streamlit UI
st.title("Enhanced ER Diagram Generator")

st.sidebar.header("Define Entities")
num_entities = st.sidebar.number_input("Number of Entities", min_value=1, value=2, step=1)

entities = {}
for i in range(num_entities):
    entity_name = st.sidebar.text_input(f"Entity {i+1} Name", f"Entity_{i+1}")
    num_attributes = st.sidebar.number_input(f"Number of attributes for {entity_name}", min_value=0, value=1, step=1)
    
    attributes = []
    for j in range(int(num_attributes)):
        attr_name = st.sidebar.text_input(f"{entity_name} - Attribute {j+1}", f"attr_{j+1}")
        if attr_name.strip():  # Only add non-empty attribute names
            attributes.append(attr_name)
        
    if entity_name.strip():  # Only add non-empty entity names
        entities[entity_name] = attributes

st.sidebar.header("Define Relationships")
num_relationships = st.sidebar.number_input("Number of Relationships", min_value=0, value=1, step=1)

relationships = []
for i in range(int(num_relationships)):
    entity1 = st.sidebar.selectbox(f"Relationship {i+1} - Entity 1", options=list(entities.keys()), key=f"rel_entity1_{i}")
    entity2 = st.sidebar.selectbox(f"Relationship {i+1} - Entity 2", options=list(entities.keys()), key=f"rel_entity2_{i}", index=1)
    rel_name = st.sidebar.text_input(f"Relationship {i+1} Name", f"Rel_{i+1}", key=f"rel_name_{i}")
    
    # Only add relationship if both entities and relationship name are non-empty
    if entity1.strip() and entity2.strip() and rel_name.strip():
        relationships.append((entity1, entity2, rel_name))

# Generate Enhanced ER Diagram
def generate_er_diagram(entities, relationships):
    dot = graphviz.Digraph()

    # Add entities (rectangles with distinct colors)
    for entity, attrs in entities.items():
        dot.node(entity, label=entity, shape="rectangle", style="filled", color="lightblue")

        for attr in attrs:
            attr_node = f"{entity}_{attr}"
            dot.node(attr_node, label=attr, shape="ellipse", style="filled", color="lightpink", fontcolor="black")
            dot.edge(attr_node, entity)  # Connect attribute to entity

    # Add relationships (diamonds with distinct colors)
    for entity1, entity2, rel_name in relationships:
        rel_node = f"{entity1}_{entity2}_{rel_name}"
        dot.node(rel_node, label=rel_name, shape="diamond", style="filled", color="lightgray", fontcolor="black")
        dot.edge(entity1, rel_node)
        dot.edge(rel_node, entity2)

    return dot

# Convert diagram to PNG and PDF for download
def convert_dot_to_bytes(dot, format="png"):
    img_data = dot.pipe(format=format)
    return img_data

# Display Diagram and provide download options
if st.button("Generate ER Diagram"):
    er_diagram = generate_er_diagram(entities, relationships)
    st.graphviz_chart(er_diagram)

    # Convert to PNG
    png_bytes = convert_dot_to_bytes(er_diagram, format="png")
    st.download_button(label="Download as PNG", data=png_bytes, file_name="er_diagram.png", mime="image/png")

    # Convert to PDF
    pdf_bytes = convert_dot_to_bytes(er_diagram, format="pdf")
    st.download_button(label="Download as PDF", data=pdf_bytes, file_name="er_diagram.pdf", mime="application/pdf")

    # Generate link to Streamlit app
    st.write("Shareable Link:")
    app_url = st.text_input("Enter your Streamlit app URL:", "https://share.streamlit.io/your_username/your_app")
    if app_url:
        st.markdown(f"[Click here to open the app]({app_url})")
