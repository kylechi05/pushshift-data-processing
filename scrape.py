from datetime import datetime
import sys
import os
import json
import csv

def main(input_file_path, output_file_path):
    fields = ["author", "created_at", "title", "content"]

    output_file = open(f"{output_file_path}.csv", "w", encoding="utf8", newline="")
    writer = csv.writer(output_file, escapechar='\\')
    writer.writerow(fields)

    with open(input_file_path, "r", encoding="utf8") as file:
        for _, line in enumerate(file):
            try:
                reddit = json.loads(line)
                output_data = []
                for field in fields:
                    if field == "author":
                        if 'author' in reddit:
                            value = f"u/{reddit['author']}"
                        else:
                            value = ""
                    elif field == "created_at":
                        if "created_utc" in reddit:
                            value = datetime.fromtimestamp(int(reddit['created_utc'])).strftime("%Y-%m-%d %H:%M")
                        else:
                            value = ""
                    elif field == "title":
                        if "title" in reddit:
                            value = reddit["title"]
                            value = ' '.join(value.splitlines())
                        else:
                            value = ""
                    elif field == "content":
                        if 'selftext' in reddit:
                            value = reddit['selftext']
                            value = ' '.join(value.splitlines())
                        else:
                            value = ""
    
                    output_data.append(str(value).encode("utf-8", errors='replace').decode())
                writer.writerow(output_data)
            except json.JSONDecodeError:
                continue
    output_file.close()

if __name__ == '__main__':
    input_file_dir = "" # input file dir
    output_file_dir = "" # output file dir
    input_file_path = os.path.join(input_file_dir, sys.argv[1])
    output_file_path = os.path.join(output_file_dir, sys.argv[1])
    main(input_file_path, output_file_path)