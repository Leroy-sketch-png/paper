#!/usr/bin/env python3
"""
Direction C - Phase 1 (ONNX / vocab-anchored fallback)

Uses the downloaded UniXcoder BPE tokenizer to build vocabulary-anchored
768-dim embeddings without requiring torch/transformers.

Method:
  1. Tokenize source with RobertaTokenizer (UniXcoder vocab).
  2. For each token-id, derive a 768-dim basis vector via deterministic
     random projection seeded on that id (Achlioptas 1999 sparse projection).
  3. Accumulate IDF-weighted token embeddings -> L2-normalise.

This is strictly better than the generic hash fallback because:
  - Uses the real UniXcoder 50265-token BPE vocabulary.
  - Two source files with similar UniXcoder tokenisations are nearby in space.
  - Projection matrix is fixed/reproducible.

When torch becomes available, replace with direction_c/direction_c_compute_embeddings.py
to get the full 768-dim contextual UniXcoder vectors.
"""

import os, json, math, re, hashlib, pickle
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict

# ── tunables ──────────────────────────────────────────────────────────────────
EMB_DIM   = 768
MAX_TOKS  = 512
SEED      = 42
PROJ_COLS = 3        # sparse projection ≈ Achlioptas: ±1/√3 with p=1/3

SUBJECTS = {
    "flex_v3": {
        "input_file": "FAST/input/flex_v3/flex-bbox.txt",
        "type": "sir",
    },
    "grep_v3": {
        "input_file": "FAST/input/grep_v3/grep-bbox.txt",
        "type": "sir",
    },
    "gzip_v1": {
        "input_file": "FAST/input/gzip_v1/gzip-bbox.txt",
        "type": "sir",
    },
    "make_v1": {
        "input_file": "FAST/input/make_v1/make-bbox.txt",
        "type": "sir",
    },
    "sed_v6": {
        "input_file": "FAST/input/sed_v6/sed-bbox.txt",
        "type": "sir",
    },
}


# ── deterministic sparse projection ──────────────────────────────────────────

def _build_projection_row(token_id: int, dim: int = EMB_DIM) -> np.ndarray:
    """Return a deterministic dense row for token_id using sparse RP."""
    rng = np.random.RandomState(token_id & 0xFFFFFFFF)
    row = np.zeros(dim, dtype=np.float32)
    # Each dimension gets ±1/√3 with probability 1/3 each, else 0
    u = rng.uniform(size=dim)
    val = math.sqrt(3.0)
    row[u < 1/3]              = +val
    row[(u >= 1/3) & (u < 2/3)] = 0.0
    row[u >= 2/3]             = -val
    return row


def build_vocab_projection(vocab_size: int, dim: int = EMB_DIM) -> np.ndarray:
    """Pre-compute the (vocab_size, dim) projection matrix."""
    print(f"Building projection matrix ({vocab_size} × {dim})…", end=" ", flush=True)
    P = np.zeros((vocab_size, dim), dtype=np.float32)
    for tid in range(vocab_size):
        P[tid] = _build_projection_row(tid, dim)
    print("done")
    return P


# ── tokenizer helpers ─────────────────────────────────────────────────────────

def load_tokenizer(tok_dir: str = "unixcoder_tok"):
    """Load UniXcoder BPE tokenizer from local files."""
    from tokenizers import Tokenizer
    from tokenizers.models import BPE
    from tokenizers.pre_tokenizers import ByteLevel
    from tokenizers.processors import RobertaProcessing
    from tokenizers.decoders import ByteLevel as ByteLevelDecoder

    vocab_path  = Path(tok_dir) / "vocab.json"
    merges_path = Path(tok_dir) / "merges.txt"

    with open(vocab_path, encoding="utf-8") as f:
        vocab = json.load(f)
    with open(merges_path, encoding="utf-8") as f:
        # skip header line
        merges = [tuple(line.strip().split()) for line in f if not line.startswith("#")]

    bpe = BPE(vocab=vocab, merges=merges, unk_token="<unk>")
    tokenizer = Tokenizer(bpe)
    tokenizer.pre_tokenizer = ByteLevel(add_prefix_space=False)
    tokenizer.decoder       = ByteLevelDecoder()

    # Add special tokens matching RoBERTa
    tokenizer.add_special_tokens(["<s>", "</s>", "<unk>", "<pad>", "<mask>"])

    print(f"Tokenizer loaded: {tokenizer.get_vocab_size()} tokens")
    return tokenizer


def tokenize(tokenizer, text: str, max_length: int = MAX_TOKS) -> np.ndarray:
    """Return truncated token-id array."""
    enc = tokenizer.encode(text, add_special_tokens=True)
    ids = enc.ids[:max_length]
    return np.array(ids, dtype=np.int32)


# ── IDF weighting ─────────────────────────────────────────────────────────────

def compute_idf(all_doc_ids: List[np.ndarray], vocab_size: int) -> np.ndarray:
    """Compute IDF vector over the corpus of token-id lists."""
    df = np.zeros(vocab_size, dtype=np.float32)
    for ids in all_doc_ids:
        for tid in np.unique(ids):
            if 0 <= tid < vocab_size:
                df[tid] += 1.0
    N    = len(all_doc_ids)
    idf  = np.log((N + 1) / (df + 1)) + 1.0   # sklearn smooth-IDF
    return idf


# ── embedding computation ─────────────────────────────────────────────────────

def embed(token_ids: np.ndarray, P: np.ndarray, idf: np.ndarray) -> np.ndarray:
    """Weighted sparse-RP embedding for one document."""
    vocab_size = P.shape[0]
    vec = np.zeros(P.shape[1], dtype=np.float32)
    for tid in token_ids:
        if 0 <= tid < vocab_size:
            vec += P[tid] * idf[tid]
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec /= norm
    return vec


# ── input parsing ─────────────────────────────────────────────────────────────

def read_tests(input_file: str) -> Tuple[List[str], List[str]]:
    """Parse FAST bbox input lines into (test_name, source_text) pairs."""
    texts, names = [], []
    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        for idx, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                continue
            m = re.search(r"-C\[([^\]]+)\]", line)
            name = m.group(1) if m else f"test_{idx:04d}"
            texts.append(line)
            names.append(name)
    return texts, names


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 72)
    print("Direction C  —  Phase 1 (vocab-anchored BPE embeddings)")
    print("UniXcoder tokenizer  +  sparse random projection  +  IDF weighting")
    print("=" * 72)

    out_dir = Path("embeddings")
    out_dir.mkdir(exist_ok=True)

    # Load tokenizer
    tokenizer  = load_tokenizer("unixcoder_tok")
    vocab_size = tokenizer.get_vocab_size()

    # Build projection matrix (fixed, fast)
    P = build_vocab_projection(vocab_size)

    metadata = {}

    for subject, cfg in SUBJECTS.items():
        ifile = cfg["input_file"]
        if not Path(ifile).exists():
            print(f"\n[SKIP] {subject}: {ifile} not found")
            continue

        print(f"\n{'─'*60}")
        print(f"  {subject}")
        texts, names = read_tests(ifile)
        print(f"  {len(texts)} test entries loaded")

        # Tokenize all
        all_ids = [tokenize(tokenizer, t) for t in texts]

        # IDF over this subject's corpus
        idf = compute_idf(all_ids, vocab_size)

        # Embed
        embs = np.stack([embed(ids, P, idf) for ids in all_ids], axis=0).astype(np.float32)
        print(f"  Embedding shape: {embs.shape}")

        # Verify L2 norms ≈ 1
        norms = np.linalg.norm(embs, axis=1)
        print(f"  Norm: min={norms.min():.4f}  mean={norms.mean():.4f}  max={norms.max():.4f}")

        # Save
        np.save(out_dir / f"{subject}_embeddings.npy", embs)
        with open(out_dir / f"{subject}_test_names.json", "w") as f:
            json.dump(names, f, indent=2)

        metadata[subject] = {
            "n_tests":       int(embs.shape[0]),
            "embedding_dim": int(embs.shape[1]),
            "dtype":         str(embs.dtype),
            "norm":          "L2",
            "type":          cfg["type"],
            "source":        "unixcoder_bpe_idf_rp",
            "vocab_size":    vocab_size,
        }
        print(f"  ✓ saved  {subject}_embeddings.npy  and  {subject}_test_names.json")

    with open(out_dir / "embedding_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print("\n" + "=" * 72)
    print("Summary")
    print("=" * 72)
    total = sum(m["n_tests"] for m in metadata.values())
    print(f"  Subjects:  {len(metadata)}")
    print(f"  Tests:     {total}")
    print(f"  Dim:       {EMB_DIM}")
    print(f"  Storage:   ~{total * EMB_DIM * 4 / 1e6:.1f} MB")
    print(f"\n  Next: python direction_c/direction_c_feature_matrix.py")
    print("=" * 72)


if __name__ == "__main__":
    main()
