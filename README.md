# Smart Syllabus Analyzer

An intelligent tool that analyzes educational Syllabus and automatically generates comprehensive learning resources, including relevant video content recommendations.

## Features

- **PDF Text Extraction**: Converts PDF syllabus into processable text while maintaining structure
- **AI-Powered Analysis**: Uses Google's Gemini AI to extract and analyze educational content
- **Comprehensive Topic Breakdown**: 
  - Learning objectives
  - Key concepts
  - Practical applications
  - Related topics
  - Recommended resources
- **Smart Video Recommendations**: Automatically finds relevant educational videos for each topic
- **Structured Output**: Generates both JSON and human-readable text formats

## Prerequisites

```bash
pip install pymupdf4llm requests youtube-search
```

You'll also need:
- Google Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))
- Python 3.7+

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/ViralVadera/smart-syllabus-analyzer.git
cd smart-syllabus-analyzer
```

2. Install dependencies:
```bash
pip install pymupdf4llm requests youtube-searc
```

3. Set up your configuration:
- Replace `YOUR_API_KEY` in the code with your Gemini API key
- Update the `PDF_PATH` to point to your syllabus PDF

4. Run the analyzer:
```bash
python syllabus_analyzer.py
```

## Performance Disclaimer

Heads up: The analysis might take longer than you'd expect. The code isn't the fastest thing around (it's more like a tortoise than a hare), especially for large or complicated syllabi. So, it might be slow, but trust me, it'll be worth the wait.

## Output

The tool generates two types of output files:
1. `detailed_syllabus_content.json`: Structured data in JSON format
2. `detailed_syllabus_content.txt`: Human-readable formatted text

### Sample Output Structure

```json
{
  "topic": "Topic Name",
  "learning_objectives": ["objective1", "objective2", ...],
  "key_concepts": ["concept1", "concept2", ...],
  "practical_applications": ["application1", "application2", ...],
  "related_topics": ["topic1", "topic2", ...],
  "recommended_resources": ["resource1", "resource2", ...],
  "videos": [
    {
      "url": "video_url",
      "title": "video_title",
      "duration": "duration",
      "views": "view_count"
    }
  ]
}
```

## Error Handling

- Comprehensive error logging
- Automatic retries for API calls
- Rate limiting to prevent API throttling
- Robust PDF processing

## Best Practices

1. Use high-quality PDF syllabi with clear structure
2. Ensure good internet connectivity for video searches
3. Monitor the logs for any processing issues
4. Keep your API key secure
