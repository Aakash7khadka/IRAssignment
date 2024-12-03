package org.example.Assignment4;

import org.apache.lucene.analysis.*;
import org.apache.lucene.analysis.tokenattributes.*;
import org.example.entity.CustomAnalyzer;

import java.util.*;
import java.util.stream.Collectors;

public class Assignment4 {

    public static void main(String[] args) throws Exception {
        String[] docs = {
                "Today is sunny.",
                "She is a sunny girl.",
                "To be or not to be.",
                "She is in Berlin today.",
                "Sunny Berlin!",
                "Berlin is always exciting!"
        };

        List<List<String>> tokenizedDocs = tokenizeDocs(docs);
        Map<String, Double[]> tfIdfVectors = calculateTFIDF(tokenizedDocs);

        Double[] vec1 = tfIdfVectors.get("doc0");
        Double[] vec2 = tfIdfVectors.get("doc1");

        double euclideanDistance = euclideanDistance(vec1, vec2);
        double dotProduct = dotProduct(vec1, vec2);
        double cosineSimilarity = cosineSimilarity(vec1, vec2);

        System.out.println("Euclidean Distance: " + euclideanDistance);
        System.out.println("Dot Product: " + dotProduct);
        System.out.println("Cosine Similarity: " + cosineSimilarity);
    }

    private static List<List<String>> tokenizeDocs(String[] docs) throws Exception {
        List<List<String>> tokenizedDocs = new ArrayList<>();
        for (String doc : docs) {
            List<String> tokens = tokenize(doc.toLowerCase());
            tokenizedDocs.add(tokens);
        }
        return tokenizedDocs;
    }

    private static List<String> tokenize(String text) throws Exception {
        List<String> tokens = new ArrayList<>();
        Analyzer analyzer = new CustomAnalyzer();
        TokenStream tokenStream = analyzer.tokenStream(null, text);
        tokenStream.reset();
        while (tokenStream.incrementToken()) tokens.add(tokenStream.getAttribute(CharTermAttribute.class).toString());
        tokenStream.close();
        Collections.sort(tokens); // to create alphabetically sorted token list
        return tokens;
    }

    private static Map<String, Double[]> calculateTFIDF(List<List<String>> docs) {
        TreeMap<String, Double[]> tfIdfVectors = new TreeMap<>(); // for keeping sorted behaviour
        TreeSet<String> vocabulary = new TreeSet<>(docs.stream().flatMap(List::stream).collect(Collectors.toSet()));
        int N = docs.size();

        Map<String, Double> idf = new HashMap<>();
        for (String term : vocabulary) {
            int docFrequency = (int) docs.stream().filter(doc -> doc.contains(term)).count();
            idf.put(term, Math.log10((double) N / docFrequency));
        }

        for (int i = 0; i < N; i++) {
            List<String> doc = docs.get(i);
            Map<String, Double> tf = new HashMap<>();
            for (String term : doc){
                try {
                    tf.put(term, tf.get(term) + 1);
                }catch (NullPointerException e){
                    tf.put(term, 1.0);
                }
            }
            tfIdfVectors.put("doc" + i, vocabulary.stream()
                    .map(term -> tf.getOrDefault(term, 0.0) * idf.getOrDefault(term, 0.0))
                    .toArray(Double[]::new));
        }
        return tfIdfVectors;
    }

    private static double euclideanDistance(Double[] vector1, Double[] vector2) {
        double sum = 0.0;
        for (int i = 0; i < vector1.length; i++) sum += Math.pow(vector1[i] - vector2[i], 2);
        return Math.sqrt(sum);
    }

    private static double dotProduct(Double[] vector1, Double[] vector2) {
        double product = 0.0;
        for (int i = 0; i < vector1.length; i++) product += vector1[i] * vector2[i];
        return product;
    }

    // Cosine Similarity
    private static double cosineSimilarity(Double[] vector1, Double[] vector2) {
        double dot = dotProduct(vector1, vector2);
        double norm1 = Math.sqrt(dotProduct(vector1, vector1));
        double norm2 = Math.sqrt(dotProduct(vector2, vector2));
        return dot / (norm1 * norm2);
    }
}
