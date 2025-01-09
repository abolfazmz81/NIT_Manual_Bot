import fitz
import re
import tiktoken


def return_doc(pdf_path):
    def extract_text(pdf_path):
        doc = fitz.open(pdf_path)
        all_text = ""
        for page_num in range(len(doc)):
            # Skip the first two pages
            if page_num < 2:
                continue

            page = doc[page_num]
            blocks = page.get_text()
            blocks = re.sub(r"""دانشگاه صنعتي نوشيرواني بابل  
آئين نامه آموزشي دوره كارشناسي  
 ويژه دانشجويان كارشناسي ورودي سال
٧٩٣١ و پس از آن""", "", blocks)
            all_text = all_text + blocks

        return all_text

    # Example usage
    text = extract_text(pdf_path)

    def split_into_sections_and_subsections(text):
        # Define the regex pattern for sections and subsections
        pattern = r"(?=\d+-\s)"  # Matches numbers followed by a dash (e.g., "1- ") or "1-1- "

        # Split the text using the pattern
        chunks = re.split(pattern, text)

        # Process the chunks to map them into sections and subsections
        sections = {}
        current_section = None
        current_subsection = None

        for chunk in chunks:
            chunk = chunk.strip()  # Remove leading/trailing whitespace
            if re.match(r"^\d+-\s", chunk):  # Match "1-" (section)
                current_section = chunk
                sections[current_section] = {}
                current_subsection = None  # Reset subsection
            elif re.match(r"^\d+-\d+-\s", chunk):  # Match "1-1-" (subsection)
                if current_section:
                    current_subsection = chunk
                    sections[current_section][current_subsection] = []
            else:  # Treat as content
                if current_subsection:
                    sections[current_section][current_subsection].append(chunk)
                elif current_section:
                    sections[current_section]["content"] = sections[current_section].get("content", []) + [chunk]

        # Format the content into clean strings
        for section, content in sections.items():
            if "content" in content:
                content["content"] = " ".join(content["content"])
            for subsection, texts in content.items():
                if isinstance(texts, list):
                    content[subsection] = " ".join(texts)

        return sections

    sections = split_into_sections_and_subsections(text)

    def count_tokens(text):
        encoding = tiktoken.encoding_for_model("gpt-4o-mini-2024-07-18")
        return len(encoding.encode(text))

    def ensure_token_limit(sections, max_tokens=128000):
        valid_sections = []
        for section in sections:
            if count_tokens(section) <= max_tokens:
                valid_sections.append(section)
            else:
                print(f"Section exceeds token limit: {section[:50]}...")
        return valid_sections

    # Ensure token limits for the sections
    valid_sections = ensure_token_limit(sections)
    print(count_tokens(text))
    return text

