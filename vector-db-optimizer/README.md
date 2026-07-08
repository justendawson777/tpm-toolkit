# Semantic Vector DB Optimization & Storage Auditor (`/Vector_db_Optimizer`)

## Quick overview (Elevator Pitch)
A storage efficiency utility that prevents unmitigated database sprawl in Retrieval-Augmented Generation (RAG) applications. It uses generator stream architecture to flag redundant or duplicate semantic vector chunks, driving down cloud database hosting costs while boosting look-up performance.

## The Problem Statement

### Pain Point
When building RAG systems, engineering teams often blindly parse, chunk, and index massive corporate data stores without deduplication rules. This leads to bloated vector database bills (e.g., Pinecone, Milvus, pgvector) and increased index latency, causing sluggish responses for end-users.

### The Project Objective
To engineer a lightweight database auditor that scans dense embedding indices using a fixed memory footprint, identifying cold, redundant, or orphaned vectors to execute tiering strategies and lower cloud overhead.

## Program Roadmap (Phased Approach)
*   **Phase 1 (MVP):** Build a data-stream generator that processes mock vector index blocks in strict batches to preserve application memory.
*   **Phase 2 (Scalability):** Integrate native connector hooks to read directly from cloud vector database endpoints via REST APIs.
*   **Phase 3 (Enterprise):** Establish cross-organizational data retention pipelines to automate old vector lifecycle pruning.

## Cross-Functional Impact
*   **Infrastructure Engineering:** Preserves local application RAM from collapsing due to Out-Of-Memory (OOM) fatal crashes during deep audits.
*   **Finance & Leadership:** Reclaims budget wasted on hosting identical duplicate database records.
*   **Engineering Quality:** Shorter index search pools result in faster backend semantic query lookups for the user app.

## Tech Stack & Setup
*   **Tech Stack:** Python 3.11+, Native Memory Management Systems (`sys`).
*   **Setup:** Ready to execute natively with zero external package dependencies.

## Quick Start Instructions
1. Navigate to the folder: `cd tpm-toolkit/vector_db_Optimizer`
2. Execute the memory-optimized storage audit script: `python vector_cleanup.py`

## Sample Output
```text
 Beginning Vector DB storage optimization audit...
 Generator memory footprint in RAM: 200 bytes.
 Final processed records: 50000
 FinOps Savings: Reclaimed 29.30 MB of wasted vector storage space.
 Optimization script duration: 0.0125 seconds.
```

## How to Read the Output
*   **`Generator memory footprint in RAM`**: Proves that even when auditing millions of records, the script's memory profile stays flat at a few bytes rather than staging gigabytes of raw database data inside RAM.
*   **`FinOps Savings`**: Translates data cleanup directly into measurable business value by highlighting exactly how much waste was purged.
