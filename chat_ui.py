css = """
<style>
    /* General layout adjustments */
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Style for the PDF upload section */
    .stFileUploader {
        background-color: #F0F2F6;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
    }

    /* Style for cards */
    .card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }

    /* Style for buttons */
    .stButton > button {
        background-color: #1F77B4;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        transition: background-color 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #0056b3;
    }

    /* Speech bubbles for the chat interface */
    .user-message {
        background-color: #1F77B4;
        color: white;
        padding: 15px;
        border-radius: 20px;
        margin-bottom: 10px;
        width: fit-content;
        max-width: 70%;
        float: right;  /* Aligns user messages to the right */
        text-align: right;
    }

    .bot-message {
        background-color: #EAEAEA;
        color: #333;
        padding: 15px;
        border-radius: 20px;
        margin-bottom: 10px;
        width: fit-content;
        max-width: 70%;
    }

    /* Avatars for user and bot */
    .avatar {
        border-radius: 50%;
        margin-right: 10px;
        height: 40px;
        width: 40px;
    }

    /* Chat layout */
    .chat-container {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    
    /* Specific to user message (right aligned) */
    .chat-container.user {
        justify-content: flex-end;  /* Pushes the user message to the right */
    }
    
    /* Font improvements */
    .stHeader, .stText {
        font-family: 'Roboto', sans-serif;
    }

    .stHeader {
        color: #1F77B4;
        font-weight: bold;
        margin-bottom: 30px;
    }

    .stText {
        color: #333;
    }
    
    /* Collapsible Source Documents styling */
    .collapsible {
        background-color: #f7f7f7;
        color: #333;
        cursor: pointer;
        padding: 10px;
        width: 100%;
        border: none;
        text-align: left;
        outline: none;
        font-size: 18px;
    }

    .active, .collapsible:hover {
        background-color: #555;
        color: white;
    }

    .content {
        padding: 0 18px;
        display: none;
        overflow: hidden;
        background-color: #f9f9f9;
        border-left: 4px solid #1F77B4;
        padding: 15px;
        border-radius: 8px;
    }

</style>
"""

bot_template = '''
<div class="chat-container">
    <div class="avatar">
        <img src="https://i.imgur.com/XivzK1Z.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="bot-message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-container">
    <div class="avatar">
        <img src="https://i.imgur.com/czqG8U1.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>    
    <div class="user-message">{{MSG}}</div>
</div>
'''

