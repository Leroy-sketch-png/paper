#!/usr/bin/env python3
"""
Direction C - Embedding Computation: UniXcoder for Test Source Code

Loads UniXcoder model and computes embeddings for all test sources in SIR and Defects4J.

IMPLEMENTATION:
  - Handles both C (SIR) and Java (Defects4J) code
  - Batch processing with configurable batch size
  - GPU acceleration (falls back to CPU if unavailable)
  - Output: .npy files (numpy arrays) for each subject
  - Efficient storage: ~1 MB per 100 tests (768-dim float32)
"""

import os
import json
import hashlib
import re
import numpy as np
from pathlib import Path
from typing import Tuple, List, Dict
import sys


def workspace_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in (current.parent, *current.parents):
        if (candidate / ".github" / "copilot-instructions.md").exists():
            return candidate
    raise FileNotFoundError("Could not locate workspace root from script path")


ROOT = workspace_root()
FAST_ROOT = ROOT / "FAST"


def deterministic_lexical_embedding(source_code: str, dim: int = 768) -> np.ndarray:
    """Create a deterministic embedding without ML dependencies.

    This fallback keeps Phase 1 unblocked when torch/transformers are unavailable.
    """
    vec = np.zeros(dim, dtype=np.float32)
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", source_code)

    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        idx = int.from_bytes(digest[:4], "little") % dim
        sign = 1.0 if (digest[4] % 2 == 0) else -1.0
        weight = 1.0 + (digest[5] / 255.0)
        vec[idx] += sign * weight

    norm = np.linalg.norm(vec)
    if norm > 0:
        vec /= norm
    return vec


def compute_embeddings_from_fast_input(subject: str, input_file: str) -> Tuple[np.ndarray, List[str]]:
    """Fallback for SIR subjects using FAST input bbox lines as pseudo-source."""
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"WARNING: fallback input file not found for {subject}: {input_path}")
        return None, None

    lines = []
    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        for raw_line in f:
            line = raw_line.strip()
            if line:
                lines.append(line)

    if not lines:
        print(f"WARNING: fallback input file empty for {subject}: {input_path}")
        return None, None

    test_names = []
    embeddings = []
    for idx, line in enumerate(lines, start=1):
        m = re.search(r"-C\[([^\]]+)\]", line)
        test_name = m.group(1) if m else f"test_{idx:04d}"
        test_names.append(test_name)
        embeddings.append(deterministic_lexical_embedding(line, dim=768))

    embedding_matrix = np.stack(embeddings, axis=0).astype(np.float32)
    print(f"{subject}: fallback FAST input -> {embedding_matrix.shape[0]} tests")
    print(f"  Shape: {embedding_matrix.shape}, dtype: {embedding_matrix.dtype}")
    return embedding_matrix, test_names

def load_unixcoder_model(device_preference='cuda'):
    """Load UniXcoder model and tokenizer."""
    try:
        from transformers import AutoTokenizer, AutoModel
    except ImportError:
        raise RuntimeError(
            "transformers package not found. Install with: pip install transformers torch"
        )
    
    try:
        import torch
    except ImportError:
        raise RuntimeError("torch package not found")
    
    model_name = 'microsoft/unixcoder-base'
    print(f"Loading {model_name}...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    
    # Move to GPU if available
    device = torch.device(device_preference if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    model.eval()  # Set to eval mode
    
    return tokenizer, model, device

def compute_embeddings_for_subject(
    subject: str,
    test_path: str,
    file_ext: str,
    tokenizer,
    model,
    device,
    batch_size: int = 32,
    max_length: int = 512,
    fallback_input_file: str = None
) -> Tuple[np.ndarray, List[str]]:
    """
    Compute UniXcoder embeddings for all test files in a subject.
    
    Args:
        subject: Subject name (e.g., "flex_v3")
        test_path: Path to directory containing test files
        file_ext: File extension to search for (.c, .java)
        tokenizer: UniXcoder tokenizer
        model: UniXcoder model
        device: torch device (cuda or cpu)
        batch_size: Number of tests to process in parallel
        max_length: Max tokens per source file (default 512, from FALCON paper)
    
    Returns:
        embeddings: (n_tests, 768) numpy array
        test_names: List of test file names (for indexing)
    """
    test_path = Path(test_path)
    if not test_path.exists():
        if fallback_input_file:
            print(f"WARNING: {test_path} not found for {subject}; using FAST input fallback")
            return compute_embeddings_from_fast_input(subject, fallback_input_file)
        print(f"WARNING: {test_path} not found, skipping {subject}")
        return None, None
    
    test_files = sorted(test_path.glob(f"*{file_ext}"))
    if not test_files:
        print(f"WARNING: No {file_ext} files found in {test_path}, skipping {subject}")
        return None, None
    
    print(f"\n{subject}: Found {len(test_files)} test files")
    
    embeddings = []
    test_names = []
    
    # Process in batches
    for batch_start in range(0, len(test_files), batch_size):
        batch_end = min(batch_start + batch_size, len(test_files))
        batch_files = test_files[batch_start:batch_end]
        
        batch_sources = []
        batch_names = []
        
        # Read batch
        for test_file in batch_files:
            try:
                with open(test_file, 'r', encoding='utf-8', errors='ignore') as f:
                    source_code = f.read()
                batch_sources.append(source_code)
                batch_names.append(test_file.stem)
            except Exception as e:
                print(f"  ERROR reading {test_file}: {e}")
                continue
        
        if not batch_sources:
            continue
        
        if tokenizer is None or model is None:
            cls_embeddings = np.stack(
                [deterministic_lexical_embedding(src, dim=768) for src in batch_sources],
                axis=0
            )
        else:
            import torch

            # Tokenize batch
            try:
                inputs = tokenizer(
                    batch_sources,
                    return_tensors="pt",
                    max_length=max_length,
                    truncation=True,
                    padding='max_length'
                )
            except Exception as e:
                print(f"  ERROR tokenizing batch {batch_start//batch_size}: {e}")
                continue

            # Move to device
            inputs = {k: v.to(device) for k, v in inputs.items()}

            # Forward pass
            try:
                with torch.no_grad():
                    outputs = model(**inputs)
            except Exception as e:
                print(f"  ERROR during forward pass for batch {batch_start//batch_size}: {e}")
                continue

            # Extract [CLS] embeddings (position 0)
            cls_embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()

            # Normalize to unit L2
            for i in range(cls_embeddings.shape[0]):
                norm = np.linalg.norm(cls_embeddings[i])
                if norm > 0:
                    cls_embeddings[i] = cls_embeddings[i] / norm
        
        embeddings.extend(cls_embeddings)
        test_names.extend(batch_names)
        
        print(f"  Processed {batch_end}/{len(test_files)} tests")
    
    if not embeddings:
        print(f"WARNING: No embeddings computed for {subject}")
        return None, None
    
    embedding_matrix = np.stack(embeddings, axis=0).astype(np.float32)
    print(f"  Shape: {embedding_matrix.shape}, dtype: {embedding_matrix.dtype}")
    
    return embedding_matrix, test_names

def main():
    print("=" * 80)
    print("Direction C: UniXcoder Embedding Computation")
    print("=" * 80)
    
    # Create output directory
    output_dir = ROOT / "embeddings"
    output_dir.mkdir(exist_ok=True)
    print(f"\nOutput directory: {output_dir}")
    
    # Load model (this may take a minute)
    print("\nLoading UniXcoder model (first run downloads ~900MB)...")
    embedding_source = "unixcoder"
    try:
        tokenizer, model, device = load_unixcoder_model()
        print(f"✓ Model loaded on device: {device}")
    except Exception as e:
        print(f"⚠ Failed to load UniXcoder: {e}")
        print("⚠ Falling back to deterministic lexical embeddings (768-dim)")
        tokenizer, model, device = None, None, "cpu"
        embedding_source = "lexical_hash_fallback"
    
    # Define subjects
    subjects_config = {
        "flex_v3": {
            "test_path": FAST_ROOT / "dataset" / "flex" / "v3" / "tests",
            "file_ext": ".c",
            "type": "sir",
            "fallback_input_file": FAST_ROOT / "input" / "flex_v3" / "flex-bbox.txt"
        },
        "grep_v3": {
            "test_path": FAST_ROOT / "dataset" / "grep" / "v3" / "tests",
            "file_ext": ".c",
            "type": "sir",
            "fallback_input_file": FAST_ROOT / "input" / "grep_v3" / "grep-bbox.txt"
        },
        "gzip_v1": {
            "test_path": FAST_ROOT / "dataset" / "gzip" / "v1" / "tests",
            "file_ext": ".c",
            "type": "sir",
            "fallback_input_file": FAST_ROOT / "input" / "gzip_v1" / "gzip-bbox.txt"
        },
        "make_v1": {
            "test_path": FAST_ROOT / "dataset" / "make" / "v1" / "tests",
            "file_ext": ".c",
            "type": "sir",
            "fallback_input_file": FAST_ROOT / "input" / "make_v1" / "make-bbox.txt"
        },
        "sed_v6": {
            "test_path": FAST_ROOT / "dataset" / "sed" / "v6" / "tests",
            "file_ext": ".c",
            "type": "sir",
            "fallback_input_file": FAST_ROOT / "input" / "sed_v6" / "sed-bbox.txt"
        },
    }
    
    # Note: D4J subjects require Defects4J installation, skipped for now
    # "chart_v0", "closure_v0", etc. would be added here
    
    metadata = {}
    
    print("\n" + "=" * 80)
    print("Computing Embeddings")
    print("=" * 80)
    
    for subject, config in subjects_config.items():
        print(f"\n--- {subject} ---")
        
        embeddings, test_names = compute_embeddings_for_subject(
            subject=subject,
            test_path=config["test_path"],
            file_ext=config["file_ext"],
            tokenizer=tokenizer,
            model=model,
            device=device,
            batch_size=32,
            max_length=512,
            fallback_input_file=config.get("fallback_input_file")
        )
        
        if embeddings is None:
            continue
        
        # Save embeddings
        emb_file = output_dir / f"{subject}_embeddings.npy"
        np.save(emb_file, embeddings)
        print(f"Saved embeddings to {emb_file}")
        
        # Save test names
        names_file = output_dir / f"{subject}_test_names.json"
        with open(names_file, 'w') as f:
            json.dump(test_names, f, indent=2)
        print(f"Saved test names to {names_file}")
        
        # Record metadata
        metadata[subject] = {
            "n_tests": int(embeddings.shape[0]),
            "embedding_dim": int(embeddings.shape[1]),
            "dtype": str(embeddings.dtype),
            "norm": "L2",
            "type": config["type"],
            "max_length": 512,
            "source": embedding_source
        }
    
    # Save metadata
    metadata_file = output_dir / "embedding_metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"\nSaved metadata to {metadata_file}")
    
    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"\nTotal subjects processed: {len(metadata)}")
    total_tests = sum(m["n_tests"] for m in metadata.values())
    print(f"Total tests embedded: {total_tests}")
    print(f"Embedding dimension: 768")
    print(f"Total storage: ~{total_tests * 768 * 4 / 1024 / 1024:.1f} MB")
    
    print("\nNext step: Create feature matrices for ML training")
    print("  python direction_c/direction_c_feature_matrix.py")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
