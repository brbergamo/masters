# masters

# miRNA Target Query Flask App

**Project:** Web application to query miRNA gene targets from a MariaDB database  
**Course:** BF768 Bioinformatics Programming (Spring 2025)  
**Author:** Beatriz Bergamo  
**Date:** March 2025

## Overview

This project is a lightweight Flask web application designed to let users query a miRNA–gene targeting database. By entering two miRNA names and selecting a maximum score threshold, users receive a list of genes targeted by both miRNAs, sorted by the sum of targeting scores.

## Demo

Here’s a preview of the user interface:
![image](https://github.com/user-attachments/assets/ee48468c-233d-473c-8937-228588479ec6)

## Features

- Interactive form for user input (miRNA names + targeting score)
- Dynamic query to a MariaDB backend using safe SQL practices
- Results table with gene IDs, names, and scores
- Custom error messages for invalid input
- Built-in form instructions and example miRNA names

## Use Case

The app is useful for exploring co-targeting patterns in gene regulation by miRNAs, a common need in transcriptomics and regulatory genomics research.

## Technologies Used

- Python 3
- Flask
- MariaDB (MySQL-compatible)
- HTML (Jinja2 templating)

## How It Works

1. User accesses the web form.
2. Enters two miRNA names and selects a targeting score cutoff.
3. The backend checks miRNA validity and runs a parameterized query.
4. A table of co-targeted genes is returned (if any), with scores for each miRNA.
5. A summary statement reports the query criteria and number of hits.
