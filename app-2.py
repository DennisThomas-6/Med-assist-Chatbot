import streamlit as st

# -----------------------------
# Load medical knowledge file
# -----------------------------
def load_medical_data():
    with open("medical_data.txt", "r") as f:
        return f.read()

medical_text = load_medical_data()

# Split data into sections properly
sections = medical_text.split("==============================")

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="MedAssist", layout="centered")

st.title("🩺 MedAssist Chatbot (Upgraded Search)")
st.warning("⚠️ General health info only. Consult a doctor for serious symptoms.")

# -----------------------------
# Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# Improved Search Function
# -----------------------------
def find_matching_answers(user_query):
    results = []
    query_words = user_query.lower().split()

    for sec in sections:
        for word in query_words:
            if word.strip() != "" and word in sec.lower():
                results.append(sec.strip())
                break

    # Remove duplicates
    unique_results = list(dict.fromkeys(results))

    return unique_results

# -----------------------------
# User Input
# -----------------------------
user_input = st.chat_input("Ask a health question (e.g., fever + cold)...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    matches = find_matching_answers(user_input)

    if matches:
        reply = "✅ Here is the best guidance based on your symptoms:\n\n"
        for ans in matches[:3]:  # limit to top 3 matches
            reply += f"---\n{ans}\n\n"
    else:
        reply = "❌ Sorry, I don't have information on that. Please consult a doctor."

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)

st.info(" ")
