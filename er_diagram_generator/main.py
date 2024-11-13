import streamlit as st
import graphviz
import ast

# Define Streamlit UI
st.title("Enhanced ER Diagram Generator")

# Set max limits for entities and attributes
MAX_ENTITIES = 10
MAX_ATTRIBUTES = 5

# Add a file uploader for text files
st.subheader("Upload a Text File for Automatic ER Diagram Generation")
uploaded_file = st.file_uploader("Choose a text file", type="txt")

# Initialize entities and relationships
entities = {}
relationships = []

# Process uploaded file if present
if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    try:
        # Parse the file content as a dictionary
        data = ast.literal_eval(content)

        # Validate and extract entities and relationships from the file
        if isinstance(data, dict) and "entities" in data and "relationships" in data:
            if isinstance(data["entities"], dict) and isinstance(data["relationships"], list):
                entities.update(data["entities"])
                relationships.extend(data["relationships"])
                st.success("Entities and relationships successfully extracted from the file.")
            else:
                st.error("Invalid file format: 'entities' should be a dictionary, and 'relationships' should be a list.")
        else:
            st.error("Invalid file format: Ensure the file has 'entities' and 'relationships' as top-level keys.")
    except (ValueError, SyntaxError) as e:
        st.error(f"Error processing the file: {e}. Ensure it's a valid dictionary format.")

# Sidebar inputs for defining additional entities manually
st.sidebar.header("Define Additional Entities")
num_entities = st.sidebar.number_input(
    "Number of Additional Entities", min_value=1, max_value=MAX_ENTITIES, value=2, step=1
)

# Collect additional entities from sidebar inputs
for i in range(num_entities):
    entity_name = st.sidebar.text_input(f"Entity {i+1} Name", f"Entity_{i+1}")
    num_attributes = st.sidebar.number_input(
        f"Number of attributes for {entity_name}",
        min_value=0,
        max_value=MAX_ATTRIBUTES,
        value=1,
        step=1,
    )
    
    attributes = []
    for j in range(int(num_attributes)):
        attr_name = st.sidebar.text_input(f"{entity_name} - Attribute {j+1}", f"attr_{j+1}")
        if attr_name.strip():
            attributes.append(attr_name)
        
    if entity_name.strip():
        entities[entity_name] = attributes

# Sidebar inputs for defining additional relationships
st.sidebar.header("Define Additional Relationships")
num_relationships = st.sidebar.number_input(
    "Number of Additional Relationships", min_value=0, max_value=MAX_ENTITIES, value=1, step=1
)

for i in range(int(num_relationships)):
    entity1 = st.sidebar.selectbox(f"Relationship {i+1} - Entity 1", options=list(entities.keys()), key=f"rel_entity1_{i}")
    entity2 = st.sidebar.selectbox(f"Relationship {i+1} - Entity 2", options=list(entities.keys()), key=f"rel_entity2_{i}", index=1)
    rel_name = st.sidebar.text_input(f"Relationship {i+1} Name", f"Rel_{i+1}", key=f"rel_name_{i}")
    relation_type = st.sidebar.selectbox(f"Relationship Type", ["One-to-One", "One-to-Many", "Many-to-Many"], key=f"rel_type_{i}")
    
    if entity1.strip() and entity2.strip() and rel_name.strip():
        relationships.append((entity1, entity2, rel_name, relation_type))

# Generate Enhanced ER Diagram with Many-to-Many support
def generate_er_diagram(entities, relationships):
    dot = graphviz.Digraph()

    # Set bounding box constraints and layout options
    dot.attr(size="8,8", ratio="fill", rankdir="LR")  # Fixed size, left-right layout

    # Add entities with convention as in the image
    for entity, attrs in entities.items():
        # Define entity as a table with a title and list of attributes
        label = f"<<TABLE BORDER='0' CELLBORDER='1' CELLSPACING='0'><TR><TD><B>{entity}</B></TD></TR>"
        for attr in attrs:
            label += f"<TR><TD>{attr}</TD></TR>"
        label += "</TABLE>>"
        dot.node(entity, label=label, shape="plaintext")

    # Add relationships with convention matching image and support for many-to-many
    for entity1, entity2, rel_name, relation_type in relationships:
        if relation_type == "Many-to-Many":
            # Create intermediary relationship node for many-to-many
            rel_node = f"{entity1}_{entity2}_{rel_name}"
            dot.node(rel_node, label=rel_name, shape="diamond", style="filled", color="lightgray", fontcolor="black", width="0.75", height="0.25")
            dot.edge(entity1, rel_node, arrowhead="none")
            dot.edge(rel_node, entity2, arrowhead="none")
        else:
            # For one-to-one and one-to-many, use direct edges
            rel_node = f"{entity1}_{entity2}_{rel_name}"
            dot.node(rel_node, label=rel_name, shape="diamond", style="filled", color="lightgray", fontcolor="black", width="0.75", height="0.25")
            dot.edge(entity1, rel_node, arrowhead="none")
            dot.edge(rel_node, entity2, arrowhead="none")

    return dot

# Convert diagram to PNG and PDF for download
def convert_dot_to_bytes(dot, format="png"):
    img_data = dot.pipe(format=format)
    return img_data

# Display Diagram and provide download options
if st.button("Generate ER Diagram"):
    # Generate diagram using combined entities and relationships
    er_diagram = generate_er_diagram(entities, relationships)
    st.graphviz_chart(er_diagram)

    # Convert to PNG
    png_bytes = convert_dot_to_bytes(er_diagram, format="png")
    st.download_button(label="Download as PNG", data=png_bytes, file_name="er_diagram.png", mime="image/png")

    # Convert to PDF
    pdf_bytes = convert_dot_to_bytes(er_diagram, format="pdf")
    st.download_button(label="Download as PDF", data=pdf_bytes, file_name="er_diagram.pdf", mime="application/pdf")

# # Shareable Link for Streamlit app
# st.write("Shareable Link:")
# app_url = st.text_input("Enter your Streamlit app URL:", "https://share.streamlit.io/your_username/your_app")
# if app_url:
#     st.markdown(f"[Click here to open the app]({app_url})")
