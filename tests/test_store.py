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


def test_rename_updates_title():
    store = TaskStore()
    task = store.add("old title")
    renamed = store.rename(task.id, "new title")
    assert renamed.title == "new title"


def test_rename_strips_whitespace():
    store = TaskStore()
    task = store.add("original")
    renamed = store.rename(task.id, "  New  ")
    assert renamed.title == "New"


def test_rename_strips_and_rejects_empty():
    store = TaskStore()
    task = store.add("original")
    with pytest.raises(ValueError):
        store.rename(task.id, "   ")


def test_rename_unknown_id_raises():
    store = TaskStore()
    with pytest.raises(KeyError):
        store.rename(999, "X")


def test_rename_preserves_id_and_done():
    store = TaskStore()
    task = store.add("do something")
    store.complete(task.id)
    original_id = task.id
    renamed = store.rename(task.id, "did something")
    assert renamed.id == original_id
    assert renamed.done is True


def test_reopen_marks_done_task_not_done():
    store = TaskStore()
    task = store.add("finish")
    store.complete(task.id)
    reopened = store.reopen(task.id)
    assert reopened.done is False
    assert reopened is task


def test_reopen_not_done_task_is_noop():
    store = TaskStore()
    task = store.add("pending")
    reopened = store.reopen(task.id)
    assert reopened.done is False
    assert reopened is task


def test_reopen_unknown_id_raises():
    store = TaskStore()
    with pytest.raises(KeyError):
        store.reopen(999)


def test_reopen_preserves_id_and_title():
    store = TaskStore()
    task = store.add("keep me")
    store.complete(task.id)
    reopened = store.reopen(task.id)
    assert reopened.id == task.id
    assert reopened.title == "keep me"
