from fs import open_fs
import json
import re

SNIPPET_DIR = "~/sublime-snippets/Snippets"
OUTPUT_FILE = "snippets.json"

re_category = re.compile("(?<=\/)(.*?)(?=\/)")
re_name = re.compile("(?<=\/)([^\/]*?)(?=\.sublime-snippet)")
re_body = re.compile("(?<=<content><!\[CDATA\[)(.*?)(?=\]\]><\/content>)", re.S)
re_prefix = re.compile("(?<=<tabTrigger>)(.*?)(?=<\/tabTrigger>)")
re_description = re.compile("(?<=<description>)(.*?)(?=<\/description>)")

def extract_snippets(fs):
	dictionary = {}

	for path in fs.walk.files(filter=['*.sublime-snippet']):
		category = re_category.search(path)
		category = category and category[0]
		dictionary[category] = dictionary.get(category, {})

		name = re_name.search(path)
		name = name and name[0]

		dictionary[category][name] = dictionary[category].get(name, {})

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

for key, value in data.items():
	print(key)
	for k in sorted(value.keys(), key=lambda x:x.lower()):
		pfx = value[k]["prefix"]
		desc = value[k]["description"]
		print(f"    {pfx} -- {desc}")

with open(OUTPUT_FILE, 'w') as outfile:  
    json.dump(data, outfile, indent=4)
