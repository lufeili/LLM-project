import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface import HuggingFaceLLM

st.set_page_config(page_title="书生带你看奥运", page_icon="🦜🔗")
st.title("书生带你看奥运")

def side_bar():
    st.sidebar.title("设置")
    state = st.session_state
    # Set a form of the settings
    with st.sidebar.form(key="settings"):
        # Set the max token length for the chatbot
        max_tokens = st.number_input("最大token长度", min_value=0, max_value=2048, value=100, step=1)
        # Set the temperature for the chatbot
        temperature = st.number_input("Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
        # Set the api key for the OpenAI API
        api_key = st.text_input("API Key", value="internlm2")
        # Set the base url for the OpenAI API
        base_url = st.text_input("Base URL",value="http://0.0.0.0:23333/v1")
        # Set the system prompt for the chatbot
        system_prompt = st.text_area("系统提示", value="")
        # Add a submit button to the form
        submit = st.form_submit_button("保存设置")
        # If the submit button is pressed, save the settings
        if submit:
            if max_tokens != 0:
                state.max_tokens = max_tokens
            state.temperature = temperature
            state.api_key = api_key
            state.base_url = base_url
            state.message_history = []
            if system_prompt != "":
                state.system_prompt = system_prompt
                state.message_history.append({"role": "system", "content": system_prompt})
            state.client = OpenAI(api_key=state.api_key, base_url=state.base_url)
            pass
    if st.sidebar.button("开启新对话"):
        if not os.path.exists("chat_history"):
            os.mkdir("chat_history")
            pass
        with open(f"chat_history/{time.time()}.json", "w") as f:
            json.dump(state.message_history, f, ensure_ascii=False)
            pass
        state.message_history = []
        st.rerun()

    pass

side_bar()

# 初始化模型
@st.cache_resource
def init_models():
    embed_model = HuggingFaceEmbedding(
        model_name="/root/model/sentence-transformer"
    )
    Settings.embed_model = embed_model

    llm = HuggingFaceLLM(
        model_name="/root/model/internlm2-chat-1_8b",
        tokenizer_name="/root/model/internlm2-chat-1_8b",
        model_kwargs={"trust_remote_code": True},
        tokenizer_kwargs={"trust_remote_code": True}
    )
    Settings.llm = llm

    documents = SimpleDirectoryReader("/root/project1634/sportsdata").load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

    return query_engine

# 检查是否需要初始化模型
if 'query_engine' not in st.session_state:
    st.session_state['query_engine'] = init_models()

def greet2(question):
    response = st.session_state['query_engine'].query(question)
    return response

      
# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "你好，我是书生AI向导，带你了解2024巴黎奥运。有什么我可以帮助你的吗？"}]    

    # Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "你好，我是书生AI向导，带你了解2024巴黎奥运。有什么我可以帮助你的吗？"}]

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response
def generate_llama_index_response(prompt_input):
    return greet2(prompt_input)

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Gegenerate_llama_index_response last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama_index_response(prompt)
            placeholder = st.empty()
            placeholder.markdown(response)
    response_list=str(response).split('\n')

    message = {"role": "assistant", "content": response_list[0]}
    st.session_state.messages.append(message)
    #st.session_state.messages.append(type(response))