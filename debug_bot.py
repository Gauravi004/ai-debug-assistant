import streamlit as st
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Debug Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------- DARK SAAS THEME ----------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #111827, #0b1220);
    color: #e5e7eb;
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
}

/* inputs */
.stTextInput input, .stSelectbox div {
    background-color: #1f2937 !important;
    color: #e5e7eb !important;
    border-radius: 10px;
    
}

/* button */
.stButton button {
    background: linear-gradient(90deg, #6366f1, #3b82f6);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.5rem 1rem;
}

/* text */
h1, h2, h3, p, label {
    color: #e5e7eb !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- MEMORY ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>🤖 AI Debug Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Professional Backend Debugging Tool</p>", unsafe_allow_html=True)

st.markdown("---")

# ---------------- AI ENGINE (DETAILED) ----------------
def ai_engine(error_type, user_input):

    text = user_input.lower()

    if "403" in text or error_type == "API / Auth Error":
        return """
🔴 403 AUTHORIZATION ERROR

🧠 Meaning:
Server understood request but refuses access.

📌 Causes:
- Missing/invalid token
- Expired session
- Wrong headers
- Permission denied (role issue)

🛠 Fix:
1. Add Authorization header (Bearer token)
2. Re-login and refresh token
3. Check backend role permissions
4. Verify API request in Postman

💡 Insight:
403 = You are identified but NOT allowed.
"""

    if "500" in text or error_type == "Server Error":
        return """
🔵 500 INTERNAL SERVER ERROR

🧠 Meaning:
Backend crashed while processing request.

📌 Causes:
- Null/undefined variables
- DB connection failure
- Unhandled exceptions
- Logic errors in backend

🛠 Fix:
1. Check backend logs
2. Wrap code in try/except
3. Validate DB connection
4. Debug last executed function

💡 Insight:
500 = Server failed internally (not user fault).
"""

    if "404" in text:
        return """
🟡 404 NOT FOUND ERROR

🧠 Meaning:
Requested API route does not exist.

📌 Causes:
- Wrong endpoint URL
- Missing route in backend
- Typo in API path

🛠 Fix:
1. Check API URL
2. Verify backend routes
3. Test in Postman

💡 Insight:
404 = Route not found on server.
"""

    if "422" in text:
        return """
🟠 422 VALIDATION ERROR

🧠 Meaning:
Request format is correct but data is invalid.

📌 Causes:
- Missing required fields
- Wrong data types
- Schema mismatch

🛠 Fix:
1. Validate request body
2. Match backend schema
3. Ensure required fields exist

💡 Insight:
422 = Data invalid, not request failure.
"""

    return f"""
🤖 GENERAL DEBUG ANALYSIS

🧠 Issue:
{user_input}

📌 Checks:
- API endpoint
- Request body
- Backend logs
- Authentication headers

💡 Tip:
Always include error codes for better debugging accuracy.
"""

# ---------------- SEARCH ----------------
col1, col2 = st.columns([1, 3])

with col1:
    search = st.text_input("🔍 Search past errors")

with col2:
    st.write("")

# ---------------- MAIN UI ----------------
st.markdown("## 💬 Debug Your Issue")

error_type = st.selectbox(
    "📌 Select Error Type",
    ["API / Auth Error", "Server Error", "Docker Issue", "Git Error", "Module Error"]
)

user_input = st.text_input(
    "💬 Describe your issue",
    placeholder="e.g. error 403 coming in login API"
)

# ---------------- BUTTON ----------------
if st.button("🚀 Ask AI Assistant"):

    response = ai_engine(error_type, user_input)

    st.session_state.history.append({
        "type": error_type,
        "input": user_input,
        "response": response
    })

    placeholder = st.empty()
    output = ""

    for char in response:
        output += char
        time.sleep(0.001)
        placeholder.markdown(output)

# ---------------- QUICK ACTIONS ----------------
st.markdown("---")
st.markdown("### 💡 Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("Check Logs")

with col2:
    st.info("Verify API")

with col3:
    st.info("Check Auth")

# ---------------- SEARCH FIXED ----------------
if search.strip():

    st.markdown("### 📂 Search Results")

    found = False
    query = search.lower()

    for item in st.session_state.history:

        if query in item["input"].lower() or query in item["response"].lower():

            st.markdown(f"""
🧑‍💻 **Issue:** {item['input']}  
📌 **Type:** {item['type']}  

🤖 **Full Debug Report:**  
{item['response']}
""")
            st.markdown("---")
            found = True

    if not found:
        st.warning("No matching results found.")

# ---------------- CLEAR HISTORY ----------------
if st.button("🧹 Clear History"):
    st.session_state.history = []
    st.success("History cleared!")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🤖 AI Debug Assistant • Professional Backend SaaS Tool")