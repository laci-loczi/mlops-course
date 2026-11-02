Exercise 2:
1. Which group is the model worst on, and by how much against the aggregate? How far can you trust that gap, given the group's n?

The model is worst on the age band 50 plus: ROC AUC 0.6071 against the aggregate 0.8345 (about 0.23 lower), and its fpr of 0.4167 is six times the 0.0685 of the 21-29 group. With only n 19 (7 positives, 12 negatives) the uncertainty on that AUC is very wide, so the gap is a strong warning sign but not a proven effect.

2. What can you do with this finding now, and what would you need before you act on it?

Now I can report it and keep 50+ as a monitored slice, so nobody reads the aggregate as "good for everyone". Before acting (retraining, reweighting, or blocking the model for older patients) I would need more 50+ patients, or at least a bootstrap/cross-validated confidence interval, to confirm the gap is real and not noise from 19 rows.

3. One group has an F1 of 0.0000 and a ROC AUC of 1.0000 on the same patients. How can both be correct, and what do they tell you about that group?

The under_normal BMI band has only 1 positive out of 30: the model gives that patient a higher probability than all 29 negatives (AUC 1.0, which ignores the threshold), but still below 0.5, so it is never predicted positive and recall and F1 are 0. With a single positive both numbers are essentially meaningless; they only say the group is almost entirely negative and too small to evaluate.

Exercise 4:
1. Week 5's gate worked because `prepare` depended on the verdict file. Why can that not work for this gate, and what replaces it?

This gate is the last stage and the thing it protects (register and promote) runs outside DVC, so there is no downstream stage that could depend on reports/gate.json. Instead `main.py gate` exits non-zero on a NO-GO so `dvc repro` fails, and `register`/`promote` call `require_go`, which refuses to release unless reports/gate.json records a GO.

2. What happens if `register` does not call `require_go`? Who would notice, and when?

The gate becomes only a suggestion: anyone can run `make register` on a NO-GO (or never-gated) model and it reaches the registry with nothing stopping it. Nobody would notice at release time; it would surface only later in production, when users, a clinic or monitoring see worse predictions, i.e. after the harm.

3. With `C: 0.005`, F1 fell by 0.1098 and ROC AUC rose. Which one is the right answer? What do you need to know about how the model is used, and what does `acceptance.regression.primary_metric` commit you to?

Both are correct: F1 scores the yes/no decisions at the 0.5 threshold (recall fell from 0.58 to 0.40, so more diabetics are missed), while ROC AUC only scores how well the probabilities rank patients, ignoring the threshold. If the model makes yes/no decisions at a fixed threshold, F1 is what matters; if it is used as a risk score for ranking, or the threshold is re-tuned, AUC matters, and `primary_metric` commits you in Git, in advance, to which one decides the verdict, so nobody can pick the better-looking number after the fact.

Exercise 5:
1. `age_band` has a selection-rate gap over 0.30, yet you gate only its TPR gap. Why is the large selection-rate gap defensible?

Diabetes prevalence really rises with age (22% positives in 21-29 against 55% in 40-49), so a correct model should flag older patients more often, and forcing equal selection rates would mean missing real cases in older groups or over-flagging young ones. What must be equal is that the true cases are found equally often in every age group, which is the TPR gap.

2. The TPR limit on `age_band` is looser than on `insulin_missing`. Why, and what would make you tighten it?

The age groups are small (31 and 19 rows, 17 and 7 positives), so one patient moves a group's TPR by 6-14 points and a tight limit would fire on noise, while insulin_missing has two large groups (88 and 104) where the gap is measured reliably. I would tighten it with more patients per age band (especially 50+), or if a larger evaluation showed a stable gap in which older patients' cases are missed.

3. This dataset has no sex, ethnicity, income or clinic column. Name one group you would want to audit this model for and cannot. What would have had to happen, and when?

I would want to audit it by ethnicity (every patient is a Pima woman, so we cannot tell how it performs on anyone else, e.g. men or other ethnic groups). That attribute, and patients from those groups, would have had to be collected at data-collection time, with consent, because it cannot be added afterwards in the evaluation pipeline.
