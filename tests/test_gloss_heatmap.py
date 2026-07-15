"""Tests for gloss coverage heatmap."""
import json
import tempfile
import os
from loru.gloss_heatmap import load_gloss, generate_heatmap


def test_load_gloss():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({"term1": "def1", "term2": "def2"}, f)
        path = f.name
    try:
        gloss = load_gloss(path)
        assert len(gloss) == 2
    finally:
        os.unlink(path)


def test_generate_heatmap():
    gloss = {"a": "def_a", "b": "def_b", "c": "def_c"}
    samples = {"a": ["sample1"], "c": ["s1", "s2"]}
    heatmap = generate_heatmap(gloss, samples)
    assert heatmap["a"]["has_samples"] is True
    assert heatmap["b"]["has_samples"] is False
    assert heatmap["c"]["sample_count"] == 2
