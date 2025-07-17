import streamlit as st
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyD5eZZP3Pfq2aeuHfgvorWHJdN32-ZX2LM"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def main():
    st.set_page_config(page_title="SQL Query Generator 🌐", page_icon="🤖")
    st.markdown(
        """<div style="text-align: center;">
               <h1>SQL Query Generator 🌐 🤖 ⚛ </h1>
               <h3>I can generate SQL queries for you!</h3>
               <h4>With Explanation as well!!!</h4>
               <p>This tool generates SQL queries based on your input.</p>
            </div>""",
        unsafe_allow_html=True,
    )

    text_input = st.text_area("Enter your Query here in Plain English:")

    if st.button("Generate SQL Query"):
        with st.spinner("Generating SQL Query..."):

            # ✅ Generate SQL Query
            template = """
                Create a SQL query snippet using the following request:
                
                {text_input}

                I just want the SQL Query.
            """
            formatted_template = template.format(text_input=text_input)
            sql_query = model.generate_content(formatted_template).text.strip()
            sql_query = sql_query.strip("```").replace("sql", "").strip()

            # ✅ Show SQL Query
            st.subheader("✅ SQL Query")
            st.code(sql_query, language="sql")

            # ✅ Generate Expected Output
            expected_output = """
                What would be the expected response of the SQL query snippet:
                
                {sql_query}

                Provide sample tabular response with no explanation.
            """
            expected_output_formatted = expected_output.format(sql_query=sql_query)
            eoutput = model.generate_content(expected_output_formatted).text

            st.subheader("📊 Expected Output")
            st.markdown(eoutput)

            # ✅ Generate Explanation
            explanation = """
                Explain this SQL Query in the simplest way:
                
                {sql_query}
            """
            explanation_formatted = explanation.format(sql_query=sql_query)
            explanation_text = model.generate_content(explanation_formatted).text

            st.subheader("ℹ️ Explanation")
            st.markdown(explanation_text)

            # ✅ Success messages
            with st.container():
                st.success("✅ SQL Query Generated Successfully! Here is your query:")
                st.code(sql_query, language="sql")

                st.success("📊 Expected Output of this SQL Query:")
                st.markdown(eoutput)

                st.success("ℹ️ Simple Explanation:")
                st.markdown(explanation_text)

main()
