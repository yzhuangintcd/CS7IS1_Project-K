# Knowledge and Data Engineering: CS7IS1 

This repository contains group K's Knowledge Graph portfolio tasks for the CS7IS1 module.

## Table of Contents
1. Project Overview
2. Repository Structure
3. Datasets
4. Project Phases & Deliverables
5. Setup & Execution

## Project Overview
This project focuses on building a Semantic Web Knowledge Graph centered around Irish Tourism. It integrates flat data into a linked RDF graph, allowing for complex spatial SPARQL queries (e.g., finding overlapping places or aggregating accommodations near specific cultural monuments) to support itinerary planning.

## Repository Structure
- Dataset/: Contains the original raw CSV files.
- Cleaned_Dataset/: Contains the processed CSV files with standardized coordinate systems (converted from ITM to WGS84 Lat/Long) and normalized columns.
- `cleaning_mesuem_data.py`: Python script used for data preprocessing, dropping unnecessary columns, and mapping geospatial coordinates.
- `requirements.txt`: Python dependencies required for data cleaning (e.g., pandas, pyproj).

## Datasets
The knowledge graph is built from Irish tourism and heritage datasets:
- Museums__Collections___Archives_2015.csv


## Project Phases & Deliverables

Steps 1-2 are completed

### Step 3. Solution Design Requirements (In progress)

- Ontology Design (Schema): A W3C-compliant custom ontology defining a minimum of 8 classes (including Place, Accommodation, Attraction, Museum, Monument), 6 object properties (including symmetric, transitive, and inverse properties like locatedInRegion and isNear), and 4 data properties (e.g., latitude, longitude). Includes a maximum of 3 external interlinks to the LODcloud.

- Data Uplift (RML Mapping): RML/YARRRML scripts converting the cleaned CSV rows into at least 30 valid RDF instance triples, restructuring the data to fit the custom ontology rather than performing a 1-to-1 column dump.

- SHACL Validation: 3 custom SHACL shapes enforcing integration rules, such as requiring valid names and spatial coordinates for geographic entity matching.

- GraphDB & SPARQL: 7 distinct SPARQL queries demonstrating advanced clauses (FILTER, GROUP BY, aggregations, etc.) executed against the final triplestore to extract insights.

## Setup & Execution

### Data Preparation:
Install the local requirements via pip install -r requirements.txt. Run cleaning_mesuem_data.py to drop irrelevant columns and convert ITM coordinates to standard Lat/Long.

### Graph Generation:
Execute the RML mapping engine over the cleaned CSV files in the Cleaned_Dataset folder to generate the final Turtle (.ttl) instance file.

### Database Import:
Start a local GraphDB Free instance. Create a new repository and upload the .ttl instances along with the ontology schema, then execute the 7 SPARQL queries via the GraphDB Workbench.