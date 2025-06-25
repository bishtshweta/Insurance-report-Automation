#!/usr/bin/env python
# coding: utf-8

# In[4]:


import streamlit as st
import fitz  # PyMuPDF
from docx import Document
import tempfile
import os
import requests
import json  # For safe parsing

# -----------------------------
# Helper: Extract text from PDF
# -----------------------------
def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# -----------------------------
# Helper: Call LLM to get key-values
# -----------------------------
def call_llm(prompt, api_key):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://your-app-name.streamlit.app",  # Replace if deployed
        "X-Title": "GLR Streamlit App",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",  # Use a valid free model
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    
    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error("❌ Error from LLM API:\n\n" + str(response.json()))
        st.stop()

# -----------------------------
# Helper: Fill .docx template
# -----------------------------
def fill_template(template, kv_pairs):
    doc = Document(template)
    for p in doc.paragraphs:
        for key, value in kv_pairs.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in p.text:
                p.text = p.text.replace(placeholder, value)
    return doc

# -----------------------------
# Streamlit App UI
# -----------------------------
st.title("📝 Insurance Template Filler (GLR Pipeline)")

template_file = st.file_uploader("Upload .docx Insurance Template", type=["docx"])
pdf_files = st.file_uploader("Upload Photo Report PDFs", type=["pdf"], accept_multiple_files=True)
api_key = st.text_input("Enter OpenRouter API Key", type="password")

if st.button("Generate Report") and template_file and pdf_files and api_key:
    all_text = ""
    for pdf in pdf_files:
        all_text += extract_text_from_pdf(pdf)

    # Strong prompt
    prompt = f"""
You are an expert insurance claims assistant.
Extract only the key-value fields from this insurance report text.

✅ Output ONLY a valid JSON object. 
❌ No markdown. ❌ No explanations. ❌ No extra text.

Report:
{all_text}
"""

    llm_output = call_llm(prompt, api_key)

    # Show LLM raw output
    st.subheader("🔍 LLM Raw Output")
    st.code(llm_output)

    try:
        kv_dict = json.loads(llm_output)
    except json.JSONDecodeError:
        st.error("⚠️ Failed to parse LLM output. Check formatting.")
        st.stop()

    # Fill the .docx template
    doc = fill_template(template_file, kv_dict)

    # Save to a temp file and offer download
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        doc.save(tmp.name)
        st.success("✅ Template filled successfully!")
        with open(tmp.name, "rb") as f:
            st.download_button("📥 Download Filled Report", f, file_name="filled_report.docx")

