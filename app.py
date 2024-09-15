import streamlit as st
import pandas as pd
import functions
import json
import os
from functions import rank_resumes  




st.set_page_config(page_title="Resume Screening", initial_sidebar_state="collapsed")
st.title("Resume Screening and Matching System")

# Sidebar with instructions
st.sidebar.header("How to Use This Application")
st.sidebar.write("""
1. **Upload Resumes**: Upload one or more resumes (PDF, DOCX).

2. **Extract Resume Data**: Then click on the "Extract All" button. The unstructured data is converted to structured form and displayed in a dataframe. It is also saved as JSON format in the backend.

3. **Enter Job Description**: Enter the job description required to rank the candidates. 

4. **Extract Job Description**: Then click on the "Extract Job Description" button. The information will be saved in JSON format in the backend.

5. **Rank Resumes**: Click on the "Rank Resumes" button to rank the uploaded resumes based on the provided job description. The resumes will be ranked by their similarity to the job description.

6. **Results**: The ranked resumes will be displayed with their rank, candidate name, and similarity score.
""")




# -----------------------------------------------Resume----------------------------------------------



uploaded_files = st.file_uploader("Upload one or more resumes", type=["pdf", "docx"], accept_multiple_files=True)
if uploaded_files:
    all_resume_data = []  
    
    if st.button("Extract All"):
        for uploaded_file in uploaded_files:
            st.write(f"Processing file: {uploaded_file.name}")
            file_type = uploaded_file.type

            # Extract text based on file type
            if file_type == "application/pdf":
                text = functions.extract_from_pdf(uploaded_file)

            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text = functions.extract_from_doc(uploaded_file)

            else:
                st.error(f"Unsupported file: {uploaded_file.name}. Please upload a PDF, DOCX, or image file.")
                continue

            # Clean the extracted text and extract resume data
            cleaned_text = functions.clean_text(text)
            resume_df, resume_json = functions.extract_resume_data(cleaned_text)

            # Add the extracted JSON data to the list
            all_resume_data.append({
                "file_name": uploaded_file.name,
                "resume_data": resume_json
            })

            # Display the resulting DataFrame for each file
            st.write(f"Extracted Data from {uploaded_file.name}")
            st.dataframe(
                resume_df,
                column_config={
                    "Entities": st.column_config.Column(width=150),
                    "Value": st.column_config.Column(width=950)
                },
                hide_index=True
            )

        # Save all resume data to a file in JSON format
        with open("resume_data.json", "w") as f:
            json.dump(all_resume_data, f, indent=4)

        st.success("All resumes have been processed and saved to resume_data.json.")
        
        



# --------------------------------- Job Description --------------------------------------------




st.subheader("Enter Job Description")
job_description_input = st.text_area("Enter the job description here")

if st.button("Extract Job Description"):
    if job_description_input:
        # Clean the job description and extract data
        cleaned_description = functions.clean_text(job_description_input)
        job_description_df, job_description_json = functions.extract_job_description(cleaned_description)

        # Display the processed job description data
        st.write("Extracted Job Description Data")
        st.dataframe(
            job_description_df,
            column_config={
                "Entities": st.column_config.Column(width=150),
                "Value": st.column_config.Column(width=950)
            },
            hide_index=True
        )

        # Save the job description data to a JSON file
        with open("job_description.json", "w") as f:
            json.dump(job_description_json, f, indent=4)

        st.success("Job description has been processed and saved to job_description.json.")
    else:
        st.error("Please enter a job description before extracting.")
        
        
        
        
# ------------------------------------------Ranking Resumes------------------------------------



if st.button("Rank Resumes"):
    if os.path.exists("resume_data.json") and os.path.exists("job_description.json"):
        # Call the ranking function to rank resumes based on job description
        ranked_resumes = rank_resumes("resume_data.json", "job_description.json")

        # Load the resume data from the JSON file
        with open("resume_data.json", "r") as f:
            resume_data = json.load(f)

        # Create a mapping of file_name to candidate name
        file_name_to_name = {
            resume['file_name']: resume['resume_data'].get('Name', 'Unknown')
            for resume in resume_data
        }

        # Custom CSS for adding little bit of styling
        st.markdown("""
        <style>
        .resume-card {
            background-color: #1E1E1E; /* Dark grey for contrast */
            padding: 20px;
            margin: 10px 0;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            color: #FFFFFF; /* White text for readability */
        }
        .resume-rank {
            font-size: 24px;
            font-weight: bold;
            color: #FFD700; /* Gold for ranking */
        }
        .resume-name {
            font-size: 18px;
            font-weight: bold;
        }
        .resume-score {
            font-size: 16px;
            color: #90EE90; /* Light green for similarity score */
        }
        .resume-matches {
            font-size: 14px;
            color: #ADD8E6; /* Light blue for combined matching info */
        }
        </style>
        """, unsafe_allow_html=True)

        st.subheader("Ranked Resumes")
        
        for rank, resume in enumerate(ranked_resumes, 1):
            file_name = resume.get('file_name', 'Unknown File')
            candidate_name = file_name_to_name.get(file_name, 'Unknown')
            st.markdown(f"""
            <div class="resume-card">
                <div class="resume-rank">Rank {rank}</div>
                <div class="resume-name">Candidate Name: {candidate_name}</div>
                <div class="resume-score">Similarity Score: {resume.get('similarity_score', 0):.2f}</div>
                <div class="resume-matches">Resume: {file_name}</div>
            </div>
            """, unsafe_allow_html=True)

            # Add a horizontal divider between ranked resumes (optional)
            st.divider()

    else:
        st.error("Please upload resumes and enter a job description before ranking.")
