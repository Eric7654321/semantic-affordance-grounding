import org.apache.jena.rdf.model.*;
import org.apache.jena.ontology.OntModel;
import org.apache.jena.query.*;
import openllet.jena.PelletReasonerFactory;

public class TrueInference {
    public static void main(String[] args) {
        System.out.println("1. 載入本體論資料與 Pellet 引擎...");
        
        // 正確的姿勢：建立帶有 Pellet 引擎的 OntModel (本體論模型)
        OntModel ontModel = ModelFactory.createOntologyModel(PelletReasonerFactory.THE_SPEC);
        
        // 用 OntModel 專屬的 read 方法載入檔案，它才會正確解析 OWL 邏輯
        ontModel.read("ontology/imports/course-affordance.ttl", "TURTLE");
        ontModel.read("ontology/group-ontology.ttl", "TURTLE");

        System.out.println("2. 執行 SPARQL 查詢...");
        String queryString = 
            "PREFIX cap: <https://hcis.io/ontology/aicapstone/2026/> " +
            "SELECT DISTINCT ?obj ?label ?role " +
            "WHERE { " +
            "  ?obj a cap:GraspableObject . " +
            "  OPTIONAL { ?obj cap:hasObjectLabel ?label . } " +
            "  OPTIONAL { ?obj cap:hasTaskRole ?role . } " +
            "} ORDER BY ?obj";

        Query query = QueryFactory.create(queryString);
        try (QueryExecution qe = QueryExecutionFactory.create(query, ontModel)) {
            ResultSetFormatter.out(System.out, qe.execSelect(), query);
        }
        
        System.out.println("\n真正的 DL 推論大功告成！");
    }
}