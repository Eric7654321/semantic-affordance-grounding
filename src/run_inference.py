import rdflib
from rdflib import URIRef
from rdflib.namespace import RDF
from owlready2 import *
import os

print("1. 透過 RDFLib 載入並合併 Turtle 檔案...")
g_base = rdflib.Graph()
g_base.parse("ontology/imports/course-affordance.ttl", format="turtle")
g_base.parse("ontology/group-ontology.ttl", format="turtle")

# 存成 XML 餵給 owlready2
temp_xml = "ontology/temp_merged.xml"
g_base.serialize(destination=temp_xml, format="xml")

print("2. 載入至 owlready2 並修復 XML 遺失的 OWL 邏輯...")
onto = get_ontology("file://" + os.path.abspath(temp_xml)).load()

# 取得 Namespace
cap = onto.get_namespace("https://hcis.io/ontology/aicapstone/2026/")

# 直接在 Python 裡用 owlready2 原生語法，把 DL 邏輯強制灌進大腦
cap.GraspableObject.equivalent_to = [cap.PhysicalObject & cap.hasAffordance.some(cap.GraspingAffordance)]

print("3. 啟動內建 HermiT 推論機 (執行真實 DL 推論)...")
with onto:
    sync_reasoner()

print("4. 從 HermiT 提取推論結果...")
inferred_iris = set()

# 推論機算完後，Cup, Knife 等類別會被自動算成 GraspableObject 的 subclass
# 我們把這些子類別底下的實例全部挖出來
for subcls in cap.GraspableObject.subclasses():
    for inst in subcls.instances():
        inferred_iris.add(inst.iri)

# 同時也抓取可能直接被歸類的個體
for inst in cap.GraspableObject.instances():
    inferred_iris.add(inst.iri)

# 將推論出來的名單，硬塞回 RDFLib 準備存檔的圖形中
graspable_uri = URIRef("https://hcis.io/ontology/aicapstone/2026/GraspableObject")
for iri in inferred_iris:
    g_base.add((URIRef(iri), RDF.type, graspable_uri))
    name = iri.split('/')[-1]
    print(f"   ✅ 成功捕捉: {name} is a GraspableObject")

print("\n5. 匯出推論圖形 (inferred-results.ttl) 並執行 SPARQL...\n")
g_base.serialize(destination="ontology/inferred-results.ttl", format="turtle")
if os.path.exists(temp_xml):
    os.remove(temp_xml)

# 執行 SPARQL 查詢
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

results = g_base.query(query)
print(f"{'Object':<25} | {'Label':<15} | {'Role'}")
print("-" * 65)

os.makedirs("results", exist_ok=True)
with open("results/graspable_objects_output.txt", "w", encoding="utf-8") as f:
    for row in results:
        obj = str(row.obj).split('/')[-1] if row.obj else ""
        label = str(row.label) if row.label else ""
        role = str(row.role).split('/')[-1] if row.role else ""
        
        line = f"{obj:<25} | {label:<15} | {role}"
        print(line)
        f.write(line + "\n")

print("\n大功告成！真正的 DL 推論已完成，作業檔案皆已就緒。")