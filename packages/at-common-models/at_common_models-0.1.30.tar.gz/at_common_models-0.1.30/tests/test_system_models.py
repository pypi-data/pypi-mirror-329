from at_common_models.system.prompt import PromptModel
from at_common_models.system.workflow import WorkflowModel
from datetime import datetime, timedelta
from at_common_models.system.cache import CacheModel

def test_prompt_model(session):
    # Create test data
    prompt = PromptModel(
        name="test_prompt",
        description="A test prompt",
        tags=["test", "example"],
        model="gpt-4",
        sys_tpl="You are a helpful assistant",
        usr_tpl="Please help with {query}"
    )
    
    session.add(prompt)
    session.commit()
    
    result = session.query(PromptModel).filter_by(name="test_prompt").first()
    assert result.name == "test_prompt"
    assert result.description == "A test prompt"
    assert result.tags == ["test", "example"]
    assert result.model == "gpt-4"
    assert result.sys_tpl == "You are a helpful assistant"
    assert result.usr_tpl == "Please help with {query}"

def test_workflow_model(session):
    # Create test data
    workflow = WorkflowModel(
        name="test_workflow",
        description="A test workflow",
        tags=["test", "workflow"],
        initial_context_schema={
            "type": "object",
            "properties": {
                "input": {"type": "string"}
            }
        }
    )
    
    session.add(workflow)
    session.commit()
    
    result = session.query(WorkflowModel).filter_by(name="test_workflow").first()
    assert result.name == "test_workflow"
    assert result.description == "A test workflow"
    assert result.tags == ["test", "workflow"]
    assert result.initial_context_schema == {
        "type": "object",
        "properties": {
            "input": {"type": "string"}
        }
    }

def test_prompt_model_unique_name(session):
    # Test unique name constraint
    prompt1 = PromptModel(
        name="same_name",
        description="First prompt",
        tags=["test"],
        model="gpt-4",
        sys_tpl="System 1",
        usr_tpl="User 1"
    )
    
    prompt2 = PromptModel(
        name="same_name",  # Same name
        description="Second prompt",
        tags=["test"],
        model="gpt-4",
        sys_tpl="System 2",
        usr_tpl="User 2"
    )
    
    session.add(prompt1)
    session.commit()
    
    try:
        session.add(prompt2)
        session.commit()
        assert False, "Should have raised an integrity error"
    except:
        session.rollback()
        assert True

def test_workflow_model_unique_name(session):
    # Test unique name constraint
    workflow1 = WorkflowModel(
        name="same_name",
        description="First workflow",
        tags=["test"],
        initial_context_schema={"type": "object"}
    )
    
    workflow2 = WorkflowModel(
        name="same_name",  # Same name
        description="Second workflow",
        tags=["test"],
        initial_context_schema={"type": "object"}
    )
    
    session.add(workflow1)
    session.commit()
    
    try:
        session.add(workflow2)
        session.commit()
        assert False, "Should have raised an integrity error"
    except:
        session.rollback()
        assert True

def test_cache_model(session):
    # Create test data
    now = datetime.now()
    cache = CacheModel(
        key="test_key",
        value=b"test binary data",
        expires_at=now + timedelta(hours=1)
    )
    
    session.add(cache)
    session.commit()
    
    result = session.query(CacheModel).filter_by(key="test_key").first()
    assert result.key == "test_key"
    assert result.value == b"test binary data"
    assert result.expires_at == cache.expires_at

def test_cache_model_unique_key(session):
    # Test unique key constraint
    now = datetime.now()
    cache1 = CacheModel(
        key="same_key",
        value=b"first value",
        expires_at=now + timedelta(hours=1)
    )
    
    cache2 = CacheModel(
        key="same_key",  # Same key
        value=b"second value",
        expires_at=now + timedelta(hours=2)
    )
    
    session.add(cache1)
    session.commit()
    
    try:
        session.add(cache2)
        session.commit()
        assert False, "Should have raised an integrity error"
    except:
        session.rollback()
        assert True 