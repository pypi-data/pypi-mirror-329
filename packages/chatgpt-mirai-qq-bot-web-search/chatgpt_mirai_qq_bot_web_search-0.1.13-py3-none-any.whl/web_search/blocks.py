from typing import Any, Dict, List, Optional
import asyncio
from framework.workflow.core.block import Block
from framework.workflow.core.block.input_output import Input, Output
from .web_searcher import WebSearcher
from .config import WebSearchConfig
from framework.llm.format.message import LLMChatMessage
from framework.llm.format.response import LLMChatResponse

class WebSearchBlock(Block):
    """Web搜索Block"""
    name = "web_search"

    inputs = {
        "llm_resp": Input(name="llm_resp",label="LLM 响应", data_type=LLMChatResponse, description="搜索关键词")
    }

    outputs = {
        "results": Output(name="results",label="搜索结果",data_type= str, description="搜索结果")
    }

    def __init__(self, name: str = None, max_results: Optional[int] = None, timeout: Optional[int] = None, fetch_content: Optional[bool] = None):
        super().__init__(name)
        self.searcher = None
        self.config = WebSearchConfig()
        self.max_results = max_results
        self.timeout = timeout
        self.fetch_content = fetch_content

    def _ensure_searcher(self):
        """同步方式初始化searcher"""
        if not self.searcher:
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                # 如果在新线程中没有事件循环，则创建一个新的
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            self.searcher = loop.run_until_complete(WebSearcher.create())

    def execute(self, **kwargs) -> Dict[str, Any]:
        llmResponse = kwargs["llm_resp"]

        query = llmResponse.choices[0].message.content if llmResponse.choices else ""
        if query == "" or query.startswith("无"):
            return {"results": ""}
        max_results = self.max_results
        timeout = self.timeout
        fetch_content = self.fetch_content
        self._ensure_searcher()

        try:
            # 在新线程中创建事件循环
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            results = loop.run_until_complete(
                self.searcher.search(
                    query=query,
                    max_results=max_results,
                    timeout=timeout,
                    fetch_content=fetch_content
                )
            )
            return {"results": "\n以下是联网搜索的结果:\n-- 搜索结果开始 --"+results+"\n-- 搜索结果结束 --"}
        except Exception as e:
            return {"results": f"搜索失败: {str(e)}"}

class AppendSystemPromptBlock(Block):
    """将搜索结果附加到系统提示的Block"""
    name = "append_system_prompt"

    inputs = {
        "results": Input(name="results",label="工具结果", data_type=str, description ="搜索结果"),
        "messages": Input(name="messages",label="LLM 响应", data_type=List[LLMChatMessage],description = "消息列表")
    }

    outputs = {
        "messages": Output(name="messages", label="拼装后的 llm 响应",data_type=List[LLMChatMessage], description = "更新后的消息列表")
    }

    def execute(self, **kwargs) -> Dict[str, Any]:
        results = kwargs["results"]
        messages: List[LLMChatMessage] = kwargs["messages"]

        if messages and len(messages) > 0:
            # 在第一条消息内容后面附加搜索结果
            messages[0].content = messages[0].content + f"{results}"

        return {"messages": messages}

