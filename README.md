# 🎯 AI Career Advisor

An intelligent career guidance system that analyzes your resume against target job descriptions and provides personalized skill development recommendations using AI-powered analysis and web search capabilities.

## ✨ Features

- **Resume Analysis**: Extract and analyze text from PDF resumes
- **Gap Analysis**: Compare your skills with job requirements
- **Personalized Recommendations**: Get tailored learning paths and resources
- **Web-Powered Research**: Real-time search for current learning materials
- **Interactive Web Interface**: Modern, responsive Streamlit UI
- **Comprehensive Reports**: Detailed analysis with actionable insights

## 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit** - Web interface
- **PyPDF2** - PDF text extraction
- **Agno Framework** - AI agent orchestration
- **Google Gemini AI** - Language model for analysis
- **DuckDuckGo Search** - Web search capabilities

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-career-advisor
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit PyPDF2 agno pathlib tempfile
   ```

3. **Set up API Keys**
   - Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Update the API key in both `recommendation_system.py` and `st.py`:
   ```python
   api_key="YOUR_GEMINI_API_KEY_HERE"
   ```

## 🚀 Usage

### Command Line Version

Run the basic command-line interface:

```bash
python recommendation_system.py
```

**Interactive prompts:**
1. Enter the full path to your PDF resume
2. Enter the target job title
3. Enter the job description
4. Wait for AI analysis and recommendations

### Web Interface (Recommended)

Launch the modern web interface:

```bash
streamlit run st.py
```

**Web Interface Steps:**
1. Upload your PDF resume
2. Enter job title and description
3. Click "Analyze Resume & Get Recommendations"
4. Review personalized recommendations
5. Download analysis report

## 📋 What You Get

The AI Career Advisor provides comprehensive analysis in these areas:

### 1. 🎯 Critical Skills Assessment
- Top skills needed for the target role
- Priority ranking by importance
- Relevance explanation for each skill

### 2. 📚 Learning Resources
- **Online Courses**: Coursera, edX, Udemy, Pluralsight links
- **Official Documentation**: Platform-specific guides
- **Interactive Tutorials**: Codecademy, freeCodeCamp resources
- **Certifications**: Industry-recognized certification programs

### 3. 🔧 Essential Tools & Technologies
- **Software/Platforms**: Industry-standard applications
- **Development Environments**: IDEs and code editors
- **Collaboration Tools**: Project management and version control
- **Installation Guides**: Direct download and setup links

### 4. 📖 Reading Materials
- Industry publications and tech blogs
- Best practices guides and documentation
- Real-world case studies
- Relevant research papers

### 5. 💪 Hands-On Practice
- **Coding Challenges**: LeetCode, HackerRank problems
- **Project Ideas**: Portfolio-building projects
- **Sandbox Environments**: Practice platforms
- **Open Source**: GitHub repositories for contribution

### 6. 🌐 Professional Development
- Networking opportunities and communities
- Industry forums and discussion groups
- Mentorship platform connections
- Interview preparation resources

## 📁 File Structure

```
Smart Recommendation System/
├── recommendation_system.py    # Command-line interface
├── st.py                      # Streamlit web interface
├── README.md                  # This file
└── requirements.txt           # Dependencies (create this)
```

## 🔧 Configuration

### API Configuration
Both scripts use the same Gemini AI configuration:
- **Model**: `gemini-2.0-flash-exp`
- **Tools**: DuckDuckGo search integration
- **Output**: Markdown-formatted responses

### Customization Options
- Modify `agent_instructions` to adjust analysis focus
- Update CSS in `st.py` for UI customization
- Adjust search parameters in DuckDuckGo tools

## 📝 Requirements.txt

Create a `requirements.txt` file with:

```
streamlit>=1.28.0
PyPDF2>=3.0.0
agno>=0.1.0
pathlib2>=2.3.0
google-generativeai>=0.3.0
```

## 🚨 Important Notes

### Security Considerations
- **API Key**: Never commit API keys to version control
- **File Handling**: Temporary files are cleaned up automatically
- **Input Validation**: Resume and job description inputs are validated

### Limitations
- PDF must be text-extractable (not scanned images)
- Requires stable internet connection for AI and search
- Processing time varies based on resume complexity

### Error Handling
- Invalid PDF format detection
- Network connectivity issues
- API rate limiting management
- Temporary file cleanup


## 🆘 Support

### Common Issues

**PDF Not Reading Properly**
- Ensure PDF is not password-protected
- Check if PDF contains extractable text (not just images)
- Try with a different PDF file

**API Errors**
- Verify Gemini API key is valid and active
- Check internet connection
- Ensure API quota is not exceeded

**Streamlit Issues**
- Update Streamlit: `pip install --upgrade streamlit`
- Clear browser cache
- Try different browser

## 🎉 Acknowledgments

- **Google Gemini AI** for powerful language processing
- **Agno Framework** for agent orchestration
- **Streamlit** for rapid web development
- **DuckDuckGo** for privacy-focused search

---

**Made with ❤️ for career growth and professional development**
