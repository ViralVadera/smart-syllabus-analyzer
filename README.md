# smart-syllabus-analyzer

An advanced tool that processes academic syllabi to extract technical topics, generate comprehensive descriptions, and find relevant educational videos. The tool uses Google's Gemini API for content generation and YouTube search for finding related tutorials.

## Features

- Extracts technical topics from PDF syllabi using intelligent content analysis
- Generates detailed technical descriptions for each identified topic
- Finds relevant tutorial videos from YouTube for each topic
- Processes content asynchronously for improved performance
- Exports results in structured JSON format

## Prerequisites

```bash
pip install aiohttp youtube-search pymupdf4llm
```

You'll also need:
- Google Gemini API key
- Python 3.7+

## Usage

```python
from syllabus_processor import SyllabusProcessor

processor = SyllabusProcessor(api_key="your_gemini_api_key")
results = processor.process_syllabus("path/to/your/syllabus.pdf")
processor.save_results(results, "output_filename")
```

## Output Format

The tool generates a JSON file with the following structure:

```json
[
  {
    "topic": "Topic Name",
    "description": "Comprehensive description...",
    "videos": [
      {
        "url": "YouTube video URL",
        "title": "Video title",
        "duration": "Video duration",
        "views": "View count"
      }
    ]
  }
]
```

## Key Components

### SyllabusProcessor

The main class that orchestrates the processing pipeline:

- `query_gemini()`: Makes API calls to Google's Gemini model with retry logic
- `get_topic_description()`: Generates detailed technical descriptions for topics
- `get_videos()`: Searches and retrieves relevant YouTube tutorials
- `process_topic()`: Combines topic description and video search functionality
- `process_all()`: Handles parallel processing of multiple topics
- `save_results()`: Exports processed data to JSON format

### Data Classes

- `VideoContent`: Stores information about YouTube tutorials
- `TopicContent`: Organizes topic information including descriptions and related videos

## Error Handling

The tool implements:
- Retry logic for API calls
- Rate limiting protection
- Parallel processing with timeout protection
- Comprehensive error logging

## Limitations

- Requires a valid Google Gemini API key
- YouTube search results are limited to 5 videos per topic
- Processing time depends on the number of topics and API response times

## Example

```python
def main():
    PDF_PATH = "path/to/syllabus.pdf"
    API_KEY = "your_gemini_api_key"
    
    processor = SyllabusProcessor(API_KEY)
    results = processor.process_syllabus(PDF_PATH)
    
    if results:
        processor.save_results(results, "technical_syllabus_content")
```

## Contributing

Feel free to submit issues and enhancement requests!
