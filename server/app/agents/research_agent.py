from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
import time
import logging

from app.core.config import settings
from app.core.exceptions import AgentException
from app.services.web_search import web_search_service_v2
from app.services.vector_store import VectorStoreService
from app.crud.conversation import ConversationCRUD, AgentLogCRUD
from app.schemas.conversation import ConversationCreate, AgentLogCreate
from app.tools import search_web, retrieve_documents, get_source_url

logger = logging.getLogger(__name__)


class ResearchState(TypedDict):
    query: str
    user_id: str
    conversation_id: str
    search_queries: List[str]
    search_results: List[dict]
    relevant_content: str
    final_report: str
    error: str


class ResearchAgentV3:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.llm = ChatOpenAI(
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=settings.OPENROUTER_API_KEY,
            model_name="nvidia/nemotron-nano-12b-v2-vl:free",
            temperature=0.7,
        )
        self.graph = self._create_graph()

    def _create_graph(self):
        workflow = StateGraph(ResearchState)

        workflow.add_node("initialize", self.initialize)
        workflow.add_node("generate_queries", self.generate_queries)
        workflow.add_node("web_search", self.web_search)
        workflow.add_node("extract_content", self.extract_content)
        workflow.add_node("synthesize_report", self.synthesize_report)
        workflow.add_node("handle_error", self.handle_error)

        workflow.set_entry_point("initialize")
        workflow.add_edge("initialize", "generate_queries")
        workflow.add_edge("generate_queries", "web_search")
        workflow.add_edge("web_search", "extract_content")
        workflow.add_edge("extract_content", "synthesize_report")
        workflow.add_edge("synthesize_report", END)
        workflow.add_edge("handle_error", END)

        return workflow.compile()

    async def initialize(self, state: ResearchState):
        """Initialize conversation and create database entry"""
        try:
            start_time = time.time()

            # Create conversation
            conversation = await ConversationCRUD.create(
                self.db,
                ConversationCreate(
                    user_id=state["user_id"],
                    messages=[{"role": "user", "content": state["query"]}],
                    metadata={"agent_type": "research"},
                ),
            )

            # Log initialization
            await AgentLogCRUD.create(
                self.db,
                AgentLogCreate(
                    conversation_id=conversation.id,
                    agent_type="research",
                    action="initialize",
                    input_data={"query": state["query"]},
                    execution_time=int((time.time() - start_time) * 1000),
                    status="success",
                ),
            )

            return {"conversation_id": str(conversation.id)}

        except Exception as e:
            logger.error(f"Initialization error: {str(e)}")
            return {"error": f"Initialization failed: {str(e)}"}

    async def generate_queries(self, state: ResearchState):
        """Generate search queries"""
        try:
            start_time = time.time()

            prompt = f"""Given this research question: "{state["query"]}"
            
Generate 3-5 specific search queries that would help answer this question.
Return only the queries, one per line."""

            response = await self.llm.ainvoke(prompt)
            queries = [
                q.strip() for q in response.content.strip().split("\n") if q.strip()
            ][:5]

            # Log action
            await AgentLogCRUD.create(
                self.db,
                AgentLogCreate(
                    conversation_id=state["conversation_id"],
                    agent_type="research",
                    action="generate_queries",
                    input_data={"query": state["query"]},
                    output_data={"queries": queries},
                    execution_time=int((time.time() - start_time) * 1000),
                    status="success",
                ),
            )

            return {"search_queries": queries}

        except Exception as e:
            logger.error(f"Query generation error: {str(e)}")
            return {"error": f"Query generation failed: {str(e)}"}

    async def web_search(self, state: ResearchState):
        """Execute web searches"""
        try:
            start_time = time.time()
            all_results = []

            for query in state["search_queries"]:
                try:
                    results = await search_web(query, num_results=3)
                    all_results.extend(results)
                except Exception as e:
                    logger.warning(f"Search failed for query '{query}': {str(e)}")
                    continue

            if not all_results:
                raise AgentException("All search attempts failed")

            # Log action
            await AgentLogCRUD.create(
                self.db,
                AgentLogCreate(
                    conversation_id=state["conversation_id"],
                    agent_type="research",
                    action="web_search",
                    input_data={"queries": state["search_queries"]},
                    output_data={"num_results": len(all_results)},
                    execution_time=int((time.time() - start_time) * 1000),
                    status="success",
                ),
            )

            return {"search_results": all_results}

        except Exception as e:
            logger.error(f"Web search error: {str(e)}")
            return {"error": f"Web search failed: {str(e)}"}

    async def extract_content(self, state: ResearchState):
        """Extract and store content"""
        try:
            start_time = time.time()

            texts = []
            metadatas = []

            for result in state["search_results"]:
                if result.get("content"):
                    texts.append(result["content"])
                    metadatas.append(
                        {
                            "title": result["title"],
                            "url": result["url"],
                            "source": result.get("source", "web"),
                        }
                    )

            if texts:
                VectorStoreService.add_documents(texts, metadatas)

            relevant_docs = retrieve_documents(state["query"], k=10)

            # If Pinecone returns empty, use search results directly
            if not relevant_docs:
                relevant_content = "\n\n".join(
                    [
                        f"Source: {result.get('title', 'Unknown')}\n{result.get('content', result.get('snippet', ''))[:1000]}"
                        for result in state["search_results"]
                        if result.get("content") or result.get("snippet")
                    ]
                )
            else:
                relevant_content = "\n\n".join(
                    [
                        f"Source: {doc.get('title', 'Unknown')}\n{doc.get('content', '')[:1000]}"
                        for doc in relevant_docs
                    ]
                )

            await AgentLogCRUD.create(
                self.db,
                AgentLogCreate(
                    conversation_id=state["conversation_id"],
                    agent_type="research",
                    action="extract_content",
                    input_data={"num_documents": len(texts)},
                    output_data={
                        "relevant_docs": len(relevant_docs)
                        if relevant_docs
                        else len(state["search_results"])
                    },
                    execution_time=int((time.time() - start_time) * 1000),
                    status="success",
                ),
            )

            return {"relevant_content": relevant_content}

        except Exception as e:
            logger.error(f"Content extraction error: {str(e)}")
            return {"error": f"Content extraction failed: {str(e)}"}

    async def synthesize_report(self, state: ResearchState):
        """Generate final report"""
        try:
            start_time = time.time()

            prompt = f"""Create a comprehensive research report answering: {state["query"]}

Research Content:
{state["relevant_content"]}

Include:
1. Executive Summary
2. Key Findings
3. Detailed Analysis
4. Conclusions"""

            response = await self.llm.ainvoke(prompt)

            # Update conversation with final report
            await ConversationCRUD.add_message(
                self.db,
                state["conversation_id"],
                {"role": "assistant", "content": response.content},
            )

            await AgentLogCRUD.create(
                self.db,
                AgentLogCreate(
                    conversation_id=state["conversation_id"],
                    agent_type="research",
                    action="synthesize_report",
                    input_data={"query": state["query"]},
                    output_data={"report_length": len(response.content)},
                    execution_time=int((time.time() - start_time) * 1000),
                    status="success",
                ),
            )

            return {"final_report": response.content}

        except Exception as e:
            logger.error(f"Report synthesis error: {str(e)}")
            return {"error": f"Report synthesis failed: {str(e)}"}

    async def handle_error(self, state: ResearchState):
        """Handle errors gracefully"""
        error_msg = state.get("error", "Unknown error occurred")
        logger.error(f"Agent error: {error_msg}")

        try:
            await AgentLogCRUD.create(
                self.db,
                AgentLogCreate(
                    conversation_id=state.get("conversation_id", ""),
                    agent_type="research",
                    action="error_handling",
                    input_data={"error": error_msg},
                    execution_time=0,
                    status="error",
                ),
            )
        except:
            pass

        return {
            "final_report": f"I apologize, but I encountered an error: {error_msg}. Please try again."
        }

    async def run(self, query: str, user_id: str):
        """Execute research workflow"""
        initial_state = {
            "query": query,
            "user_id": user_id,
            "conversation_id": "",
            "search_queries": [],
            "search_results": [],
            "relevant_content": "",
            "final_report": "",
            "error": "",
        }

        try:
            logger.info(f"Starting research agent for query: {query}")
            result = await self.graph.ainvoke(initial_state)
            logger.info(f"Agent result keys: {result.keys() if result else 'None'}")
            logger.info(f"Conversation ID: {result.get('conversation_id', 'N/A')}")
            return result
        except Exception as e:
            logger.error(f"Agent execution failed: {str(e)}")
            raise AgentException(f"Research agent failed: {str(e)}")
