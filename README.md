# Resume-Screening-And-Matching-System
### Project Description
* This project is a resume screening and matching system built with applications of Gen AI and NLP . It allows the HR of a company to upload resumes (in PDF or DOCX format) of the candidates, extract key data (such 
  as skills, qualifications, and experience), and compare them to a given job description to rank candidates based on their relevance to the role.
* This application uses Llama3 for text extraction and spaCy model to rank resumes by similarity to a job description.
---
### Clone the Repository
---
### Folder Structure
```
resume-screening-system/
│
├── nebula9.ipynb               # Step by Step process and Methodology file
├── app.py                       # Streamlit application file
├── functions.py               # Helper functions are initialized
├──reinforcementLearning.py      # Reinforcement Learning for Feedback Mechanism
├── requirements.txt             # Project dependencies
├── README.md                    # Project documentation
├── resume_data.json             # Stored extracted resume data (if any , generates when you run the streamlit application) 
├── job_description.json         # Stored extracted job description data (if any, generates when you run the streamlit application)
└── sample resume inputs          # you can find some sample resume pdfs or docxs
```

---
### Installing / Getting started
#### 1.Generating the Groq Api Key
* Open the Groq website by [click here](https://console.groq.com/keys) and sign in.
* Click on **Create Api Key** Button.
* Name the project and submit.
* Copy the Api_key and paste it someplace secure, to use it.
* Paste yout api_key in the nebula9.ipynb and .env files.
---
### Install Dependencies
`pip install -r requirements.txt`

You can find the Methodology and Flow Diagram of the project in the `nebula9.ipynb` file. Open it first for complete understanding of the project and then run the application for demo.

---
### Run the Project
`streamlit run app.py`

Further instructions are mentioned in the streamlit sidebar of the application once you run it.
