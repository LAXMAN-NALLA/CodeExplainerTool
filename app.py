import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Initialize Gemini AI Model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

# Define Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", """Please explain this code in plain language, focusing on:
    1. What the code does
    2. How it works
    3. Any important concepts or patterns used."""),
    
    ("user", "{user_query}")
])

def main():
    # Sidebar for instructions
    st.sidebar.title("ℹ️ Instructions")
    st.sidebar.write("""
    1. Paste your code in the text box (can be in any programming language).
    2. Click **EXPLAIN CODE** to get a detailed explanation of your code.
    3. Click **See Example** to try a sample code.
    4. Scroll down to read the explanation clearly.
    """)

    # Main title
    st.title("💡 CODE EXPLAINER")
    st.write("This tool helps you understand code snippets in plain language.")

    # Code input area
    user_query = st.text_area("Paste your CODE here:", height=200)

    # Example button to show a sample
    if st.button("See Example"):
        example_code = '''def factorial(n): 
    if n == 0: return 1
    return n * factorial(n-1)'''
        st.code(example_code, language="python")

    # Explain button logic
    if st.button("EXPLAIN CODE"):
        if user_query.strip():
            with st.spinner("🔍 Analyzing code..."):
                try:
                    # Generate explanation with the prompt and AI model
                    chain = prompt | llm
                    response = chain.invoke({"user_query": user_query})

                    # Extract the explanation text correctly
                    explanation = response.content if hasattr(response, "content") else str(response)

                    st.subheader("📝 Explanation:")
                    st.success("✅ Analysis completed successfully!")
                    st.markdown(explanation)  # Clean display of explanation

                    st.download_button(
                        "📥 Download Explanation", explanation, file_name="code_explanation.txt"
                        )

                except Exception as e:
                    st.error(f"⚠️ API Error: Unable to process request. Details: {e}")
        else:
            st.warning("⚠️ Please enter some code before clicking EXPLAIN.")

if __name__ == "__main__":
    main()
