import streamlit as st
import pandas as pd
from pandasql import sqldf
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.agents import create_agent
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

# PAGE TITLE
st.title("Intelligent Multi-Tool Agent")


# SIDEBAR AGENT SELECTION
agent_type = st.sidebar.radio(
    "Choose Agent",
    ["CSV Question Answering Agent", "Sunbeam Internship Agent"]
)


# SESSION STATE
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def show_chat():
    for role, msg in st.session_state.chat_history:
        if role == "user":
            st.markdown(f"**You:** {msg}")
        else:
            st.markdown(f"**Agent:** {msg}")


# LLM INITIALIZATION (COMMON)
llm = init_chat_model(
    model="llama3-docchat-1.0-8b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy_key"
)


#  CSV AGENT
if agent_type == "CSV Question Answering Agent":

    st.subheader("CSV Question Answering Agent")

    file = st.file_uploader("Upload CSV", type="csv")

    if file:
        df = pd.read_csv(file)

        st.subheader("CSV Schema")
        st.write(df.dtypes)

        # CSV TOOL
        @tool
        def csv_tool(query: str) -> str:
            """
            Executes an SQL query on the uploaded CSV file
            and returns the result as text.
            """
            try:
                return sqldf(query, {"data": df}).to_string(index=False)
            except Exception as e:
                return f"SQL Error: {e}"

        agent = create_agent(
            model=llm,
            tools=[csv_tool]
        )

        user_input = st.text_input("Ask a question about the CSV")

        if st.button("Run") and user_input:

            st.session_state.chat_history.append(("user", user_input))

            sql_prompt = f"""
            Table: data
            Schema: {df.dtypes}
            Convert the question into SQL only.
            Question: {user_input}
            """

            response = agent.invoke(
                {"messages": [{"role": "user", "content": sql_prompt}]}
            )

            sql = response["messages"][-1].content

            st.session_state.chat_history.append(
                ("agent", f"Generated SQL:\n{sql}")
            )

            explain_prompt = f"""
            Explain this SQL query in simple English.
            SQL: {sql}
            """

            response = agent.invoke(
                {"messages": [{"role": "user", "content": explain_prompt}]}
            )

            explanation = response["messages"][-1].content

            st.session_state.chat_history.append(
                ("agent", f"Explanation:\n{explanation}")
            )

            st.subheader("Generated SQL")
            st.code(sql, language="sql")

            st.subheader("Explanation")
            st.write(explanation)


#  SUNBEAM SCRAPING AGENT
else:
    st.subheader("Sunbeam Internship Agent")

    #SCRAPING TOOL
    @tool
    def sunbeam_scraping_tool(query: str) -> str:
        """
        Scrapes internship and batch information from
        Sunbeam Institute website.
        """
        driver = webdriver.Chrome()
        driver.get("https://www.sunbeaminfo.in/internship")
        time.sleep(3)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        try:
            plus_button = driver.find_element(By.XPATH, "//a[@href='#collapseSix']")
            driver.execute_script("arguments[0].scrollIntoView(true);", plus_button)
            plus_button.click()
            time.sleep(2)
        except:
            pass

        info = []
        para = driver.find_elements(By.CSS_SELECTOR, ".main_info.wow.fadeInUp")
        for p in para:
            info.append(p.text)

        rows = driver.find_elements(By.TAG_NAME, "tr")
        batches = []

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 8:
                continue

            batches.append({
                "batch": cols[1].text,
                "duration": cols[2].text,
                "start_date": cols[3].text,
                "end_date": cols[4].text,
                "time": cols[5].text,
                "fees": cols[6].text
            })

        driver.quit()

        return json.dumps(
            {"internship_info": info, "batches": batches},
            indent=2
        )

    agent = create_agent(
        model=llm,
        tools=[sunbeam_scraping_tool]
    )

    user_input = st.text_input("Ask about Sunbeam internships")

    if st.button("Run") and user_input:

        st.session_state.chat_history.append(("user", user_input))

        response = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]}
        )

        answer = response["messages"][-1].content

        st.session_state.chat_history.append(("agent", answer))

        st.subheader("Agent Response")
        st.write(answer)

# CHAT HISTORY
st.subheader("Complete Chat History")
show_chat()