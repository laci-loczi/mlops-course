False Positives: 19
False Negatives: 32

1. Do F1 and ROC-AUC pick the same winner?

No. F1 evaluates the model at a single, fixed threshold (0.5) and is highly sensitive to class imbalance. ROC-AUC evaluates the model's ranking performance globally across all possible thresholds.

2. Chosen run and justification:
Run ID: cee206e472d541869696d28391a32332 (Random Forest, n_estimators=300)

In medical screening, minimizing false negatives is critical. This model has the highest recall (0.5821) and F1 score, meaning it most reliably identifies actual diabetic patients at the default threshold.

3. Automatically recorded feature:
The Git commit hash (via the git_commit tag). MLflow automatically links the run to the exact code version that produced it without you having to remember it.