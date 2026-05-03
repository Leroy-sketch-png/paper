#!/usr/bin/env python3
"""
Direction C - Phase 2: Feature Matrix Generation

Loads computed UniXcoder embeddings and converts them to sklearn-compatible
feature matrices for ML training (MART, ACER-PA, etc).

Input: embeddings/{subject}_embeddings.npy from direction_c_compute_embeddings.py
Output: feature_matrices/{subject}_features.pkl (sklearn-compatible)
"""

import os
import json
import pickle
import numpy as np
from pathlib import Path
from typing import Dict, Tuple


def split_train_test(
    X: np.ndarray,
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[np.ndarray, np.ndarray]:
    """Deterministic split with NumPy fallback when sklearn is unavailable."""
    n_samples = X.shape[0]
    if n_samples == 0:
        return X, X

    indices = np.arange(n_samples)
    rng = np.random.RandomState(random_state)
    rng.shuffle(indices)

    n_test = max(1, int(round(n_samples * test_size)))
    n_test = min(n_test, n_samples - 1) if n_samples > 1 else 1

    test_idx = indices[:n_test]
    train_idx = indices[n_test:]

    return X[train_idx], X[test_idx]

def load_embeddings(embeddings_dir: str = "embeddings") -> Dict[str, np.ndarray]:
    """Load all computed embeddings from directory."""
    embeddings_path = Path(embeddings_dir)
    
    embeddings = {}
    metadata = {}
    
    # Load metadata
    metadata_file = embeddings_path / "embedding_metadata.json"
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
    
    print(f"Loading embeddings from {embeddings_dir}")
    
    for subject in metadata.keys():
        emb_file = embeddings_path / f"{subject}_embeddings.npy"
        if emb_file.exists():
            emb = np.load(emb_file)
            embeddings[subject] = emb
            print(f"  ✓ {subject}: shape {emb.shape}")
        else:
            print(f"  ✗ {subject}: embeddings not found")
    
    return embeddings, metadata

def create_feature_matrices(
    embeddings: Dict[str, np.ndarray],
    metadata: Dict,
    test_split: float = 0.2,
    random_state: int = 42
) -> Dict[str, Dict]:
    """
    Convert embeddings to train/test feature matrices.
    
    Matches the split used in FALCON paper (80/20).
    
    Returns:
        {subject: {"X_train": ..., "X_test": ..., "n_train": ..., "n_test": ...}}
    """
    feature_matrices = {}
    
    for subject, emb in embeddings.items():
        n_samples = emb.shape[0]
        
        # 80/20 split (same as FALCON); implemented with NumPy to avoid hard sklearn dependency.
        X_train, X_test = split_train_test(
            emb,
            test_size=test_split,
            random_state=random_state
        )
        
        n_train = X_train.shape[0]
        n_test = X_test.shape[0]
        
        feature_matrices[subject] = {
            "X_train": X_train.astype(np.float32),
            "X_test": X_test.astype(np.float32),
            "n_train": n_train,
            "n_test": n_test,
            "embedding_dim": X_train.shape[1],
            "type": metadata[subject].get("type", "unknown")
        }
        
        print(f"{subject}: train={n_train}, test={n_test}, dim={X_train.shape[1]}")
    
    return feature_matrices

def save_feature_matrices(feature_matrices: Dict, output_dir: str = "feature_matrices"):
    """Save feature matrices as pickle files."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print(f"\nSaving feature matrices to {output_dir}")
    
    for subject, matrices in feature_matrices.items():
        pkl_file = output_path / f"{subject}_features.pkl"
        with open(pkl_file, 'wb') as f:
            pickle.dump(matrices, f)
        print(f"  ✓ {subject}: {pkl_file}")

def main():
    print("=" * 80)
    print("Direction C - Phase 2: Feature Matrix Generation")
    print("=" * 80)
    
    # Load embeddings
    embeddings, metadata = load_embeddings()
    
    if not embeddings:
        print("\nERROR: No embeddings found. Run direction_c_compute_embeddings.py first.")
        return
    
    # Create feature matrices
    print("\nCreating train/test splits (80/20)...")
    feature_matrices = create_feature_matrices(embeddings, metadata)
    
    # Save
    save_feature_matrices(feature_matrices)
    
    # Summary
    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    
    total_train = sum(m["n_train"] for m in feature_matrices.values())
    total_test = sum(m["n_test"] for m in feature_matrices.values())
    
    print(f"\nTotal training samples: {total_train}")
    print(f"Total test samples: {total_test}")
    print(f"Embedding dimension: 768")
    
    print("\nFeature matrices ready for ML training:")
    print("  - MART re-training: feature_matrices/*_features.pkl")
    print("  - ACER-PA re-training: feature_matrices/*_features.pkl")
    
    print("\nNext steps:")
    print("  1. Train MART on UniXcoder embeddings")
    print("  2. Train ACER-PA on UniXcoder embeddings")
    print("  3. Compare APFD vs handcrafted features")
    print("  4. Compute ranking correlation (Spearman ρ)")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
