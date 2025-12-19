import gradio as gr
import redis
import os

# 从环境变量获取 Redis 配置
REDIS_HOST = os.getenv("REDIS_HOST", "localhost") #从系统环境变量中读取 REDIS_HOST 如果没设置环境变量，就用 "localhost"
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

def get_redis_client():
    try:
        return redis.Redis(host = REDIS_HOST, port = REDIS_PORT, decode_responses=True)# 创建 Redis 连接客户端
    #decode_responses=True: 自动将 Redis 返回的字节串解码为字符串
    except:
        return None

def chat(message, history):
    r = get_redis_client()

    # 记录消息次数
    if r:
        count = r.incr('count') # 对键 message_count 的值加 1，如果键不存在：自动创建并初始化为 0，然后加 1，只要 Redis 数据卷存在，重启后计数继续
        response = f"Echo：{message}(消息 #{count})"
    else:
        response = f"Echo:{message}(redis未连接)"
    # 构造新历史
    new_history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": response}
    ]
    return new_history

# 自定义 CSS：控制聊天气泡、高度、输入框等
custom_css = """
/* 聊天区域高度 */
.gradio-chatbot {
    height: 600px !important;
}

/* 用户消息气泡（右侧） */
.message.user-message {
    background-color: #4299e1 !important;  /* 蓝色 */
    color: white !important;
    border-radius: 12px !important;
}

/* AI 消息气泡（左侧） */
.message.bot-message {
    background-color: #f0f0f0 !important;  /* 浅灰 */
    color: #333 !important;
    border-radius: 12px !important;
}

/* 输入框样式 */
.input-container textarea {
    border: 2px solid #4299e1;
    border-radius: 16px;
    padding: 12px;
    font-size: 16px;
}
"""


def create_chat_interface():
    with gr.Blocks(title="简单聊天机器人", css=custom_css) as demo:
        gr.Markdown("# 🤖 简单聊天机器人")
        chatbot = gr.Chatbot(height=500)
        msg = gr.Textbox(label="输入消息", placeholder="请输入...")
        btn = gr.Button("发送")

        btn.click(
            fn=chat,
            inputs=[msg, chatbot],
            outputs=chatbot
        ).then(
            fn=lambda: "",
            inputs=None,
            outputs=msg
        )

        msg.submit(
            fn=chat,
            inputs=[msg, chatbot],
            outputs=chatbot
        ).then(
            fn=lambda: "",
            inputs=None,
            outputs=msg
        )

    return demo