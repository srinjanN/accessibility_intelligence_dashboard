"""
WCAG 2.2 Compliance Mapping Engine.
Maps cognitive and accessibility violation categories to official WCAG 2.2 Success Criteria,
U.S. Section 508 Standards, and European EN 301 549 Accessibility Requirements.
"""

from typing import Dict, Any, List, Optional
import copy


# Complete Mapping Catalog from Violation Categories to Accessibility Standards
WCAG_CATEGORY_MAPPING: Dict[str, Dict[str, Any]] = {
    "Long Sentence": {
        "wcag_criterion": "3.1.5",
        "wcag_name": "Reading Level",
        "wcag_level": "Level AAA",
        "wcag_principle": "Understandable",
        "wcag_guideline": "3.1 Readable",
        "section_508": "Section 508 Chapter 5: 504.2 (Content Creation & Plain Language)",
        "en_301_549": "EN 301 549 Clause 9.3.1.5 (Reading Level)",
        "description": "Sentences exceeding recommended word counts burden working memory and reduce comprehension for users with ADHD, dyslexia, and cognitive impairments.",
        "remediation": "Break lengthy sentences into concise statements of 15-20 words or fewer using active voice."
    },
    "Jargon": {
        "wcag_criterion": "3.1.3",
        "wcag_name": "Unusual Words",
        "wcag_level": "Level AAA",
        "wcag_principle": "Understandable",
        "wcag_guideline": "3.1 Readable",
        "section_508": "Section 508 Chapter 5: 504.2 (Plain Writing Act Standards)",
        "en_301_549": "EN 301 549 Clause 9.3.1.3 (Unusual Words)",
        "description": "Technical jargon, legalisms, or esoteric idioms create significant reading barriers for non-specialists and cognitive disability groups.",
        "remediation": "Provide definitions, glossaries, or replace complex terms with familiar Plain English alternatives."
    },
    "Jargon & Complex Vocabulary": {
        "wcag_criterion": "3.1.3",
        "wcag_name": "Unusual Words",
        "wcag_level": "Level AAA",
        "wcag_principle": "Understandable",
        "wcag_guideline": "3.1 Readable",
        "section_508": "Section 508 Chapter 5: 504.2 (Plain Writing Act Standards)",
        "en_301_549": "EN 301 549 Clause 9.3.1.3 (Unusual Words)",
        "description": "Technical jargon and obscure polysyllabic terms impair reading fluency.",
        "remediation": "Replace with plain language equivalents or supply inline glossaries."
    },
    "Passive Voice": {
        "wcag_criterion": "3.1.5",
        "wcag_name": "Reading Level",
        "wcag_level": "Level AAA",
        "wcag_principle": "Understandable",
        "wcag_guideline": "3.1 Readable",
        "section_508": "Section 508 Chapter 5: 504.2 (Federal Plain Language Guidelines)",
        "en_301_549": "EN 301 549 Clause 9.3.1.5 (Reading Level & Clarity)",
        "description": "Passive voice obscures the actor of the sentence, increasing the cognitive processing time needed to understand instructions.",
        "remediation": "Restructure sentences with active subject-verb-object order (e.g., 'The user must click' instead of 'It is required that it be clicked')."
    },
    "Ambiguous Wording": {
        "wcag_criterion": "3.3.2",
        "wcag_name": "Labels or Instructions",
        "wcag_level": "Level A",
        "wcag_principle": "Understandable",
        "wcag_guideline": "3.3 Input Assistance",
        "section_508": "Section 508 Chapter 5: 502.3.1 (Object Information & Labels)",
        "en_301_549": "EN 301 549 Clause 9.3.3.2 (Labels or Instructions)",
        "description": "Vague phrasing and unclear directions cause mistakes and disorientation for users requiring predictable guidance.",
        "remediation": "Provide precise, unambiguous step-by-step labels and explicit instructions."
    },
    "Non-Inclusive": {
        "wcag_criterion": "3.1.5",
        "wcag_name": "Reading Level",
        "wcag_level": "Level AAA",
        "wcag_principle": "Understandable",
        "wcag_guideline": "3.1 Readable",
        "section_508": "Section 508 Chapter 5: 504.2 (Inclusive Representation Guidelines)",
        "en_301_549": "EN 301 549 Clause 9.3.1.5 (Accessible & Inclusive Terminology)",
        "description": "Gendered, archaic, or non-inclusive terminology alienates users and hinders universal comprehension.",
        "remediation": "Adopt modern, gender-neutral, and welcoming language (e.g., 'they', 'workforce', 'allowlist')."
    },
    "Ableist Term": {
        "wcag_criterion": "4.1.2",
        "wcag_name": "Name, Role, Value",
        "wcag_level": "Level A",
        "wcag_principle": "Robust",
        "wcag_guideline": "4.1 Compatible",
        "section_508": "Section 508 Chapter 5: 504.2 (Inclusive Standards & Non-Stigmatizing Phrasing)",
        "en_301_549": "EN 301 549 Clause 9.4.1.2 (Accessible Terminology & Roles)",
        "description": "Ableist metaphors and pejorative terms create hostile digital experiences and mischaracterize accessibility aids.",
        "remediation": "Replace ableist metaphors with accurate descriptive terms (e.g., 'unseen gap' instead of 'blind spot')."
    },
    "Unclear CTA": {
        "wcag_criterion": "2.4.4",
        "wcag_name": "Link Purpose (In Context)",
        "wcag_level": "Level A",
        "wcag_principle": "Operable",
        "wcag_guideline": "2.4 Navigable",
        "section_508": "Section 508 Chapter 5: 502.3.1 (Accessible Names & Contextual Links)",
        "en_301_549": "EN 301 549 Clause 9.2.4.4 (Link Purpose In Context)",
        "description": "Non-descriptive call-to-action labels such as 'click here' or 'read more' fail when read out of context by screen readers or users skimming UI copy.",
        "remediation": "Use meaningful action labels that describe target actions (e.g., 'Download Accessibility Audit PDF')."
    },
    "Poor Headings": {
        "wcag_criterion": "2.4.6",
        "wcag_name": "Headings and Labels",
        "wcag_level": "Level AA",
        "wcag_principle": "Operable",
        "wcag_guideline": "2.4 Navigable",
        "section_508": "Section 508 Chapter 5: 504.2 (Document Structure & Descriptive Headings)",
        "en_301_549": "EN 301 549 Clause 9.2.4.6 (Headings and Labels)",
        "description": "ALL-CAPS headings, missing hierarchy, or vague headers impede navigation and reduce reading speed for dyslexic readers.",
        "remediation": "Use Sentence case or Title Case headings with clear hierarchical tags (H1, H2, H3)."
    },
    "Poor Heading / Typography": {
        "wcag_criterion": "2.4.6",
        "wcag_name": "Headings and Labels",
        "wcag_level": "Level AA",
        "wcag_principle": "Operable",
        "wcag_guideline": "2.4 Navigable",
        "section_508": "Section 508 Chapter 5: 504.2 (Document Structure & Descriptive Headings)",
        "en_301_549": "EN 301 549 Clause 9.2.4.6 (Headings and Labels)",
        "description": "ALL-CAPS text and unstructured headings disrupt scanning and reduce legibility.",
        "remediation": "Format headings in mixed case with explicit semantic hierarchy."
    },
    "Repeated Words": {
        "wcag_criterion": "3.1.5",
        "wcag_name": "Reading Level",
        "wcag_level": "Level AAA",
        "wcag_principle": "Understandable",
        "wcag_guideline": "3.1 Readable",
        "section_508": "Section 508 Chapter 5: 504.2 (Text Quality & Editorial Clarity)",
        "en_301_549": "EN 301 549 Clause 9.3.1.5 (Reading Level & Editorial Accuracy)",
        "description": "Consecutive duplicate words introduce confusion and interrupt audio text-to-speech synthesis.",
        "remediation": "Remove duplicate consecutive words."
    },
    "Repeated Words / Typo": {
        "wcag_criterion": "3.1.5",
        "wcag_name": "Reading Level",
        "wcag_level": "Level AAA",
        "wcag_principle": "Understandable",
        "wcag_guideline": "3.1 Readable",
        "section_508": "Section 508 Chapter 5: 504.2 (Text Quality & Editorial Clarity)",
        "en_301_549": "EN 301 549 Clause 9.3.1.5 (Reading Level & Editorial Accuracy)",
        "description": "Duplicate consecutive tokens create stutters in screen readers and degrade reader focus.",
        "remediation": "Eliminate redundant words."
    },
    "Cognitive Overload": {
        "wcag_criterion": "3.1.5",
        "wcag_name": "Reading Level",
        "wcag_level": "Level AAA",
        "wcag_principle": "Understandable",
        "wcag_guideline": "3.1 Readable",
        "section_508": "Section 508 Chapter 5: 504.2 (Cognitive Accessibility Requirements)",
        "en_301_549": "EN 301 549 Clause 9.3.1.5 (Cognitive Accessibility & Information Density)",
        "description": "Excessive commas, multi-clause syntax, and high syntactic depth tax executive function and working memory.",
        "remediation": "Split sentences, convert complex enumerations into bulleted lists, and clarify logical flow."
    },
    "Dense Paragraph": {
        "wcag_criterion": "1.4.12",
        "wcag_name": "Text Spacing",
        "wcag_level": "Level AA",
        "wcag_principle": "Perceivable",
        "wcag_guideline": "1.4 Distinguishable",
        "section_508": "Section 508 Chapter 5: 504.2 (Visual Presentation & Spacing)",
        "en_301_549": "EN 301 549 Clause 9.1.4.12 (Text Spacing)",
        "description": "Walls of text without paragraph breaks or whitespace make line tracking difficult for readers with low vision and dyslexia.",
        "remediation": "Limit paragraphs to 3-4 sentences and introduce whitespace or visual breaks."
    }
}

# Master Catalog of Standard Criteria Evaluated in the Cognitive Audit
EVALUATED_WCAG_CRITERIA: List[Dict[str, Any]] = [
    {
        "criterion": "2.4.4",
        "name": "Link Purpose (In Context)",
        "level": "Level A",
        "principle": "Operable",
        "guideline": "2.4 Navigable",
        "section_508": "508 Chapter 5: 502.3.1",
        "en_301_549": "EN 301 549 Clause 9.2.4.4",
        "monitored_categories": ["Unclear CTA"]
    },
    {
        "criterion": "3.3.2",
        "name": "Labels or Instructions",
        "level": "Level A",
        "principle": "Understandable",
        "guideline": "3.3 Input Assistance",
        "section_508": "508 Chapter 5: 502.3.1",
        "en_301_549": "EN 301 549 Clause 9.3.3.2",
        "monitored_categories": ["Ambiguous Wording"]
    },
    {
        "criterion": "4.1.2",
        "name": "Name, Role, Value",
        "level": "Level A",
        "principle": "Robust",
        "guideline": "4.1 Compatible",
        "section_508": "508 Chapter 5: 504.2",
        "en_301_549": "EN 301 549 Clause 9.4.1.2",
        "monitored_categories": ["Ableist Term"]
    },
    {
        "criterion": "2.4.6",
        "name": "Headings and Labels",
        "level": "Level AA",
        "principle": "Operable",
        "guideline": "2.4 Navigable",
        "section_508": "508 Chapter 5: 504.2",
        "en_301_549": "EN 301 549 Clause 9.2.4.6",
        "monitored_categories": ["Poor Headings", "Poor Heading / Typography"]
    },
    {
        "criterion": "1.4.12",
        "name": "Text Spacing",
        "level": "Level AA",
        "principle": "Perceivable",
        "guideline": "1.4 Distinguishable",
        "section_508": "508 Chapter 5: 504.2",
        "en_301_549": "EN 301 549 Clause 9.1.4.12",
        "monitored_categories": ["Dense Paragraph"]
    },
    {
        "criterion": "3.1.3",
        "name": "Unusual Words",
        "level": "Level AAA",
        "principle": "Understandable",
        "guideline": "3.1 Readable",
        "section_508": "508 Chapter 5: 504.2",
        "en_301_549": "EN 301 549 Clause 9.3.1.3",
        "monitored_categories": ["Jargon", "Jargon & Complex Vocabulary"]
    },
    {
        "criterion": "3.1.5",
        "name": "Reading Level",
        "level": "Level AAA",
        "principle": "Understandable",
        "guideline": "3.1 Readable",
        "section_508": "508 Chapter 5: 504.2",
        "en_301_549": "EN 301 549 Clause 9.3.1.5",
        "monitored_categories": [
            "Long Sentence", "Passive Voice", "Non-Inclusive",
            "Repeated Words", "Repeated Words / Typo", "Cognitive Overload"
        ]
    }
]


def normalize_category(category: str) -> str:
    """Normalize issue category string for consistent mapping lookup."""
    clean = category.strip()
    if clean in WCAG_CATEGORY_MAPPING:
        return clean
    # Fallback normalizations
    lower = clean.lower()
    if "jargon" in lower:
        return "Jargon"
    if "sentence" in lower and "long" in lower:
        return "Long Sentence"
    if "passive" in lower:
        return "Passive Voice"
    if "heading" in lower or "caps" in lower:
        return "Poor Headings"
    if "repeat" in lower or "typo" in lower:
        return "Repeated Words"
    if "cta" in lower or "button" in lower or "link" in lower:
        return "Unclear CTA"
    if "ableist" in lower:
        return "Ableist Term"
    if "inclusive" in lower or "diversity" in lower:
        return "Non-Inclusive"
    if "cognitive" in lower or "complex" in lower:
        return "Cognitive Overload"
    if "dense" in lower or "paragraph" in lower:
        return "Dense Paragraph"
    if "ambiguous" in lower:
        return "Ambiguous Wording"
    return clean


def get_wcag_mapping(category: str) -> Optional[Dict[str, Any]]:
    """Retrieve WCAG success criteria metadata for a violation category."""
    norm = normalize_category(category)
    return WCAG_CATEGORY_MAPPING.get(norm)


def enrich_issue_with_wcag(issue: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enrich a single issue with WCAG, Section 508, and EN 301 549 metadata.
    IMPORTANT: Creates a new copy without mutating the input dictionary.
    """
    enriched = copy.deepcopy(issue)
    cat = enriched.get("category", "")
    mapping = get_wcag_mapping(cat)
    
    if mapping:
        enriched["wcag_criterion"] = mapping["wcag_criterion"]
        enriched["wcag_name"] = mapping["wcag_name"]
        enriched["wcag_level"] = mapping["wcag_level"]
        enriched["wcag_principle"] = mapping["wcag_principle"]
        enriched["wcag_guideline"] = mapping["wcag_guideline"]
        enriched["section_508"] = mapping["section_508"]
        enriched["en_301_549"] = mapping["en_301_549"]
        enriched["standard_explanation"] = mapping["description"]
        enriched["wcag_remediation"] = mapping["remediation"]
    else:
        enriched["wcag_criterion"] = "3.1.5"
        enriched["wcag_name"] = "Reading Level"
        enriched["wcag_level"] = "Level AAA"
        enriched["wcag_principle"] = "Understandable"
        enriched["wcag_guideline"] = "3.1 Readable"
        enriched["section_508"] = "Section 508 Chapter 5: 504.2"
        enriched["en_301_549"] = "EN 301 549 Clause 9.3.1.5"
        enriched["standard_explanation"] = "Cognitive accessibility requirement for clear communication."
        enriched["wcag_remediation"] = "Refactor language for clarity and accessibility."
        
    return enriched


def evaluate_wcag_compliance(issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Evaluate pass/fail status per criterion and calculate overall compliance metrics.
    Does not mutate any original issue objects.
    """
    enriched_issues = [enrich_issue_with_wcag(i) for i in issues]
    
    # Map violations to criteria
    criterion_violations: Dict[str, List[Dict[str, Any]]] = {}
    for crit in EVALUATED_WCAG_CRITERIA:
        criterion_violations[crit["criterion"]] = []
        
    for issue in enriched_issues:
        cid = issue.get("wcag_criterion")
        if cid in criterion_violations:
            criterion_violations[cid].append(issue)
        else:
            criterion_violations[cid] = [issue]
            
    # Compile criterion results
    criteria_results = []
    level_counts = {
        "Level A": {"total": 0, "passed": 0, "failed": 0},
        "Level AA": {"total": 0, "passed": 0, "failed": 0},
        "Level AAA": {"total": 0, "passed": 0, "failed": 0}
    }
    
    for crit in EVALUATED_WCAG_CRITERIA:
        cid = crit["criterion"]
        lvl = crit["level"]
        violating_issues = criterion_violations.get(cid, [])
        is_pass = len(violating_issues) == 0
        
        level_counts[lvl]["total"] += 1
        if is_pass:
            level_counts[lvl]["passed"] += 1
        else:
            level_counts[lvl]["failed"] += 1
            
        criteria_results.append({
            "criterion": cid,
            "name": crit["name"],
            "level": lvl,
            "principle": crit["principle"],
            "guideline": crit["guideline"],
            "section_508": crit["section_508"],
            "en_301_549": crit["en_301_549"],
            "status": "PASS" if is_pass else "FAIL",
            "passed": is_pass,
            "violations_count": len(violating_issues),
            "issues": violating_issues
        })
        
    # Determine overall certification tier
    level_a_passed = level_counts["Level A"]["failed"] == 0
    level_aa_passed = level_a_passed and (level_counts["Level AA"]["failed"] == 0)
    level_aaa_passed = level_aa_passed and (level_counts["Level AAA"]["failed"] == 0)
    
    if level_aaa_passed:
        overall_tier = "Level AAA"
        badge_text = "WCAG 2.2 Level AAA Compliant"
        badge_color = "#10b981"
        badge_status = "passed"
    elif level_aa_passed:
        overall_tier = "Level AA"
        badge_text = "WCAG 2.2 Level AA Compliant"
        badge_color = "#6366f1"
        badge_status = "passed"
    elif level_a_passed:
        overall_tier = "Level A"
        badge_text = "WCAG 2.2 Level A Compliant"
        badge_color = "#eab308"
        badge_status = "partial"
    else:
        overall_tier = "Non-Compliant"
        badge_text = "Non-Compliant (Failed Level A)"
        badge_color = "#ef4444"
        badge_status = "failed"
        
    total_criteria = len(EVALUATED_WCAG_CRITERIA)
    passed_criteria = sum(1 for c in criteria_results if c["passed"])
    compliance_score = round((passed_criteria / total_criteria) * 100, 1) if total_criteria > 0 else 100.0
    
    return {
        "overall_tier": overall_tier,
        "badge_text": badge_text,
        "badge_color": badge_color,
        "badge_status": badge_status,
        "compliance_score": compliance_score,
        "total_criteria": total_criteria,
        "passed_criteria": passed_criteria,
        "failed_criteria": total_criteria - passed_criteria,
        "level_counts": level_counts,
        "level_a_passed": level_a_passed,
        "level_aa_passed": level_aa_passed,
        "level_aaa_passed": level_aaa_passed,
        "criteria_results": criteria_results,
        "enriched_issues": enriched_issues
    }


def enrich_analysis_with_wcag(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """
    Non-mutating helper to produce an enriched copy of analysis with WCAG compliance data.
    Ensures existing session state or analysis dict is NEVER modified.
    """
    enriched = copy.deepcopy(analysis)
    issues = enriched.get("issues", [])
    compliance = evaluate_wcag_compliance(issues)
    enriched["wcag_compliance"] = compliance
    return enriched
