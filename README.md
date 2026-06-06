# AI Capstone 2026 - Homework 5: Ontology-based Semantic Grounding

**Group: 11**

**Members: 簡嫚萱、周佳瑩、劉逸安、呂杰軒、朱修毅**

## 1. Selected Tasks
Our group modeled objects across all three entry-level tasks:
1. **Cup Stacking** (Target: Cup; Reference: Cup)
2. **Cutlery Arrangement** (Target: Knife, Fork; Reference: Plate)
3. **Toy Block Collection** (Target: Toy blocks; Container: Basket)

## 2. Ontology Design Overview
Our ontology is designed to provide explicit semantic grounding for physical objects perceived by the robot. We distinguish between the object's physical type (eg. `cap:Cup`), its context-dependent task role (eg. `cap:TargetObject`), and its manipulation affordances (eg. `cap:GraspingAffordance`). Reference objects (`Plate`) and container objects (`Basket`) are deliberately isolated from grasping affordances to reflect their distinct roles in the manipulation pipeline.

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

(Note: Target instances implicitly possess `cap:GraspingAffordance` based on the OWL restrictions defined in the core `course-affordance.ttl`.)

## 4. Namespace Policy
We strictly adhere to the separation of shared vocabulary used in the course and modeling specific to our group:
- **`cap`** (`<https://hcis.io/ontology/aicapstone/2026/>`): Used for the shared course vocabulary (core classes, predefined roles, affordance types, and data properties).
- **(Default) / `g11:`** (`<https://hcis.io/ontology/aicapstone/group11/>`): The group-specific namespace used exclusively for our custom task-relevant instances and group-level design extensions.

## 5. Inference Mechanism & Reasoning Pattern 
We achieved full Semantic Grounding by implementing OWL Description Logic (DL) reasoning, strictly avoiding manual assertions of the `cap:GraspableObject` class.

In our `group-ontology.ttl`, we defined the logical axiom for `cap:GraspableObject` using `owl:equivalentClass` and `owl:intersectionOf`. Since `course-affordance.ttl` defines existential restrictions (`owl:someValuesFrom cap:GraspingAffordance`) for classes like `Cup`, `Knife`, and `ToyBlock`, the DL reasoner dynamically infers that instances of these classes are implicitly `cap:GraspableObject`. Objects lacking this affordance restriction (eg. `Plate`, `Basket`) are successfully excluded during the inference process.

## 6. How `inferred-results.ttl` was Generated
The `ontology/inferred-results.ttl` file was autonomously generated using our custom Python script (`src/run_inference.py`). 
We utilized `owlready2` and its integrated HermiT Reasoner to perform the offline DL inference. To ensure robust cross-format parsing (Turtle to XML) of complex blank nodes (eg. `owl:intersectionOf`), the script dynamically asserts the equivalent class logic in the Python memory model before executing the reasoner. The inferred instances are then extracted and serialized back into a static Turtle file using `rdflib`, ready for SPARQL endpoint deployment.

## 7. Instructions for Running the Query
To reproduce our results using the Python automated workflow:

1. Ensure Python 3 is installed and create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install the required dependencies:
    ```bash
    pip install rdflib owlready2
    ```

3. Execute the inference script from the repository root:
    ```bash
    python src/run_inference.py
    ```

This script will autonomously load the ontologies, invoke HermiT for DL reasoning, export the inferred graph, and execute the SPARQL queries.

## 8. Live SPARQL Endpoint (Proof of Concept)
To demonstrate the practical deployment of our semantic grounding layer, we have deployed the inferred knowledge graph to a live edge server hosted on a Raspberry Pi. The endpoint is exposed via a reverse proxy with SSL termination.

**🔗 Live Endpoint URL:** [https://hw5-ai.kiwikiwiki.com/](https://hw5-ai.kiwikiwiki.com/)
*(Login credentials provided to TAs via internal submission if required)*

**Dataset Name:** `/aicapstone`

## 9. Expected Query Output
The SPARQL query correctly retrieves the inferred graspable objects while omitting the reference `plate01` and the container `basket01`.

**Output:**
```text
Object                    | Label           | Role
-----------------------------------------------------------------
block01                   | red block       | TargetObject
block02                   | green block     | TargetObject
blueCup01                 | blue cup        | TargetObject
fork01                    | fork            | TargetObject
knife01                   | knife           | TargetObject
pinkCup01                 | pink cup        | TargetObject
```

## 10. Repository File Links
- Group Ontology: ontology/group-ontology.ttl
- Imported Course Ontology: ontology/imports/course-affordance.ttl
- Inferred Graph (Output): ontology/inferred-results.ttl
- Base SPARQL Query: queries/graspable_objects.rq
- Advanced Task-Specific Query: queries/task_objects.rq (Filters graspable objects specifically for defined Manipulation Tasks)
- Inference Script: src/run_inference.py
- Saved Query Results: results/graspable_objects_output.txt
- Screenshots: results/screenshots/ (Contains verification from Fuseki Endpoint)
