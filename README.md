# slideHarvest

This PDF to PowerPoint Presentation Generator is a streamlit application designed to simplify the process of summarizing and visualizing the content of PDF documents into PowerPoint presentations. The tool allows users to upload PDF files containing textual information, input a query related to the document's content, and automatically generate a PowerPoint presentation slide based on the query. 

**Note:** Currently it is capable to generate only one slide per query

**Usage:**
1. Set up your OpenAI API key
2. streamlit run slideHarvest.py

**Dependencies:**  
streamlit: A Python library for building interactive web applications.  
llama_index: A library for natural language processing and text summarization.  
openai: OpenAI Python library for accessing OpenAI's GPT models.  
python-pptx: A Python library for creating and updating PowerPoint (.pptx) files.  
