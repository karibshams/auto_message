#!/usr/bin/env python3
"""
Streamlit-based ChatGPT-like interface for testing AI comment reply system.
Run with: streamlit run test.py
"""

import streamlit as st
import os
import sys
from datetime import datetime
from typing import Dict, Any, List
import time

# Import our AI system
try:
    from app import CommentReplyAI
    from prompt import PromptGenerator
except ImportError as e:
    st.error(f"❌ Import Error: {e}")
    st.error("Make sure app.py and prompt.py are in the same directory as test.py")
    st.stop()

# Configure Streamlit page
st.set_page_config(
    page_title="AI Comment Reply Tester",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for ChatGPT-like appearance
st.markdown("""
<style>
    /* Main chat container */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* User message styling */
    .user-message {
        background-color: #f0f0f0;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        margin-left: 50px;
        position: relative;
    }
    
    /* AI message styling */
    .ai-message {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        margin-right: 50px;
        position: relative;
    }
    
    /* Message metadata */
    .message-meta {
        font-size: 12px;
        color: #666;
        margin-top: 8px;
        font-style: italic;
    }
    
    /* Input styling */
    .stTextInput input {
        border-radius: 20px;
        border: 2px solid #e0e0e0;
        padding: 10px 15px;
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 20px;
        background-color: #10a37f;
        color: white;
        border: none;
        padding: 8px 20px;
    }
    
    /* Sidebar styling */
    .sidebar-content {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    /* Success/error indicators */
    .success-indicator {
        color: #10a37f;
        font-weight: bold;
    }
    
    .error-indicator {
        color: #ef4444;
        font-weight: bold;
    }
    
    /* Typing indicator */
    .typing-indicator {
        color: #666;
        font-style: italic;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 0.5; }
        50% { opacity: 1; }
        100% { opacity: 0.5; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'ai_system' not in st.session_state:
    st.session_state.ai_system = None
if 'stats' not in st.session_state:
    st.session_state.stats = {
        'total_messages': 0,
        'successful_replies': 0,
        'tone_usage': {},
        'sentiment_distribution': {}
    }

def initialize_ai_system():
    """Initialize the AI system with API key validation."""
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return None, "❌ OpenAI API key not found. Please set OPENAI_API_KEY in your .env file."
        
        ai_system = CommentReplyAI()
        return ai_system, "✅ AI system initialized successfully!"
    except Exception as e:
        return None, f"❌ Error initializing AI system: {str(e)}"

def update_stats(result: Dict[str, Any]):
    """Update conversation statistics."""
    st.session_state.stats['total_messages'] += 1
    
    if result.get('success'):
        st.session_state.stats['successful_replies'] += 1
        
        # Update tone usage
        tone = result.get('tone_used', 'unknown')
        st.session_state.stats['tone_usage'][tone] = st.session_state.stats['tone_usage'].get(tone, 0) + 1
        
        # Update sentiment distribution
        sentiment = result.get('sentiment_detected', 'unknown')
        st.session_state.stats['sentiment_distribution'][sentiment] = st.session_state.stats['sentiment_distribution'].get(sentiment, 0) + 1

def render_message(message: Dict[str, Any], is_user: bool = True):
    """Render a chat message with ChatGPT-like styling."""
    if is_user:
        st.markdown(f"""
        <div class="user-message">
            <strong>👤 You:</strong><br>
            {message['content']}
            <div class="message-meta">
                {message.get('timestamp', '')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        status_icon = "✅" if message.get('success', False) else "❌"
        reply_text = message.get('reply', 'Error generating reply')
        
        st.markdown(f"""
        <div class="ai-message">
            <strong>🤖 AI Assistant:</strong><br>
            {reply_text}
            <div class="message-meta">
                {status_icon} Sentiment: {message.get('sentiment', 'N/A')} | 
                Tone: {message.get('tone', 'N/A')} | 
                {message.get('timestamp', '')}
            </div>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main Streamlit application."""
    
    # Header
    st.title("🤖 AI Comment Reply Tester")
    st.markdown("**ChatGPT-like Interface for Testing Spiritual AI Responses**")
    
    # Sidebar for controls and stats
    with st.sidebar:
        st.header("🎛️ Controls")
        
        # Initialize AI system
        if st.session_state.ai_system is None:
            with st.spinner("Initializing AI system..."):
                st.session_state.ai_system, init_message = initialize_ai_system()
            
            if st.session_state.ai_system is None:
                st.error(init_message)
                st.markdown("""
                **Setup Instructions:**
                1. Create a `.env` file in your project directory
                2. Add your OpenAI API key: `OPENAI_API_KEY=sk-your-key-here`
                3. Restart the Streamlit app
                """)
                st.stop()
            else:
                st.success(init_message)
        
        # Clear conversation
        if st.button("🗑️ Clear Conversation", type="secondary"):
            st.session_state.messages = []
            st.session_state.stats = {
                'total_messages': 0,
                'successful_replies': 0,
                'tone_usage': {},
                'sentiment_distribution': {}
            }
            st.rerun()
        
        # Model settings
        st.subheader("⚙️ AI Settings")
        current_model = getattr(st.session_state.ai_system, 'model', 'gpt-4')
        st.info(f"**Model:** {current_model}")
        
        max_tokens = getattr(st.session_state.ai_system, 'max_tokens', 300)
        temperature = getattr(st.session_state.ai_system, 'temperature', 0.7)
        st.info(f"**Max Tokens:** {max_tokens}")
        st.info(f"**Temperature:** {temperature}")
        
        # Available tones
        st.subheader("🎭 Available Tones")
        prompt_gen = PromptGenerator()
        available_tones = prompt_gen.get_available_tones()
        for tone in available_tones:
            description = prompt_gen.get_tone_description(tone)
            with st.expander(f"**{tone.title()}**"):
                st.write(description)
                example = prompt_gen.get_tone_examples(tone)
                if example:
                    st.write(f"*Example: \"{example['reply']}\"*")
        
        # Statistics
        if st.session_state.stats['total_messages'] > 0:
            st.subheader("📊 Session Stats")
            stats = st.session_state.stats
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Messages", stats['total_messages'])
            with col2:
                success_rate = (stats['successful_replies'] / stats['total_messages']) * 100
                st.metric("Success Rate", f"{success_rate:.1f}%")
            
            if stats['tone_usage']:
                st.write("**Tone Usage:**")
                for tone, count in stats['tone_usage'].items():
                    st.write(f"• {tone.title()}: {count}")
            
            if stats['sentiment_distribution']:
                st.write("**Sentiment Distribution:**")
                for sentiment, count in stats['sentiment_distribution'].items():
                    st.write(f"• {sentiment.title()}: {count}")
    
    # Main chat interface
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display conversation history
    if st.session_state.messages:
        for i, message in enumerate(st.session_state.messages):
            if message['type'] == 'user':
                render_message(message, is_user=True)
            else:
                render_message(message, is_user=False)
    else:
        # Welcome message
        st.markdown("""
        <div class="ai-message">
            <strong>🤖 AI Assistant:</strong><br>
            Hello! I'm your AI comment reply assistant. I specialize in generating empathetic, 
            spiritual responses to comments. Try sending me a comment to see how I respond!
            
            <div class="message-meta">
                💡 Tip: I can detect sentiment and adjust my tone accordingly (empathetic, biblical, humble, inviting, witty)
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Input area
    st.markdown("---")
    
    # Create columns for input and controls
    col1, col2, col3 = st.columns([6, 1, 1])
    
    with col1:
        user_input = st.text_input(
            "Type your comment here...",
            placeholder="Example: I'm struggling to believe this applies to me...",
            key="user_input"
        )
    
    with col2:
        # Optional tone override
        tone_override = st.selectbox(
            "Tone",
            options=["Auto"] + [tone.title() for tone in available_tones],
            key="tone_override"
        )
    
    with col3:
        send_button = st.button("Send 📤", type="primary")
    
    # Process user input
    if send_button and user_input.strip():
        # Add user message to conversation
        user_message = {
            'type': 'user',
            'content': user_input.strip(),
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        st.session_state.messages.append(user_message)
        
        # Show typing indicator
        typing_placeholder = st.empty()
        typing_placeholder.markdown(
            '<div class="typing-indicator">🤖 AI is thinking...</div>',
            unsafe_allow_html=True
        )
        
        # Generate AI response
        try:
            custom_tone = None if tone_override == "Auto" else tone_override.lower()
            
            with st.spinner("Generating response..."):
                result = st.session_state.ai_system.generate_reply(
                    user_input.strip(),
                    custom_tone
                )
            
            # Remove typing indicator
            typing_placeholder.empty()
            
            # Add AI response to conversation
            ai_message = {
                'type': 'ai',
                'reply': result.get('reply', 'Error generating reply'),
                'sentiment': result.get('sentiment_detected', 'unknown'),
                'tone': result.get('tone_used', 'unknown'),
                'success': result.get('success', False),
                'error': result.get('error'),
                'timestamp': datetime.now().strftime("%H:%M:%S")
            }
            st.session_state.messages.append(ai_message)
            
            # Update statistics
            update_stats(result)
            
        except Exception as e:
            typing_placeholder.empty()
            st.error(f"❌ Error: {str(e)}")
            
            # Add error message to conversation
            error_message = {
                'type': 'ai',
                'reply': f"Sorry, I encountered an error: {str(e)}",
                'sentiment': 'error',
                'tone': 'error',
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().strftime("%H:%M:%S")
            }
            st.session_state.messages.append(error_message)
        
        # Clear input and rerun to show new messages
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 12px;">
        🤖 AI Comment Reply Testing System | 
        Built with Streamlit | 
        Powered by OpenAI
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()