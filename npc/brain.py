from pydantic_ai import Agent, ModelSettings
from pydantic_ai.models.openai import OpenAIModel
from config import settings
from npc.models import ConversationInput, ConversationOutput

class SarahBrain:
    def __init__(self, memory_repo):
        self.memory_repo = memory_repo
        # Using OpenAIModel because Ollama is OpenAI-compatible
        self.model = OpenAIModel(
            model_name=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_URL,
        )
        self.agent = Agent(
            self.model,
            result_type=ConversationOutput,
            system_prompt=(
                "You are Sarah, a character in a text adventure game. "
                "Your personality: A grumpy morning person who softens after coffee. "
                "You are currently in the {npc_room}. The player is in the {player_room}. "
                "The current game time is {current_time}. "
                "You can see the following past memories: {recent_memories}. "
                "Respond to the player's message. If you want to update your mood, "
                "use the mood_delta field. If there is something important to remember, "
                "provide a brief summary in new_memory_summary."
            ),
        )

    async def converse(self, input_data: ConversationInput) -> ConversationOutput:
        # Prepare context for the prompt
        recent_memories_str = "\n".join(input_data.recent_memories)
        
        # We use a dynamic system prompt by injecting context into the agent call
        # In PydanticAI, we can use agent.run with a prompt that includes context
        # or use context variables. For simplicity in this prototype, we'll 
        # construct the prompt manually or use the agent's system prompt capability.
        
        prompt = (
            f"Player message: {input_data.player_message}\n"
            f"Context: Player is in {input_data.player_room}, you are in {input_data.npc_room}. "
            f"Time: {input_data.current_time}. "
            f"Memories: {recent_memories_str}"
        )

        result = await self.agent.run(prompt)
        return result.data
