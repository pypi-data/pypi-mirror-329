import time
from datetime import timedelta
from pydantic import BaseModel
from typing import Any, Dict, List, Tuple, Callable

# General model for the health check response
class GeneralCheckResponse(BaseModel):
    Name: str
    status: str
    Details: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    Runtime: str
    Agent_Name: str
    customChecks: Dict[str,Any]
    checks: List[GeneralCheckResponse]


def calculate_uptime(start_time: float) -> str:
    uptime_seconds = time.time() - start_time
    return str(timedelta(seconds=int(uptime_seconds)))


def generate_health_check_response(start_time: float,
                                   app_checks: List[Tuple[Callable, bool, Dict[str, Any]]],
                                   agent_name: str,custom_checks: Dict[str, Any]) -> HealthResponse:
    uptime = calculate_uptime(start_time)

    formatted_checks = [
        GeneralCheckResponse(
            Name=check_function.__name__,
            status="ok" if status else "fail",
            Details=details
        )
        for check_function, status, details in app_checks
    ]
    overall_status = "ok" if all(c.status == "ok" for c in formatted_checks) else "warning"
    return HealthResponse(
        status=overall_status,
        Runtime=uptime,
        Agent_Name=agent_name,
        customChecks= custom_checks,
        checks=formatted_checks
    )


class HealthCheck:
    def __init__(self):
        self.checks = []
        self.custom_checks = {}  # To store custom key-value pairs
        self.agent_name = "default_agent"
        self.start_time = 0

    def add(self, check_function: Callable, *args, **kwargs):
        """Registers a health check function."""
        self.checks.append((check_function, args, kwargs))

    def add_custom(self, name: str, value: Any):
        """Add a custom check as a key-value pair."""
        self.custom_checks[name] = value

    def run(self):
        """Runs all registered checks and returns the results."""
        results = []
        for check_function, args, kwargs in self.checks:
            status, details = check_function(*args, **kwargs)
            results.append((check_function, status, details))
        return results

    def function(self, check_function: Callable, *args, **kwargs):
        """Decorator to automatically register health check functions."""
        self.add(check_function, *args, **kwargs)

    def addAgent(self, agent_name: str):
        """Set the agent name dynamically."""
        self.agent_name = agent_name

    def startTime(self):
        """Set the start time for calculating uptime."""
        self.start_time = time.time()

    def get_health_status(self):
        """Gets the health status, making the API handler cleaner."""
        app_checks = self.run()
        return generate_health_check_response(self.start_time, app_checks, self.agent_name,self.custom_checks)



# Create a global instance of the HealthCheck utility
healthCheck = HealthCheck()