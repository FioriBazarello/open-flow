import os
import json

class PromptManager:
    def __init__(self, prompts_dir: str | None = None):
        if prompts_dir is None:
            prompts_dir = os.path.join(os.path.dirname(__file__), '..', 'prompts')
        self.prompts_dir = prompts_dir

    def load_prompt(self, prompt_name: str) -> str:
        prompt_path = os.path.join(self.prompts_dir, f'{prompt_name}.json')
        with open(prompt_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data["template"]

    def fill_prompt(self, template: str, **kwargs) -> str:
        return template.format(**kwargs)

    def get_filled_prompt(self, prompt_name: str, **kwargs) -> str:
        template = self.load_prompt(prompt_name)
        return self.fill_prompt(template, **kwargs) 