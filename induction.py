import os
import csv
from anthropic import Anthropic

class PromptRefinementLoop:
    def __init__(self, api_key, seed_prompt, initial_prompt="", initial_critique=""):
        self.client = Anthropic(api_key=api_key)
        self.seed_prompt = seed_prompt
        
        self._initialize_files(initial_prompt, initial_critique)
        
        if not os.path.exists('history.csv'):
            with open('history.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['prompt', 'score'])

    def _initialize_files(self, initial_prompt, initial_critique):
        """Initialize the prompt and critique files if they don't exist."""
        files = {
            'prompt_n-1.txt': initial_prompt,
            'prompt_n.txt': initial_prompt,
            'critique_n-1.txt': initial_critique,
            'critique_n.txt': initial_critique
        }
        
        for filename, content in files.items():
            if not os.path.exists(filename):
                with open(filename, 'w') as f:
                    f.write(content)

    def _read_file(self, filename):
        """Read content from a file."""
        with open(filename, 'r') as f:
            return f.read().strip()

    def _write_file(self, filename, content):
        """Write content to a file."""
        with open(filename, 'w') as f:
            f.write(content)

    def _rotate_files(self, new_prompt, new_critique):
        """Rotate the contents of the files."""
        # Rotate prompts
        old_prompt = self._read_file('prompt_n.txt')
        self._write_file('prompt_n-1.txt', old_prompt)
        self._write_file('prompt_n.txt', new_prompt)
        
        # Rotate critiques
        old_critique = self._read_file('critique_n.txt')
        self._write_file('critique_n-1.txt', old_critique)
        self._write_file('critique_n.txt', new_critique)

    def _save_to_history(self, prompt, score):
        """Save the prompt and its score to history.csv."""
        with open('history.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([prompt, score])

    def _construct_prompt_message(self):
        """Construct the full message for generating a new prompt."""
        prev_prompt = self._read_file('prompt_n-1.txt')
        current_prompt = self._read_file('prompt_n.txt')
        
        return f"""Human: {self.seed_prompt}