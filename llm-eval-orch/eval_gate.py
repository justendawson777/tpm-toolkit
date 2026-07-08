import numpy as np
import time

def evaluate_batch_vectorized(model_outputs: list, ground_truths: list, threshold: float = 0.85):
    """Uses vectorized token-matching matrix operations instead of slow for-loops."""
    start_time = time.perf_counter()
    
    # 1. Build a unique vocabulary across all strings
    all_words = list(set(" ".join(model_outputs + ground_truths).lower().split()))
    vocab_idx = {word: i for i, word in enumerate(all_words)}
    
    # 2. Pre-allocate optimized NumPy arrays (contiguous memory blocks)
    num_samples = len(model_outputs)
    vocab_len = len(all_words)
    out_matrix = np.zeros((num_samples, vocab_len), dtype=np.int32)
    truth_matrix = np.zeros((num_samples, vocab_len), dtype=np.int32)
    
    # 3. Fast population of the matrices
    for idx, (out, truth) in enumerate(zip(model_outputs, ground_truths)):
        for word in out.lower().split():
            out_matrix[idx, vocab_idx[word]] += 1
        for word in truth.lower().split():
            truth_matrix[idx, vocab_idx[word]] += 1

    # 4. Vectorized Dot-Product (calculating Jaccard/overlap token similarity instantly)
    intersection = np.minimum(out_matrix, truth_matrix).sum(axis=1)
    union = np.maximum(out_matrix, truth_matrix).sum(axis=1)
    
    # Prevent division by zero errors cleanly
    scores = np.divide(intersection, union, out=np.zeros_like(intersection, dtype=float), where=union!=0)
    
    # Vectorized boolean masking to determine pass/fail
    passed_ci_cd = scores >= threshold
    pass_percentage = (np.sum(passed_ci_cd) / num_samples) * 100
    
    duration = time.perf_counter() - start_time
    return {
        "pass_rate_percent": round(pass_percentage, 2),
        "avg_score": round(float(np.mean(scores)), 3),
        "execution_time_seconds": round(duration, 5)
    }

if __name__ == "__main__":
    # Mocking 10,000 CI/CD test cases
    mock_outputs = ["the system successfully executed the script context"] * 10000
    mock_truths = ["the system successfully executed the script code"] * 10000
    
    print(" Evaluating 10,000 test cases with vectorized NumPy matrix processing...")
    metrics = evaluate_batch_vectorized(mock_outputs, mock_truths)
    
    print(f" Evaluation Complete in {metrics['execution_time_seconds']} seconds.")
    print(f" CI/CD Gate Metrics: {metrics}")
