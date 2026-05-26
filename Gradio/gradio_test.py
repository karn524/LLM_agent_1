import gradio as gr

#１入力１出力のUI
def text2text(text):
    text = "<<" + text + ">>"
    return text

input_text = gr.Textbox(label="入力") #Textコンポーネントを作成
output_text = gr.Textbox(label="出力") #Textコンポーネントを作成

demo = gr.Interface(inputs=input_text, outputs=output_text, fn=text2text)
demo.launch(debug=True)


# with句の利用
def text2text_rich(text):
    top = "^" * len(text)
    bottom = "v" * len(text)
    text = f" {top}\n<{text}>\n {bottom}"
    return text

with gr.Blocks() as demo:
    