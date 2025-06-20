import streamlit as st
import PyPDF2
from pathlib import Path
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
import tempfile
import os

# Set page configuration
st.set_page_config(
    page_title="AI Career Advisor",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for minimalistic modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 2.8rem;
        font-weight: 600;
        color: #1a1a1a;
        text-align: center;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    .section-header {
        font-size: 1.4rem;
        font-weight: 500;
        color: #374151;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        letter-spacing: -0.01em;
    }
    
    .info-box {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin: 1.5rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #fbbf24;
        margin: 1.5rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .stFileUploader > div {
        border-radius: 12px;
        border: 2px dashed #d1d5db;
        background: #fafafa;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: #6366f1;
        background: #f8fafc;
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 1px solid #d1d5db;
        font-size: 0.95rem;
        padding: 0.75rem;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.95rem;
        padding: 0.75rem 1.5rem;
        transition: all 0.2s ease;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border: none;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
    }
    
    .sidebar-content {
        background: #f8fafc;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .sidebar-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 1rem;
    }
    
    .sidebar-text {
        font-size: 0.9rem;
        color: #6b7280;
        line-height: 1.6;
    }
    
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        margin: 1rem 0;
    }
    
    .stExpander {
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        background: white;
    }
    
    .stMarkdown {
        font-size: 0.95rem;
    }
    
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, #e5e7eb, transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Original function preserved exactly as is
def extract_text_from_pdf(pdf_file: str) -> str:
    with open(pdf_file, "rb") as pdf:
        reader = PyPDF2.PdfReader(pdf, strict=False)
        text = []

        for page in reader.pages:
            content = page.extract_text()
            text.append(content)

        return text

# Function to create agent with original logic
def create_agent(job_title: str, job_description: str) -> Agent:
    agent_instructions = f"""
        You are an expert AI Career Advisor. Your primary function is to analyze a user's resume against a target job and provide comprehensive, actionable recommendations for skill improvement and career development.
        
        Analysis Protocol:
        1. Parse Resume: From the user's PDF resume, extract their existing skills, programming languages, tools, technologies, certifications, and relevant experiences.
        2. Analyze Job: From the {job_title} and {job_description}, identify the core skills, key technologies, essential qualifications, preferred tools, and industry-specific requirements for the role.
        3. Identify Gaps: Perform a comprehensive gap analysis by comparing the user's profile with the job's requirements to pinpoint the most critical missing skills, tools, and knowledge areas.

        Output Requirements:
        Comprehensive Recommendations for The User to better fit the {job_title}:

        1. Critical Skills Assessment
            a. List the top skills the user needs to develop to become a perfect candidate for the job
            b. Rank skills by importance and impact on job performance
            c. Explain the relevance of each skill to the specific job role

        2. Learning Resources (Minimum 2 per skill)
        Provide direct, real, and currently functional hyperlinks to high-quality learning resources:
            a. Online Courses: Specific courses on platforms like Coursera, edX, Udemy, Pluralsight, LinkedIn Learning
            b. Official Documentation: Platform-specific guides and documentation
            c. Interactive Tutorials: Hands-on learning platforms like Codecademy, freeCodeCamp, Khan Academy
            d. Certification Programs: Industry-recognized certifications relevant to the role

        3. Essential Tools & Technologies
        Recommend specific tools the user should master:
            a. Software/Platforms: Industry-standard tools and applications
            b. Development Environments: IDEs, code editors, and development tools
            c. Collaboration Tools: Project management, version control, and team communication tools
            d. Installation Guides: Direct links to download pages and setup tutorials

        4. Reading Materials & Articles
        Curate high-quality educational content:
            a. Industry Publications: Relevant articles from reputable tech blogs, industry magazines
            b. Best Practices Guides: Methodology and framework documentation
            c. Case Studies: Real-world implementation examples and success stories
            d. Research Papers: Academic or industry research relevant to the field

        5. Hands-On Practice Exercises
        Provide actionable practice opportunities:
            a. Coding Challenges: Platform-specific challenges (LeetCode, HackerRank, Codewars)
            b. Project Ideas: Step-by-step project suggestions that align with job requirements
            c. Sandbox Environments: Online platforms for experimentation and practice
            d. GitHub Repositories: Open-source projects for contribution and learning
            e. Portfolio Development: Specific project recommendations to showcase relevant skills

        6. Professional Development
        Additional career enhancement recommendations:
            a. Networking Opportunities: Professional communities, meetups, conferences
            b. Industry Forums: Stack Overflow, Reddit communities, Discord servers
            c. Mentorship Platforms: Connections to industry professionals
            d. Job-Specific Preparation: Interview preparation resources, common technical questions

        Quality Standards:
            1. Link Integrity: Ensure all links are direct and lead to the actual resource, not generic search pages or homepages
            2. Currency: Verify resources are up-to-date and actively maintained
            3. Relevance: All recommendations must directly align with the target job requirements
            4. Accessibility: Include both free and premium options when possible
            5. Difficulty Progression: Structure learning paths from beginner to advanced levels

        Format Requirements:
            1. Structure response with clear headings and subheadings
            2. Use bullet points and numbered lists for easy scanning
            3. Maintain a professional, encouraging, and actionable tone
            4. Include estimated time commitments for major learning resources
            5. Provide priority rankings (High/Medium/Low) for each recommendation category
    """

    agent = Agent(
        model=Gemini(id="gemini-2.0-flash-exp", api_key="AIzaSyBs9RqqwapIaJfrcEudkpaJxrUccS8rwzo"),
        markdown=True,
        tools=[DuckDuckGoTools()],
        show_tool_calls=False,
        instructions=agent_instructions,
        create_default_user_message=False
    )
    
    return agent

# Main Streamlit App
def main():
    # Header
    st.markdown('<h1 class="main-header">🎯 AI Career Advisor</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Discover the skills you need to land your dream job</p>', unsafe_allow_html=True)

    # Sidebar for configuration
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">⚙️ Configuration</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-text">Using Gemini AI with integrated search capabilities</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">📈 How it works</div>', unsafe_allow_html=True)
        st.markdown('''
        <div class="sidebar-text">
        <strong>1.</strong> Upload your resume<br>
        <strong>2.</strong> Describe your target role<br>
        <strong>3.</strong> Get personalized recommendations<br>
        <strong>4.</strong> Access curated learning resources
        </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Main content area with better spacing
    st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<h2 class="section-header">📄 Resume Upload</h2>', unsafe_allow_html=True)
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload your resume",
            type="pdf",
            help="Select a PDF file containing your resume",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.success(f"✅ {uploaded_file.name}")
            st.caption(f"File size: {uploaded_file.size:,} bytes")
            st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<h2 class="section-header">💼 Target Position</h2>', unsafe_allow_html=True)
        
        # Job title input with symmetric placeholder
        job_title = st.text_input(
            "Job Title",
            placeholder="Senior Software Engineer",
            help="Enter the exact job title you're targeting",
            label_visibility="collapsed"
        )
        
        # Job description input with symmetric placeholder
        job_description = st.text_area(
            "Job Description",
            placeholder="Looking for a Senior Software Engineer with 5+ years of experience in Python, React, and cloud technologies. Must have strong problem-solving skills and experience with agile methodologies...",
            height=150,
            help="Paste the complete job description here",
            label_visibility="collapsed"
        )

    # Analysis section
    st.markdown('<h2 class="section-header">🔍 Analysis & Recommendations</h2>', unsafe_allow_html=True)

    # Validation and processing
    if st.button("🚀 Analyze Resume & Get Recommendations", type="primary", use_container_width=True):
        
        # Validation
        if uploaded_file is None:
            st.error("❌ Please upload a PDF resume file")
            return
            
        if not job_title.strip():
            st.error("❌ Please enter a job title")
            return
            
        if not job_description.strip():
            st.error("❌ Please enter a job description")
            return

        # Processing
        try:
            with st.spinner("🔄 Processing your resume..."):
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name

                # Extract text using original function
                extracted_text = str(extract_text_from_pdf(tmp_file_path))
                
                # Clean up temporary file
                os.unlink(tmp_file_path)
                
                # Show extracted text preview
                with st.expander("📖 Resume Text Preview"):
                    st.text_area("Extracted Text", extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text, height=200)

            with st.spinner(f"🤖 Analyzing resume for '{job_title}'..."):
                st.info("⏳ This might take a few moments depending on the resume complexity and web search speed")
                
                # Create agent using original logic
                agent = create_agent(job_title, job_description)
                
                # Get recommendations using original agent logic
                response = agent.run(extracted_text)
                
                # Display results
                st.markdown("### 📊 Analysis Results")
                st.markdown("---")
                
                # Display the agent's response
                if hasattr(response, 'content'):
                    st.markdown(response.content)
                else:
                    st.markdown(str(response))
                
                # Success message
                st.success("✅ Analysis completed successfully!")
                
                # Download option for results
                if hasattr(response, 'content'):
                    result_text = response.content
                else:
                    result_text = str(response)
                    
                st.download_button(
                    label="📥 Download Analysis Report",
                    data=result_text,
                    file_name=f"career_analysis_{job_title.replace(' ', '_')}.md",
                    mime="text/markdown"
                )

        except Exception as e:
            st.error(f"❌ An error occurred during processing: {str(e)}")
            st.markdown('<div class="warning-box">Please check your resume file format and try again. Make sure the PDF is not corrupted or password-protected.</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>🤖 AI Career Advisor - Powered by Gemini AI & DuckDuckGo Search</p>
        <p><em>Get personalized career recommendations and skill development paths</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()