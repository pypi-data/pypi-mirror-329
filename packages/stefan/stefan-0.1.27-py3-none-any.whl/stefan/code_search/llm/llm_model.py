from enum import Enum

class LLM_MODEL(Enum):
    OPEN_AI_GPT_4o = "OPEN_AI_GPT_4o"
    OPEN_AI_4o_MINI = "OPEN_AI_4o_MINI"
    OPEN_AI_o3_MINI = "OPEN_AI_o3_MINI"
    CLAUDE_SONNET_3_5 = "CLAUDE_SONNET_3_5"
    CLAUDE_SONNET_3_5_NEW = "CLAUDE_SONNET_3_5_NEW"
    CLAUDE_HAIKU_3_5 = "CLAUDE_HAIKU_3_5"
    CLAUDE_HAIKU = "CLAUDE_HAIKU"
    DEEPSEEK_V3 = "DEEPSEEK_V3"
    DEEPSEEK_R1 = "DEEPSEEK_R1"

    def get_model_name(self) -> str:
        if self == LLM_MODEL.OPEN_AI_GPT_4o:
            return "gpt-4o"
        elif self == LLM_MODEL.OPEN_AI_4o_MINI:
            return "gpt-4o-mini-2024-07-18"
        elif self == LLM_MODEL.OPEN_AI_o3_MINI:
            return "o3-mini-2025-01-31"
        elif self == LLM_MODEL.CLAUDE_SONNET_3_5:
            return "claude-3-5-sonnet-20240620"
        elif self == LLM_MODEL.CLAUDE_SONNET_3_5_NEW:
            return "claude-3-5-sonnet-20241022"
        elif self == LLM_MODEL.CLAUDE_HAIKU_3_5:
            return "claude-3-5-haiku-20241022"
        elif self == LLM_MODEL.CLAUDE_HAIKU:
            return "claude-3-haiku-20240307"
        elif self == LLM_MODEL.DEEPSEEK_V3:
            return "deepseek/deepseek-chat"
        elif self == LLM_MODEL.DEEPSEEK_R1:
            return "deepseek/deepseek-reasoner"
        else:
            raise ValueError(f"Unsupported model: {self}")
        
    def is_openai_model(self) -> bool:
        return self in [LLM_MODEL.OPEN_AI_GPT_4o, LLM_MODEL.OPEN_AI_4o_MINI, LLM_MODEL.OPEN_AI_o3_MINI]
    
    def is_anthropic_model(self) -> bool:
        return self in [LLM_MODEL.CLAUDE_SONNET_3_5, LLM_MODEL.CLAUDE_HAIKU_3_5, LLM_MODEL.CLAUDE_SONNET_3_5_NEW, LLM_MODEL.CLAUDE_HAIKU, LLM_MODEL.CLAUDE_HAIKU_3_5]
    
    def is_deepseek_model(self) -> bool:
        return self in [LLM_MODEL.DEEPSEEK_V3, LLM_MODEL.DEEPSEEK_R1]
    