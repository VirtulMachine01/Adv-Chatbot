css = '''
<style>
.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    width: 100%;
}
.chat-message.user {
    background-color: #2b313e;
    flex-direction: row-reverse;
}
.chat-message.bot {
    background-color: #475063;
    flex-direction: row;
}
.chat-message .avatar {
    width: 20%;
}
.chat-message .avatar img {
    max-width: 78px;
    max-height: 78px;
    border-radius: 50%;
    object-fit: cover;
}
.chat-message .message {
    width: 100%;
    padding: 0 1.5rem;
    color: #fff;
    overflow-wrap: break-word; /* Break long words */
    word-wrap: break-word; /* For older browsers */
    white-space: pre-wrap; /* Preserve whitespace and wrap lines */
    # max-height: 150px; /* Optional: limit height */
    overflow-y: auto; /* Enable vertical scroll for overflow */
}
'''

def get_bot_template(MSG):
    with open("icons/txt/image2.txt", "r") as f:
        image_base64 = f.read()
    bot_template = f'''
    <div class="chat-message bot">
        <div class="avatar">
        <img src="{image_base64}" width="350" alt="Grab Vector Graphic"></img>
        </div>
        <div class="message">{MSG}</div>
    </div>
    '''
    return bot_template

def get_user_template(MSG):
    with open("icons/txt/image1.txt", "r") as f:
        image_base64 = f.read()
    user_template = f'''
    <div class="chat-message user">
        <div class="avatar">
        <img src="{image_base64}" width="350" alt="Grab Vector Graphic"></img>
        </div>
        <div class="message">{MSG}</div>
    </div>
    '''
    return user_template