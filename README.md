# AI Capstone 2026 - Homework 5: Ontology-based Semantic Grounding

**Group:** 11

**Members:** - 簡嫚萱、周佳瑩、劉逸安、呂杰軒、朱修毅

## 1. Selected Tasks
Our group modeled objects across all three baseline entry-level tasks:
1. **Cup Stacking** (Target: Cups)
2. **Cutlery Arrangement** (Target: Knife, Fork; Reference: Plate)
3. **Toy Block Collection** (Target: Toy Blocks; Container: Basket)

## 2. Ontology Design Overview
Our ontology is designed to provide explicit semantic grounding for physical objects perceived by the robot. We distinguish between the object's physical type (e.g., `cap:Cup`), its context-dependent task role (e.g., `cap:TargetObject`), and its manipulation affordances (e.g., `cap:GraspingAffordance`). Reference objects (`Plate`) and container objects (`Basket`) are deliberately isolated from grasping affordances to reflect their distinct roles in the manipulation pipeline.

## 3. Modeled Objects and Affordances

| Object Instance | Type (Class) | Task Role | Affordance |
| :--- | :--- | :--- | :--- |
| `:blueCup01` | `cap:Cup` | `cap:TargetObject` | `:graspAffordance` |
| `:pinkCup01` | `cap:Cup` | `cap:TargetObject` | `:graspAffordance` |
| `:knife01` | `cap:Knife` | `cap:TargetObject` | `:graspAffordance` |
| `:fork01` | `cap:Fork` | `cap:TargetObject` | `:graspAffordance` |
| `:plate01` | `cap:Plate` | `cap:ReferenceObject` | *(None required for grasping)* |
| `:block01` | `cap:ToyBlock` | `cap:TargetObject` | `:graspAffordance` |
| `:block02` | `cap:ToyBlock` | `cap:TargetObject` | `:graspAffordance` |
| `:basket01` | `cap:Basket` | `cap:ContainerTarget` | *(None required for grasping)* |

*(Note: `:graspAffordance` is instantiated as a `cap:GraspingAffordance`)*

## 4. Namespace Policy
We strictly adhere to the separation of course-level shared vocabulary and group-specific modeling:
- **`cap:`** (`<https://hcis.io/ontology/aicapstone/2026/>`): Used for the shared course vocabulary (core classes, predefined roles, affordance types, and data properties).
- **`:` (Default) / `g11:`** (`<https://hcis.io/ontology/aicapstone/group11/>`): The group-specific namespace used exclusively for our custom task-relevant instances and group-level design extensions.

## 5. Inference Mechanism & Affordance Modeling Explanation
All graspable instances in our ontology are correctly annotated with a semantic link to `cap:GraspingAffordance` (e.g., via `cap:hasAffordance :graspAffordance`) to fulfill the semantic richness requirement. 

However, due to the limited support for full OWL Description Logic (specifically existential restrictions like `owl:someValuesFrom` and `owl:intersectionOf`) in our chosen Python `OWL-RL` reasoning workflow, we simplified the inference pattern. We asserted explicit `rdfs:subClassOf` relations for the target object classes (`Cup`, `Knife`, `Fork`, `ToyBlock`) directly to `cap:GraspableObject`. This allows the reasoner to successfully infer instance graspability dynamically while retaining all affordance annotations as valid semantic grounding information in the knowledge graph.

## 6. How `inferred-results.ttl` was Generated
The `ontology/inferred-results.ttl` file was autonomously generated using our custom Python script (`src/run_inference.py`). The script parses both the base ontology and our group's ontology using `RDFLib`, initializes an `owlrl.DeductiveClosure` engine to execute forward-chaining over the `rdfs:subClassOf` rules, and serializes the expanded graph into the output `.ttl` file.

## 7. Instructions for Running the Query
To reproduce our results using the Python workflow:
1. Ensure Python 3 is installed.
2. Install the required dependencies:
   ```bash
   pip install rdflib owlrl
   ```
3. Execute the inference script from the repository root:
    ```bash
    python src/run_inference.py
    ```
    This script will automatically load the ontologies, perform the inference, export the inferred graph, and execute the SPARQL query locally.

## 8. Expected Query Output
The SPARQL query correctly retrieves the inferred graspable objects while omitting the reference plate01 and the container basket01.

Output:

```Plaintext
Object                                        | Label           | Role
--------------------------------------------------------------------------------
block01                                       | red block       | TargetObject
block02                                       | green block     | TargetObject
blueCup01                                     | blue cup        | TargetObject
fork01                                        | fork            | TargetObject
knife01                                       | knife           | TargetObject
pinkCup01                                     | pink cup        | TargetObject
```

## 9. Repository File Links
- Group Ontology: ontology/group-ontology.ttl

- Imported Course Ontology: ontology/imports/course-affordance.ttl

- Inferred Graph (Output): ontology/inferred-results.ttl

- SPARQL Query: queries/graspable_objects.rq

- Inference Script: src/run_inference.py

- Saved Query Results: results/graspable_objects_output.txt