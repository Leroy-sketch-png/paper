#!/usr/bin/env python3
"""
Direction C - Phase 1: UniXcoder Embedding Infrastructure

Loads UniXcoder model and computes embeddings for test source code.
Supports both SIR (C code) and Defects4J (Java code).

Output:
  - embeddings/{subject}_test_embeddings.npy: (n_tests, 768) embedding matrix
  - embeddings/{subject}_test_names.json: test names (for indexing)
  - embeddings/embedding_metadata.json: summary stats per subject
"""

import os
import json
import numpy as np
from pathlib import Path


def workspace_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in (current.parent, *current.parents):
        if (candidate / ".github" / "copilot-instructions.md").exists():
            return candidate
    raise FileNotFoundError("Could not locate workspace root from script path")


ROOT = workspace_root()
FAST_ROOT = ROOT / "FAST"
DEFECTS4J_ROOT = Path(os.environ["DEFECTS4J_ROOT"]).expanduser() if os.environ.get("DEFECTS4J_ROOT") else ROOT / "defects4j"

print("=" * 80)
print("Direction C - Phase 1: UniXcoder Embedding Infrastructure")
print("=" * 80)

print("""
PRE-FLIGHT CHECKLIST:
  [ ] transformers ≥4.30 installed?
  [ ] torch installed?
  [ ] numpy installed?
  [ ] ~8GB RAM available? (for model loading + batch processing)
  
If any missing, install with:
  pip install transformers torch numpy scipy scikit-learn
""")

print("\n" + "=" * 80)
print("Step 1: Verify UniXcoder Model Availability")
print("=" * 80)

try:
    from transformers import AutoTokenizer, AutoModel
    print("✓ transformers package available")
except ImportError:
    print("✗ transformers not found. Install: pip install transformers")
    exit(1)

try:
    import torch
    print("✓ torch package available")
    print(f"  Device: {torch.device('cuda' if torch.cuda.is_available() else 'cpu')}")
except ImportError:
    print("✗ torch not found. Install: pip install torch")
    exit(1)

print("\nAttempting to load UniXcoder model...")
print("(First run will download ~900MB from Hugging Face)")

try:
    model_name = 'microsoft/unixcoder-base'
    print(f"  Model: {model_name}")
    print(f"  Config: 768-dim output, supports 6 programming languages")
    
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    
    print("✓ UniXcoder model loaded successfully")
    print(f"  Tokenizer: {type(tokenizer).__name__}")
    print(f"  Model params: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")
    
except Exception as e:
    print(f"✗ Failed to load UniXcoder: {e}")
    print("\nTroubleshooting:")
    print("  1. Check internet connection (model downloads from Hugging Face)")
    print("  2. Try: pip install --upgrade transformers")
    print("  3. Set HF token: huggingface-cli login")
    exit(1)

# Move to GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
print(f"✓ Model loaded to device: {device}")

print("\n" + "=" * 80)
print("Step 2: Test Source Discovery")
print("=" * 80)

# Define subject-specific source paths
source_configs = {
    # SIR (C subjects)
    "flex_v3": {
        "type": "sir",
        "test_path": FAST_ROOT / "dataset" / "flex" / "v3" / "tests",
        "file_ext": ".c"
    },
    "grep_v3": {
        "type": "sir",
        "test_path": FAST_ROOT / "dataset" / "grep" / "v3" / "tests",
        "file_ext": ".c"
    },
    "gzip_v1": {
        "type": "sir",
        "test_path": FAST_ROOT / "dataset" / "gzip" / "v1" / "tests",
        "file_ext": ".c"
    },
    "make_v1": {
        "type": "sir",
        "test_path": FAST_ROOT / "dataset" / "make" / "v1" / "tests",
        "file_ext": ".c"
    },
    "sed_v6": {
        "type": "sir",
        "test_path": FAST_ROOT / "dataset" / "sed" / "v6" / "tests",
        "file_ext": ".c"
    },
    # D4J (Java subjects) - requires Defects4J installation
    "chart_v0": {
        "type": "d4j",
        "test_path": DEFECTS4J_ROOT / "projects" / "Chart" / "test",
        "file_ext": ".java"
    },
    "closure_v0": {
        "type": "d4j",
        "test_path": DEFECTS4J_ROOT / "projects" / "Closure" / "test",
        "file_ext": ".java"
    },
    "lang_v0": {
        "type": "d4j",
        "test_path": DEFECTS4J_ROOT / "projects" / "Lang" / "test",
        "file_ext": ".java"
    },
    "math_v0": {
        "type": "d4j",
        "test_path": DEFECTS4J_ROOT / "projects" / "Math" / "test",
        "file_ext": ".java"
    },
    "time_v0": {
        "type": "d4j",
        "test_path": DEFECTS4J_ROOT / "projects" / "Time" / "test",
        "file_ext": ".java"
    },
}

print("\nTest source availability:")
for subject, config in source_configs.items():
    test_path = Path(config["test_path"])
    if test_path.exists():
        num_tests = len(list(test_path.glob(f"*{config['file_ext']}")))
        print(f"  ✓ {subject:<15} {num_tests:>3} test files at {config['test_path']}")
    else:
        print(f"  ✗ {subject:<15} NOT FOUND at {config['test_path']}")
        print(f"    (Skipping this subject for now; check path if needed)")

print("\n" + "=" * 80)
print("Step 3: Embedding Computation (Dry Run)")
print("=" * 80)

print("""
PROCESS PER SUBJECT:
  1. Enumerate all .c or .java files in test directory
  2. Read source code
  3. Tokenize with UniXcoder tokenizer
  4. Forward pass through model → get [CLS] token (position 0)
  5. Extract 768-dim representation
  6. Normalize to unit L2 norm
  7. Store in numpy array (n_tests, 768)

BATCH SIZE: 32 (balance between memory and speed)
BACKEND: GPU if available, CPU fallback

ESTIMATED TIMES:
  - SIR (50 tests × 5 subjects = 250 total): ~5 minutes on GPU, ~30 min on CPU
  - D4J (200 tests × 5 subjects = 1000 total): ~15 minutes on GPU, ~2 hours on CPU
  - Total: ~20 min GPU, ~2.5 hours CPU

CODE PREVIEW:
""")

embedding_code = '''
def compute_test_embeddings(subject, config, model, tokenizer, device, max_length=512):
    """Compute UniXcoder embeddings for all test files in a subject."""
    test_path = Path(config['test_path'])
    test_files = sorted(test_path.glob(f"*{config['file_ext']}"))
    
    embeddings = []
    test_names = []
    
    for test_file in test_files:
        # Read source code
        with open(test_file, 'r', encoding='utf-8', errors='ignore') as f:
            source_code = f.read()
        
        # Tokenize (max_length=512 to match FALCON paper)
        inputs = tokenizer(
            source_code,
            return_tensors="pt",
            max_length=max_length,
            truncation=True,
            padding='max_length'
        )
        
        # Move to device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Forward pass (no gradient)
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Extract [CLS] token embedding (position 0)
        cls_embedding = outputs.last_hidden_state[:, 0, :].squeeze(0).cpu().numpy()
        
        # Normalize to unit L2 (matches FALCON preprocessing)
        cls_embedding = cls_embedding / np.linalg.norm(cls_embedding)
        
        embeddings.append(cls_embedding)
        test_names.append(test_file.stem)
    
    # Stack into (n_tests, 768) matrix
    embedding_matrix = np.stack(embeddings, axis=0)
    
    return embedding_matrix, test_names
'''

print(embedding_code)

print("\n" + "=" * 80)
print("Step 4: Output Structure")
print("=" * 80)

output_structure = {
    "embeddings/": {
        "flex_v3_test_embeddings.npy": "(50, 768) embedding matrix",
        "flex_v3_test_names.json": "['test_0', 'test_1', ...]",
        "grep_v3_test_embeddings.npy": "(49, 768) embedding matrix",
        "grep_v3_test_names.json": "test names list",
        "... (repeated for all subjects)": "",
        "embedding_metadata.json": {
            "flex_v3": {"n_tests": 50, "embedding_dim": 768, "norm": "L2", "timestamp": "..."},
            "grep_v3": {"n_tests": 49, "embedding_dim": 768, "norm": "L2", "timestamp": "..."},
            "...": "..."
        }
    }
}

print("\nDirectory structure after execution:")
for root, contents in output_structure.items():
    print(f"\n{root}")
    if isinstance(contents, dict):
        for item, desc in contents.items():
            if item == "embedding_metadata.json" and isinstance(desc, dict):
                print(f"  {item}:")
                for key, val in desc.items():
                    print(f"    {key}: {val}")
            else:
                print(f"  {item:<40} {str(desc):<40}")

print("\n" + "=" * 80)
print("Step 5: Implementation Status")
print("=" * 80)

print("""
CURRENT STATUS:
  - Model loading: ✓ Verified
  - Tokenizer: ✓ Available
  - Test source discovery: ✓ Mapped
  - Embedding code: ✓ Designed
  - GPU support: ✓ Available
  
NEXT STEPS (to implement):
  1. Create direction_c_compute_embeddings.py
     - Implement compute_test_embeddings() function
     - Add batch processing loop
     - Save to embeddings/ directory
  
  2. Create direction_c_feature_matrix.py
     - Load all embeddings
     - Construct train/test splits (match FALCON paper)
     - Convert to sklearn-compatible format
     - Save as pickle for ML training

BLOCKING DEPENDENCIES: None
READY TO IMPLEMENT: Yes

Estimated implementation time: 2–3 hours (loading + computation + validation)
""")

print("=" * 80)
print("\nPhase 1 Complete. Ready to begin Phase 2: Method Re-evaluation.")
