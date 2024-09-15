import numpy as np
import random
import json
import spacy
from collections import defaultdict
from functions import load_data, rank_resumes

# Load spaCy model
nlp = spacy.load("en_core_web_md")

resume_data, job_desc_data = load_data()

# Define the environment setup
num_resumes = len(resume_data)  
num_jobs = len(job_desc_data)   

# Define Q-table
q_table = defaultdict(lambda: np.zeros(num_jobs))

# Hyperparameters
alpha = 0.1                
gamma = 0.99               
epsilon = 1.0              
min_epsilon = 0.01         
epsilon_decay = 0.995
num_episodes = 1000

def get_similarity_score(resume_data, job_data):
    resume_text = f"Skills: {resume_data.get('skills', '')}, Experience: {resume_data.get('experience', '')}, Qualification: {resume_data.get('qualification', '')}"
    
    job_text = f"Skills: {job_data.get('required_skills', '')}, Experience: {job_data.get('experience', '')}, Qualification: {job_data.get('qualification', '')}"
    
    resume_doc = nlp(resume_text)
    job_doc = nlp(job_text)
    
    return resume_doc.similarity(job_doc)

def q_learning(num_episodes, alpha, gamma, epsilon, min_epsilon, epsilon_decay, resume_data, job_desc_data):
    for episode in range(num_episodes):
        resume_index = random.randint(0, num_resumes - 1)
        state = resume_index

        resume_fields = resume_data[resume_index]["resume_data"]
        
        # Get similarity score as the reward
        reward = get_similarity_score(resume_fields, job_desc_data)

        # Q-value update (assuming we're just comparing with one job description)
        best_future_q = np.max(q_table[state])
        q_table[state][0] += alpha * (reward + gamma * best_future_q - q_table[state][0])  # Assume one job

        # Decay epsilon
        epsilon = max(min_epsilon, epsilon * epsilon_decay)



def rank_resumes_with_rl(resume_file="resume_data.json", job_desc_file="job_description.json"):
    with open(resume_file, "r") as rf:
        resume_data = json.load(rf)
    
    with open(job_desc_file, "r") as jf:
        job_desc_data = json.load(jf)
    
    # Train Q-learning agent
    q_learning(num_episodes, alpha, gamma, epsilon, min_epsilon, epsilon_decay, resume_data, job_desc_data)

    ranked_resumes = []

    for resume_index in range(num_resumes):
        resume_text = resume_data[resume_index]["resume_data"]
        similarity = q_table[resume_index][0]  
        ranked_resumes.append({
            "resume_index": resume_index,
            "similarity_score": similarity
        })

    # Sort resumes based on the highest similarity score
    ranked_resumes = sorted(ranked_resumes, key=lambda x: x["similarity_score"], reverse=True)

    return ranked_resumes


