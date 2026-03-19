Repository Intelligence Platform
Architecture Document — Repository Ingestion Pipeline
1. Overview

The Repository Ingestion Pipeline is responsible for transforming a raw source-code repository into a structured knowledge representation that can be used for:

repository insights

architectural understanding

flow reconstruction

optimization detection

chatbot interaction

diagram generation

The ingestion pipeline converts a repository into:

Abstract Syntax Trees (AST)

normalized code entities

traceability metadata

dependency graphs

function specifications

The system is designed to be:

scalable for very large repositories

language extensible

deterministic where possible

minimally dependent on LLM reasoning

The initial implementation supports the Python language with a plugin-based architecture for future expansion.

2. Architectural Goals

The ingestion architecture is designed with the following objectives:

Scalability

Support repositories with thousands of files and millions of lines of code.

Deterministic Analysis

Use static analysis (AST parsing) rather than relying on LLM interpretation of raw code.

Structured Metadata Generation

Convert code into structured representations such as entities, relationships, and metadata graphs.

Language Extensibility

Enable support for additional languages through plugins.

LLM-Assisted Reasoning

Use LLMs only for high-level reasoning such as functionality descriptions.

Models used may include:

Gemini

NVIDIA NIM

3. High-Level Pipeline Architecture

The repository ingestion pipeline consists of multiple sequential processing stages.

Repository
    │
    ▼
Repository Scanner
    │
    ▼
File Classification
    │
    ▼
AST Generation
    │
    ▼
Entity Extraction
    │
    ▼
Traceability Graph Builder
    │
    ▼
Functionality Spec Generator
    │
    ▼
Metadata Aggregation
    │
    ▼
Knowledge Store

Each stage produces artifacts that are consumed by subsequent stages.

4. Component Architecture
4.1 Repository Scanner
Purpose

The repository scanner performs initial discovery and builds an index of all files.

Responsibilities

Traverse repository directories

Identify source code files

Detect programming languages

Generate repository metadata

Input
Repository Path
Output
repo_metadata.json
file_index.json

Example metadata:

repo_name
languages_detected
total_files
source_file_count
directory_structure
4.2 File Classifier
Purpose

Classify files into meaningful categories to filter out non-relevant files.

Responsibilities

Filter test files

Ignore build artifacts

Ignore virtual environments

Identify application layers

Example Categories
controllers
services
repositories
models
utilities
Output
classified_files.json
4.3 AST Generation
Purpose

Convert source code into Abstract Syntax Trees for deterministic analysis.

For Python files, AST parsing uses the built-in Python AST module.

Responsibilities

Parse each source file

Generate structured AST representation

Capture syntactic constructs

Extracted Elements
imports
classes
functions
decorators
method calls
variables
Output
asts/
   file_name.ast.json
4.4 Entity Extraction
Purpose

Transform AST structures into normalized code entities.

Entity Types
Repository
Module
File
Class
Function
Method
Import
Example Entity
Function
name: login
file: auth_controller.py
parameters: username,password
class: AuthController
Output
entities.json
4.5 Traceability Graph Builder
Purpose

Construct a graph of relationships between code entities.

This graph forms the foundation for:

flow reconstruction

dependency analysis

architecture discovery

Relationship Types
CALLS
IMPORTS
DEFINES
BELONGS_TO
DEPENDS_ON
Example Traceability Graph
AuthController.login
      │
      CALLS
      ▼
AuthService.authenticate
      │
      CALLS
      ▼
UserRepository.find_user
Output
traceability_graph.json
4.6 Functionality Specification Generator
Purpose

Generate human-readable descriptions of code functionality.

This stage uses LLM reasoning based on structured metadata rather than raw code.

LLMs used may include:

Gemini

NVIDIA NIM

Input
Function Metadata
Call Graph
Dependencies
Parameters
Output
function_specs.json

Example:

Function: login

Purpose:
Handles user authentication requests and delegates authentication to AuthService.

Inputs:
username
password

Dependencies:
AuthService
4.7 Metadata Aggregation
Purpose

Aggregate outputs from all ingestion stages into a unified knowledge representation.

Aggregated Data
repository metadata
file index
entities
dependency graph
call graph
function specifications
traceability metadata
Output
repo_analysis/

repo.json
entities.json
traceability_graph.json
function_specs.json
5. Knowledge Store Design

The ingestion pipeline produces a structured knowledge store used by downstream systems such as agents and chatbots.

Metadata Types
Repository Metadata
File Metadata
Function Metadata
Call Graph
Dependency Graph
Traceability Graph
Functional Specifications
Storage Format

Initial implementation may use JSON-based storage.

Future implementations may leverage:

graph databases

vector stores

hybrid knowledge graphs

6. Parallel Processing Architecture

Large repositories require parallel processing to reduce ingestion time.

Parallelizable Stages
AST Generation
Entity Extraction
Spec Generation
Worker Pool Architecture
File Index
    │
    ▼
Worker Pool
    │
    ▼
AST Extraction
    │
    ▼
Entity Extraction

This design enables processing thousands of files efficiently.

7. Extensibility Design

The ingestion pipeline supports additional languages via a plugin architecture.

Each plugin must implement:

Language Detection
AST Parsing
Entity Extraction
Relationship Extraction

Future language support may leverage Tree-sitter for multi-language parsing.

8. Error Handling and Resilience

The ingestion pipeline must be resilient to malformed or incomplete code.

Strategies

Skip files with parsing errors

Log failures with metadata

Continue pipeline execution

Error logs should capture:

file path
error type
stack trace
9. Integration with Agent Systems

Once ingestion completes, the metadata becomes accessible to agents implemented using Agno.

Agents can query the knowledge store to generate:

architecture diagrams

flow diagrams

performance insights

optimization recommendations

Outputs may include:

Mermaid diagrams

text explanations

code examples

10. Future Enhancements

Future improvements to the ingestion pipeline may include:

Multi-Language Support

Extending the plugin system for Java, Go, and JavaScript.

Framework Detection

Automatic detection of frameworks such as:

Django

FastAPI

Flask

Advanced Static Analysis

Detection of performance issues and architectural anti-patterns.

Continuous Ingestion

Support for incremental ingestion when repositories change.