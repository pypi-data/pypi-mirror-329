from asyncio import Queue
from langchain_core.agents import AgentFinish
from langchain_core.outputs import ChatGenerationChunk, GenerationChunk
from langchain.callbacks.base import AsyncCallbackHandler
from ws_bom_robot_app.llm.utils.print import printJson, printString
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
import ws_bom_robot_app.llm.settings as settings
from langchain_core.callbacks.base import AsyncCallbackHandler
from langchain_core.outputs import ChatGenerationChunk, GenerationChunk
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import json

# Here is a custom handler that will print the tokens to stdout.
# Instead of printing to stdout you can send the data elsewhere; e.g., to a streaming API response


def _parse_token(llm:str,token: str) -> str:
    """Parses the token based on the LLM provider."""
    if llm == "anthropic" and isinstance(token, list):
      first = token[0]
      if 'text' in first:
        token = first['text']
      else:
        #[{'id': 'toolu_01GGLwJcrQ8PvFMUkQPGu8n7', 'input': {}, 'name': 'document_retriever_xxx', 'type': 'tool_use', 'index': 1}]
        token = ""
    return token

class AgentHandler(AsyncCallbackHandler):

    def __init__(self, queue: Queue, llm:str, threadId: str = None) -> None:
        super().__init__()
        self._threadId = threadId
        self.json_block = ""
        self.is_json_block = False
        self.backtick_count = 0  # Conteggio dei backticks per il controllo accurato
        self.queue = queue
        self.llm = llm

    async def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: UUID = None,
        tags: List[str] = None,
        metadata: Dict[str, Any] = None,
        **kwargs: Any,
    ) -> None:
        firstChunk = {
            "type": "info",
            "threadId": self._threadId,
        }
        await self.queue.put(printString(firstChunk))

    """async def on_chat_model_start(self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], *, run_id: UUID = None, parent_run_id = None, tags = None, metadata = None, **kwargs: Any) -> Any:
        pass"""

    async def on_tool_end(self, output: Any, *, run_id: UUID, parent_run_id: UUID = None, tags: List[str] = None, **kwargs: Any) -> None:
      pass

    async def on_llm_new_token(
        self,
        token: str,
        *,
        chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Gestisce i nuovi token durante lo streaming."""

        if token:
            token = _parse_token(self.llm,token)
            if token:
              self.backtick_count += token.count("`")

              if self.backtick_count >= 3:
                  if not self.is_json_block:
                      self.is_json_block = True
                      self.json_block = ""
                  else:
                      self.is_json_block = False
                      self.json_block += token.replace("```json", '')
                      await self.process_json_block(self.json_block)
                      self.json_block = ""
                  self.backtick_count = 0
              elif self.is_json_block:
                  self.json_block += token
              else:
                  await self.queue.put(printString(token))

    async def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: UUID = None,
        tags: List[str] = None,
        **kwargs: Any,
    ) -> None:
        settings.chat_history.extend(
            [
                AIMessage(content=_parse_token(self.llm,finish.return_values["output"])),
            ]
        )
        finalChunk = {"type": "end"}
        await self.queue.put(printJson(finalChunk))
        await self.queue.put(None)

    async def process_json_block(self, json_block: str):
      """Processa il blocco JSON completo."""
      # Rimuove il delimitatore iniziale '```json' se presente, e spazi vuoti
      json_block_clean = json_block.replace('```', '').replace('json', '').strip()
      # Verifica che il blocco non sia vuoto prima di tentare il parsing
      if json_block_clean:
          try:
              # Prova a fare il parsing del JSON
              parsed_json = json.loads(json_block_clean)
              await self.queue.put(printJson(parsed_json))
          except json.JSONDecodeError as e:
              # Se il JSON è malformato, logga l'errore
              raise e

class RawAgentHandler(AsyncCallbackHandler):

    def __init__(self,queue: Queue, llm: str) -> None:
        super().__init__()
        self.queue = queue
        self.llm = llm
    async def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: UUID = None,
        tags: List[str] = None,
        metadata: Dict[str, Any] = None,
        **kwargs: Any,
    ) -> None:
        pass

    """async def on_chat_model_start(self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], *, run_id: UUID = None, parent_run_id = None, tags = None, metadata = None, **kwargs: Any) -> Any:
        pass"""

    async def on_tool_end(self, output: Any, *, run_id: UUID, parent_run_id: UUID = None, tags: List[str] = None, **kwargs: Any) -> None:
      pass

    async def on_llm_new_token(
        self,
        token: str,
        *,
        chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Handles new tokens during streaming."""
        if token:  # Only process non-empty tokens
            await self.queue.put(_parse_token(self.llm,token))

    async def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: UUID = None,
        tags: List[str] = None,
        **kwargs: Any,
    ) -> None:
        settings.chat_history.extend(
            [
                AIMessage(content=_parse_token(self.llm,finish.return_values["output"]))
            ]
        )
        await self.queue.put(None)
