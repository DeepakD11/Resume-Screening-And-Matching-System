## Output
<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/3361b513-286c-46af-aca5-fe07e8fadeb4" width="300"/></td>
    <td><img src="https://github.com/user-attachments/assets/8758b515-8914-4c4a-985a-d7cb97ddbdbb" width="300"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/71cf57c0-61a2-416c-989e-390b7230a4eb" width="300"/></td>
    <td><img src="https://github.com/user-attachments/assets/2c6cbe47-a52c-4a65-8bcf-7bc801b3b5c9" width="300"/></td>
  </tr>
</table>

---
# Resume-Screening-And-Matching-System
### Project Description
* This project is a resume screening and matching system built with applications of Gen AI and NLP . It allows the HR of a company to upload resumes (in PDF or DOCX format) of the candidates, extract key data (such 
  as skills, qualifications, and experience), and compare them to a given job description to rank candidates based on their relevance to the role.
* This application uses Llama3 for text extraction and spaCy model to rank resumes by similarity to a job description.
---
### Clone the Repository
```
git clone https://github.com/DeepakD11/Resume-Screening-And-Matching-System.git
cd Resume-Screening-And-Matching-System
cp .env .envexample
```
---
### Folder Structure
```
resume-screening-system/
│
├── .env                        # Contains the api key 
├── nebula9.ipynb               # Step by Step process and Methodology file
├── app.py                       # Streamlit application file
├── functions.py               # Helper functions are initialized
├──reinforcementLearning.py      # Reinforcement Learning for Feedback Mechanism
├── requirements.txt             # Project dependencies
├── README.md                    # Project documentation
├── resume_data.json             # Stored extracted resume data ( generates when you run the streamlit application) 
├── job_description.json         # Stored extracted job description data (generates when you run the streamlit application)
└── sample resume inputs          # you can find some sample resume pdfs or docxs
```

---
### Installing / Getting started
#### 1.Generating the Groq Api Key
* Open the Groq website by [click here](https://console.groq.com/keys) and sign in.
* Click on **Create Api Key** Button.
* Name the project and submit.
* Copy the Api_key and paste it someplace secure, to use it.
* Paste your api_key in the nebula9.ipynb and .env files.

#### 2.Install Dependencies
```
pip install -r requirements.txt
```
You can find the Methodology and Flow Diagram of the project in the `nebula9.ipynb` file. Open it first for complete understanding of the project and then run the application for demo.

```
python -m spacy download en_core_web_md
```

#### 3.Run the Project
```
streamlit run app.py
```
Further instructions are mentioned in the streamlit sidebar of the application once you run it.
