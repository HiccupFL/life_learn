import itchat
from itchat.content import *
import time

def login_with_retry():
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Save QR code as an image file and use it for login
            itchat.auto_login(hotReload=True, enableCmdQR=-1)
            print("Successfully logged in!")
            print("QR code has been saved as 'QR.png' in your current directory")
            return True
        except Exception as e:
            retry_count += 1
            print(f"Login attempt {retry_count} failed: {str(e)}")
            if retry_count < max_retries:
                print(f"Retrying in 5 seconds...")
                time.sleep(5)
    
    print("Failed to login after maximum retries")
    return False

# Text message handler
@itchat.msg_register(TEXT)
def text_reply(msg):
    # Get the text content
    text = msg['Text']
    
    # Simple response logic
    if 'hello' in text.lower():
        return 'Hello! I am a bot. Nice to meet you!'
    elif 'how are you' in text.lower():
        return "I'm doing great, thank you for asking!"
    elif 'bye' in text.lower():
        return 'Goodbye! Have a nice day!'
    else:
        return f"I received your message: {text}"

# Friend request handler
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

# Run the bot
if __name__ == '__main__':
    print('WeChat bot is starting...')
    if login_with_retry():
        itchat.run()
    else:
        print("Bot startup failed")