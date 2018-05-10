from fs import open_fs
import json

DIR = "/Users/dace/sublime-snippets/Snippets"
# FILE = "after.sublime-snippet"

def count_python_loc(fs):
    count = 0
    for path in fs.walk.files(filter=['*.sublime-snippet']):
        with fs.open(path) as python_file:
            count += sum(1 for line in python_file if line.strip())
    return count

projects_fs = open_fs('~/sublime-snippets/Snippets')
print(count_python_loc(projects_fs))