#!/usr/bin/env python3
"""Gloss coverage heatmap CLI - show which DEFAULT_GLOSS entries lack samples."""
import sys
import json


def load_gloss(path="gloss.json"):
    with open(path) as f:
        return json.load(f)


def load_samples(path="samples.json"):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def generate_heatmap(gloss, samples):
    heatmap = {}
    for term, definition in gloss.items():
        has_samples = term in samples and len(samples[term]) > 0
        heatmap[term] = {
            "definition": definition,
            "has_samples": has_samples,
            "sample_count": len(samples.get(term, []))
        }
    return heatmap


def print_heatmap(heatmap):
    total = len(heatmap)
    covered = sum(1 for v in heatmap.values() if v["has_samples"])
    uncovered = total - covered
    
    print(f"Gloss Coverage Heatmap")
    print(f"{'=' * 60}")
    print(f"Total terms: {total}")
    print(f"Covered: {covered} ({covered/total*100:.1f}%)")
    print(f"Uncovered: {uncovered} ({uncovered/total*100:.1f}%)")
    print(f"{'=' * 60}\n")
    
    print("UNCOVERED TERMS (need samples):")
    print("-" * 40)
    for term, data in sorted(heatmap.items()):
        if not data["has_samples"]:
            print(f"  {term}: {data['definition'][:50]}...")
    
    print(f"\nCOVERED TERMS:")
    print("-" * 40)
    for term, data in sorted(heatmap.items()):
        if data["has_samples"]:
            print(f"  {term}: {data['sample_count']} samples")


def main():
    gloss_path = sys.argv[1] if len(sys.argv) > 1 else "gloss.json"
    gloss = load_gloss(gloss_path)
    samples = load_samples()
    heatmap = generate_heatmap(gloss, samples)
    print_heatmap(heatmap)


if __name__ == "__main__":
    main()
