"""
Course Generator Module
Creates training course outlines using Google Gemini
"""

import google.generativeai as genai

def generate_course_with_gemini(topic, num_modules, skill_level, documents):
    """
    Generate a structured training course outline using Google Gemini
    Tailored to skill level: Beginner, Intermediate, or Advanced
    """
    
    if not documents:
        return "Please upload some training materials first!"
    
    try:
        # Combine all document content
        combined_content = ""
        for doc in documents:
            combined_content += f"\n\n=== Content from {doc['filename']} ===\n"
            combined_content += doc['content'][:10000]  # Limit to avoid token limits
        
        doc_names = [doc['filename'] for doc in documents]
        
        # Define skill-level specific instructions
        skill_level_config = {
            "Beginner": {
                "target_audience": "Complete beginners with no prior knowledge",
                "language_style": "Simple, non-technical language with clear explanations",
                "content_depth": "Focus on fundamental concepts with step-by-step guidance",
                "module_count": "7-10 short modules (15-20 minutes each)",
                "prerequisites": "No prerequisites required",
                "learning_pace": "Slow, methodical pace with frequent reviews",
                "examples": "Abundant real-world examples and analogies",
                "glossary": "Include a comprehensive glossary of all technical terms",
                "focus": "Emphasize 'what' and 'how' over 'why'",
                "assessments": "Simple knowledge checks and guided exercises"
            },
            "Intermediate": {
                "target_audience": "Learners with basic familiarity who want to deepen understanding",
                "language_style": "Standard industry terminology with clear context",
                "content_depth": "Practical application with real-world scenarios",
                "module_count": "5-7 medium modules (30-45 minutes each)",
                "prerequisites": "Basic understanding of core concepts required",
                "learning_pace": "Moderate pace balancing theory and practice",
                "examples": "Real-world case studies and scenarios",
                "glossary": "Brief glossary for advanced terms only",
                "focus": "Balance 'how' and 'why' with practical applications",
                "assessments": "Scenario-based exercises and practical assignments"
            },
            "Advanced": {
                "target_audience": "Experienced practitioners seeking expert-level knowledge",
                "language_style": "Technical terminology used freely, assumes domain knowledge",
                "content_depth": "Deep technical details, optimization, edge cases, and best practices",
                "module_count": "3-5 comprehensive modules (60+ minutes each)",
                "prerequisites": "Strong foundation and practical experience required",
                "learning_pace": "Fast pace, assumes quick comprehension",
                "examples": "Complex scenarios, architectural decisions, troubleshooting",
                "glossary": "Not needed - assumes expert vocabulary",
                "focus": "Emphasize 'why' and architectural/strategic decisions",
                "assessments": "Advanced projects, optimization challenges, design reviews"
            }
        }
        
        config = skill_level_config[skill_level]
        
        # Create the prompt for Gemini with skill-level customization
        prompt = f"""You are an expert instructional designer. Create a professional {skill_level.upper()}-level training course based on the provided materials.

TRAINING MATERIALS:
{combined_content}

COURSE REQUIREMENTS:
- Topic: {topic}
- Skill Level: {skill_level}
- Number of Modules: {num_modules}

SKILL LEVEL SPECIFICATIONS FOR {skill_level.upper()}:
- Target Audience: {config['target_audience']}
- Language Style: {config['language_style']}
- Content Depth: {config['content_depth']}
- Module Structure: {config['module_count']}
- Prerequisites: {config['prerequisites']}
- Learning Pace: {config['learning_pace']}
- Examples: {config['examples']}
- Glossary: {config['glossary']}
- Focus Areas: {config['focus']}
- Assessments: {config['assessments']}

Please create a comprehensive training course outline with:

1. **Course Title and Overview**
   - Clear title reflecting {skill_level} level
   - Target audience description
   - Overall learning objectives
   - Prerequisites (if any)

2. **{num_modules} Detailed Modules** - Each with:
   - Module title
   - Duration estimate
   - Learning objectives (specific to {skill_level} level)
   - Key topics covered (depth appropriate for {skill_level})
   - Suggested activities/exercises (difficulty matched to {skill_level})
   - Assessment methods

3. **Additional Components**
   - Resources and references
   - {config['glossary']}
   - Next steps for continued learning

Format the output in clear Markdown with proper headers and structure.
Ensure all content is appropriately challenging for {skill_level} learners.

COURSE OUTLINE:"""
        
        # Call Gemini API (using latest model)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        
        # Format the response
        course_outline = response.text
        
        # Add metadata footer
        formatted_course = f"""{course_outline}

---

## 📊 Course Metadata

**Based on materials:** {', '.join(doc_names)}  
**Skill Level:** {skill_level}  
**Generated:** Using Google Gemini AI  
**Modules:** {num_modules}  
**Target Audience:** {config['target_audience']}

---

## 🎯 Next Steps

**For {skill_level} Learners:**
1. **Review** the course outline above
2. **Assess** your current knowledge against prerequisites
3. **Customize** specific modules based on your needs
4. **Develop** detailed content for each module
5. **Practice** with the suggested exercises and assessments

---

*This {skill_level}-level course outline was auto-generated by TrainBot Voice Assistant using Google Gemini.*
"""
        
        return formatted_course
        
    except Exception as e:
        return f"Error generating course: {str(e)}\n\nPlease check your Gemini API key in the .env file."
