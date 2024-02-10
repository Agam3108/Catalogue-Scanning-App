import base64
import streamlit as st
import PyPDF2
import os
from langchain_community.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

#Please replace your Hugging face access token in the below 'api_key'

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

llm = HuggingFaceHub(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2", model_kwargs={"temperature": 0.5, "max_length": 2048}
)

template = """
        The task involves evaluating text from a catalogue PDF, assigning a score of 100, and identifying errors like formatting and semantic inaccuracies. The evaluation should provide detailed insights into these issues, highlighting their impact on content accuracy and quality. Actionable suggestions for improvement should be offered, focusing on precision, semantic fidelity, and coherent information presentation. The evaluation and recommendations should be limited to a word constraint of 100.
        Question: {question}
        """

prompt = PromptTemplate.from_template(template)

llm_chain = LLMChain(prompt=prompt, llm=llm)

def model(question):
    template = """
            The task involves evaluating text from a catalogue PDF, assigning a score of 100, and identifying errors like formatting and semantic inaccuracies.The evaluation should provide detailed insights into these issues, highlighting their impact on content accuracy and quality. Actionable suggestions for improvement should be offered, focusing on precision, semantic fidelity, and coherent information presentation. The evaluation should be accurate and limited to a word constraint of 100.
            Question: {question}
            """
             

    prompt = PromptTemplate.from_template(template)

    llm_chain = LLMChain(prompt=prompt, llm=llm)

    st.subheader("Evaluation Result")
    st.write(llm_chain.run(question))


def displayPDF(file):
    # Opening file from file path
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

st.title("Catalog Scanning App")

pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

if pdf_file is not None:
    displayPDF(pdf_file)

    # Read the PDF file
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    # Extract the content
    content = ""
    for page in range(len(pdf_reader.pages)):
        content += pdf_reader.pages[page].extract_text()

    model(content)