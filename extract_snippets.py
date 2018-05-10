from fs import open_fs
import json
import re

DIR = "~/sublime-snippets/Snippets"

dictionary = {}

def extract_snippets(fs):
	count = 0
	for path in fs.walk.files(filter=['*.sublime-snippet']):
		pattern = re.compile("(?<=\/)(.*?)(?=\/)")
		category = pattern.search(path)
		category = subdir and subdir[0]
		print(subdir)
		with fs.open(path) as snippet:
			count += sum(1 for line in snippet if line.strip())

	return count

projects_fs = open_fs(DIR)
print(extract_snippets(projects_fs))