**Insurance Report Automation Using AI and Python**
This project automates the processing of insurance photo reports using computer vision and large language models (LLMs). It includes:

**Tasks Covered:**

Task 1: RGB-Thermal Overlay
- Overlayed RGB and thermal images.
- Enhanced thermal data with color mapping.
- Output shows damage in colored format.

Task 2: Change Detection
- Compared Before (X.jpg) and After (X~2.jpg) images.
- Detected and highlighted missing items using bounding boxes.

Task 3: Insurance Report Filler (Streamlit + LLM)
- Built a Streamlit app to:
  - Upload .docx template
  - Extract text from PDFs
  - Use OpenRouter LLM to fill the template
- Output: auto-filled `.docx` reports.

Tools & Tech Used:
- Python (OpenCV, PyMuPDF, python-docx, Streamlit, Requests)
- OpenRouter (Mistral model for LLM)
- Streamlit for frontend
- OBS Studio for video demo.
