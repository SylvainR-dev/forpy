"""
Prompt builder — Factory pattern.

Loads the .txt prompt file matching chapter + sublevel,
then injects:
    {language}     — language of the exercise
    {last_topic}   — last generated topic (anti-repetition instruction)
    {category}     — pattern category (pattern sublevels only)
    {pattern}      — specific pattern (pattern sublevels only)
"""

import os

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")


class PromptBuilder:
    def get_prompt(
        self,
        chapter: str,
        sublevel: str,
        exercise_language: str,
        last_topic: str = "",
        category: str = "",
        pattern: str = "",
    ) -> str:
        path = os.path.join(PROMPTS_DIR, chapter, f"{sublevel}.txt")

        if not os.path.exists(path):
            raise FileNotFoundError(f"Prompt file not found: {path}")

        with open(path, encoding="utf-8") as f:
            prompt = f.read()

        prompt = prompt.replace("{language}", exercise_language)
        prompt = prompt.replace("{category}", category)
        prompt = prompt.replace("{pattern}", pattern)

        if last_topic:
            anti_repeat = (
                f"\nIMPORTANT: The previous exercise was about: \"{last_topic}\". "
                "Generate an exercise on a DIFFERENT topic.\n"
            )
        else:
            anti_repeat = ""

        prompt = prompt.replace("{last_topic}", anti_repeat)

        return prompt
