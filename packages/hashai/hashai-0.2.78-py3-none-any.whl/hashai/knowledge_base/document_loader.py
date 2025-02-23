import os
import json
import csv
import re
from pathlib import Path
from typing import List, Dict, Any
from io import BytesIO

import requests
from bs4 import BeautifulSoup

# Optional: Import pandas for XLSX and PyPDF2 for PDF support
try:
    import pandas as pd
except ImportError:
    pd = None

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None


class DynamicDocumentLoader:
    """
    A dynamic document loader that supports multiple source types:
    
    - Local files: CSV, TXT, JSON, XLSX, PDF
    - URL sources: Web pages (HTML), JSON APIs, PDF URLs
    - YouTube links: Extracts transcripts via youtube_transcript_api

    Additional formats (e.g., DOCX, Markdown) can be added following the same pattern.
    """

    def load(self, source: str) -> List[Dict[str, Any]]:
        """
        Dynamically load documents from a given source. If the source is a URL,
        it uses load_from_url; otherwise, it treats it as a local file.
        """
        if source.startswith("http"):
            return self.load_from_url(source)
        else:
            return self.load_from_file(source)

    def load_from_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load a document from a local file path.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = path.suffix.lower()
        if ext == ".json":
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Ensure the result is a list of documents
                return data if isinstance(data, list) else [data]
        elif ext == ".txt":
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                return [{"text": content}]
        elif ext == ".csv":
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return [row for row in reader]
        elif ext == ".xlsx":
            if pd is None:
                raise ImportError("pandas is required to load XLSX files")
            df = pd.read_excel(path)
            return df.to_dict(orient="records")
        elif ext == ".pdf":
            if PdfReader is None:
                raise ImportError("PyPDF2 is required to load PDF files")
            reader = PdfReader(str(path))
            content = ""
            for page in reader.pages:
                content += page.extract_text() or ""
            return [{"text": content}]
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def load_from_url(self, url: str) -> List[Dict[str, Any]]:
        """
        Load a document from a URL. Supports:
        
        - YouTube links (transcript extraction)
        - JSON APIs
        - HTML websites (text extraction)
        - PDF URLs
        """
        # Handle YouTube links separately
        if "youtube.com" in url or "youtu.be" in url:
            return self._load_youtube(url)

        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch data from URL: {url}")

        content_type = response.headers.get("Content-Type", "").lower()
        if "application/json" in content_type:
            data = response.json()
            return data if isinstance(data, list) else [data]
        elif "text/html" in content_type:
            soup = BeautifulSoup(response.text, "html.parser")
            # Extract text; you might want to refine this extraction
            text = soup.get_text(separator="\n")
            return [{"text": text}]
        elif "application/pdf" in content_type:
            if PdfReader is None:
                raise ImportError("PyPDF2 is required to load PDF files")
            pdf_file = BytesIO(response.content)
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return [{"text": text}]
        else:
            # Fallback: treat content as plain text
            return [{"text": response.text}]

    def _load_youtube(self, url: str) -> List[Dict[str, Any]]:
        """
        Load transcript text from a YouTube video using youtube_transcript_api.
        Make sure to install the package:
            pip install youtube_transcript_api
        """
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
        except ImportError:
            raise ImportError("youtube_transcript_api is required to load YouTube transcripts")

        # Extract the video ID from various URL formats
        video_id = None
        patterns = [r"v=([^&]+)", r"youtu\.be/([^?&]+)"]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                break

        if not video_id:
            raise ValueError("Could not extract video ID from URL")

        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # Combine transcript segments into a single text blob
        text = " ".join(segment["text"] for segment in transcript)
        return [{"text": text}]
