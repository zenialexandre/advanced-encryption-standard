from program_gui import generate_program_gui
import os
import shutil

file_path: str = generate_program_gui()

def upload_inputted_file(
    file_path: str
) -> None:
    if (os.path.exists(file_path)):
        file_name: str = os.path.basename(file_path)
        destionation_path: str = os.path.join('content', file_name)
        shutil.copy(file_path, destionation_path)

upload_inputted_file(file_path)
