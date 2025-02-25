import os
from pathlib import Path
import pprint
import typer
from fpcli.function.check_class import check_class
from ..fpcli_settings import APP_FOLDER,API_KEY


def find_files_by_keyword(app_name, keyword):
    """Finds all files related to a given keyword in the app folder."""
    base_path = Path(f"{APP_FOLDER}/{app_name}").resolve()
    urls_file = f"{base_path}/urls.py"
    matched_files = []
    matched_files.append(urls_file)
    for root, _, files in os.walk(base_path):
        for file in files:
            if keyword in file:
                matched_files.append(os.path.join(root, file))
    return matched_files


def read_files(file_paths):
    """Reads and returns content of all given files."""
    content = {}
    for file in file_paths:
        with open(file, "r", encoding="utf-8") as f:
            content[file] = f.read()
    return content


def send_to_google_api(content):
    import requests
    import json

    URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"generate the unit testing code for fastapi routes you can assume the routes accroding to the given view name example-> if the view name is the permission then you and assume the route route resource is the permissions for [GET,POST,PUT,DELETE]  accroding to the my given content {content}  don't add any extra explaination i wana only code  also remove  "
                    }
                ],
            }
        ],
        "generationConfig": {
            "temperature": 2,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 8192,
            "responseMimeType": "text/plain",
        },
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")


def write_file(app_name: str, name: str, content: str):
    app_dir = Path(f"{APP_FOLDER}/{app_name}").resolve()

    services_dir = app_dir / "tests"
    # Capitalize the service name and generate file name
    class_name = f"{name.capitalize()}Test"
    file_name = f"{name.lower()}_test.py"
    file_path = services_dir / file_name

    # Check if the service file already exists
    check_class(file_path=file_path, app_name=app_name, class_name=class_name)

    # Service boilerplate content

    # Ensure the services directory exists
    services_dir.mkdir(parents=True, exist_ok=True)
    content = content
    # Write the service file
    file_path.write_text(content)
    typer.echo(f"Service '{class_name}' created successfully in '{file_path}'!")


def test_file_processing(app_name, keyword):
    files = find_files_by_keyword(app_name, keyword)

    pprint.pprint(files)

    content = read_files(files)

    response = send_to_google_api(content)

    content: str = response["candidates"][0]["content"]["parts"][0]["text"]
    content = content.replace("```python", "")
    content = content.replace("```", "")
    write_file(app_name=app_name, name=keyword, content=content)
