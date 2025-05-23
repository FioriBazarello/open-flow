import os
import json

class PromptManager:
    def __init__(self, prompts_dir: str | None = None):
        if prompts_dir is None:
            prompts_dir = os.path.join(os.path.dirname(__file__), '..', 'prompts')
        self.prompts_dir = prompts_dir

    def load_prompt(self, prompt_name: str) -> str:
        # Validate prompt name to prevent path traversal
        if not prompt_name or '/' in prompt_name or '\\' in prompt_name or '..' in prompt_name:
            raise ValueError(f"Invalid prompt name: {prompt_name}")
        prompt_path = os.path.join(self.prompts_dir, f'{prompt_name}.json')
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "template" not in data:
                    raise KeyError(f"Missing 'template' key in {prompt_name}.json")
                return data["template"]
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {prompt_name}.json: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading prompt {prompt_name}: {e}")

    def fill_prompt(self, template: str, **kwargs) -> str:
        return template.format(**kwargs)

    def get_filled_prompt(self, prompt_name: str, **kwargs) -> str:
        template = self.load_prompt(prompt_name)
        return self.fill_prompt(template, **kwargs) 