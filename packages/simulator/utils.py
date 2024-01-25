import os
import platform

def get_run_command(file: str) -> list[str]:
    file_name, ext = os.path.splitext(os.path.basename(file))
    path = os.path.dirname(file)
    ext = ext.lower()

    if ext == ".py":  # Python
        python_command = "python" if platform.system().lower() == "windows" else "python3"
        return [python_command, file]

    elif ext == ".exe":  # Binary code
        return [file]
    else:
        raise ValueError(f"Unsupported file type for running: {ext}")



# def compile(compile_command: list[str]) -> None:
#     try:
#         if compile_command:
#             subprocess.run(compile_command, check=True)
#     except subprocess.CalledProcessError:
#         raise RuntimeError("Error during compilation. Invalid command.")
    
