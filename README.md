# Task Manager

Task Manager est une application CLI minimaliste développée en Python permettant de créer, modifier, lister, supprimer des tâches, etc. Le projet suit une approche TDD avec `pytest` et utilise la bibliothèque `click` pour la gestion des commandes en ligne.

## Fonctionnalités principales

- Ajouter une tâche
- Lister les tâches existantes
- Modifier une tâche (titre, description, statut)
- Supprimer une tâche
- Marquer une tâche comme terminée

## Structure du projet
```
.
├── src/
│   ├── classes/
│   │   └── errors.py
│   ├── tasks_manager/
│   │   ├── cli_tools/
│   │   │   ├── cli_data_manager.py
│   │   │   ├── priority_tasks.py
│   │   │   ├── tags.py
│   │   │   ├── task_sheduler.py
│   │   │   └── view_tasks.py
│   │   ├── utils/
│   │   │   ├── data_manager.py
│   │   │   ├── file_utils.py
│   │   │   ├── priority_manager.py
│   │   │   ├── query_utils.py
│   │   │   ├── task_deadline.py
│   │   │   └── task_tags.py
│   │   └── task_manager.py
├── tests/
├── requirements.txt
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

Lancez l'application via la CLI :

```bash
python src/task_manager.py [commande] [options]
```

Pour connaitre les commandes existantes :

```bash
python src/task_manager.py --help
```


Exemples :

```bash
python src/task_manager.py create_task --title 'Nouveau titre' --description 'Nouvelle description'

python src/task_manager.py modify_task 1 --title 'Courses' --description 'Acheter des poires'

python src/task_manager.py priority_manager 1 set --priority 'HIGH'

python src/task_manager.py tags_manager 1 add '#shopping, #fun'

python src/task_manager.py task_sheduler 1 --add_deadline --deadline '2025-07-07'

python src/task_manager.py view_tasks 
```

## Lancer les tests

```bash
coverage run -m pytest
```

## Couverture de tests

```bash
coverage report
```

### Licence
Canac Julia
Lemos Emma