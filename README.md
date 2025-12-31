# Bayesian Network Inference — Likelihood Weighting (PySMILE / GeNIe)

This project implements **approximate inference** in **Bayesian Networks** using the **Likelihood Weighting** algorithm.  
The Bayesian network is loaded from a **GeNIe/SMILE `.xdsl`** file through **PySMILE** (`pysmile`).

Given:
- **evidence** (observed variables),
- a **query node**,
- a number of **samples**,

the engine estimates the **posterior distribution**:

\[
P(Query \mid Evidence)
\]

---

## Features

- Load Bayesian Networks from `.xdsl` files (GeNIe / SMILE format)
- Topological ordering of nodes (for ancestral sampling)
- Likelihood Weighting sampling:
  - observed nodes contribute to the **sample weight**
  - non-observed nodes are **sampled** from their CPT given parent assignments
- Posterior estimation from weighted samples

---

## Project Structure

├── main.py # example runner: sets evidence/query and prints posterior
├── network.py # BayesianNetwork wrapper around pysmile.Network
├── sampler.py # LikelihoodWeightingSampler implementation
├── engine.py # InferenceEngine: posterior estimation
└── complex_network.xdsl # example Bayesian network (created with GeNIe Academic)



---

## How it Works

### 1) Load the network
`BayesianNetwork` wraps `pysmile.Network` and provides helper methods for:
- getting node ids, parents, outcomes
- reading CPT definitions
- computing CPT indices given parent values (`get_cpt_index`)
- generating a **topological order** of nodes

### 2) Likelihood Weighting
For each sample:
- iterate nodes in topological order
- for an **evidence node**:
  - fix the node value to the observed outcome
  - multiply the sample weight by the probability of that outcome given the parent assignment
- for a **non-evidence node**:
  - sample an outcome from the CPT distribution given the parent assignment

The sampler returns:
- a list of samples (assignments)
- a list of weights

### 3) Posterior estimation
`InferenceEngine.estimate_posterior(...)` computes:

- weighted counts for each outcome of the query node
- normalization by total weight

and returns a `{outcome_name: probability}` dictionary.

---

## Requirements

- Python 3.10+ (any modern 3.x works)
- PySMILE (`pysmile`) + a valid SMILE license
  - `pysmile_license` must be imported **before** `pysmile.Network()`

> Note: PySMILE is not available on PyPI in the standard way. Installation depends on your SMILE/GeNIe distribution and license.

---

## Running the Example

Edit `main.py` (or keep the defaults):

```python
evidence = {"E": 0}   # observed value for node E
query = "D"
num_samples = 1000

Run:
python main.py

Example output:
Posterior distribution of 'D' given evidence:
  True: 0.XXXX
  False: 0.XXXX
