from collections import Counter
import numpy as np

def get_char_ngrams(sentence, n):
    """Generate character n-grams from a sentence."""
    sentence = sentence.replace(" ", "")  # Remove spaces for chrF
    return [sentence[i : i + n] for i in range(len(sentence) - n + 1)]

def precision_recall(reference, hypothesis, n):
    """Calculate precision and recall for character n-grams."""
    ref_ngrams = get_char_ngrams(reference, n)
    hyp_ngrams = get_char_ngrams(hypothesis, n)

    ref_count = Counter(ref_ngrams)
    hyp_count = Counter(hyp_ngrams)

    common_ngrams = ref_count & hyp_count
    true_positives = sum(common_ngrams.values())

    precision = true_positives / max(len(hyp_ngrams), 1)
    recall = true_positives / max(len(ref_ngrams), 1)

    return precision, recall

def f_score(precision, recall, beta=1):
    """Calculate the F1 score."""
    if precision + recall == 0:
        return 0.0
    return (1 + beta**2) * (precision * recall) / (beta**2 * precision + recall)

def chrF(reference, hypothesis, max_n=6, beta=2):
    """Calculate the chrF score from scratch."""
    precisions = []
    recalls = []

    for n in range(1, max_n + 1):
        precision, recall = precision_recall(reference, hypothesis, n)
        precisions.append(precision)
        recalls.append(recall)

    avg_precision = sum(precisions) / max_n
    avg_recall = sum(recalls) / max_n

    return f_score(avg_precision, avg_recall, beta)

# From scratch implementation f1score 3 class
def calculate_f1(true_labels, pred_labels, num_classes):
    f1_scores = []

    for i in range(num_classes):
        TP = np.sum((true_labels == i) & (pred_labels == i))  # True Positives
        FP = np.sum((true_labels != i) & (pred_labels == i))  # False Positives
        FN = np.sum((true_labels == i) & (pred_labels != i))  # False Negatives

        precision = TP / (TP + FP) if (TP + FP) > 0 else 0
        recall = TP / (TP + FN) if (TP + FN) > 0 else 0

        # Calculate F1 score
        f1 = (
            2 * (precision * recall) / (precision + recall)
            if (precision + recall) > 0
            else 0
        )
        f1_scores.append(f1)

    macro_f1 = np.mean(f1_scores)

    return macro_f1