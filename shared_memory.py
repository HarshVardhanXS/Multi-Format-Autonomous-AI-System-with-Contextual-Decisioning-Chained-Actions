from datetime import datetime
from typing import Dict, Any
import threading
import json
import os

class SharedMemory:
    def __init__(self, log_path=None):
        self.lock = threading.Lock()
        self.memory_store: Dict[str, Any] = {
            "input_metadata": {},
            "extracted_fields": {},
            "chained_actions": [],
            "decision_traces": [],
            "agent_decisions": [],
        }
        self.log_path = log_path
        if log_path:
            os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def reset_memory(self):
        with self.lock:
            self.memory_store = {
                "input_metadata": {},
                "extracted_fields": {},
                "chained_actions": [],
                "decision_traces": [],
                "agent_decisions": [],
            }
            if self.log_path:
                self._log_to_file()

    def update_memory(self, data: Dict[str, Any], section=None):
        with self.lock:
            if section:
                if section in ["input_metadata", "extracted_fields"]:
                    self.memory_store[section].update(data)
                elif section in ["chained_actions", "decision_traces", "agent_decisions"]:
                    if isinstance(data, list):
                        self.memory_store[section].extend(data)
                    else:
                        self.memory_store[section].append(data)
                else:
                    self.memory_store.update({section: data})
            else:
                for key, value in data.items():
                    if key in ["input_metadata", "extracted_fields"]:
                        self.memory_store[key].update(value)
                    elif key in ["chained_actions", "decision_traces", "agent_decisions"]:
                        if isinstance(value, list):
                            self.memory_store[key].extend(value)
                        else:
                            self.memory_store[key].append(value)
                    else:
                        self.memory_store[key] = value
            if self.log_path:
                self._log_to_file()

    def get_memory(self):
        with self.lock:
            return self.memory_store.copy()

    def print_shared_memory(self):
        with self.lock:
            return json.dumps(self.memory_store, indent=2)

    def export_memory(self, export_path):
        with self.lock:
            os.makedirs(os.path.dirname(export_path), exist_ok=True)
            with open(export_path, "w") as f:
                json.dump(self.memory_store, f, indent=2)

    def _log_to_file(self):
        try:
            with open(self.log_path, "w") as f:
                json.dump(self.memory_store, f, indent=2)
        except Exception as e:
            print(f"Failed to log memory to file: {e}")
