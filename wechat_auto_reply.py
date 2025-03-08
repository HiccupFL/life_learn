import os
import time
import json
import itchat
from itchat.content import TEXT, FRIENDS

def login_with_qr():
    """使用二维码登录微信"""
    # 设置二维码路径
    qr_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wechat_qr.png')
    
    try:
        # 使用二维码图片文件登录，增加更多参数以提高成功率
        itchat.auto_login(hotReload=True, 
                          statusStorageDir='wechat_login.pkl',
                          picDir=qr_path, 
                          enableCmdQR=2,
                          loginCallback=lambda: print("扫码成功！正在登录..."),
                          exitCallback=lambda: print("登录超时或失败，请重试"))
        print(f"登录成功！二维码已保存到 {qr_path}")
        return True
    except Exception as e:
        print(f"登录失败: {e}")
        print("可能的原因：")
        print("1. 微信网页版可能限制了你的账号登录")
        print("2. 网络连接问题")
        print("3. 二维码扫描超时")
        print("建议：尝试删除 wechat_login.pkl 文件后重试")
        return False

def load_responses():
    """从JSON文件加载回复内容"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wechat_responses.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # 默认回复内容
        default_responses = {
            "你好": "你好！我是自动回复机器人。",
            "在吗": "我在的，有什么可以帮到你？",
            "你是谁": "我是一个自动回复机器人，可以帮助回答一些简单问题。",
            "再见": "再见！祝你有愉快的一天！",
            "帮助": "我可以回答一些基本问题，试着和我打个招呼吧！",
        }
        # 保存默认回复到文件
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_responses, f, ensure_ascii=False, indent=4)
        print(f"已创建默认回复配置文件: {config_path}")
        return default_responses

# 加载回复内容
responses = load_responses()

# 文本消息处理器
@itchat.msg_register(TEXT)
def text_reply(msg):
    # 获取文本内容
    text = msg['Text']
    print(f"收到消息: {text}")
    
    # 检查是否匹配我们的回复字典
    for keyword, response in responses.items():
        if keyword in text:
            print(f"发送回复: {response}")
            return response
    
    # 如果没有匹配的关键词，使用默认回复
    default_reply = f"谢谢你的消息: '{text}'。我稍后会回复你。"
    print(f"发送默认回复")
    return default_reply

# 好友请求处理器
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    itchat.send_msg('很高兴认识你！', msg['RecommendInfo']['UserName'])

def main():
    print("启动微信自动回复机器人...")
    if login_with_qr():
        print("机器人正在运行。按Ctrl+C退出。")
        print(f"你可以编辑 {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wechat_responses.json')} 文件来自定义回复内容。")
        itchat.run()
    else:
        print("机器人启动失败。")

if __name__ == "__main__":
    main()