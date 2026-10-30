"""
Accessibility & Cognitive Inclusion Rule Engine + Explainable AI (XAI) Scoring.
Detects 10+ distinct accessibility and cognitive inclusion violations in text/UI copy.
"""

import sys
import os
import site

user_site = site.USER_SITE
if user_site and os.path.exists(user_site) and user_site not in sys.path:
    sys.path.insert(0, user_site)

import re
from typing import Dict, Any, List, Tuple
from utils.nlp_engine import get_sentences, compute_readability_metrics

# Known non-inclusive or non-accessible terminology database
INCLUSIVE_LANGUAGE_DB = {
    "click here": {"category": "Unclear CTA", "suggestion": "Use descriptive action verbs (e.g., 'View Terms', 'Download Guide')", "severity": "High"},
    "read more": {"category": "Unclear CTA", "suggestion": "Specify the destination (e.g., 'Read Product Details')", "severity": "Medium"},
    "learn more": {"category": "Unclear CTA", "suggestion": "Specify context (e.g., 'Learn about Pricing')", "severity": "Medium"},
    "submit": {"category": "Unclear CTA", "suggestion": "Use specific action phrase (e.g., 'Send Registration', 'Save Changes')", "severity": "Low"},
    "go": {"category": "Unclear CTA", "suggestion": "Use descriptive label (e.g., 'Search', 'Open Dashboard')", "severity": "Low"},
    "guys": {"category": "Non-Inclusive", "suggestion": "Use 'everyone', 'team', or 'people'", "severity": "Medium"},
    "he/she": {"category": "Non-Inclusive", "suggestion": "Use gender-neutral 'they'", "severity": "Medium"},
    "manpower": {"category": "Non-Inclusive", "suggestion": "Use 'workforce', 'staff', or 'personnel'", "severity": "Low"},
    "master/slave": {"category": "Non-Inclusive", "suggestion": "Use 'primary/secondary' or 'leader/follower'", "severity": "Critical"},
    "whitelist": {"category": "Non-Inclusive", "suggestion": "Use 'allowlist'", "severity": "Medium"},
    "blacklist": {"category": "Non-Inclusive", "suggestion": "Use 'denylist' or 'blocklist'", "severity": "Medium"},
    "dummy": {"category": "Non-Inclusive", "suggestion": "Use 'sample', 'placeholder', or 'mock'", "severity": "Low"},
    "blind spot": {"category": "Ableist Term", "suggestion": "Use 'unseen area' or 'gap'", "severity": "Medium"},
    "crazy": {"category": "Ableist Term", "suggestion": "Use 'wild', 'intense', or 'unusual'", "severity": "Medium"},
    "insane": {"category": "Ableist Term", "suggestion": "Use 'extreme' or 'remarkable'", "severity": "Medium"},
    "cripple": {"category": "Ableist Term", "suggestion": "Use 'restrict', 'impair', or 'disable'", "severity": "Critical"}
}

JARGON_LIST = set([
    "indemnify", "indemnification", "pursuant", "herein", "aforementioned",
    "heretofore", "alimentary", "pharmacotherapy", "antihypertensive",
    "anesthesiologic", "ambulatory", "pulmonary", "gastric", "notwithstanding",
    "imperative", "precipitate", "synergistic", "paradigm", "leverage", "utilize"
])

PASSIVE_VOICE_PATTERNS = [
    r'\b(?:am|is|are|was|were|be|been|being)\s+([a-z]+ed|[a-z]+en)\b',
    r'\b(?:it\s+is\s+recommended|it\s+is\s+required|it\s+is\s+advised)\b'
]

def analyze_accessibility(text: str, custom_thresholds: Dict[str, Any] = None) -> Dict[str, Any]:
    """Run full accessibility & cognitive inclusion audit on given text."""
    if custom_thresholds is None:
        custom_thresholds = {
            "max_sentence_length": 20,
            "target_reading_level": 8.0,
            "max_passive_pct": 15.0
        }
        
    sentences = get_sentences(text)
    metrics = compute_readability_metrics(text)
    
    issues: List[Dict[str, Any]] = []
    
    total_words = metrics["word_count"]
    total_sents = max(len(sentences), 1)
    
    passive_count = 0
    jargon_count = 0
    
    # 1. Check Sentence Length & Complexity per sentence
    for idx, sent in enumerate(sentences):
        words = re.findall(r'\b\w+\b', sent)
        word_len = len(words)
        
        # Rule 1: Overly Long Sentence
        if word_len > custom_thresholds["max_sentence_length"]:
            issues.append({
                "id": f"sent_len_{idx}",
                "category": "Long Sentence",
                "severity": "High" if word_len > 30 else "Medium",
                "title": f"Sentence too long ({word_len} words)",
                "snippet": sent,
                "explanation": f"Sentence contains {word_len} words, exceeding the recommended max of {custom_thresholds['max_sentence_length']} words. Long sentences increase cognitive load.",
                "suggestion": "Split into 2 or 3 shorter, clear sentences.",
                "confidence": 0.98
            })
            
        # Rule 2: Passive Voice Detection
        is_passive = False
        for pattern in PASSIVE_VOICE_PATTERNS:
            if re.search(pattern, sent, re.IGNORECASE):
                is_passive = True
                break
        if is_passive:
            passive_count += 1
            issues.append({
                "id": f"passive_{idx}",
                "category": "Passive Voice",
                "severity": "Low",
                "title": "Passive Voice Detected",
                "snippet": sent,
                "explanation": "Passive sentence structure can obscure who is performing the action.",
                "suggestion": "Rewrite using active voice (e.g. 'Patients must take...' instead of 'It is recommended that patients take...').",
                "confidence": 0.92
            })
            
        # Rule 3: Syntactic Cognitive Overload (excessive clauses/commas)
        comma_count = sent.count(",")
        semicolon_count = sent.count(";")
        if comma_count >= 4 or semicolon_count >= 2:
            issues.append({
                "id": f"cognitive_{idx}",
                "category": "Cognitive Overload",
                "severity": "High",
                "title": "Complex Sentence Structure (High Syntactic Depth)",
                "snippet": sent,
                "explanation": f"Sentence has {comma_count} commas and nested sub-clauses, creating high working-memory burden.",
                "suggestion": "Simplify structure. Use bullet points or separate statements.",
                "confidence": 0.94
            })

    # 2. Check Jargon & Complex Vocabulary
    words_in_text = re.findall(r'\b[a-zA-Z]+\b', text)
    found_jargon = []
    for w in words_in_text:
        w_lower = w.lower()
        if w_lower in JARGON_LIST:
            jargon_count += 1
            if w_lower not in found_jargon:
                found_jargon.append(w_lower)
                
    if found_jargon:
        issues.append({
            "id": "jargon_terms",
            "category": "Jargon & Complex Vocabulary",
            "severity": "High",
            "title": f"Jargon Terms Detected ({len(found_jargon)} unique terms)",
            "snippet": ", ".join(found_jargon[:6]),
            "explanation": f"Contains complex technical or legal terms ({', '.join(found_jargon[:4])}) that lower comprehension.",
            "suggestion": "Replace with plain English alternatives (e.g., 'pay for' instead of 'indemnify', 'before' instead of 'pursuant').",
            "confidence": 0.96
        })

    # 3. Non-Inclusive & Unclear CTAs / Button Labels
    text_lower = text.lower()
    for term, meta in INCLUSIVE_LANGUAGE_DB.items():
        if term in text_lower:
            # Find snippet
            matches = [m.start() for m in re.finditer(re.escape(term), text_lower)]
            for match_idx, start_pos in enumerate(matches):
                snippet_start = max(0, start_pos - 15)
                snippet_end = min(len(text), start_pos + len(term) + 20)
                snippet = text[snippet_start:snippet_end]
                
                issues.append({
                    "id": f"inclusive_{term}_{match_idx}",
                    "category": meta["category"],
                    "severity": meta["severity"],
                    "title": f"Found term: '{term}'",
                    "snippet": snippet.strip(),
                    "explanation": f"Term '{term}' violates cognitive accessibility or inclusive content standards.",
                    "suggestion": meta["suggestion"],
                    "confidence": 0.99
                })

    # 4. Poor Headings / All-Caps Copy
    lines = text.split("\n")
    for l_idx, line in enumerate(lines):
        line_clean = line.strip()
        if line_clean.isupper() and len(line_clean) > 15:
            issues.append({
                "id": f"all_caps_{l_idx}",
                "category": "Poor Heading / Typography",
                "severity": "Medium",
                "title": "All-Caps Text Detected",
                "snippet": line_clean[:50],
                "explanation": "ALL-CAPS text reduces reading speed by 15-20% and hurts legibility for dyslexic users.",
                "suggestion": "Convert to Sentence case or Title Case with bold font weight.",
                "confidence": 0.99
            })

    # 5. Repeated Words / Typos
    repeated_matches = re.findall(r'\b(\w+)\s+\1\b', text, re.IGNORECASE)
    if repeated_matches:
        unique_repeated = list(set(repeated_matches))
        issues.append({
            "id": "repeated_words",
            "category": "Repeated Words / Typo",
            "severity": "Low",
            "title": "Duplicate Consecutive Words",
            "snippet": ", ".join(unique_repeated),
            "explanation": f"Found repeated consecutive words: {', '.join(unique_repeated)}.",
            "suggestion": "Remove duplicate word.",
            "confidence": 0.99
        })

    # Deduplicate issues by snippet & title
    unique_issues = []
    seen = set()
    for item in issues:
        key = (item["category"], item.get("snippet", "")[:30])
        if key not in seen:
            seen.add(key)
            unique_issues.append(item)

    # Calculate Summary Statistics
    passive_pct = round((passive_count / total_sents) * 100, 1)
    difficult_words_pct = round((jargon_count / max(total_words, 1)) * 100, 1)
    
    # Cognitive Complexity Index (0-100 scale, 0=Simple, 100=Extreme)
    cog_comp = min(100.0, max(0.0, (
        (metrics["avg_words_per_sentence"] * 2.2) +
        (metrics["flesch_kincaid_grade"] * 3.5) +
        (passive_pct * 0.8) +
        (difficult_words_pct * 4.0)
    )))
    
    # Accessibility Score Calculation (0-100 scale, 100=Perfect Accessibility)
    # Balanced multidimensional evaluation:
    # 1. Reading Ease Factor (30% weight) - Flesch Reading Ease normalized
    fre_normalized = max(0.0, min(100.0, metrics["flesch_reading_ease"]))
    
    # 2. Structural Clarity Factor (35% weight) - Sentence length, grade level, passive voice, jargon
    avg_wps = metrics["avg_words_per_sentence"]
    grade = max(0.0, metrics["flesch_kincaid_grade"])
    
    # Target: 15-18 words per sentence; deduct above 18
    wps_deduction = max(0.0, avg_wps - 18.0) * 1.5
    # Target: Grade 8 (Plain Language standard); deduct above Grade 8
    grade_deduction = max(0.0, grade - 8.0) * 2.2
    # Target: <= 15% passive voice
    passive_deduction = max(0.0, passive_pct - 15.0) * 0.4
    # Jargon vocabulary deduction
    jargon_deduction = min(20.0, difficult_words_pct * 2.5)
    
    structural_clarity_score = max(10.0, min(100.0, 100.0 - (wps_deduction + grade_deduction + passive_deduction + jargon_deduction)))
    
    # 3. Violation Density Compliance (35% weight)
    # Weighted severity points normalized per 100 words so large documents are not penalized unfairly
    weighted_violation_points = 0.0
    for iss in unique_issues:
        sev = iss["severity"].lower()
        if sev == "critical":
            weighted_violation_points += 4.0
        elif sev == "high":
            weighted_violation_points += 2.5
        elif sev == "medium":
            weighted_violation_points += 1.2
        else:
            weighted_violation_points += 0.5
            
    hundred_word_units = max(total_words / 100.0, 1.0)
    violation_density = weighted_violation_points / hundred_word_units
    violation_compliance_score = max(10.0, min(100.0, 100.0 - (violation_density * 8.0)))
    
    # Composite Final Score (0-100 scale)
    final_accessibility_score = round(
        (fre_normalized * 0.30) +
        (structural_clarity_score * 0.35) +
        (violation_compliance_score * 0.35),
        1
    )
    final_accessibility_score = max(5.0, min(100.0, final_accessibility_score))

    # Feature Importance Breakdown for Explainable AI (XAI)
    feature_importance = {
        "Sentence Length Impact": round(min(35.0, max(0.0, (avg_wps - 15.0) * 1.8)), 1),
        "Reading Grade Impact": round(min(35.0, max(0.0, (grade - 8.0) * 2.5)), 1),
        "Jargon/Vocabulary Penalty": round(min(25.0, difficult_words_pct * 3.0), 1),
        "Passive Voice Penalty": round(min(20.0, max(0.0, (passive_pct - 15.0) * 0.5)), 1),
        "Violation Density Penalty": round(min(40.0, violation_density * 5.0), 1)
    }

    # Human-Readable XAI Explanation
    xai_explanation = generate_xai_summary(final_accessibility_score, metrics, len(unique_issues), found_jargon, passive_pct)

    return {
        "accessibility_score": final_accessibility_score,
        "readability_score": metrics["flesch_reading_ease"],
        "grade_level": metrics["flesch_kincaid_grade"],
        "reading_time_seconds": metrics["reading_time_seconds"],
        "passive_voice_pct": passive_pct,
        "jargon_count": jargon_count,
        "cognitive_complexity": round(cog_comp, 1),
        "violations_count": len(unique_issues),
        "issues": unique_issues,
        "metrics": metrics,
        "feature_importance": feature_importance,
        "xai_explanation": xai_explanation
    }

def generate_xai_summary(score: float, metrics: Dict[str, Any], issues_count: int, jargon: List[str], passive_pct: float) -> str:
    """Generate human-readable Explainable AI rationale for accessibility score."""
    rating = "EXCELLENT" if score >= 85 else ("GOOD" if score >= 70 else ("NEEDS IMPROVEMENT" if score >= 50 else "POOR"))
    
    reasons = []
    if metrics["avg_words_per_sentence"] > 20:
        reasons.append(f"high average sentence length ({metrics['avg_words_per_sentence']} words/sentence)")
    if metrics["flesch_kincaid_grade"] > 10:
        reasons.append(f"advanced reading grade level (Grade {metrics['flesch_kincaid_grade']})")
    if jargon:
        reasons.append(f"presence of complex jargon terms ({', '.join(jargon[:3])})")
    if passive_pct > 15:
        reasons.append(f"frequent passive voice usage ({passive_pct}%)")
        
    reason_str = ", ".join(reasons) if reasons else "clean sentence structure and accessible vocabulary"
    
    return f"The content achieved an Accessibility Score of **{score}/100** ({rating}). This score is primarily driven by: {reason_str}. Total violations detected: **{issues_count}**."
