import os
import gradio as gr
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from agent import BankingAgent

# Initialize Agent
agent = BankingAgent()

def chat(message, history):
    """
    Gradio chat interface function.
    history is a list of [user_message, bot_message]
    """
    result = agent.process_query(message)
    
    # Format the sources
    sources_text = ""
    if result["sources"]:
        sources_text = "\n\n**Sources:**\n"
        for s in result["sources"]:
            sources_text += f"- [{s['title']}]({s['url']})\n"
    elif result["search_required"]:
        sources_text = "\n\n**Sources:**\nSearch required, but no reliable sources found or search failed."
    else:
        sources_text = "\n\n**Sources:**\nNo web search required."
        
    # Format the activity log
    activity_text = "\n".join(result["activity_log"])
    
    final_bot_message = result["response"] + sources_text
    
    return final_bot_message, activity_text

with gr.Blocks(title="Banking AI Agent") as demo:
    gr.Markdown(
        """
        # 🏦 Banking AI Agent
        ### AI-Powered Customer Support
        
        *Disclaimer: This is a demonstration AI agent. It does not connect to real banking systems and uses mock data for accounts. Please do not share any real personal or banking information.*
        """
    )
    
    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(height=500, label="Customer Support Chat")
            msg = gr.Textbox(label="Your Question", placeholder="Type your banking query here...", lines=2)
            with gr.Row():
                send_btn = gr.Button("Send", variant="primary")
                clear_btn = gr.ClearButton([msg, chatbot])
                
        with gr.Column(scale=1):
            activity_panel = gr.Textbox(
                label="Agent Activity",
                lines=10,
                interactive=False,
                value="Waiting for query..."
            )
            
    def respond(message, chat_history):
        bot_message, activity = chat(message, chat_history)
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": bot_message})
        return "", chat_history, activity

    msg.submit(respond, [msg, chatbot], [msg, chatbot, activity_panel])
    send_btn.click(respond, [msg, chatbot], [msg, chatbot, activity_panel])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(theme=gr.themes.Soft(), server_name="0.0.0.0", server_port=port)
