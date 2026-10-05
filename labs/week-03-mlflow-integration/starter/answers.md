False Positives: 19
False Negatives: 32
Exercise 3:
1. Do F1 and ROC-AUC pick the same winner?

No. F1 evaluates the model at a single, fixed threshold (0.5) and is highly sensitive to class imbalance. ROC-AUC evaluates the model's ranking performance globally across all possible thresholds.

2. Chosen run and justification:
Run ID: cee206e472d541869696d28391a32332 (Random Forest, n_estimators=300)

In medical screening, minimizing false negatives is critical. This model has the highest recall (0.5821) and F1 score, meaning it most reliably identifies actual diabetic patients at the default threshold.

3. Automatically recorded feature:
The Git commit hash (via the git_commit tag). MLflow automatically links the run to the exact code version that produced it without you having to remember it.

Exercise 6:
1. Write the traceability chain as an ordered list of lookups, starting from models:/diabetes-classifier@staging. What call do you make at each hop?

Alias -> Version: client.get_model_version_by_alias()
Version -> Run ID: Read the run_id attribute from the version
Run ID -> Params/Tags/Metrics: client.get_run()
Git Commit -> Code: git checkout <hash> or git diff <hash> --

2. What did hop 4 give you in Part 2, concretely? What did recording git_dirty fix, and what does it still not give you?

Hop 4 gave: The exact code snapshot at the time of the run
git_dirty fixed: The "lying commit" problem (where a commit hash is recorded, but uncommitted local changes were actually executed)
It still lacks: The state of the data (file contents) and the exact Python environment/dependencies

3. Should promote_to_staging refuse a version whose source run had git_dirty=true? Take a side, and name what your choice costs.
Yes. Guaranteeing strict reproducibility is critical for staging/production. The cost is developer velocity: it forces developers to make "WIP" (Work In Progress) commits just to test the full pipeline

4. What can an alias do that a fixed Staging stage could not? Give at least two things

You can use custom, arbitrary names (e.g., @challenger, @shadow).
Multiple aliases can point to the same version simultaneously, enabling flexible A/B testing

5. Walk the chain as far back as it goes. It ends at a file path — data/diabetes.csv. What does that mean for the metrics you just recorded, and what would you need in order to close that last gap?

Because it ends at a local, mutable file path, your metrics are not perfectly reproducible if someone alters the CSV file. To close this gap, you need data versioning (e.g., DVC, Delta Lake, or immutable object storage URIs)

Exercise 7:
1. What changed when you rolled back, and what did not? Think of a server that loads models:/diabetes-classifier@champion.

Changed: The alias pointers (@staging and @champion) moved from version 3 back to version 2. A server polling models:/diabetes-classifier@champion would now fetch version 2
Did not change: The versions themselves (they are immutable), their source runs, and their original parameters/metrics

2. A month from now, how would an auditor learn that version 3 was champion for a while? What would they have if roll_back did not write tags?
They would look at the tags on Version 3. roll_back recorded rolled_back_at, rolled_back_to, and rollback_reason on Version 3 before moving the alias. If roll_back did not write these tags, there would be zero historical record that Version 3 was ever promoted, because the MLflow database only stores the current state of aliases.

3. Look at line 4 of your last make trace. Was version 2 a safe rollback target?
No, it was not. Line 4 states tree state not recorded: nothing says this commit is the code that ran. Version 2 was promoted before git_dirty was implemented (it was a dirty run), meaning it is impossible to guarantee what exact code produced it, making it an unsafe target for a production rollback.