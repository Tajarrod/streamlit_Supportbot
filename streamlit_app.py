import streamlit as st
import requests
import base64
import json
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="SyncroPatch Support Bot",
    page_icon="]i[",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: inline-block;
        max-width: 80%;
        word-wrap: break-word;
        clear: both;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        margin-left: auto;
        text-align: right;
        float: right;
    }
    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
        margin-right: auto;
        text-align: left;
        float: left;
    }
    .file-info {
        background-color: #e8f5e8;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
    }
    
    /* Clearfix for chat messages */
    .chat-container::after {
        content: "";
        display: table;
        clear: both;
    }
    
    /* Teams-like input bar */
    .teams-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 12px 20px;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        z-index: 1000;
        border-top: 1px solid #e0e0e0;
    }
    
    .teams-input-bar {
        display: flex;
        align-items: center;
        background: #f8f9fa;
        border: 1px solid #e1e5e9;
        border-radius: 20px;
        padding: 8px 16px;
        gap: 12px;
        max-width: 100%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .teams-input-field {
        flex: 1;
        border: none;
        background: transparent;
        outline: none;
        font-size: 14px;
        color: #323130;
        min-width: 0;
    }
    
    .teams-input-field::placeholder {
        color: #8a8886;
    }
    
    .teams-icon-button {
        width: 40px;
        height: 40px;
        border: none;
        background: #ff6b35;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 20px;
        font-weight: bold;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .teams-icon-button:hover {
        background: #e55a2b;
        color: white;
        transform: scale(1.05);
    }
    
    .teams-send-button {
        background: #0078d4;
        color: white;
        border-radius: 50%;
        width: 32px;
        height: 32px;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        transition: all 0.2s ease;
    }
    
    .teams-send-button:hover {
        background: #106ebe;
        transform: scale(1.05);
    }
    
    .teams-separator {
        width: 1px;
        height: 20px;
        background: #e1e5e9;
        margin: 0 4px;
    }
    
    /* Hide the default file uploader completely */
    .stFileUploader > div {
        display: none !important;
    }
    
    /* Hide drag and drop area completely */
    .stFileUploader > div > div:nth-child(2) {
        display: none !important;
    }
    
    /* Hide file list area */
    .stFileUploader > div > div:nth-child(3) {
        display: none !important;
    }
    
    /* Hide the drag and drop area */
    .stFileUploader > div:first-child > div:nth-child(2) {
        display: none !important;
    }
    
    /* Hide all file uploader content except the button */
    .stFileUploader > div > div {
        display: none !important;
    }
    
    /* Show only the button */
    .stFileUploader > div > div:first-child {
        display: block !important;
    }
    
    /* Hide any text or labels */
    .stFileUploader label {
        display: none !important;
    }
    
    /* Hide file uploader text */
    .stFileUploader span {
        display: none !important;
    }
    
    /* Hide any file list or multiple file indicators */
    .stFileUploader > div:first-child > div:nth-child(3) {
        display: none !important;
    }
    
    /* Hide all drag and drop areas completely */
    .stFileUploader > div > div[data-testid="stFileUploaderDropzone"] {
        display: none !important;
    }
    
    /* Hide any drag and drop text */
    .stFileUploader > div > div:contains("Drag and drop") {
        display: none !important;
    }
    
    /* Hide file uploader container content except button */
    .stFileUploader > div > div:not(:first-child) {
        display: none !important;
    }
    
    /* Hide all file uploader content except the button */
    .stFileUploader > div {
        display: flex !important;
        align-items: center !important;
    }
    
    /* Hide any drag and drop areas */
    .stFileUploader [data-testid*="dropzone"],
    .stFileUploader [class*="dropzone"],
    .stFileUploader [class*="drag"] {
        display: none !important;
    }
    
    /* Hide any text elements */
    .stFileUploader p,
    .stFileUploader div:not(:first-child) {
        display: none !important;
    }
    
    /* Style the gray drag area to show "Drop here" */
    .stFileUploader > div > div:nth-child(2) {
        display: block !important;
        background: #f0f0f0 !important;
        border: 2px dashed #ccc !important;
        border-radius: 8px !important;
        padding: 20px !important;
        text-align: center !important;
        color: #666 !important;
        font-size: 16px !important;
        font-weight: bold !important;
    }
    
    /* Hide any drag and drop text */
    .stFileUploader > div > div:nth-child(3) {
        display: none !important;
    }
    
    /* Hide any text elements */
    .stFileUploader p {
        display: none !important;
    }
    
    /* Keep the button visible */
    .stFileUploader > div > div:first-child {
        display: block !important;
    }
    
    /* Keep the message bar visible */
    .stChatInput {
        display: block !important;
    }
    
    /* Custom file uploader container */
    .custom-upload-container {
        position: relative;
        display: inline-block;
    }
    
    /* Style the clear file button */
    .stButton > button[kind="secondary"] {
        background: #f44336 !important;
        color: white !important;
        border: none !important;
        border-radius: 50% !important;
        width: 32px !important;
        height: 32px !important;
        min-height: 32px !important;
        padding: 0 !important;
        font-size: 16px !important;
        margin-right: 8px !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #d32f2f !important;
        transform: scale(1.05) !important;
    }
    
    /* Chat input styling */
    .chat-input-container {
        flex: 1;
        min-width: 0;
    }
    
    /* Add padding to main content to prevent overlap */
    .main .block-container {
        padding-bottom: 100px;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .fixed-bottom-container {
            padding: 10px 15px;
        }
        .upload-button {
            width: 44px;
            height: 44px;
            font-size: 20px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_id" not in st.session_state:
    st.session_state.user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()
if "current_file" not in st.session_state:
    st.session_state.current_file = None
if "file_uploader_key" not in st.session_state:
    st.session_state.file_uploader_key = 0

# Azure Function URLs
AZURE_FUNCTION_URL = os.getenv("AZURE_FUNCTION_URL", "https://openai-teams-bot-file-text2-f6d3f6bce5d7g6hx.canadacentral-01.azurewebsites.net/api/getOpenAIReply")
JIRA_QUERY_URL = os.getenv("JIRA_QUERY_URL", "mock")
JIRA_STATS_URL = os.getenv("JIRA_STATS_URL", "mock")
CREATE_ISSUE_URL = os.getenv("CREATE_ISSUE_URL", "mock")

# JIRA Integration Functions
def call_jira_function(endpoint, data):
    """Call Azure Function endpoint for JIRA operations"""
    if endpoint == "mock":
        # Return mock data for demonstration
        if "jira-query" in str(data) or "query" in str(data):
            return {
                "issues": [
                    {"key": "FSM-123", "summary": "Fix login issue", "status": "In Progress", "assignee": "John Doe"},
                    {"key": "FSM-124", "summary": "Update documentation", "status": "Done", "assignee": "Jane Smith"},
                    {"key": "FSM-125", "summary": "Add new feature", "status": "To Do", "assignee": "Mike Johnson"}
                ]
            }
        elif "jira-stats" in str(data) or "stats" in str(data):
            return {
                "total_issues": 15,
                "by_status": {"To Do": 5, "In Progress": 7, "Done": 3},
                "by_assignee": {"John Doe": 6, "Jane Smith": 4, "Mike Johnson": 5}
            }
        elif "create-issue" in str(data) or "create" in str(data):
            return {
                "success": True,
                "issue_key": "FSM-126",
                "message": "Issue created successfully"
            }
    
    try:
        response = requests.post(endpoint, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Function call failed: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}

def handle_jira_query(user_input):
    """Handle JIRA queries through Azure Function"""
    if JIRA_QUERY_URL == "mock":
        # Return formatted mock data for better display
        issues = [
            {"key": "FSM-123", "summary": "Fix login issue", "status": "In Progress", "assignee": "John Doe"},
            {"key": "FSM-124", "summary": "Update documentation", "status": "Done", "assignee": "Jane Smith"},
            {"key": "FSM-125", "summary": "Add new feature", "status": "To Do", "assignee": "Mike Johnson"}
        ]
        
        # Format the response nicely
        response = f"🔍 **JIRA Issues Found**\n\n"
        for issue in issues:
            response += f"**{issue['key']}** - {issue['summary']}\n"
            response += f"• Status: {issue['status']}\n"
            response += f"• Assignee: {issue['assignee']}\n\n"
        
        return response
    
    data = {"question": user_input}
    result = call_jira_function(JIRA_QUERY_URL, data)
    
    if "error" in result:
        return f"❌ Error: {result['error']}"
    else:
        return result.get("reply", "No response received")

def handle_jira_stats(user_input):
    """Handle JIRA statistics through Azure Function"""
    if JIRA_STATS_URL == "mock":
        # Return formatted mock data for better display
        stats = {
            "total_issues": 15,
            "by_status": {"To Do": 5, "In Progress": 7, "Done": 3},
            "by_assignee": {"John Doe": 6, "Jane Smith": 4, "Mike Johnson": 5}
        }
        
        # Format the response nicely
        response = f"📊 **JIRA Statistics**\n\n"
        response += f"**Total Issues:** {stats['total_issues']}\n\n"
        response += f"**By Status:**\n"
        for status, count in stats['by_status'].items():
            response += f"• {status}: {count}\n"
        response += f"\n**By Assignee:**\n"
        for assignee, count in stats['by_assignee'].items():
            response += f"• {assignee}: {count}\n"
        
        return response
    
    data = {"question": user_input}
    result = call_jira_function(JIRA_STATS_URL, data)
    
    if "error" in result:
        return f"❌ Error: {result['error']}"
    else:
        return result.get("reply", "No response received")

def handle_issue_creation(user_input):
    """Handle issue creation through Azure Function"""
    if CREATE_ISSUE_URL == "mock":
        # Return mock data directly
        return {
            "success": True,
            "issue_key": "FSM-126",
            "message": "Issue created successfully"
        }
    
    data = {"request": user_input}
    result = call_jira_function(CREATE_ISSUE_URL, data)
    
    if "error" in result:
        return f"❌ Error: {result['error']}"
    else:
        return result.get("reply", "No response received")

# Header
st.markdown('<h1 class="main-header"><span style="font-size: 1.5em; font-weight: bold; color: #000000;">]i[</span><br>SyncroPatch Support Bot</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    # Bot Information
    st.subheader("🤖 About SyncroPatch Bot")
    st.markdown("""
    I am **SyncroPatch support bot** and you can ask me technical and application questions. 
    
    **My capabilities:**
    - 🔍 **JIRA Integration** - Query issues, create tickets, view statistics
    - 📄 **Document Analysis** - PDF, Word, Excel, images
    - 🧠 **Memory** - Remembers context for one hour
    - 🎯 **Project Access** - FSM, FSO, SP-WISHLIST, SCS projects
    - 💬 **Technical Support** - SyncroPatch questions and help
    
    **JIRA Commands:**
    - "Show recent issues in FSM project"
    - "Create new bug ticket in SPWISH"
    - "What are the statistics for FSO project?"
    
    **To reset my memory:** Just tell me!
    """)
    
    st.markdown("---")
    
    # Quick Instructions
    st.subheader("💡 Quick Tips")
    st.markdown("""
    • **Type messages** and press Enter
    • **Upload files** using the + icon
    • **Ask questions** about documents or images
    • **Get technical support** for SyncroPatch
    • **JIRA live queries** - "show me issues in FSM project live query"
    • **Create issues** - "create new issue in FSM project live query"
    """)
    
    st.markdown("---")
    
    # JIRA Test Button
    st.subheader("🔧 JIRA Connection Test")
    if st.button("Test JIRA Connection", type="secondary"):
        with st.spinner("Testing JIRA connection..."):
            test_result = handle_jira_query("what are the recent issues in SPWISH project?")
            st.write("**Test Result:**")
            st.write(test_result)
    
    st.markdown("---")
    
    # Clear chat button at bottom
    if st.button("🗑️ Clear Chat", type="secondary"):
        st.session_state.messages = []
        st.session_state.processed_files = set()
        st.session_state.current_file = None
        st.session_state.file_uploader_key += 1
        st.rerun()

# Main chat interface
st.subheader("💬 Chat with SyncroPatch Bot")

# Show current file status in compact box with X button
if st.session_state.current_file is not None:
    st.markdown(f"""
    <div style="background-color: #ffebee; border: 1px solid #f44336; border-radius: 4px; padding: 8px 12px; margin: 8px 0; display: inline-flex; align-items: center; gap: 8px;">
        <span style="color: #d32f2f; font-size: 12px;">📎 <strong>File ready:</strong> {st.session_state.current_file.name}</span>
        <button onclick="clearFile()" style="background: #f44336; color: white; border: none; border-radius: 3px; padding: 4px 8px; cursor: pointer; font-size: 12px;">✕</button>
    </div>
    """, unsafe_allow_html=True)

# Display chat messages
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.messages:
    timestamp = message.get("timestamp", "")
    if message["role"] == "user":
        st.markdown(f'<div class="chat-message user-message"><div style="font-size: 0.8em; color: #666; margin-bottom: 0.3rem;">{timestamp}</div><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message bot-message"><div style="font-size: 0.8em; color: #666; margin-bottom: 0.3rem;">{timestamp}</div><strong>SyncroPatch Bot:</strong> {message["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Simplified input bar
st.markdown('<div class="teams-input-container">', unsafe_allow_html=True)
st.markdown('<div class="teams-input-bar">', unsafe_allow_html=True)

# Clear file button is now in the file status box above

# File upload button (+ icon)
uploaded_file = st.file_uploader(
    "+",
    type=['pdf', 'docx', 'xlsx', 'txt', 'jpg', 'jpeg', 'png', 'gif', 'webp'],
    help="Attach file",
    label_visibility="collapsed",
    key=f"file_uploader_main_{st.session_state.get('file_uploader_key', 0)}",
    accept_multiple_files=False
)

# Message input field
user_input = st.chat_input("Type a message", key="chat_input_main")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Handle X button click for clearing file
if st.button("Clear File", key="clear_file_x", help="Clear the attached file"):
    st.session_state.current_file = None
    st.session_state.file_uploader_key += 1
    st.rerun()

# Handle file upload - store in session state without processing
if uploaded_file is not None and st.session_state.current_file is None:
    st.session_state.current_file = uploaded_file
    st.success(f"📎 File ready: {uploaded_file.name}")

# JavaScript to style the file uploader as plus icon button
st.markdown("""
<script>
// Function to clear file
function clearFile() {
    // Trigger a Streamlit rerun with clear file action
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        key: 'clear_file_x',
        value: true
    }, '*');
}

// Wait for the page to load
setTimeout(function() {
    // Find the file uploader button
    const fileUploader = document.querySelector('[data-testid="stFileUploader"] button');
    if (fileUploader) {
        // Style it as a circular orange plus icon button
        fileUploader.style.cssText = `
            width: 40px !important;
            height: 40px !important;
            border-radius: 50% !important;
            background: #ff6b35 !important;
            border: none !important;
            color: white !important;
            font-size: 20px !important;
            font-weight: bold !important;
            cursor: pointer !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: all 0.2s ease !important;
            margin: 0 !important;
            padding: 0 !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        `;
        
        // Hide the text and add plus icon
        const span = fileUploader.querySelector('span');
        if (span) {
            span.style.display = 'none';
        }
        
        // Add plus icon
        if (!fileUploader.querySelector('.plus-icon')) {
            const plusIcon = document.createElement('div');
            plusIcon.className = 'plus-icon';
            plusIcon.innerHTML = '+';
            plusIcon.style.cssText = `
                font-size: 20px;
                font-weight: bold;
                line-height: 1;
                color: white;
            `;
            fileUploader.appendChild(plusIcon);
        }
        
        // Add hover effect
        fileUploader.addEventListener('mouseenter', function() {
            this.style.background = '#e55a2b';
            this.style.transform = 'scale(1.05)';
        });
        
        fileUploader.addEventListener('mouseleave', function() {
            this.style.background = '#ff6b35';
            this.style.transform = 'scale(1)';
        });
        
        // Style the gray drag area to show "Drop here"
        const fileUploaderContainer = document.querySelector('[data-testid="stFileUploader"]');
        if (fileUploaderContainer) {
            // Style the gray drag area (second child)
            const dragArea = fileUploaderContainer.querySelector('div:nth-child(2)');
            if (dragArea) {
                dragArea.style.display = 'block';
                dragArea.style.background = '#f0f0f0';
                dragArea.style.border = '2px dashed #ccc';
                dragArea.style.borderRadius = '8px';
                dragArea.style.padding = '20px';
                dragArea.style.textAlign = 'center';
                dragArea.style.color = '#666';
                dragArea.style.fontSize = '16px';
                dragArea.style.fontWeight = 'bold';
                dragArea.innerHTML = 'Drop here';
            }
            
            // Hide any text elements
            const textElements = fileUploaderContainer.querySelectorAll('p');
            textElements.forEach(element => {
                element.style.display = 'none';
            });
        }
    }
}, 1000);
</script>
""", unsafe_allow_html=True)

# Process user input - when user sends a message or uploads a file
if user_input or (uploaded_file is not None and st.session_state.current_file is None):
    # Add user message to chat immediately with timestamp
    if user_input:
        current_time = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "role": "user", 
            "content": user_input,
            "timestamp": current_time
        })
    
    # Determine which function to call based on user input
    user_input_lower = user_input.lower() if user_input else ""
    
    # Check if this is a JIRA-related request with "live query" specified
    if any(keyword in user_input_lower for keyword in ["jira", "issue", "ticket", "bug", "task", "story", "epic"]) and "live query" in user_input_lower:
        # Handle JIRA live query requests
        with st.spinner("]i[ SyncroPatch Bot is querying JIRA live data..."):
            try:
                if "create" in user_input_lower or "new" in user_input_lower or "add" in user_input_lower:
                    ai_response = handle_issue_creation(user_input)
                elif "stat" in user_input_lower or "dashboard" in user_input_lower or "how many" in user_input_lower or "count" in user_input_lower:
                    ai_response = handle_jira_stats(user_input)
                else:
                    ai_response = handle_jira_query(user_input)
                
                # Add JIRA response to chat with timestamp
                bot_time = datetime.now().strftime("%H:%M")
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": ai_response,
                    "timestamp": bot_time
                })
                
                # Clear the current file after processing
                if st.session_state.current_file is not None:
                    st.session_state.current_file = None
                    st.session_state.file_uploader_key += 1
                    st.rerun()
                
            except Exception as e:
                error_msg = f"JIRA processing error: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": f"❌ {error_msg}"})
                st.error(error_msg)
    
    else:
        # Handle regular AI requests (original functionality)
        # Prepare request to Azure Function
        payload = {
            "question": user_input or "Please analyze this file",
            "userId": st.session_state.user_id
        }
        
        # Handle file upload - only if there's a current file
        if st.session_state.current_file is not None:
            # Read file content
            file_content = st.session_state.current_file.read()
            file_base64 = base64.b64encode(file_content).decode('utf-8')
            
            payload["fileContent"] = file_base64
            payload["fileType"] = st.session_state.current_file.type
        
        # Show loading spinner and process request
        with st.spinner("]i[ SyncroPatch Bot is analyzing..."):
            try:
                # Call Azure Function
                response = requests.post(
                    AZURE_FUNCTION_URL,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result.get("reply", "No response received")
                    
                    # Add Support AI response to chat with timestamp
                    bot_time = datetime.now().strftime("%H:%M")
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": ai_response,
                        "timestamp": bot_time
                    })
                    
                    # Clear the current file after processing
                    st.session_state.current_file = None
                    
                    # Increment file uploader key to reset the widget
                    st.session_state.file_uploader_key += 1
                    
                    # Force clear the file uploader by rerunning
                    st.rerun()
                    
                else:
                    error_msg = f"Error {response.status_code}: {response.text}"
                    st.session_state.messages.append({"role": "assistant", "content": f"❌ {error_msg}"})
                    st.error(error_msg)
                    
            except requests.exceptions.RequestException as e:
                error_msg = f"Connection error: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": f"❌ {error_msg}"})
                st.error(error_msg)
    
    # Rerun to update the chat
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>]i[ SyncroPatch Support Bot | 🚀 Powered by OpenAI Assistant API</p>
    <p>Technical support for SyncroPatch systems and applications</p>
</div>
""", unsafe_allow_html=True)