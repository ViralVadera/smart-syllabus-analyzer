import asyncio
import aiohttp
import logging
from typing import List
from dataclasses import dataclass
import json
from youtube_search import YoutubeSearch
import pymupdf4llm
from concurrent.futures import ThreadPoolExecutor
from functools import partial

@dataclass
class VideoContent:
    url: str
    title: str
    duration: str
    views: str

@dataclass
class TopicContent:
    topic: str
    description: str
    videos: List[VideoContent]

class SyllabusProcessor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        self.executor = ThreadPoolExecutor(max_workers=10)

    async def query_gemini(self, session: aiohttp.ClientSession, prompt: str) -> str:
        max_retries = 3
        base_delay = 1  # seconds

        for attempt in range(max_retries):
            try:
                async with session.post(
                    self.gemini_url,
                    json={
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {
                            "temperature": 0.1,
                            "maxOutputTokens": 8192
                        }
                    },
                    timeout=30
                ) as response:
                    if response.status == 429:
                        delay = base_delay * (2 ** attempt)
                        await asyncio.sleep(delay)
                        continue
                        
                    data = await response.json()
                    return data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                    
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(base_delay * (2 ** attempt))
                
        return ""

    async def get_topic_description(self, session: aiohttp.ClientSession, topic: str) -> str:
        """Get a detailed description for a specific topic."""
        description_prompt = f"""Provide a comprehensive technical description of '{topic}' in 5-7 lines.
        Focus on:
        - Key concepts and fundamentals
        - Important applications and use cases
        - Technical challenges and considerations
        - Best practices and common patterns
        - Real-world relevance

        Make it educational and suitable for a technical course syllabus."""

        description = await self.query_gemini(session, description_prompt)
        print(description)
        logging.info(f"Generated description for {topic}: {description[:100]}...")  # Log first 100 chars
        
        if not description:
            logging.warning(f"Failed to get description for topic: {topic}")
            description = f"Description generation failed for {topic}"
            
        return description.strip()

    def get_videos(self, topic: str) -> List[VideoContent]:
        try:
            results = YoutubeSearch(f"tutorial {topic}", max_results=5).to_dict()
            return [VideoContent(
                url=f"https://youtube.com{r['url_suffix']}",
                title=r['title'],
                duration=r['duration'],
                views=r.get('views', 'N/A')
            ) for r in results]
        except Exception:
            return []

    async def process_topic(self, session: aiohttp.ClientSession, topic: str) -> TopicContent:
        # Get description for the topic
        description = await self.get_topic_description(session, topic)
        # Get videos in parallel
        videos = await asyncio.get_event_loop().run_in_executor(
            self.executor, 
            partial(self.get_videos, topic)
        )
        
        return TopicContent(
            topic=topic,
            description=description,
            videos=videos
        )

    async def process_all(self, pdf_path: str) -> List[TopicContent]:
        text = pymupdf4llm.to_markdown(pdf_path)
        topic_prompt = """Analyze this text and extract ALL technical topics being taught.
                        Ignore headings, sections, or administrative text.
                        Each topic should be a specific concept or skill.
                        List each topic on a new line starting with 'Topic:'.
                        
                        Rules:
                        - Extract every possible topic, even if briefly mentioned
                        - Break down composite topics into individual components
                        - Exclude course logistics, grading policies, or administrative text
                        - Focus on actual learning content
                        - Each topic should be granular - break larger topics into specific sub-topics
                        """
    
        async with aiohttp.ClientSession() as session:
            topics_text = await self.query_gemini(session, f"{topic_prompt}\n\nText to analyze:\n{text}")
            
            # Extract topics
            topics = []
            for line in topics_text.split('\n'):
                if line.startswith('Topic:'):
                    topic = line.replace('Topic:', '').strip()
                    if topic:
                        topics.append(topic)

            # Process each topic in parallel
            tasks = [
                self.process_topic(session, topic)
                for topic in topics
            ]
            return await asyncio.gather(*tasks)

    def process_syllabus(self, pdf_path: str) -> List[TopicContent]:
        return asyncio.run(self.process_all(pdf_path))

    def save_results(self, results: List[TopicContent], output_path: str):
        with open(f"{output_path}.json", "w") as f:
            json.dump([{
                "topic": r.topic,
                "description": r.description,
                "videos": [vars(v) for v in r.videos]
            } for r in results], f, indent=2)

def main():
    PDF_PATH = "path/to/syllabus.pdf"
    API_KEY = "your_gemini_api_key"
    processor = SyllabusProcessor(API_KEY)
    if results := processor.process_syllabus(PDF_PATH):
        processor.save_results(results, "syllabus_content")
    else:
        logging.warning("No results generated")

if __name__ == "__main__":
    main()
