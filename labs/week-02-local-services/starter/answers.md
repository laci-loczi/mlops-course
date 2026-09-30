Since MiniO is not in Docker Hub anymore and moved under quay.io, I used an open source fork of MiniO, called Silo, and it seems to work fine, it doesnt require a login like quay.io.  
  
**Which storage plane holds which data?**

**MinIO** (**Silo** in this case): Stores large, unstructured artifacts (eg: model.pkl, plots, configs)
**Postgres**: Stores structured metadata (eg: run ID, parameters, metrics).

**Why are model files not stored in Postgres?**

**Performance**: Storing large binary files bloats the database, slowing down queries
**Scalability**: Object stores are purpose-built for cheap, infinitely scalable file storage
**Ecosystem**: ML tools natively expect to load models from file systems or APIs, not from SQLrows

**Now that runs are centrally recorded, what can you answer that you could not answer after Week 1?**

**Reproducibility**: We can permanently link a specific performance (eg: 78.1% accuracy) to the exact parameters and model artifact that produced it, even after the treminal is closed
**Comparability**: We can compare multiple runs side-by-side in the UI to see exact deltas (eg: seed 7 outperformed seed 42 by approx 4.7% in accuracy), instead of relying on closed terminal scroll back
**Shareability**: We can share a single URL to a server as a single source of truth, rather than locally copying and pasting terminal logs that nobody else can verify