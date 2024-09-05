import streamlit as st
from openai import OpenAI
from sqlalchemy import text

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What's up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})

    conn = st.connection("chat_db", type='sql')
    with conn.session as s:
        s.execute(text('CREATE TABLE IF NOT EXISTS dialog (user TEXT, assistant TEXT);'))
        s.execute(
            text('INSERT INTO dialog (user, assistant) VALUES (:in_prompt, :in_response);'),
            params=dict(in_prompt=prompt, in_response=response)
        )
        dialog = s.execute(text("SELECT * FROM dialog"))
        s.commit()

    st.dataframe(dialog)