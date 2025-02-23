from autogen_ext.models.openai import OpenAIChatCompletionClient

# model_client = OpenAIChatCompletionClient(model="gpt-4o", api_key="sk-xxx")

# ollama local deployment
def get_model_client_ollama() -> OpenAIChatCompletionClient:  # type: ignore
    return OpenAIChatCompletionClient(
        model="llama3.2:latest",
        api_key="ollama",
        base_url="http://localhost:11434/v1",
        model_capabilities={
            "json_output": True,
            "vision": False,
            "function_calling": True,
        },
    )


def custom_model_client() -> OpenAIChatCompletionClient:
    return OpenAIChatCompletionClient(
        model="custom-model-name",
        base_url="https://custom-model.com/reset/of/the/path",
        api_key="placeholder",
        model_info={
            "vision": True,
            "function_calling": True,
            "json_output": True,
            "family": "unknown",
        },
    )

def get_model_client_siliconflow() -> OpenAIChatCompletionClient:  # type: ignore
    return OpenAIChatCompletionClient(
        model="deepseek-ai/DeepSeek-V3",
        #model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
        api_key="sk-uefrbugirppbfzegplcdszjgrfimuifcglivcqhuzzilokkv", #germany
        base_url="https://api.siliconflow.cn/v1",
        model_capabilities={
            "json_output": False,
            "vision": False,
            "function_calling": True,
        },
    )



# model_client = get_model_client_ollama()

model_client = get_model_client_siliconflow()
