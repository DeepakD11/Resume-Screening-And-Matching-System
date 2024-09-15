import json
import pandas as pd
import os
from groq import Groq
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import pytesseract
import re
import spacy

# Load spaCy model (use a pre-trained model such as 'en_core_web_md')
nlp = spacy.load("en_core_web_md")

# Load environment variables
load_dotenv()  # Assumes .env file contains GROQ_API_KEY=your_actual_api_key_here

# Retrieve the API key from the environment
api_key = os.getenv('GROQ_API_KEY')

# Initialize the Groq client with the API key
client = Groq(api_key=api_key)


def extract_resume_data(text):
    prompt = get_prompt() + text
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.choices[0].message.content

        # Extract JSON from the response using regex
        json_pattern = r'\{.*\}'
        match = re.search(json_pattern, content, re.DOTALL)
        
        if match:
            json_content = match.group(0)

            # Try parsing the extracted content as JSON
            data = json.loads(json_content)
            
            # Return both the DataFrame and JSON data
            return pd.DataFrame(data.items(), columns=["Entities", "Value"]), data
    
    except (json.JSONDecodeError, IndexError) as e:
        # Handle errors gracefully and return empty structure if an error occurs
        data = {
            "Name": "", "email_id": "", "mob_number": "", "qualification": "",
            "experience": "", "skills": "", "certification": "", "achievement": ""
        }
        return pd.DataFrame(data.items(), columns=["Entities", "Value"]), data

def get_prompt():
    return '''Extract the following details from the resume in the exact JSON format below. 
    Do not include any other text except the JSON. If a field is missing or unknown, use an empty string ("").

    Expected JSON format:
    {
        "Name": "",
        "email_id": "",
        "mob_number": "",
        "qualification": "",
        "experience": "",
        "skills": "",
        "certification": "",
        "achievement": ""
    }

    Resume Text:
    ============
    '''


def extract_from_pdf(file):
    pdf_text = ""
    pdf_reader = PdfReader(file)
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()
    return pdf_text

def extract_from_doc(file):
    doc = Document(file)
    doc_text = ""
    for paragraph in doc.paragraphs:
        doc_text += paragraph.text + "\n"
    return doc_text

def extract_from_image(file):
    img = Image.open(file)
    ocr_text = pytesseract.image_to_string(img)
    return ocr_text

def extract_job_description(text):
    prompt = get_job_description_prompt() + text
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.choices[0].message.content

        # Extract JSON from the response using regex
        json_pattern = r'\{.*\}'
        match = re.search(json_pattern, content, re.DOTALL)
        
        if match:
            json_content = match.group(0)

            # Try parsing the extracted content as JSON
            data = json.loads(json_content)
            
            # Return both the DataFrame and JSON data
            return pd.DataFrame(data.items(), columns=["Entities", "Value"]), data
    
    except (json.JSONDecodeError, IndexError) as e:
        # Handle errors gracefully and return empty structure if an error occurs
        data = {
            "required_skills": "", "experience": "", "qualification": "", "certification": ""
        }
        return pd.DataFrame(data.items(), columns=["Entities", "Value"]), data


def get_job_description_prompt():
    return '''Extract the following details from the job description in the exact JSON format below.
    Do not include any other text except the JSON. If a field is missing or unknown, use an empty string ("").

    Expected JSON format:
    {
        "required_skills": "",
        "experience": "",
        "qualification": "",
        "certification": ""
    }

    Job Description:
    ============

    '''


def clean_text(text):
    # Replace multiple spaces or newlines with a single space
    cleaned_text = re.sub(r'\s+', ' ', text)
    cleaned_text = cleaned_text.strip()
    return cleaned_text


# Function to rank resumes using spaCy similarity
def rank_resumes(resume_file="resume_data.json", job_desc_file="job_description.json"):
    # Load the resume data and job description data
    with open(resume_file, "r") as rf:
        resume_data = json.load(rf)
    
    with open(job_desc_file, "r") as jf:
        job_desc_data = json.load(jf)

    # Extract relevant fields from the job description
    job_skills = job_desc_data.get("required_skills", "")
    job_experience = job_desc_data.get("experience", "")
    job_qualification = job_desc_data.get("qualification", "")

    # Convert job description fields to spaCy docs
    job_doc = nlp(f"Skills: {job_skills}, Experience: {job_experience}, Qualification: {job_qualification}")

    ranked_resumes = []

    # Iterate through each resume and calculate similarity score
    for resume in resume_data:
        resume_name = resume["file_name"]
        resume_skills = resume["resume_data"].get("skills", "")
        resume_experience = resume["resume_data"].get("experience", "")
        resume_qualification = resume["resume_data"].get("qualification", "")

        # Create spaCy docs for the resume fields
        resume_doc = nlp(f"Skills: {resume_skills}, Experience: {resume_experience}, Qualification: {resume_qualification}")

        # Calculate similarity between resume and job description
        similarity_score = job_doc.similarity(resume_doc)

        # Append the resume with its similarity score
        ranked_resumes.append({
            "file_name": resume_name,
            "similarity_score": similarity_score,
            "skills": resume_skills,
            "experience": resume_experience,
            "qualification": resume_qualification
        })

    # Sort resumes based on similarity score
    ranked_resumes = sorted(ranked_resumes, key=lambda x: x["similarity_score"], reverse=True)

    # Return ranked resumes
    return ranked_resumes


# Example usage
if __name__ == "__main__":
    ranked_resumes = rank_resumes()
    
    # Print the ranked resumes
    for rank, resume in enumerate(ranked_resumes, 1):
        print(f"Rank {rank}: {resume['file_name']} - Similarity Score: {resume['similarity_score']:.2f}")
        print(f"Matching Skills: {resume['skills']}, Experience: {resume['experience']}, Qualification: {resume['qualification']}\n")