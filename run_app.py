import gradio as gr
from app.gradio_text import create_chat_interface

if __name__ == '__main__':
    demo = create_chat_interface()
    demo.launch(server_name = "0.0.0.0", server_port = 7860) #server_name="0.0.0.0"允许从外部(浏览器)访问