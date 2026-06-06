# Homework 5: Ontology-based Semantic Grounding

This folder contains the specification and starter ontology resources for Homework 5 in the AI Capstone course.

## Files

- `Homework 5 Ontology-based Semantic Grounding.pdf`  
  The full homework specification. Students should read this document carefully before starting the assignment. It defines the task objective, required repository structure, ontology requirements, reasoning workflow, SPARQL query requirements, and grading criteria.

- `course-affordance.ttl`  
  The shared course ontology for affordance-based semantic grounding. Students should import or reuse this vocabulary when building their group ontology.

- `course-alignment.ttl`  
  The alignment ontology that connects the course vocabulary to broader semantic references where appropriate. Students may inspect it to understand how course terms are positioned relative to external or upper-level semantic structures.

## Submission Reminder

Each group should submit a GitHub repository following the structure specified in the homework document. The submitted repository should include the group-authored ontology, imported ontology files, inferred results, SPARQL queries, query outputs, screenshots when appropriate, and a report or README explaining the modeling and reasoning workflow.

## Assessment Note: Ontology Documentation Verification with Widoco

As part of the assessment of ontology completeness and readability, groups are encouraged to check whether their ontology can be successfully processed by [Widoco](https://github.com/dgarijo/Widoco), a tool for generating ontology documentation from OWL/RDF ontology files. 

Widoco generation is not the only criterion for evaluating the group ontology. However, it will be used as one practical verification tool for checking whether the submitted ontology is sufficiently well-formed, structurally complete, and readable for automatic documentation. If Widoco can generate documentation from your ontology without major errors, this is a good indication that the ontology file is suitable for further inspection and reuse.

A reference command is shown below:

```bash
java -jar widoco-{{version-number}}-jar-with-dependencies_JDK-17.jar \
  -ontFile course-affordance.ttl \
  -outFolder docs \
  -rewriteAll \
  -uniteSections
```

Questions about the homework may be sent to: `ccy@hptp.org`.
