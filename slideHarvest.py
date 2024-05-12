import streamlit as st
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, PromptTemplate
from llama_index.core.program import LLMTextCompletionProgram
from typing import List
from pydantic import BaseModel, Field
import openai
from llama_index.llms.openai import OpenAI
from pptx.util import Inches
import base64
from pptx import Presentation
from io import BytesIO


# Set up OpenAI API key
openai.api_key = [YOUR-OPEN-API-KEY]

# Define Pydantic model for output
class PythonCode(BaseModel):
    comments: str = Field(description='Comments about the code')
    code: List[str] = Field(description='Python-pptx code')

# Define prompt template
template = (
    "We have provided information below. \n"
    "---------------------\n"
    "{title}"
    "{bullet_points}"
    "\n---------------------\n"
    "Given this information, please generate python-pptx code for a single slide with this title & bullet points\n"
    "Make sure to not include any single quotes (') in the text"
    "Separate the bullet points into separate texts"
    "Do not set font size"
    "Include code to save the presentation"
)

# Create a PromptTemplate instance
prompt_template = PromptTemplate(template)

# Function to extract title and bullet points from response
def extract_info(response):
    title = ""
    bullet_points = ""
    for node_with_score in response.source_nodes:
        text = node_with_score.node.text
        # Splitting the text into sections based on bullet point patterns
        sections = text.split("○")
        # The first section corresponds to the title
        title += sections[0].strip() + "\n"
        # The subsequent sections correspond to bullet points
        for section in sections[1:]:
            bullet_points += "○" + section.strip() + "\n"
    return title, bullet_points


# Streamlit app
def main():
    st.title("PDF to PowerPoint Presentation Generator")
    st.write("Upload a PDF file and get a PowerPoint presentation with summarized bullet points!")

    # Upload PDF file
    pdf_file = st.file_uploader("Upload PDF file", type=["pdf"])

    if pdf_file is not None:
        # Process the PDF file
        reader = SimpleDirectoryReader(input_files=[pdf_file.name])
        docs = reader.load_data()
        
        llm = OpenAI()

        # Create an index for the documents
        index = VectorStoreIndex.from_documents(docs)

        # Query engine
        query_engine = index.as_query_engine(
            similarity_top_k=3,
            llm=llm,
            text_qa_template=prompt_template,
            response_mode='tree_summarize',
            output_cls=PythonCode,
            description="This class represents the structured output for the query response."
        )

        # Query and response
        query = st.text_input("Enter query to summarize:")
        response = query_engine.query(query)

        # Extract title and bullet points
        title, bullet_points = extract_info(response)


        # Generate Python-pptx code
        output = LLMTextCompletionProgram.from_defaults(output_cls=PythonCode, prompt_template_str=template, verbose=True, llm=llm)(title=title, bullet_points=bullet_points)
        st.write(output)

        escaped_code = [line.replace('"', '\\"') for line in output.code]
        joined_code = "\n".join(escaped_code)
        # Execute the generated code
        exec(joined_code)

        # Save the presentation to BytesIO buffer
        presentation = Presentation()
        presentation_buffer = BytesIO()
        presentation.save(presentation_buffer)
        # presentation_buffer.seek(0)

        # # Convert the buffer to bytes and encode it to base64
        # pptx_bytes = presentation_buffer.getvalue()
        # b64 = base64.b64encode(pptx_bytes).decode()

        # # Create a download link for the PowerPoint presentation
        # href = f'<a href="data:file/pptx;base64,{b64}" download="generated_presentation.pptx">Click here to download</a>'
        # st.markdown(href, unsafe_allow_html=True)
       

if __name__ == "__main__":
    main()


# Recent Trends Shaping Adidas Logistics
       