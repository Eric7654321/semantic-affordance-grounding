import rdflib
import owlrl

print("1. 載入本體論資料...")
g = rdflib.Graph()
g.parse("ontology/imports/course-affordance.ttl", format="turtle")
g.parse("ontology/group-ontology.ttl", format="turtle")

print("2. 發動推論引擎 (擴充隱藏屬性)...")
# 根據你寫的 rdfs:subClassOf，自動幫物件貼上 cap:GraspableObject 標籤
owlrl.DeductiveClosure(owlrl.OWLRL_Semantics, axiomatic_triples=False, datatype_axioms=False).expand(g)

print("3. 匯出推論結果 (inferred-results.ttl)...")
g.serialize(destination="ontology/inferred-results.ttl", format="turtle")

print("4. 執行 SPARQL 查詢...\n")
query = """
PREFIX cap: <https://hcis.io/ontology/aicapstone/2026/>
SELECT DISTINCT ?obj ?label ?role
WHERE {
  ?obj a cap:GraspableObject .
  OPTIONAL { ?obj cap:hasObjectLabel ?label . }
  OPTIONAL { ?obj cap:hasTaskRole ?role . }
}
ORDER BY ?obj
"""

results = g.query(query)
print(f"{'Object':<45} | {'Label':<15} | {'Role'}")
print("-" * 80)

# 將結果印出並存入 txt
with open("results/graspable_objects_output.txt", "w", encoding="utf-8") as f:
    for row in results:
        obj = str(row.obj).split('/')[-1] if row.obj else ""
        label = str(row.label) if row.label else ""
        role = str(row.role).split('/')[-1] if row.role else ""
        
        line = f"{obj:<45} | {label:<15} | {role}"
        print(line)
        f.write(line + "\n")

print("\n大功告成！所有作業檔案皆已就緒。")
