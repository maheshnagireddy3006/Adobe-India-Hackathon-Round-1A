# Adobe India Hackathon Round 1A

# SmartPDF Insight is a tool that:

Extracts headings and organization from any PDF

Recognizes your persona (e.g., Analyst, Researcher)

Marks sections most important to your goals

Outputs clean, neat JSON files showing what to focus on

# Key Features:

Role-based relevance scoring

Handles multiple PDFs at once

Offline-capable (no internet necessary)

Fast, light, and simple to deploy (Python or Docker)

How It Works:

Reads PDF and detects headings using font and layout hints

Matches content to your persona and task

Ranks sections by priority

Outputs ordered outlines and a persona_analysis.json file

# Setup Options:

# Docker: Single line build an# Smart PDF Reader for Adobe Hackathon

Imagine you're drowning in PDF documents and need to quickly find what's important for YOUR specific job. That's exactly what this tool solves!

Here's what it does in simple terms:
- **Reads your PDFs** and figures out the main headings and structure (like a table of contents)
- **Understands your role** - whether you're an analyst, researcher, student, etc.
- **Finds what matters to YOU** - it looks through all the content and highlights sections that are relevant to your specific job
- **Gives you organized results** - everything is saved in easy-to-read files that show you exactly what to focus on

## The Magic Behind It

The tool is pretty smart about how it works:

1. **It reads your PDFs** - Uses a Python library to scan through PDF files and understand their structure
2. **It identifies important parts** - Looks at font sizes and bold text to figure out what are titles, headings, and subheadings
3. **It gets to know you** - You tell it who you are (like "Investment Analyst") and what you're trying to do (like "find financial trends")
4. **It matches content to your needs** - The tool scores each section based on how relevant it is to your role and goals
5. **It organizes everything** - Creates neat files showing you what's most important, ranked by relevance

## How to Use This Tool

### The Easy Way (Using Docker)
If you have Docker installed, this is the simplest approach:

```bash
# First, build the tool
docker build --platform linux/amd64 -t pdfanalyzer .

# Then run it (it will process all PDFs in your input folder)
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdfanalyzer
```

### The Direct Way (Using Python)
If you prefer to run Python directly:

```bash
# Install the PDF reading library
pip install pymupdf

# Run the tool
python python.py
```

### How to Tell the Tool About Yourself

The tool needs to know who you are and what you're trying to accomplish. You have three ways to do this:

#### Way 1: Create a Config File (Easiest)
Create a file called `persona_config.json` in your `input` folder:
```json
{
  "persona": "Investment Analyst",
  "job_to_be_done": "Find financial trends and investment opportunities"
}
```

#### Way 2: Use Environment Variables
```bash
export PERSONA="Research Analyst"
export JOB_TO_BE_DONE="Extract key research methodologies"
python python.py
```

#### Way 3: Pass Arguments When Running
```bash
python python.py "Data Scientist" "Find datasets and statistical methods"
```

## What You Get Back

### For Each PDF Document
The tool creates a file for each PDF showing its structure:

```json
{
  "title": "Annual Financial Report 2023",
  "outline": [
    {"level": "H1", "text": "Executive Summary", "page": 1},
    {"level": "H2", "text": "Revenue Growth", "page": 3},
    {"level": "H3", "text": "Q4 Performance", "page": 5}
  ]
}
```

This basically gives you a smart table of contents with page numbers!

### The Smart Analysis File
This is where the magic happens - a file called `persona_analysis.json` that shows you exactly what matters:

```json
{
  "metadata": {
    "input_documents": ["financial_report.pdf", "market_analysis.pdf"],
    "persona": "Investment Analyst",
    "job_to_be_done": "Find investment opportunities",
    "processing_timestamp": "2024-01-27T12:00:00"
  },
  "extracted_sections": [
    {
      "document": "financial_report.pdf",
      "page_number": 12,
      "section_title": "Growth Projections",
      "importance_rank": 1
    }
  ]
}
```

### What Makes This Smart?
- **It understands context** - Matches your role and goals with document content
- **It ranks by importance** - Shows you the most relevant sections first
- **It works with multiple documents** - Processes all your PDFs at once
- **It keeps track** - Records when it was processed and with what settings

## Why This Tool is Great

- **Works with any PDF** - Doesn't matter what kind of document it is
- **No internet needed** - Everything runs on your computer, completely private
- **Super fast** - Uses a lightweight library that processes documents quickly
- **Flexible setup** - Multiple ways to configure it based on your preferences
- **Easy to deploy** - Works with Docker if you want to run it anywhere
- **Handles multiple files** - Drop in a bunch of PDFs and it processes them all
- **Clean results** - Gives you organized data you can easily work with

## Technical Details (For the Developers)

- **Built with:** Python 3.10 or newer
- **PDF processing:** Uses PyMuPDF (also called 'fitz') - it's fast and reliable
- **Dependencies:** Just one - PyMuPDF. That's it!
- **Docker:** Runs on linux/amd64 platform
- **Hardware:** Only needs CPU, no fancy GPU required
- **What goes in:** PDF files
- **What comes out:** JSON files with all the analysis

## Getting Started

1. **Put your PDFs** in the `input` folder
2. **Tell the tool about yourself** using one of the three methods above
3. **Run the tool** using Docker or Python
4. **Check the `output` folder** for your resultsd run

# Python: Direct run with pymupdf

Customize your role through JSON file, env variables, or CLI arguments

# Ideal For:

Analysts pulling out insights from reports

Researchers finding methodologies

Students summarizing study texts