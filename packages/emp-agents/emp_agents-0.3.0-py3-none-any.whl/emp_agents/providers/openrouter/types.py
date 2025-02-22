from enum import StrEnum


class OpenRouterModelType(StrEnum):
    gpt3_5_turbo = "openai/gpt-3.5-turbo"
    liquid_lfm_7b = "liquid/lfm-7b"
    deepseek_r1_distill_llama_70b = "deepseek/deepseek-r1-distill-llama-70b"
    deepseek_r1_free = "deepseek/deepseek-r1:free"
    openai_chatgpt_4o_latest = "openai/chatgpt-4o-latest"
    openai_o1 = "openai/o1"
