from PIL import Image
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
apikey = st.secrets["API_KEY"]

# App UI framework
favicon = Image.open("assets/favicon.ico")
st.set_page_config(
    page_title="RuhaniyatAI",
    page_icon=favicon,
    layout="wide",
)



# Title and Subheader
# Change the title color
st.markdown("<h1 style='color: #3498db;'>RuhaniyatAI - Your Personal Spiritual Companion</h1>", unsafe_allow_html=True)

st.subheader(
    ' Welcome to RuhaniyatAI: Your Personal Spiritual Companion! \nDiscover spiritual insights and guidance tailored just for you. RuhaniyatAI is here to accompany you on your journey of self-discovery and reflection.\nShare your emotions, and let our advanced AI provide you with uplifting messages inspired by the divine wisdom of Quran and Hadith.'
)
st.markdown("<hr style='border: 2px solid #2c3e50;'>", unsafe_allow_html=True)
st.markdown("<h2>Express your emotions, and let the verses of the Quran and the wisdom of Hadith resonate with your soul. Share your thoughts below.</h2>",unsafe_allow_html=True)
# Text Input for Keywords
keywords = st.text_input("Enter Here:")
st.markdown("<hr style='border: 2px solid #2c3e50;'>", unsafe_allow_html=True)

# Prompt templates
prompt_template = f'generate a paragraph from Quran or hadith giving me an islamic reminder based on this sentence: {keywords}' if keywords else ''

title_template = PromptTemplate(
    input_variables=['keywords'],
    template=prompt_template
)

wisdom_template = PromptTemplate(
    input_variables=['keywords'],
    template='generate a paragraph from Quran or hadith giving me an islamic reminder based on this sentence: {keywords}'
)

# Memory
title_memory = ConversationBufferMemory(input_key='keywords', memory_key='chat_history')
wisdom_memory = ConversationBufferMemory(input_key='keywords', memory_key='chat_history')

# Llms
llm = OpenAI(model_name="text-davinci-003", temperature=0.9)
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
wisdom_chain = LLMChain(llm=llm, prompt=wisdom_template, verbose=True, output_key='script', memory=wisdom_memory)

# Chaining the components and displaying outputs
if keywords:
    # Generate wisdom
    with st.spinner("Generating Wisdom..."):
        wisdom = wisdom_chain.run({'keywords': keywords})

    # Display generated wisdom
    st.subheader('Extracted Quotes From Quran and Hadith:')
    st.info(wisdom)
# Add a horizontal line
st.markdown("<hr style='border: 2px solid #2c3e50;'>", unsafe_allow_html=True)
    
   
with st.expander('History'):
  history = wisdom_memory.buffer
  st.info(history)
if not history:
     st.info("No history yet.")


st.markdown("<hr style='border: 2px solid #2c3e50;'>", unsafe_allow_html=True)

# Footer
footer_html = """
    <div style="padding: 10px; background-color:#00BF00; left:0; position:static; bottom: 0; width: 100%; text-align:center; justify-content:center; margin-top:20px;">
        <p style="color: white;">Built with ❤️ by Aquib Hussain | <a href="https://twitter.com/AquibG1?t=UQlKWtQKEqYneDmph_FHcQ&s=09" style="color: white;">𝕏</a></p>
    </div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
