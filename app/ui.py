from tkinter.ttk import Style
import gradio as gr
import requests
def welcome(text):
    response = requests.request("POST", "http://localhost:8000/translate/?source=kinyarwanda&target=english&text="+text)
    # print("s: "+source)
    # print(text_options.value)
    # print(text_option.value)
    # print("t: "+target)
    return response.text


with gr.Blocks(server_port=5005) as demo:
    css="footer {visibility: hidden}"
    gr.Markdown(
  "<h1 ><center>Digital Umuganda Machine Translation</center><style>footer {visibility: hidden} h1{margin: 1.6875rem}</style></h1>")
    with gr.Row():
        text_options = gr.Dropdown(['kinyarwanda', 'lingara', 'english','swahili', 'luganda', 'french'], label="Source language")
    # with gr.Column(scale=2, min_width=600):
        t="kinyarwanda"
        s="english"
        text_option = gr.Dropdown(['kinyarwanda', 'lingara', 'english','swahili', 'luganda', 'french'], label="Target language")
        # text_option.change(print("helloo"), text_options.value,text_option.value)
    with gr.Row(equal_height=True,css="footer {visibility: hidden}"):
        inp = gr.Textbox(lines=10,placeholder="type your text here")
        out = gr.Textbox(lines=10,placeholder="outpu........")
        # inp.change(print(text_options.value), inp,out)
        inp.change(welcome, inp,out)
    # text_options.change(drops,[text_options.value,text_option.value],text_option.value)
    
    # print(text_options.value)
    # print(text_option)
demo.launch()