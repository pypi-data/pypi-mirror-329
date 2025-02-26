# 🚀 Huggingface-TogetherAI LangChain Wrapper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)

A **LangChain** integration for **DeepSeek-R1** and **Meta Llama-3.3-70B-Instruct-Turbo** models via **Hugging Face's Inference API**, enabling seamless interaction with state-of-the-art language models.

## ✨ Features

- 🚀 **Custom LangChain Chat Model** – Optimized for Hugging Face + Together AI.
- ⚡ **Sync & Async Support** – Run queries in synchronous or asynchronous mode.
- 🌊 **Streaming Capabilities** – Supports token streaming for real-time responses.
- 🛠️ **Tool Calling & Structured Output** – Enables function calling and JSON outputs.
- 🔧 **Configurable Model Parameters** – Fine-tune temperature, max tokens, etc.

## 📦 Installation

```bash
pip install huggingface-togetherai 
```

## 🚀 Quick Start

```python
from huggingface_togetherai import ChatHuggingFaceTogetherAI

hf_token = "your_huggingface_token"
hf_llm = ChatHuggingFaceTogetherAI(
    model="deepseek-ai/DeepSeek-R1",
    hf_token=hf_token
)

response = hf_llm.invoke("Hi!")
print(response)
```

## 🤔 Why Use Huggingface-TogetherAI?

In **LangChain**, the `HuggingFaceEndpoint` class is typically used for Hugging Face models:

```python
from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface.chat_models import ChatHuggingFace

hf_endpoint = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1",
    task="text-generation",
    huggingfacehub_api_token=hf_token
)

langchain_llm = ChatHuggingFace(llm=hf_endpoint)
langchain_llm.invoke("Hello")
```

However, this results in an error:

```
The model deepseek-ai/DeepSeek-R1 is too large to be loaded automatically (688GB > 10GB).
```

### ✅ The Better Alternative: Huggingface-TogetherAI

With **Huggingface-TogetherAI**, you can seamlessly use large models without running into memory issues:

```python
from huggingface_togetherai import ChatHuggingFaceTogetherAI

hf_llm = ChatHuggingFaceTogetherAI(
    model="deepseek-ai/DeepSeek-R1",
    hf_token=hf_token,
    other_params...
)

response = hf_llm.invoke("Hello")
print(response)  # Output: '<think>\n\n</think>\n\nHello! How can I assist you today? 😊'
```

### 🎉 Good News!

✅ You can leverage **all [Langchain](https://www.langchain.com/) functionalities** for standard LLMs with this package.

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

