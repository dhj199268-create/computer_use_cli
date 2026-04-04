from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseSkill(ABC):
    """Abstract base class for all skills."""

    @abstractmethod
    def execute(self, context: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        """
        Execute the skill.

        Args:
            context: Shared context dictionary
            **kwargs: Skill-specific parameters

        Returns:
            Result of the skill execution
        """
        pass

    def validate(self, **kwargs) -> bool:
        """
        Validate input parameters before execution.

        Args:
            **kwargs: Parameters to validate

        Returns:
            True if parameters are valid

        Raises:
            ValidationError: If parameters are invalid
        """
        return True

    @classmethod
    def get_description(cls) -> str:
        """Get a description of the skill."""
        return cls.__doc__ or ""

    @classmethod
    def get_parameters(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get parameter specifications for the skill.

        Returns:
            Dictionary mapping parameter names to their specifications:
            {
                "param_name": {
                    "type": "str|int|float|bool",
                    "required": True|False,
                    "default": ...,
                    "description": "...",
                }
            }
        """
        return {}
