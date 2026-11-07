import pytest

from tasks import TaskStore


def test_add_and_list():
    store = TaskStore()
    store.add("write tests")
    assert [t.title for t in store.list()] == ["write tests"]


def test_complete_hides_from_open_list():
    store = TaskStore()
    task = store.add("ship it")
    store.complete(task.id)
    assert store.list(include_done=False) == []


def test_empty_title_rejected():
    with pytest.raises(ValueError):
        TaskStore().add("   ")


def test_remove_returns_task():
    store = TaskStore()
    task = store.add("clean up")
    removed = store.remove(task.id)
    assert removed == task
    assert store.list() == []


def test_remove_unknown_id_raises_key_error():
    store = TaskStore()
    with pytest.raises(KeyError):
        store.remove(999)
