import streamlit as pd_stream
import os
from google import genai
from google.genai import types

# Configure the local web interface canvas properties
pd_stream.set_page_config(
    page_title="AI PRD to Jira Story Generator", 
    layout="wide"
)

pd_stream.title("Agile Workspace Automation: PRD to Jira Story Generator")
pd_stream.caption(
    "A programmatic transformation pipe turning raw Product Requirement Documents "
    "into highly structured Agile backlogs utilizing the Gemini API."
)

# Sidebar setup for secure configuration tracking
pd_stream.sidebar.header("API Authentication Setup")
api_key_input = pd_stream.sidebar.text_input(
    "Gemini API Key", 
    type="password", 
    placeholder="AIzaSy...",
    help="Generate a secure free key at Google AI Studio (://google.com)"
)

# Text canvas for raw product specification ingestion; enter your requirements
pd_stream.subheader("Inbound Product Requirements Document (PRD)")
prd_raw_text = pd_stream.text_area(
    "Paste your product specification document text parameters here:",
    height=280,
    placeholder=(
        "Example: Users must be able to log in using their enterprise credentials. "
        "The system should validate credentials against the active database, log transaction "
        "metadata, and display an intuitive error prompt if authentication fails within 3 attempts."
    )
)

# Trigger execution controller
if pd_stream.button("Transform Document to Jira Backlog", type="primary"):
    # Priority Validation Check: Verify API configuration vector exists
    target_key = api_key_input if api_key_input else os.getenv("GEMINI_API_KEY")
    
    if not target_key:
        pd_stream.error("Execution Blocker: Please supply a valid Gemini API Key in the sidebar or shell environment.")
    elif not prd_raw_text.strip():
        pd_stream.warning("Input Validation Flag: Inbound PRD parameters are empty. Please supply product requirements.")
    else:
        with pd_stream.spinner("Parsing requirements and structuring Agile backlogs..."):
            try:
                # Initialize the official Google GenAI runtime client instance
                client = genai.Client(api_key=target_key)
                
                # Enforce engineering constraint rules via System Instructions
                system_instruction = (
                    "Act as a Principal Technical Program Manager (TPM). Your task is to extract execution scopes "
                    "from raw product specifications and translate them into engineering ticket structures. "
                    "Output exactly 3 strict User Stories conforming to the enterprise Agile framework architecture. "
                    "Each ticket must have a distinct ID prefix (e.g., STORY-01) and must strictly match this structural schema:\n"
                    "1. User Story Description (Using the standard format: 'As a... I want to... So that...')\n"
                    "2. Technical Dependencies & Constraints\n"
                    "3. Quantifiable Acceptance Criteria (Formatted as an ordered list using clear, measurable metrics)"
                )
                
                # Execute inference pipeline using the optimized gemini-2.5-flash engine checkpoint
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prd_raw_text,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.2, # Lower variance to enforce strict pattern conformity
                    )
                )
                
                # Render structured generation payloads back to visual canvas container
                pd_stream.success("Backlog generation phase complete. Review technical tickets below:")
                pd_stream.markdown("### Generated Jira Engineering Tickets")
                pd_stream.markdown(response.text)
                
            except Exception as e:
                pd_stream.error(f"Execution Error Runtime Exception occurred: {str(e)}")
