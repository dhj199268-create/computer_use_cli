import time
from typing import Any, Dict, List, Optional

from ..core.logger import get_logger
from .base import BaseSkill
from .navigation import NavigationSkill
from .text_input import TextInputSkill
from .screenshot_analysis import ScreenshotAnalysisSkill

logger = get_logger(__name__)


class AutomationSkill(BaseSkill):
    """Skill for orchestrating multi-step automation workflows."""

    def __init__(self):
        self.navigation = NavigationSkill()
        self.text_input = TextInputSkill()
        self.screenshot = ScreenshotAnalysisSkill()

    @classmethod
    def get_description(cls) -> str:
        return "Orchestrate multi-step automation workflows."

    @classmethod
    def get_parameters(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "workflow": {
                "type": "list",
                "required": True,
                "description": "List of workflow steps to execute",
            },
            "delay": {
                "type": "float",
                "required": False,
                "default": 0.5,
                "description": "Delay between steps in seconds",
            },
        }

    def execute(self, context: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        workflow = kwargs.get("workflow", [])
        delay = kwargs.get("delay", 0.5)
        context = context or {}

        results = []
        for i, step in enumerate(workflow):
            logger.info(f"Executing step {i + 1}/{len(workflow)}")
            try:
                result = self._execute_step(step, context)
                results.append({"step": i + 1, "success": True, "result": result})
            except Exception as e:
                logger.error(f"Step {i + 1} failed: {e}")
                results.append({"step": i + 1, "success": False, "error": str(e)})
                if step.get("stop_on_failure", True):
                    break

            if i < len(workflow) - 1:
                time.sleep(delay)

        return results

    def _execute_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Any:
        skill_type = step.get("skill")
        params = step.get("params", {})

        # Replace context variables in params
        params = self._resolve_params(params, context)

        if skill_type == "navigation":
            result = self.navigation.execute(context, **params)
        elif skill_type == "text_input":
            result = self.text_input.execute(context, **params)
        elif skill_type == "screenshot":
            result = self.screenshot.execute(context, **params)
        elif skill_type == "wait":
            duration = params.get("duration", 1.0)
            time.sleep(duration)
            result = f"Waited {duration}s"
        else:
            raise ValueError(f"Unknown skill type: {skill_type}")

        # Store result in context if requested
        if "store_as" in step:
            context[step["store_as"]] = result

        return result

    def _resolve_params(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve context variables in parameters (format: ${var_name})."""
        resolved = {}
        for key, value in params.items():
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                var_name = value[2:-1]
                if var_name in context:
                    resolved[key] = context[var_name]
                else:
                    resolved[key] = value
            elif isinstance(value, dict):
                resolved[key] = self._resolve_params(value, context)
            elif isinstance(value, list):
                resolved[key] = [
                    self._resolve_params({"v": item}, context)["v"]
                    for item in value
                ]
            else:
                resolved[key] = value
        return resolved
