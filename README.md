# Multi-Agent Development System

A Python-based multi-agent system that coordinates development tasks between a Manager Agent and specialized sub-agents.

## Project Structure
```
.
├── agents/                  # Agent implementations
│   ├── manager_agent.py    # Main manager agent
│   ├── frontend_agent.py   # Frontend specialist agent
│   └── backend_agent.py    # Backend specialist agent
├── knowledge_base/         # Shared knowledge store
│   └── knowledge_store.yaml
├── tests/                  # Test suite
│   └── test_agents.py
├── utils/                  # Utility functions
│   └── git_utils.py
└── requirements.txt        # Project dependencies
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Manager Agent:
```bash
python -m agents.manager_agent
```

2. The Manager Agent will coordinate with sub-agents automatically based on incoming tasks.

## Development

- Add new sub-agents by creating new agent classes in the `agents/` directory
- Update knowledge base schemas in `knowledge_base/`
- Add tests for new functionality in `tests/`
