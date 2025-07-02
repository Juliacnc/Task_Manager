import json
import pytest
from unittest.mock import mock_open, patch

from src.tasks_manager.utils.data_manager import _load_tasks, _save_tasks


class TestLoadTasks:
    @patch("src.tasks_manager.utils.data_manager.os.path.exists")
    @patch("src.tasks_manager.utils.data_manager.open", new_callable=mock_open, read_data="[]")
    def test_load_existing_file_returns_list(self, mock_file, mock_exists):
        mock_exists.return_value = True

        result = _load_tasks("fakefile.json")

        assert result == []
        mock_file.assert_called_once_with("fakefile.json", "r", encoding="utf-8")

    @patch("src.tasks_manager.utils.data_manager.os.path.exists")
    @patch("src.tasks_manager.utils.data_manager.open", new_callable=mock_open)
    def test_load_creates_file_if_missing(self, mock_file, mock_exists):
        mock_exists.return_value = False

        # Simuler la lecture d'un fichier vide après création
        mock_file().read.return_value = "[]"

        result = _load_tasks("newfile.json")

        assert result == []
        assert mock_file.call_count >= 2  # Une écriture + une lecture
        mock_file.assert_any_call("newfile.json", "w", encoding="utf-8")
        mock_file.assert_any_call("newfile.json", "r", encoding="utf-8")


class TestSaveTasks:
    @patch("src.tasks_manager.utils.data_manager.open", new_callable=mock_open)
    def test_save_tasks_correctly_writes_json(self, mock_file):
        tasks = [{"id": 1, "title": "Tâche", "status": "TODO", "description": "", "created_at": "2024-01-01T10:00:00"}]

        _save_tasks(tasks, "savefile.json")

        mock_file.assert_called_once_with("savefile.json", "w", encoding="utf-8")

        handle = mock_file()
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)
        assert json.loads(written_data) == tasks

    @patch("src.tasks_manager.utils.data_manager.open", side_effect=IOError)
    def test_save_tasks_handles_ioerror(self, mock_file):
        tasks = [{"id": 1, "title": "Tâche"}]

        try:
            _save_tasks(tasks, "errorfile.json")
        except Exception:
            pytest.fail("L'appel à _save_tasks ne doit pas lever d'exception en cas d'IOError.")
