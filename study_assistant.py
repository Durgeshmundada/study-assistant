import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="centered"
)

# Title
st.title("📚 AI Study Assistant")
st.markdown("Your personal AI tutor for exam preparation")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    model = st.selectbox(
        "AI Model",
        ["llama-3.1-8b-instant"]
    )
    st.markdown("---")
    st.markdown("### 📊 Study Tools")
    st.info("""
    - **Explain**: Understand concepts
    - **Examples**: See real cases
    - **Quiz**: Test yourself
    - **Notes**: Get summaries
    - **Flashcards**: Quick revision
    """)

# Initialize LLM
@st.cache_resource
def get_llm(model_name):
    return ChatGroq(model=model_name, temperature=0.3)

# Tool selection
tool = st.radio(
    "Choose a study tool:",
    ["🎯 Explain Concept", "💡 Generate Examples", "❓ Create Quiz", "📝 Make Notes", "🎴 Flashcards"],
    horizontal=True
)

# Input area
if tool == "🎯 Explain Concept":
    st.markdown("### 🎯 Concept Explainer")
    topic = st.text_input("Enter topic to explain:", placeholder="e.g., Binary Search Tree")
    difficulty = st.select_slider("Difficulty Level:", ["Beginner", "Intermediate", "Advanced"])

    if st.button("Explain", type="primary"):
        if topic:
            with st.spinner("Generating explanation..."):
                llm = get_llm(model)
                prompt = PromptTemplate(
                    template="""Explain {topic} at a {difficulty} level.

Structure your explanation with:
1. Simple definition
2. Key concepts
3. How it works
4. Real-world analogy
5. Common use cases

Keep it clear and concise.""",
                    input_variables=["topic", "difficulty"]
                )

                chain = prompt | llm | StrOutputParser()
                result = chain.invoke({"topic": topic, "difficulty": difficulty})

                st.success("✅ Explanation ready!")
                st.markdown(result)

                # Download option
                st.download_button(
                    "📥 Download as TXT",
                    data=result,
                    file_name=f"{topic.replace(' ', '_')}_explanation.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Please enter a topic!")

elif tool == "💡 Generate Examples":
    st.markdown("### 💡 Example Generator")
    topic = st.text_input("Enter topic:", placeholder="e.g., Recursion in Python")
    num_examples = st.slider("Number of examples:", 1, 5, 3)

    if st.button("Generate Examples", type="primary"):
        if topic:
            with st.spinner("Creating examples..."):
                llm = get_llm(model)
                prompt = PromptTemplate(
                    template="""Generate {num_examples} practical examples for: {topic}

For each example provide:
- Clear problem statement
- Solution with explanation
- Key takeaway

Make examples progressively challenging.""",
                    input_variables=["topic", "num_examples"]
                )

                chain = prompt | llm | StrOutputParser()
                result = chain.invoke({"topic": topic, "num_examples": num_examples})

                st.success("✅ Examples ready!")
                st.markdown(result)

                st.download_button(
                    "📥 Download Examples",
                    data=result,
                    file_name=f"{topic.replace(' ', '_')}_examples.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Please enter a topic!")

elif tool == "❓ Create Quiz":
    st.markdown("### ❓ Quiz Generator")
    topic = st.text_input("Enter topic:", placeholder="e.g., DBMS Normalization")
    num_questions = st.slider("Number of questions:", 3, 10, 5)
    question_type = st.selectbox("Question Type:", ["Multiple Choice", "True/False", "Short Answer", "Mixed"])

    if st.button("Create Quiz", type="primary"):
        if topic:
            with st.spinner("Preparing quiz..."):
                llm = get_llm(model)
                prompt = PromptTemplate(
                    template="""Create a {num_questions}-question {question_type} quiz on: {topic}

Format:
Q1. [Question]
A) [Option]
B) [Option]
C) [Option]
D) [Option]

At the end, provide:
--- ANSWERS ---
1. [Correct answer with brief explanation]

Make questions test understanding, not just memorization.""",
                    input_variables=["topic", "num_questions", "question_type"]
                )

                chain = prompt | llm | StrOutputParser()
                result = chain.invoke({
                    "topic": topic,
                    "num_questions": num_questions,
                    "question_type": question_type
                })

                st.success("✅ Quiz ready!")
                st.markdown(result)

                st.download_button(
                    "📥 Download Quiz",
                    data=result,
                    file_name=f"{topic.replace(' ', '_')}_quiz.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Please enter a topic!")

elif tool == "📝 Make Notes":
    st.markdown("### 📝 Notes Maker")
    topic = st.text_area("Enter topic or paste content:", 
                         placeholder="e.g., Explain File Systems", 
                         height=150)
    note_style = st.selectbox("Note Style:", ["Bullet Points", "Cornell Notes", "Mind Map", "Summary"])

    if st.button("Generate Notes", type="primary"):
        if topic:
            with st.spinner("Creating notes..."):
                llm = get_llm(model)
                prompt = PromptTemplate(
                    template="""Create {note_style} style notes for: {topic}

Make it:
- Easy to scan and review
- Highlight key terms
- Include important formulas/algorithms if applicable
- Add memory aids or mnemonics
- Perfect for exam revision""",
                    input_variables=["topic", "note_style"]
                )

                chain = prompt | llm | StrOutputParser()
                result = chain.invoke({"topic": topic, "note_style": note_style})

                st.success("✅ Notes ready!")
                st.markdown(result)

                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "📥 Download as TXT",
                        data=result,
                        file_name=f"{topic[:30].replace(' ', '_')}_notes.txt",
                        mime="text/plain"
                    )
                with col2:
                    # Convert to PDF-ready format
                    pdf_content = f"# {topic}\n\n{result}"
                    st.download_button(
                        "📄 Download as MD",
                        data=pdf_content,
                        file_name=f"{topic[:30].replace(' ', '_')}_notes.md",
                        mime="text/markdown"
                    )
        else:
            st.warning("Please enter a topic!")

elif tool == "🎴 Flashcards":
    st.markdown("### 🎴 Flashcard Generator")
    topic = st.text_input("Enter topic:", placeholder="e.g., Data Structures Key Terms")
    num_cards = st.slider("Number of flashcards:", 5, 20, 10)

    if st.button("Generate Flashcards", type="primary"):
        if topic:
            with st.spinner("Creating flashcards..."):
                llm = get_llm(model)
                prompt = PromptTemplate(
                    template="""Create {num_cards} flashcards for: {topic}

Format each as:
CARD 1
Front: [Question/Term]
Back: [Answer/Definition with brief example]

---

Focus on the most important concepts for exam preparation.""",
                    input_variables=["topic", "num_cards"]
                )

                chain = prompt | llm | StrOutputParser()
                result = chain.invoke({"topic": topic, "num_cards": num_cards})

                st.success("✅ Flashcards ready!")

                # Display in expandable format
                cards = result.split("---")
                for idx, card in enumerate(cards):
                    if card.strip():
                        with st.expander(f"🎴 Card {idx + 1}"):
                            st.markdown(card)

                st.download_button(
                    "📥 Download Flashcards",
                    data=result,
                    file_name=f"{topic.replace(' ', '_')}_flashcards.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Please enter a topic!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>💡 <b>Study Tip:</b> Use multiple tools together for better retention!</p>
    <p>📚 Built for students, by students</p>
</div>
""", unsafe_allow_html=True)
