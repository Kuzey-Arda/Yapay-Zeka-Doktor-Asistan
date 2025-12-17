import gradio as gr
import google.generativeai as genai
from PIL import Image

# API yapılandırması
model = genai.GenerativeModel("gemini-2.5-flash")

instruction = "Sen bir Doktor Asistanısın. Senin adın Mehmet. 30 yaşındasın. Sen bir insansın. Sorulan sorulara tıbbi açıdan teknik olarak bir doktora açıklayacak şekilde açıkla. "
history = ""
hisn = 0
GEMINI_API_KEY = ""

def analyze_image(image, soru, api_key):
    global history
    global hisn
    global GEMINI_API_KEY
    if GEMINI_API_KEY != api_key:
        GEMINI_API_KEY = api_key
        genai.configure(api_key=GEMINI_API_KEY)
    if hisn > 3:
        history = model.generate_content("Yazacağım metni özetle, kısalt ve sadece gereken önemli yerleri al ve metin formatını değiştirme. Metin şu: " + history).text
    history += ("user: " + soru + " ").replace("\n", "") + "\n"
    if image is None:
        response = model.generate_content(instruction + history)
        history += "AI: " + (response.text + " ").replace("\n", "") + "\n"
        hisn += 1
        print(history)
        print(str(hisn)+":")
        return response.text
    else:
        pil_image = Image.fromarray(image)
        response = model.generate_content([instruction + history, pil_image])
        history += "AI: " + (response.text + " ").replace("\n", "") + "\n"
        hisn += 1
        print(history)
        print(str(hisn)+":")
        return response.text.replace("*", "")

# Özel CSS stilleri
theme_css = """
    .gradio-container {
        padding: 30px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.2);
    }
    .gr-button {
        background: #ff9800;
        color: white;
        border-radius: 10px;
        padding: 12px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .gr-button:hover {
        background: #e68900;
        transform: scale(1.05);
    }
    .gr-title {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 15px;
    }
"""

# Gradio Arayüzü
with gr.Blocks(css=theme_css, theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
        <h1 class='gr-title'>🏥 Akıllı Medikal Analiz</h1>
        <hr>
    """, elem_id='header')
    
    with gr.Row():
        api_key = gr.Textbox(label="Gemini API'nizi Giriniz", placeholder="Gemini API'nizi Giriniz", elem_classes="gr-input")
    
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="numpy", label="📸 Tıbbi Görüntüyü Yükleyin", elem_classes="gr-input")
        with gr.Column():
            result_output = gr.Textbox(label="📋 Analiz Sonucu", lines=10, interactive=False, elem_classes="gr-input")
        
    with gr.Row():
        soru_input = gr.Textbox(label="💬 Semptomlarınızı Yazın", placeholder="Örnek: Bu görüntüde hastalık belirtisi var mı?", elem_classes="gr-input")
        
    with gr.Row():
        analyze_btn = gr.Button("🔍 Analiz Et", elem_classes="gr-button")
        
    analyze_btn.click(fn=analyze_image, inputs=[image_input, soru_input, api_key], outputs=result_output)

if __name__ == "__main__":
    demo.launch()

