from fs import open_fs
import json
import re

DIR = "~/sublime-snippets/Snippets"

dictionary = {}

re_category = re.compile("(?<=\/)(.*?)(?=\/)")
re_body = re.compile("(?<=<content><!\[CDATA\[)(.*?)(?=\]\]><\/content>)", re.S)
re_prefix = re.compile ("(?<=<tabTrigger>)(.*?)(?=<\/tabTrigger>)")

def extract_snippets(fs):
	# count = 0
	for path in fs.walk.files(filter=['*.sublime-snippet']):
		category = re_category.search(path)
		category = category and category[0]
		print(category)
		with fs.open(path) as snippet:
			file_contents = ""
			for line in snippet:
				file_contents += line
			body = re_body.search(file_contents)
			body = body and body[0]
			print(body)

projects_fs = open_fs(DIR)
extract_snippets(projects_fs)