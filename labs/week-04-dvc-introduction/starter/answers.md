Exercise 2:
1. What did Git gain in this commit, and about how many bytes is it? What did Silo gain? Why is that difference the whole idea of DVC?

Git gained the data/measurements.csv.dvc pointer file and .gitignore (only about 100-200 bytes). Silo gained the actual heavy data blob (measurements.csv). This is the core idea of DVC: keeping large data out of the Git history to prevent repository bloat, while still versioning it using tiny text pointers.

2. A classmate runs make build-data with the same batch and gets a byte-identical .dvc file. Name two things build_measurements does to make that true, and one thing that would break it.

Two things it does: It exports the CSV without the index (index=False) and enforces consistent Unix line endings (lineterminator="\n"). One thing that would break it: Allowing pandas to use the default OS-dependent line endings (which would write \r\n on Windows and change the file's MD5 hash).

3. A teammate clones the repository. They have data/measurements.csv.dvc but no data/measurements.csv. What single command do they run, and what two things must be true for it to work?

Command: uv run dvc pull
Two things that must be true: 1. The teammate must have the correct AWS/Silo authentication credentials in their environment. 2. The actual data blob matching the hash in the .dvc file must have been pushed to and still exist in the remote Silo bucket.

Exercise 4:
1. Time travel took two commands. What did git checkout change on disk, what did dvc checkout change, and why can neither do the other's job?

git checkout changed the lightweight .dvc pointer file (updating the MD5 hash in the text file)
dvc checkout read that pointer file and changed the actual, heavy measurements.csv data file on disk by replacing it with the corresponding version from the DVC cache.
Neither can do the other's job because Git does not track the heavy data blob (it only sees the pointer), and DVC does not version control the project's history (it relies on Git to tell it which pointer is currently active).

2. You try the same time travel on a laptop that never pulled version 1. What happens?
git checkout will successfully change the .dvc pointer. However, dvc checkout will fail because the physical data blob corresponding to Version 1's MD5 hash is not in the local DVC cache. You would have to run dvc pull first to download the missing data from the remote Silo bucket.

Exercise 5:

1. List the deps of your evaluate stage. Pick one and say what happens if it is missing from the list. Does the pipeline fail, or does it run and give a wrong result?

The dependencies: data/processed/test.csv, models/model.pkl, src/week_04_dvc_introduction/model.py, and src/week_04_dvc_introduction/pipeline.py
If you omit models/model.pkl, the pipeline will run without failing, but it will give a wrong result. DVC will not know that evaluate needs to re-run when the model is retrained, leaving you with stale metrics from an older model.

2. Version 3 has the same 768 rows as data/diabetes.csv. Compare make metrics with the course's pinned baseline (accuracy 0.7344, F1 0.5785). They differ. Explain why "the same rows" is not "the same dataset".

My Version 3 metrics (Accuracy 0.7656, F1 0.6154) differ from the baseline because the row order is different. Since the data was assembled chronologically from three separate batches rather than read from one original file, train_test_split partitions the rows differently (even with the same random seed). A different train/test split yields a different model and different metrics.

Exercise 6: 
1. a) MLflow's digest has 8 characters; DVC's md5 has 32. What does each one hash? Which would you give an auditor who asks you to prove which bytes trained this model? What is the other one good for?

MLflow digest hashes: The logical data content in memory (schema and rows), ignoring the file format
DVC md5 hashes: The exact physical bytes of the file on disk
For the auditor: Give them the DVC md5, because it proves the exact byte-for-byte file that was used

1. b) What the other is good for: 
The MLflow digest is useful for checking if two datasets contain the same information, even if they are saved in different formats (e.g., CSV vs. Parquet).

2. Run make runs-for-data and write down the filter string it used. What question does it answer that Week 3 could not?

Filter string: tags.dvc_md5 = '<your_dvc_hash>'
Question answered: "Which exact dataset version was used to train this model?" Week 3 tracked the code and parameters, but it could not track which data file was used.

3. Run make trace and compare it with Week 3's output. Which line is new? Is the chain now complete, or is there still a link you cannot follow?

New line: 5. Data version: (showing the DVC md5 and Silo URI)
Is the chain complete? Yes, the chain is now complete. We can trace a deployed alias back to the model version, the run, the exact code commit, and the exact data bytes. There are no missing links