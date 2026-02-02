"""JSON-based state repository."""

import json
import os
from pathlib import Path
from typing import Optional
from datetime import datetime

from src.domain.entities import PityState


class JsonStateRepository:
    """
    Concrete implementation of StateRepository using JSON files.
    
    Saves state to user's home directory: ~/.endfield_pity_state.json
    """
    
    def __init__(self, file_path: Optional[Path] = None):
        """
        Initialize repository.
        
        Args:
            file_path: Custom file path (defaults to ~/.endfield_pity_state.json)
        """
        if file_path is None:
            home = Path.home()
            self.file_path = home / ".endfield_pity_state.json"
        else:
            self.file_path = file_path
        
        self.backup_path = self.file_path.with_suffix(".json.bak")
    
    def save(self, state: PityState) -> None:
        """
        Save pity state to JSON file.
        
        Creates backup of existing file before overwriting.
        """
        data = {
            "version": "1.0",
            "timestamp": datetime.now().isoformat(),
            "state": {
                "pulls_without_6_star": state.pulls_without_6_star,
                "pulls_without_5_star": state.pulls_without_5_star,
                "banner_pulls": state.banner_pulls,
                "total_pulls": state.total_pulls,
            }
        }
        
        # Backup existing file
        if self.file_path.exists():
            self.file_path.replace(self.backup_path)
        
        # Write new file
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            # Restore backup if write failed
            if self.backup_path.exists():
                self.backup_path.replace(self.file_path)
            raise IOError(f"Failed to save state: {e}")
    
    def load(self) -> Optional[PityState]:
        """
        Load pity state from JSON file.
        
        Returns None if file doesn't exist or is invalid.
        """
        if not self.file_path.exists():
            return None
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            state_data = data.get("state", {})
            return PityState(
                pulls_without_6_star=state_data.get("pulls_without_6_star", 0),
                pulls_without_5_star=state_data.get("pulls_without_5_star", 0),
                banner_pulls=state_data.get("banner_pulls", 0),
                total_pulls=state_data.get("total_pulls", 0),
            )
        except Exception as e:
            print(f"Warning: Failed to load state: {e}")
            return None
    
    def exists(self) -> bool:
        """Check if saved state exists."""
        return self.file_path.exists()
    
    def delete(self) -> None:
        """Delete saved state file."""
        if self.file_path.exists():
            self.file_path.unlink()
        if self.backup_path.exists():
            self.backup_path.unlink()
    
    def get_file_path(self) -> Path:
        """Get the path to the state file."""
        return self.file_path
