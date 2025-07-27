import os
import json
import datetime
import sys
import fitz  

def extract_outline(pdf_path):
    """Extract title and headings (H1/H2/H3) using font size and boldness."""
    try:
        doc = fitz.open(pdf_path)
        blocks = []
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_dict = page.get_text("dict")
            
            for block in page_dict["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if text:  
                                blocks.append({
                                    "text": text,
                                    "size": span["size"],
                                    "bold": "Bold" in span["font"],
                                    "page": page_num + 1,
                                    "x0": span["bbox"][0],
                                    "x1": span["bbox"][2]
                                })
        
        doc.close()
        
        if not blocks:
            return {"title": "", "outline": []}
        
        sizes = sorted(list(set(b["size"] for b in blocks)), reverse=True)
        
        title = ""
        outline = []
       
        for block in blocks:
            if block["bold"] and block["text"]:
                if (block["size"] == sizes[0] and 
                    not title and 
                    len(sizes) > 0):
                    title = block["text"]
                    continue
                if block["size"] == sizes[0]:
                    outline.append({"level": "H1", "text": block["text"], "page": block["page"]})
                elif len(sizes) > 1 and block["size"] == sizes[1]:
                    outline.append({"level": "H2", "text": block["text"], "page": block["page"]})
                elif len(sizes) > 2 and block["size"] == sizes[2]:
                    outline.append({"level": "H3", "text": block["text"], "page": block["page"]})
        
        return {"title": title, "outline": outline}
        
    except Exception as e:
        print(f"Error processing {pdf_path}: {str(e)}")
        return {"title": "", "outline": []}

def get_directories():
    """Get input and output directories based on environment."""
    if os.path.exists("/app/input"):
        return "/app/input", "/app/output"
    else:
        return "input", "output"

def process_pdfs_to_json():
    """Process all PDFs in input directory and generate JSON files in output directory."""
    input_dir, output_dir = get_directories()
    os.makedirs(output_dir, exist_ok=True)
    if os.path.exists(input_dir):
        for filename in os.listdir(input_dir):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(input_dir, filename)
                json_filename = filename.replace('.pdf', '.json')
                json_path = os.path.join(output_dir, json_filename)
                
                print(f"Processing {filename}...")
                outline_data = extract_outline(pdf_path)
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(outline_data, f, indent=2, ensure_ascii=False)
                
                print(f"Generated {json_filename}")
    else:
        print(f"Input directory {input_dir} not found")

def score_section(text, keywords):
    """Score a section by keyword matches."""
    if not text or not keywords:
        return 0
    text_lower = text.lower()
    return sum(1 for kw in keywords if kw in text_lower)

def read_persona_config():
    """Read persona and job configuration from various sources."""
    persona = None
    job = None
    input_dir, _ = get_directories()
    config_path = os.path.join(input_dir, "persona_config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                persona = config.get("persona", "")
                job = config.get("job_to_be_done", "")
                print(f"Loaded persona config from {config_path}")
        except Exception as e:
            print(f"Error reading config file: {e}")
    
    if not persona:
        persona = os.environ.get("PERSONA", "")
    if not job:
        job = os.environ.get("JOB_TO_BE_DONE", "")
    if not persona and len(sys.argv) > 1:
        persona = sys.argv[1]
    if not job and len(sys.argv) > 2:
        job = sys.argv[2]
    if not persona:
        persona = "Research Analyst"
    if not job:
        job = "Extract key insights and methodologies from technical documents"
    
    return persona, job

def generate_persona_analysis():
    """Generate persona-driven analysis from extracted outlines."""
    persona, job = read_persona_config()
    
    print(f"Using persona: {persona}")
    print(f"Job to be done: {job}")
    
    keywords = [word.lower() for word in (persona + " " + job).split() if len(word) > 2]
    
    result = {
        "metadata": {
            "input_documents": [],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.datetime.now().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }
    
    _, output_dir = get_directories()
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            if filename.endswith(".json"):
                json_path = os.path.join(output_dir, filename)
                
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        outline_data = json.load(f)
                    
                    pdf_name = filename.replace(".json", ".pdf")
                    result["metadata"]["input_documents"].append(pdf_name)
                    scored_sections = []
                    for item in outline_data.get("outline", []):
                        score = score_section(item["text"], keywords)
                        if score > 0:
                            scored_sections.append((score, item))
                    
                    scored_sections.sort(key=lambda x: x[0], reverse=True)
                    for rank, (score, item) in enumerate(scored_sections, 1):
                        result["extracted_sections"].append({
                            "document": pdf_name,
                            "page_number": item["page"],
                            "section_title": item["text"],
                            "importance_rank": rank
                        })
                        
                        result["subsection_analysis"].append({
                            "document": pdf_name,
                            "refined_text": item["text"],
                            "page_number": item["page"]
                        })
                        
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")
    persona_output_path = os.path.join(output_dir, "persona_analysis.json")
    with open(persona_output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Generated persona analysis: {persona_output_path}")

def main():
    """Main function to process PDFs and generate analysis."""
    print("Starting PDF processing...")
    process_pdfs_to_json()
    generate_persona_analysis()
    print("Processing complete!")

if __name__ == "__main__":
    main()