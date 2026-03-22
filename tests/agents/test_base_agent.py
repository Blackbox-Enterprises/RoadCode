"""Tests for BaseAgent."""
import pytest
import asyncio
from agents.base import BaseAgent, AgentConfig

class TestAgent(BaseAgent):
    async def process(self, message, context=None):
        self.add_to_history("user", message)
        response = f"echo: {message}"
        self.add_to_history("assistant", response)
        return response

@pytest.fixture
def agent():
    return TestAgent(AgentConfig(name="test", role="tester", group="test"))

def test_agent_creation(agent):
    assert agent.name == "test"
    assert agent.config.role == "tester"
    assert not agent._running

@pytest.mark.asyncio
async def test_agent_process(agent):
    result = await agent.process("hello")
    assert result == "echo: hello"
    assert len(agent.history) == 2

@pytest.mark.asyncio
async def test_agent_start_stop(agent):
    await agent.start()
    assert agent._running
    await agent.stop()
    assert not agent._running

def test_agent_to_dict(agent):
    d = agent.to_dict()
    assert d["name"] == "test"
    assert d["role"] == "tester"
    assert d["running"] is False

def test_history_truncation(agent):
    for i in range(250):
        agent.add_to_history("user", f"msg {i}")
    assert len(agent.history) <= 200
