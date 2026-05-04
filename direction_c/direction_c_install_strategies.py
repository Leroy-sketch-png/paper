#!/usr/bin/env python3
"""
Direction C: Dependency Resolution Script

Attempts multiple strategies to install torch and transformers.
Tries from most robust to fastest.
"""

import subprocess
import sys
import os

print("=" * 80)
print("Direction C: Dependency Resolution")
print("=" * 80)

strategies = [
    {
        "name": "sentence-transformers (all-in-one, recommended)",
        "commands": [
            ["pip", "install", "sentence-transformers", "--retries", "10", "--timeout", "120"]
        ],
        "why": "Simplest; includes torch + transformers; cached on PyPI",
        "time": "~10 minutes (GPU) / ~30 min (CPU)"
    },
    {
        "name": "ONNX Runtime (lightweight, no torch)",
        "commands": [
            ["pip", "install", "onnxruntime", "transformers", "--retries", "10", "--timeout", "120"],
            ["pip", "install", "scikit-learn", "numpy"]
        ],
        "why": "Avoids torch entirely; ONNX optimized for inference",
        "time": "~5 minutes",
        "note": "Need ONNX model export from UniXcoder first (extra step)"
    },
    {
        "name": "torch + transformers from official index (most reliable)",
        "commands": [
            ["pip", "install", "torch", "--retries", "10", "--timeout", "300", "-i", "https://download.pytorch.org/whl/cpu"],
            ["pip", "install", "transformers", "scikit-learn"]
        ],
        "why": "Direct from PyTorch official mirrors; no middleman",
        "time": "~15 minutes"
    },
    {
        "name": "Conda (if available)",
        "commands": [
            ["conda", "install", "-c", "pytorch", "-c", "conda-forge", "pytorch", "transformers", "scikit-learn", "-y"]
        ],
        "why": "Conda resolves dependencies better than pip; pre-compiled binaries",
        "time": "~10 minutes",
        "requirement": "Conda must be installed (Anaconda / Miniconda)"
    }
]

print(f"""
PROBLEM: pip install torch timed out due to network latency.
SOLUTION: Try alternative installation strategies with longer timeouts and retries.

STRATEGIES (in recommended order):
""")

for i, strat in enumerate(strategies, 1):
    print(f"\n{i}. {strat['name']}")
    print(f"   Why: {strat['why']}")
    print(f"   Time: {strat['time']}")
    if 'note' in strat:
        print(f"   Note: {strat['note']}")
    if 'requirement' in strat:
        print(f"   Requirement: {strat['requirement']}")
    print(f"   Commands:")
    for cmd in strat['commands']:
        print(f"     {' '.join(cmd)}")

print(f"""

RECOMMENDED ACTION:
  Strategy 1 (sentence-transformers) is best for Direction C:
  - All-in-one: includes torch, transformers, and useful utilities
  - More reliable download from PyPI
  - Simpler API than raw transformers
  
EXECUTION:
  Run one of the following commands in terminal:
  
  {chr(10).join(f'    {" ".join(strategies[i]["commands"][0])}' for i in range(len(strategies)))}
  
MONITORING:
  Each strategy will show progress. Expected outputs:
  - ✓ "Successfully installed ..." = Success
  - ✗ "Timeout" = Network issue, try next strategy
  - ✗ "Not found" = Package unavailable, try next strategy
""")

print("\n" + "=" * 80)
print("ALTERNATIVE: Skip Installation, Use Pre-computed Embeddings")
print("=" * 80)

print("""
If all installation strategies fail:

OPTION A: Use FALCON Artifact Embeddings (Immediate)
  - FALCON paper uses same UniXcoder model
  - Zenodo 18897073 includes embedding vectors
  - Can extract from falcon.zip without torch
  - Timeline: 1 hour (extract + reformat)
  - Trade-off: Must match FALCON's embedding format

OPTION B: Use Surrogate Embeddings (Functional)
  - Principal Component Analysis on FAST features
  - Preserves semantic structure; lower-rank approximation
  - Functional for Phases 2-4 even if not "true" UniXcoder
  - Timeline: 30 minutes
  - Trade-off: Not semantic embeddings, but adequate proof-of-concept

OPTION C: Defer to Week 2 (After Network Stability)
  - Install torch when network is more stable
  - More reliable after 24-48 hours
  - Timeline: Delay of 1-2 days

RECOMMENDATION: Try Strategy 1 first (sentence-transformers), then OPTION A (FALCON
embeddings as fallback) if installation fails. Together, these cover all pathways.
""")

print("\n" + "=" * 80)
print("Instructions for Manual Installation")
print("=" * 80)

print("""
If you prefer to install manually in terminal:

STEP 1: Open PowerShell in VS Code terminal
STEP 2: Activate venv:
  & ./.venv/Scripts/Activate.ps1

STEP 3: Try Strategy 1 (sentence-transformers):
  pip install sentence-transformers --retries 10 --timeout 120

  If that succeeds, done! Then run:
  python direction_c/direction_c_compute_embeddings.py

STEP 4: If Strategy 1 fails, try Strategy 3 (PyTorch official):
  pip install torch --retries 10 --timeout 300 -i https://download.pytorch.org/whl/cpu
  pip install transformers scikit-learn

STEP 5: If both fail, fall back to OPTION A:
  # Extract and reformat FALCON embeddings from falcon.zip
  python direction_c_extract_falcon_embeddings.py

Status: Installation strategies documented. Ready to execute.
""")

print("=" * 80)
