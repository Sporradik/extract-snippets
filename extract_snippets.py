from fs import open_fs
import json
import re
from pprint import pprint

SNIPPET_DIR = "~/sublime-snippets/Snippets"
OUTPUT_FILE = "snippets.json"

dictionary = {}

re_category = re.compile("(?<=\/)(.*?)(?=\/)")
re_name = re.compile("(?<=\/)([^\/]*?)(?=\.sublime-snippet)")
re_body = re.compile("(?<=<content><!\[CDATA\[)(.*?)(?=\]\]><\/content>)", re.S)
re_prefix = re.compile("(?<=<tabTrigger>)(.*?)(?=<\/tabTrigger>)")
re_description = re.compile("(?<=<description>)(.*?)(?=<\/description>)")

def extract_snippets(fs):
	for path in fs.walk.files(filter=['*.sublime-snippet']):
		category = re_category.search(path)
		category = category and category[0]
		dictionary[category] = dictionary.get(category, {})

		name = re_name.search(path)
		name = name and name[0]

		dictionary[category][name] = dictionary[category].get(name, {})

		dictionary[category]
		with fs.open(path) as snippet:
			file_contents = ""

			for line in snippet:
				 file_contents += line

			body = re_body.search(file_contents)
			body = body and body[0]
			dictionary[category][name]["body"] = [line for line in body.splitlines()]

			prefix = re_prefix.search(file_contents)
			prefix = prefix and prefix[0]
			dictionary[category][name]["prefix"] = prefix

			description = re_description.search(file_contents)
			description = description and description[0]

			dictionary[category][name]["description"] = description

	return dictionary

projects_fs = open_fs(SNIPPET_DIR)

data = extract_snippets(projects_fs)

with open(OUTPUT_FILE, 'w') as outfile:  
    json.dump(data, outfile, indent=4)