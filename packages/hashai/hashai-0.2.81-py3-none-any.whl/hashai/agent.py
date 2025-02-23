from __future__ import annotations

import asyncio
import json
import logging
import uuid
import base64
import io
from typing import Any, Dict, List, Optional, TypeVar
from pathlib import Path

from pydantic import BaseModel
from PIL import Image

from hashai.llm.groq import GroqLlm  # Custom Groq integration
from hashai.tools.web_browser import WebBrowserTool  # Browser automation tool
from hashai.utils.logger import logger  # Logging utility

# Define types
T = TypeVar('T', bound=BaseModel)

class Agent:
    def __init__(
        self,
        task: str,
        llm: GroqLlm,
        browser_tool: WebBrowserTool,
        max_failures: int = 5,
        retry_delay: int = 10,
        max_input_tokens: int = 128000,
        validate_output: bool = False,
        generate_gif: bool = True,
        save_conversation_path: Optional[str] = None,
    ):
        """
        Initialize the Agent.

        Args:
            task (str): The task to be performed.
            llm (GroqLlm): The LLM instance to use for task decomposition and action generation.
            browser_tool (WebBrowserTool): The browser automation tool.
            max_failures (int): Maximum number of consecutive failures before stopping.
            retry_delay (int): Delay (in seconds) between retries.
            max_input_tokens (int): Maximum number of input tokens for the LLM.
            validate_output (bool): Whether to validate the output of each step.
            generate_gif (bool): Whether to generate a GIF of the task execution.
            save_conversation_path (Optional[str]): Path to save the conversation history.
        """
        self.agent_id = str(uuid.uuid4())  # Unique identifier for the agent
        self.task = task
        self.llm = llm
        self.browser_tool = browser_tool
        self.max_failures = max_failures
        self.retry_delay = retry_delay
        self.max_input_tokens = max_input_tokens
        self.validate_output = validate_output
        self.generate_gif = generate_gif
        self.save_conversation_path = save_conversation_path

        # Tracking variables
        self.history: List[Dict[str, Any]] = []
        self.n_steps = 1
        self.consecutive_failures = 0

    async def decompose_task(self, task: str) -> List[Dict[str, Any]]:
        """
        Use the LLM to decompose a task into smaller, actionable steps.

        Args:
            task (str): The task to decompose.

        Returns:
            List[Dict[str, Any]]: A list of action JSONs.
        """
        prompt = f"""
        You are a task decomposition assistant. Break down the following task into smaller, actionable steps:
        Task: {task}

        Return the steps as a list of dictionaries with the following format:
        - "action": The action to perform (e.g., "navigate", "fill_form", "click", "scrape").
        - "details": Details about the action (e.g., URL, form fields, element selector).
        - "website": The website to perform the action on (optional, default is Google).
        """
        response = await self.llm.generate(prompt=prompt)
        return json.loads(response)  # Convert the response into a list of dictionaries

    async def execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single step using the WebBrowserTool.

        Args:
            step (Dict[str, Any]): The action JSON to execute.

        Returns:
            Dict[str, Any]: The result of the step execution.
        """
        try:
            result = await self.browser_tool.execute_step(step)
            return {"step": step, "result": result, "error": None}
        except Exception as e:
            logger.error(f"Error executing step: {e}")
            return {"step": step, "result": None, "error": str(e)}

    async def run(self, max_steps: int = 100) -> List[Dict[str, Any]]:
        """
        Execute the task with a maximum number of steps.

        Args:
            max_steps (int): Maximum number of steps to execute.

        Returns:
            List[Dict[str, Any]]: The history of actions and results.
        """
        logger.info(f'🚀 Starting task: {self.task}')

        for step in range(max_steps):
            if self._too_many_failures():
                break

            await self.step()

            if self._is_task_complete():
                logger.info('✅ Task completed successfully')
                break
        else:
            logger.info('❌ Failed to complete task in maximum steps')

        return self.history

    async def step(self) -> None:
        """
        Execute one step of the task.
        """
        logger.info(f'\n📍 Step {self.n_steps}')
        try:
            steps = await self.decompose_task(self.task)
            for step in steps:
                result = await self.execute_step(step)
                self.history.append(result)
                self.n_steps += 1

                if result.get("error"):
                    self.consecutive_failures += 1
                    if self._too_many_failures():
                        break
                    await asyncio.sleep(self.retry_delay)
                else:
                    self.consecutive_failures = 0
        except Exception as e:
            self._handle_step_error(e)

    def _handle_step_error(self, error: Exception) -> None:
        """
        Handle errors that occur during a step.

        Args:
            error (Exception): The error that occurred.
        """
        error_msg = str(error)
        logger.error(f'❌ Step failed: {error_msg}')
        self.consecutive_failures += 1
        if self.consecutive_failures >= self.max_failures:
            logger.error(f'❌ Stopping due to {self.max_failures} consecutive failures')

    def _too_many_failures(self) -> bool:
        """
        Check if the agent should stop due to too many failures.

        Returns:
            bool: True if too many failures, False otherwise.
        """
        return self.consecutive_failures >= self.max_failures

    def _is_task_complete(self) -> bool:
        """
        Check if the task is complete based on the history.

        Returns:
            bool: True if the task is complete, False otherwise.
        """
        # Placeholder logic: Task is complete if no errors in the last step
        return not any(step.get("error") for step in self.history[-1:])

    def save_history(self, file_path: Optional[str | Path] = None) -> None:
        """
        Save the task execution history to a file.

        Args:
            file_path (Optional[str | Path]): The path to save the history file.
        """
        if not file_path:
            file_path = Path(self.save_conversation_path) if self.save_conversation_path else Path("agent_history.json")
        with open(file_path, "w") as f:
            json.dump(self.history, f, indent=2)
        logger.info(f'📄 History saved to {file_path}')

    def create_history_gif(self, output_path: str = "agent_history.gif", duration: int = 3000) -> None:
        """
        Create a GIF from the agent's history with overlaid task and goal text.

        Args:
            output_path (str): The path to save the GIF.
            duration (int): The duration of each frame in the GIF.
        """
        if not self.history:
            logger.warning('No history to create GIF from')
            return

        images = []
        for step in self.history:
            if "screenshot" in step:
                img_data = base64.b64decode(step["screenshot"])
                image = Image.open(io.BytesIO(img_data))
                images.append(image)

        if images:
            images[0].save(
                output_path,
                save_all=True,
                append_images=images[1:],
                duration=duration,
                loop=0,
                optimize=False,
            )
            logger.info(f'🎥 GIF created at {output_path}')
        else:
            logger.warning('No images found in history to create GIF')