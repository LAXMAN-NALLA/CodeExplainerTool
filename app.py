import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Language options for explanation
LANGUAGES = ["English", "Hindi", "Telugu" , "Tamil", "Spanish", "French", "German"]
DEPTH_LEVELS = ["Beginner", "Intermediate", "Advanced"]

# Initialize Gemini AI Model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    google_api_key=GOOGLE_API_KEY
)

def main():
    # Sidebar instructions
    st.sidebar.title("ℹ️ Instructions")
    st.sidebar.write("""
    1. Paste your code in the text box (any programming language).
    2. Choose the language and explanation depth.
    3. Click *EXPLAIN CODE*.
    4. Scroll down to view or download the explanation.
    """)

    st.title("💡 CODE EXPLAINER")
    st.write("This tool helps you understand code snippets in plain language.")

    # Code input
    user_query = st.text_area("Paste your CODE here:", height=200)

    # Language dropdown
    selected_language = st.selectbox("🌍 Select explanation language:", LANGUAGES)
    selected_depth = st.selectbox("📚 Select explanation depth:", DEPTH_LEVELS)


    # See Example button
    if st.button("See Example"):
        example_code = '''def factorial(n): 
    if n == 0: return 1
    return n * factorial(n-1)'''
        st.code(example_code, language="python")

    # Explain button
    if st.button("EXPLAIN CODE"):
        if user_query.strip():
            with st.spinner("🔍 Analyzing code..."):
                try:
                    # Prompt with dynamic language
                    prompt = ChatPromptTemplate.from_messages([
                        ("system",f"""You are an expert programming tutor. Explain the code below in {selected_language} with {selected_depth} level of detail. 
Break down the explanation into:
- What the code does
- How it works (line-by-line or logically)
- Key concepts, programming patterns, or edge cases
Make it simple and readable for a {selected_depth} learner."""),
                        ("user", "{user_query}")
                    ])

                    chain = prompt | llm
                    response = chain.invoke({"user_query": user_query})
                    explanation = response.content if hasattr(response, "content") else str(response)

                    st.subheader("📝 Explanation:")
                    st.success("✅ Analysis completed successfully!")
                    st.markdown(explanation)

                    st.download_button(
                        "📥 Download Explanation", explanation, file_name="code_explanation.txt"
                    )

                except Exception as e:
                    st.error(f"⚠️ API Error: Unable to process request. Details: {e}")
        else:
            st.warning("⚠️ Please enter some code before clicking EXPLAIN.")

# Corrected entry point
if __name__ == "__main__":
    main()
