import json
import pytest
from src.tasks_manager.utils.file_utils import _load_tasks, _save_tasks


class TestLoadTasks:
    def test_load_existing_file_returns_list(self):
        data = [{"id": 1, "title": "Tâche test"}]
        file_path = "tests/data/tasks.json"
        file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

        loaded = _load_tasks(str(file_path))

        assert loaded == data

    def test_load_creates_file_if_missing(self, tmp_path):
        file_path = tmp_path / "missing.json"

        assert not file_path.exists()

        loaded = _load_tasks(str(file_path))

        assert loaded == []
        assert file_path.exists()

        # Vérifier que le contenu du fichier est une liste vide
        content = json.loads(file_path.read_text(encoding="utf-8"))
        assert content == []


class TestSaveTasks:
    def test_save_tasks_writes_file(self, tmp_path):
        file_path = tmp_path / "saved.json"
        tasks = [{"id": 42, "title": "À sauvegarder", "description": "", "status": "TODO", "created_at": "2024-01-01T10:00:00"}]

        _save_tasks(tasks, str(file_path))

        assert file_path.exists()

        saved = json.loads(file_path.read_text(encoding="utf-8"))
        assert saved == tasks

    def test_save_tasks_overwrites_existing_file(self, tmp_path):
        file_path = tmp_path / "overwrite.json"
        file_path.write_text("n'importe quoi", encoding="utf-8")

        tasks = [{"id": 99, "title": "Réécriture", "description": "", "status": "DONE", "created_at": "2024-01-01T10:00:00"}]

        _save_tasks(tasks, str(file_path))

        saved = json.loads(file_path.read_text(encoding="utf-8"))
        assert saved == tasks
