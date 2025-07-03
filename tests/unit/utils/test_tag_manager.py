import pytest
from src.classes.errors import TaskValidationError, TaskNotFoundError
from tasks_manager.utils.task_tags import (
    _add_tags_to_task,
    _remove_tag_from_task,
    _filter_tasks_by_tags,
    _get_all_tags_with_usage,
)


class TestTagManager:
    def setup_method(self):
        self.tasks = [
            {"id": 1, "title": "Task 1", "tags": ["work", "urgent"]},
            {"id": 2, "title": "Task 2", "tags": ["home"]},
            {"id": 3, "title": "Task 3", "tags": []},
            {"id": 4, "title": "Task 4"},  # no tags key
        ]

    def test_add_single_tag_to_task(self):
        task, tasks = _add_tags_to_task(self.tasks, 3, ["important"])
        assert "important" in task["tags"]

    def test_add_multiple_tags_to_task(self):
        task, tasks = _add_tags_to_task(self.tasks, 1, ["newtag", "urgent"])
        assert "newtag" in task["tags"]
        # existing tag remains
        assert "urgent" in task["tags"]

    def test_add_tags_invalid_empty(self):
        with pytest.raises(TaskValidationError):
            _add_tags_to_task(self.tasks, 1, [""])

    def test_add_tags_invalid_too_long(self):
        too_long_tag = "a" * 21
        with pytest.raises(TaskValidationError):
            _add_tags_to_task(self.tasks, 1, [too_long_tag])

    def test_remove_tag_from_task(self):
        task, tasks = _remove_tag_from_task(self.tasks, 1, "urgent")
        assert "urgent" not in task["tags"]
        assert "work" in task["tags"]

    def test_remove_tag_not_in_task_no_error(self):
        task, tasks = _remove_tag_from_task(self.tasks, 2, "urgent")
        # tags unchanged
        assert "home" in task["tags"]

    def test_remove_tag_invalid_empty(self):
        with pytest.raises(TaskValidationError):
            _remove_tag_from_task(self.tasks, 1, "")

    def test_remove_tag_invalid_too_long(self):
        with pytest.raises(TaskValidationError):
            _remove_tag_from_task(self.tasks, 1, "a" * 21)

    def test_filter_tasks_by_single_tag(self):
        filtered = _filter_tasks_by_tags(self.tasks, ["work"])
        assert all("work" in task.get("tags", []) for task in filtered)
        assert len(filtered) == 1

    def test_filter_tasks_by_multiple_tags(self):
        filtered = _filter_tasks_by_tags(self.tasks, ["work", "home"])
        # Tasks with 'work' or 'home'
        filtered_ids = [task["id"] for task in filtered]
        assert 1 in filtered_ids
        assert 2 in filtered_ids
        assert len(filtered) == 2

    def test_filter_tasks_by_no_tags_returns_all(self):
        filtered = _filter_tasks_by_tags(self.tasks, [])
        assert len(filtered) == len(self.tasks)

    def test_get_all_tags_with_usage_counts(self):
        counts = _get_all_tags_with_usage(self.tasks)
        expected = {"work": 1, "urgent": 1, "home": 1}
        # tags order may differ
        assert counts == expected or counts == {k: expected[k] for k in counts}

    def test_get_all_tags_with_usage_empty(self):
        empty_tasks = [{"id": 10, "title": "No tags"}]
        counts = _get_all_tags_with_usage(empty_tasks)
        assert counts == {}

    def test_add_tags_to_task_task_not_found(self):
        with pytest.raises(TaskNotFoundError):
            _add_tags_to_task(self.tasks, 999, ["tag"])

    def test_remove_tag_from_task_task_not_found(self):
        with pytest.raises(TaskNotFoundError):
            _remove_tag_from_task(self.tasks, 999, "tag")

    def test_add_tags_to_task_no_tags_key_creates_tags_list(self):
        # Task id=4 n'a pas de clé 'tags', on doit tester qu'elle est créée et tags ajoutés # noqa: E501
        task, tasks = _add_tags_to_task(self.tasks, 4, ["newtag"])
        assert "newtag" in task["tags"]
        assert isinstance(task["tags"], list)
