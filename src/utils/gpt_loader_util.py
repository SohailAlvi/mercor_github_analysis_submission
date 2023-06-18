import os
import sys
import fnmatch
import logging

from src.constants import CUSTOM_IGNORE_LIST


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))





class GPTLoader:

    def __init__(self, repository_path, file_batch_size=None):
        self.content_buffer = []
        self.repository_path = repository_path
        self.ignore_list = []
        self.file_batch_size = 10 if file_batch_size is None else file_batch_size

    def get_ignore_list(self):
        ignore_file_path = os.path.join(self.repository_path, ".gitignore")
        if os.path.exists(ignore_file_path):
            with open(ignore_file_path, 'r') as ignore_file:
                for line in ignore_file:
                    if sys.platform == "win32":
                        line = line.replace("/", "\\")
                    self.ignore_list.append(line.strip())
        self.ignore_list.extend(CUSTOM_IGNORE_LIST)

    def should_ignore(self, file_path):
        for pattern in self.ignore_list:
            if fnmatch.fnmatch(file_path, pattern):
                return True
        return False

    def process_repository(self, root, files):
        for file in files:
            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, self.repository_path)

            if not self.should_ignore(relative_file_path):
                if relative_file_path.endswith(".ipynb"):
                    # Convert Jupyter Notebook to txt
                    os.system(f"jupyter nbconvert --to script {relative_file_path}")
                    file_path = ""
                with open(file_path, 'r', errors='ignore') as file_pointer:
                    contents = file_pointer.read()
                    self.content_buffer.append(contents)
                logging.info(f"File Path traversed {relative_file_path}\n")

    def process(self, output_file_path):
        self.get_ignore_list()
        for root, _, files in os.walk(self.repository_path):
            self.process_repository(root, files)
            with open(output_file_path, 'a') as output_file:
                for content in self.content_buffer:
                    output_file.write(content)
                output_file.close()
                self.content_buffer.clear()


def convert_to_prompt_input(repository_path: str, output_file_path: str):
    with open(output_file_path, 'w') as output_file:
        output_file.write("--START OF FILE--")
    GPTLoader(repository_path=repository_path).process(output_file_path)
    with open(output_file_path, 'a') as output_file:
        output_file.write("--END OF FILE--")
    print(f"Repository contents written to {output_file_path}.")


if __name__ == '__main__':
    convert_to_prompt_input("cloned/SohailAlvi/elasticsearch", "cloned/SohailAlvi/elasticsearch.txt")
