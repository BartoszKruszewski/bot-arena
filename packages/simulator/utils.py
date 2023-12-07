import subprocess
import os
import platform


def get_run_command(file: str) -> list[str]:
    file_name, ext = os.path.splitext(os.path.basename(file))
    path = os.path.dirname(file)
    ext = ext.lower()
    bin_path = os.path.join(path, "bin")

    if ext == ".py":  # Python
        python_command = "python" if platform.system().lower() == "windows" else "python3"
        return [python_command, file]

    elif ext == ".cpp":  # C++
        bin_file = os.path.join(bin_path, file_name)
        compile_command = ["g++", file, "-o", bin_file, "-std=c++17"]
        compile(compile_command)
        return [bin_file]
    else:
        raise ValueError(f"Unsupported file type for running: {ext}")



def compile(compile_command: list[str]) -> None:
    try:
        if compile_command:
            subprocess.run(compile_command, check=True)
    except subprocess.CalledProcessError:
        raise RuntimeError("Error during compilation. Invalid command.")