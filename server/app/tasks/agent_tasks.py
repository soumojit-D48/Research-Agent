
from app.tasks.celery_app import celery_app
from app.agents.research_agent import research_agent
import asyncio

@celery_app.task(name="run_research_agent")
def run_research_agent_task(query: str, user_id: str):
    """Background task for running agent"""
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(research_agent.run(query))
    
    # Store result in database
    # Log to agent_logs table
    
    return {
        "status": "completed",
        "result": result,
        "user_id": user_id
    }