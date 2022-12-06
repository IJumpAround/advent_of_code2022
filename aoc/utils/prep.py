import shutil
import sys
from typing import Optional

from aoc.puzzles import puzzles_path
from aoc.utils.input_loader import get_day_input_path
from aoc.utils.consts import day_int_to_str, template_solve_file, INPUT_FILE, SAMPLE_FILE


def prompt_bool(prompt, choices: Optional[dict]=None) -> bool:
    choices = choices or {'y': True, 'n': False}

    prompt = f'{prompt} {list(choices.keys())}>'
    choice = ''
    while choice.lower() not in choices:
        choice = input(prompt)

    return choices[choice]


def prepare_new_day(day: int):
    day = day_int_to_str(day)
    potential_input_path = get_day_input_path(day, raising=False)
    potential_puzzles_path = puzzles_path() / day

    if potential_input_path.is_dir():
        raise FileExistsError(potential_input_path)
    elif potential_puzzles_path.is_dir():
        raise FileExistsError(potential_puzzles_path)

    prompt = f"Creating new day folders: \n{potential_puzzles_path}\n{potential_input_path}\nIs this okay?"
    if prompt_bool(prompt):
        potential_puzzles_path.mkdir()
        (potential_puzzles_path / '__init__.py').touch()

        template = template_solve_file()
        new_solver_file = potential_puzzles_path / f'solve_{day}.py'
        shutil.copy(template, new_solver_file)

        potential_input_path.mkdir()
        (potential_input_path / INPUT_FILE).touch()
        (potential_input_path / SAMPLE_FILE).touch()


def write_puzzle_input(day: int, content: str):
    day = day_int_to_str(day)
    input_path = get_day_input_path(day)
    (input_path / INPUT_FILE).write_text(content, encoding='utf-8')


if __name__ == '__main__':
    prepare_new_day(sys.argv[1])