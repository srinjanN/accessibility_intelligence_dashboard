"""
AI Simplifier & Persona Rewriter Service.
Integrates Gemini API with smart offline rule-based fallback.
Supports 6 Audience Personas:
1. Plain English
2. Dyslexia-Friendly
3. ADHD-Friendly
4. Elderly-Friendly
5. Child-Friendly
6. Inclusive Language
"""

import os
import re
from typing import Dict, Any

def get_gemini_client():
    """Attempt to initialize Gemini client if API key is present."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
        
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        return client
    except Exception:
        try:
            import google.generativeai as genai_legacy
            genai_legacy.configure(api_key=api_key)
            return genai_legacy
        except Exception:
            return None

def simplify_text_gemini(text: str, persona: str, model_name: str = "gemini-2.5-flash") -> str:
    """Use Gemini API to simplify and rewrite text based on requested persona."""
    client = get_gemini_client()
    if not client:
        return simplify_text_offline(text, persona)
        
    prompt = f"""
You are an expert accessibility consultant and plain language editor. 
Your task is to rewrite the following input text specifically for the persona: **{persona}**.

Persona Guidelines:
- Plain English: Use simple vocabulary, active voice, short sentences, and direct statements.
- Dyslexia-Friendly: Use clear formatting, bullet points, short paragraphs (max 2 sentences), and simple words.
- ADHD-Friendly: Use bite-sized bullet lists, **bold key terms**, actionable headings, and concise steps.
- Elderly-Friendly: Use clear step-by-step instructions, plain non-jargon language, and explicit explanations.
- Child-Friendly: Use simple words (Grade 3-5 reading level), short sentences, friendly tone, and clear examples.
- Inclusive Language: Use gender-neutral, accessible, respectful, non-ableist terms throughout.

Original Text:
\"\"\"
{text}
\"\"\"

Output ONLY the rewritten simplified text without extra conversational preamble.
"""
    try:
        if hasattr(client, "models"):
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            return response.text.strip()
        elif hasattr(client, "GenerativeModel"):
            model = client.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return response.text.strip()
    except Exception:
        pass
        
    return simplify_text_offline(text, persona)

def simplify_text_offline(text: str, persona: str) -> str:
    """Offline rule-based NLP text simplifier fallback."""
    if not text:
        return ""
        
    # Replace complex jargon dictionary
    jargon_map = {
        "indemnify": "protect from legal loss",
        "indemnification": "protection from loss",
        "pursuant to": "following",
        "notwithstanding": "despite",
        "aforementioned": "mentioned earlier",
        "heretofore": "before now",
        "alimentary": "food and drink",
        "pharmacotherapy": "medication",
        "antihypertensive": "blood pressure medication",
        "anesthesiologic": "anesthesia",
        "ambulatory": "outpatient / walk-in",
        "pulmonary": "lung",
        "gastric": "stomach",
        "imperative": "important",
        "precipitate": "cause",
        "click here": "select this link",
        "read more": "read details",
        "submit": "send",
        "whitelist": "allowlist",
        "blacklist": "blocklist",
        "master/slave": "primary/secondary",
        "manpower": "staffing / workforce",
        "he/she": "they"
    }
    
    simplified = text
    for term, replacement in jargon_map.items():
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        simplified = pattern.sub(replacement, simplified)
        
    # Convert passive phrasing patterns to active voice markers
    simplified = re.sub(r'\bIt is recommended that patients\b', 'Patients should', simplified, flags=re.IGNORECASE)
    simplified = re.sub(r'\bIt is imperative that you\b', 'You must', simplified, flags=re.IGNORECASE)

    # Split into clean sentences
    raw_sents = re.split(r'(?<=[.!?])\s+', simplified)
    cleaned_sents = [s.strip() for s in raw_sents if s.strip()]
    
    persona_lower = persona.lower()
    
    if "dyslexia" in persona_lower:
        # Short paragraphs, bullet list
        formatted = ["### Dyslexia-Friendly Summary\n"]
        for s in cleaned_sents:
            formatted.append(f"• {s}")
        return "\n\n".join(formatted)
        
    elif "adhd" in persona_lower:
        # Bold key words and bite-sized steps
        formatted = ["### Action Steps (ADHD-Friendly)\n"]
        for i, s in enumerate(cleaned_sents, 1):
            words = s.split()
            if len(words) > 3:
                words[0] = f"**{words[0]}**"
                words[1] = f"**{words[1]}**"
            formatted.append(f"**Step {i}**: {' '.join(words)}")
        return "\n\n".join(formatted)
        
    elif "elderly" in persona_lower:
        formatted = ["### Step-by-Step Guide for Seniors\n"]
        for i, s in enumerate(cleaned_sents, 1):
            formatted.append(f"{i}. {s}")
        return "\n\n".join(formatted)
        
    elif "child" in persona_lower:
        formatted = ["### Simple Child-Friendly Explanation\n"]
        for s in cleaned_sents:
            # Replace remaining long words
            shortened = re.sub(r'\b\w{9,}\b', 'simple word', s)
            formatted.append(f"• {shortened}")
        return "\n\n".join(formatted)
        
    elif "inclusive" in persona_lower:
        return "### Inclusive & Accessible Copy\n\n" + " ".join(cleaned_sents)
        
    else:
        # Plain English
        return "### Plain English Revision\n\n" + "\n\n".join(cleaned_sents)
