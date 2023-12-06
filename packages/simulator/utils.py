import os
import subprocess

def get_run_command(file: str) -> list:
    file_name, ext = os.path.splitext(file)
    ext = ext.lower()

    if ext == ".py": # Python
        return ["python3", file]
    elif ext == ".cpp": # C++
        compile(["g++", file, "-o", file_name, "-std=c++17"])
        return [file_name]
    else:
        raise ValueError(f"Unsupported file type for running: {ext}")


def compile(compile_command: list) -> None:
    try:
        if compile_command:
            subprocess.run(compile_command, check=True)
    except subprocess.CalledProcessError:
        raise RuntimeError("Error during compilation. Invalid command.")