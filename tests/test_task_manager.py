# test_task_manager.py - Tests pour la logique métier
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.task_manager import get_tasks, task_list

class TestTaskManager:
    
    def setup_method(self):
        """Initialise les données de test avant chaque test"""
        # Réinitialise la liste avec des données de test connues
        task_list.clear()
        task_list.extend([
            {
                "id": 1,
                "title": "Première tâche",
                "description": "Description de la première tâche",
                "status": "TODO"
            },
            {
                "id": 2,
                "title": "Deuxième tâche",
                "description": "Description de la deuxième tâche",
                "status": "DONE"
            }
        ])
    
    def test_get_tasks_returns_list(self):
        """Test que get_tasks retourne une liste"""
        tasks = get_tasks()
        
        assert isinstance(tasks, list)
    
    def test_get_tasks_returns_two_tasks(self):
        """Test que get_tasks retourne 2 tâches"""
        tasks = get_tasks()
        
        assert len(tasks) == 2
    
    def test_get_tasks_returns_correct_structure(self):
        """Test que les tâches ont la bonne structure"""
        tasks = get_tasks()
        
        assert "id" in tasks[0]
        assert "title" in tasks[0]
        assert "description" in tasks[0]
        assert "status" in tasks[0]
