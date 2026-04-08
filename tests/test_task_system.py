import pytest
import os
from main import add_task, delete_task, mark_task, load, get_next_id, save_tasks, FILE

@pytest.fixture
def empty_file():
    """Empty tasks file"""
    if os.path.exists(FILE):
        os.remove(FILE)
    yield


@pytest.fixture
def sample_tasks():
    """Tasks file with sample data"""
    if os.path.exists(FILE):
        os.remove(FILE)
    
    tasks = [
        {"id": 1, "description": "Buy milk", "date": "2026-04-08", "priority": 2, "done": False},
        {"id": 2, "description": "Clean room", "date": "2026-04-07", "priority": 1, "done": False},
        {"id": 3, "description": "Finish report", "date": "2026-04-10", "priority": 3, "done": True},
    ]
    save_tasks(tasks)
    yield

def test_get_next_id_empty():
    assert get_next_id([]) == 1


def test_get_next_id_with_tasks():
    assert get_next_id([{"id": 5}, {"id": 10}]) == 11


def test_load_empty_file(empty_file):
    tasks = load()
    assert tasks == []


def test_add_task_success(empty_file):
    task_id = add_task("Write tests", 2)
    tasks = load()
    assert len(tasks) == 1


def test_add_task_invalid_priority(empty_file):
    with pytest.raises(ValueError):
        add_task("Test task", 0)


def test_add_task_empty_description(empty_file):
    with pytest.raises(ValueError):
        add_task("", 3)


def test_delete_existing_task(sample_tasks):
    delete_task(2)
    tasks = load()
    assert len(tasks) == 2


def test_mark_task_as_done(sample_tasks):
    mark_task(1)
    tasks = load()
    assert any(t["id"] == 1 and t["done"] is True for t in tasks)


def test_mark_nonexistent_task(sample_tasks):
    with pytest.raises(ValueError):
        mark_task(999)


def test_mark_already_done_task(sample_tasks):
    mark_task(3)
    tasks = load()
    assert any(t["id"] == 3 and t["done"] is True for t in tasks)


@pytest.mark.parametrize("priority", [0, 6, -1, 10])
def test_add_invalid_priority(empty_file, priority):
    with pytest.raises(ValueError):
        add_task("Invalid priority task", priority)


@pytest.mark.parametrize("description", ["", "   ", None])
def test_add_invalid_description(empty_file, description):
    with pytest.raises(ValueError):
        add_task(description, 3)
