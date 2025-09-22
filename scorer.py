from typing import List
import numpy as np
import pandas as pd

def compute_f1(real_indices: List[int], pred_indices: List[int]) -> float:
    if not pred_indices or not real_indices:
        return 0.0
    true_positives = len(set(real_indices) & set(pred_indices))
    precision = true_positives / len(pred_indices) if pred_indices else 0.0
    recall = true_positives / len(real_indices) if real_indices else 0.0
    if precision + recall == 0:
        return 0.0
    f1 = 2 * (precision * recall) / (precision + recall)
    return f1

def evaluate_f1_scores(data: pd.DataFrame):
    f1_scores = []
    for _, example in data.iterrows():  
        real_indices = example["real_index"]
        pred_indices = example["pred_index"]
        f1 = compute_f1(real_indices, pred_indices)
        f1_scores.append(f1)
        # print(f"Real indices: {real_indices}, Pred indices: {pred_indices}, F1: {f1:.4f}")
    mean_f1 = np.mean(f1_scores) if f1_scores else 0.0
    return mean_f1

