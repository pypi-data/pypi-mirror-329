# ParseThis

![Coverage](./coverage.svg)
![PyPI](https://img.shields.io/pypi/v/ParseThis)
![Build Status](https://img.shields.io/github/workflow/status/jdde/ParseThis/CI)
![License](https://img.shields.io/github/license/jdde/ParseThis)


**ParseThis** is a powerful and flexible, tool with zero additional OS dependencies, that makes raw data effortlessly readable and structured for your AI and data processing workflows. Whether you're extracting information from PDFs, transforming files into Markdown or preparing data for LLMs and RAG pipelines, **ParseThis** gets the job done—quickly, effectively, and with a touch of magic.
Just install as a pip package and enjoy, no configuring around with third party tools before you can use this package. Just parseThis.

For some parsers there are API Key's required. They're not required, when you just dont use them - they will error on usage when no api key was found.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [ParserMatrix - Dependency overview](#ParserMatrix)


---

## Features
- Auto-detects file types (PDF, DOCX, CSV, and more).
- Converts files into readable Markdown or plain text.
- Extracts structured data for use in LLM and RAG pipelines.
- Simple API for seamless integration into your workflows.

The mapping of parser to file type can be found in the [ParserMatrix](#parsermatrix---when-is-which-dependency-used).

---

## Prerequisites
Use Python 3.12 - maximum version supported by PyO3 - dependency of scrapegraph-ai, use a virtual environment with version 3.12
```sh
python3.12 -m venv myenv
source myenv/bin/activate
```

---

## Installation

To install **ParseThis**, use pip:

```bash
pip install parsethis
```
For more information, see the [how we install in our github action](.github/workflows/coverage.yml).

---

### Usage
Use the parse() function to auto-detect the current type of content - when the autodetection is not working you can provide more information to help detect the type.
The auto-parse function accepts any input - file_path, url strings, file byte content.
```python
import parsethis

#extract image description for llm
with open('tests/fixtures/test_data_diagram.png', 'rb') as f:
    image_description = parsethis.parse(f.read(), result_format=ResultFormat.TXT)

#get transcript of audio
with open('tests/fixtures/test_data_ttsmaker-test-generated-file.mp3', 'rb') as f:
    audio_transcript = parsethis.parse(f.read(), result_format=ResultFormat.TXT)
```

The generic parse() function detects automatically which parsers will be used based on the file content.

```python
import parsethis

from parsethis import ResultFormat


#automatic parse based on file_path
parsed_pdf_text = parsethis.parse('tests/fixtures/text_data_meeting_notes.pdf', result_format=ResultFormat.TXT)

#automatic parse based on file content
with open('tests/fixtures/text_data_meeting_notes.pdf', 'rb') as f:
    parsed_pdf_text = parsethis.parse(f.read(), result_format=ResultFormat.TXT)  # works with any bytes content

#automatic parse based on string
parsed_github_repository = parsethis.parse('https://github.com/jdde/ParseThis', result_format=ResultFormat.TXT)

#automatic parse based on YouTube URL
transcribed_youtube_text = parsethis.parse('https://www.youtube.com/watch?v=ca7QkcAGe', result_format=ResultFormat.TXT)
```

Use the parser detection when you want to just find the parser and configure it differently before it parses the content.
```python
import parsethis

with open('tests/fixtures/text_data_meeting_notes.pdf', 'rb') as f:
    file_content = f.read()
    parser = parsethis.get_parser(file_content)
    text = parser.parse(file_content)
```

Or just directly use a any parser.
```python
from parsethis import PDFParser

with open('tests/fixtures/text_data_meeting_notes.pdf', 'rb') as f:
    text = PDFParser.parse(file_content)
```

For more examples how to use it - see our [testing section](tests/test_automatic_parsing.py).

---

## ParserMatrix
Overview of dependencies used for specific parsing processes.

| File Type | Parser         | Dependency          | External Access Required |
|-----------|----------------|---------------------|---------------------|
| PDF       | PDFParser      | PyPDF2, Markitdown | ❌ |
| Image     | ImageParser    | OpenAI GPT         | ✅ env.OPENAI_API_KEY|
| Audio     | AudioParser    | OpenAI Whisper     | ✅ env.OPENAI_API_KEY |
| URL       | TextParser     | scrapegraphai      | ✅ env.OPENAI_API_KEY |
| YouTube   | TextParser  | youtube-transcript-api | ❌ |
| Github    | TextParser     | gitingest          | ❌ |
| DOCX      | OfficeParser   | Markitdown         | ❌ |
| PPTX      | OfficeParser   | Markitdown         | ❌ |
| XLSX/XLS  | OfficeParser   | Markitdown         | ❌ |
| CSV       | DataParser     | Markitdown         | ❌ |
| JSON      | DataParser     | Markitdown         | ❌ |
| XML       | DataParser     | Markitdown         | ❌ |
| ZIP       | ArchiveParser  | Markitdown         | ❌ |


If you're working with the source code, you can install all dependencies using:

```bash
pip install -r requirements.txt
```


## Testing
To execute tests use this:

```bash
coverage run -m pytest
#or for a single test:
pytest -k test_text_parser_github_url
```


## License
This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
