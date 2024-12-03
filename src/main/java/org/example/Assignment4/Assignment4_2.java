package org.example.Assignment4;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.*;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.*;
import org.apache.lucene.search.similarities.BM25Similarity;
import org.apache.lucene.search.similarities.ClassicSimilarity;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.RAMDirectory;
import org.apache.lucene.util.BytesRef;

import java.io.IOException;
import java.text.MessageFormat;
import java.util.*;

public class Assignment4_2 {

    public static void main(String[] args) throws IOException, ParseException {

        String[] docCollection = {
                "Today is sunny.",
                "She is a sunny girl.",
                "To be or not to be.",
                "She is in Berlin today.",
                "Sunny Berlin!",
                "Berlin is always exciting!"
        };


        Directory directory = new RAMDirectory();
        IndexWriterConfig config = new IndexWriterConfig(new StandardAnalyzer());
        IndexWriter indexWriter = new IndexWriter(directory, config);
        for(int i = 0; i < docCollection.length; i++){
            Document doc = new Document();
            doc.add(new TextField("content", docCollection[i], Field.Store.YES));
            indexWriter.addDocument(doc);
        }
        indexWriter.close();

        // search the docs using index reader
        IndexReader indexReader = DirectoryReader.open(directory);
        IndexSearcher indexSearcher = new IndexSearcher(indexReader);

        //A) create vector space model and tfidf weights
        // vector space model with tf-idf weights
        calculateTFIDFVectors(indexSearcher);

        //B)Use Vector space model and BM25 Model to find relevant documents while following query:

        //query
        String query = "She is a sunny girl.";
        QueryParser parser = new QueryParser("content", new StandardAnalyzer());
        org.apache.lucene.search.Query queryObj = parser.parse(query);

        // get the scores
        ScoreDoc[] bm25 = getBM25Scores(indexSearcher, queryObj);
        ScoreDoc[] tfidf = getTFIDFScores(indexSearcher, queryObj);

        // print documents as per bm25 and vsm
        System.out.println("BM25 model : ");
        printScores(bm25,indexSearcher);
        System.out.println();

        System.out.println("Vector Space model : ");
        printScores(tfidf,indexSearcher);

        indexReader.close();
        directory.close();

    }

    private static void calculateTFIDFVectors(IndexSearcher indexSearcher) throws IOException {
        IndexReader indexReader = indexSearcher.getIndexReader();
        int numDocs = indexReader.numDocs();

        Terms terms = MultiFields.getTerms(indexReader, "content");
        TermsEnum termsEnum = terms.iterator();

        // TF-IDF vectors
        while (termsEnum.next() != null) {
            String term = termsEnum.term().utf8ToString();

            // Calculate the term frequency-inverse document frequency (tf-idf) weight for each term
            double idf = Math.log10((double) numDocs / (double) (indexReader.docFreq(new Term("content", term))));
            for (int i = 0; i < numDocs; i++) {
                PostingsEnum postingsEnum = MultiFields.getTermDocsEnum(indexReader, "content", termsEnum.term());
                double tfidf = 0;
                if (postingsEnum != null && postingsEnum.advance(i) == i) {
                    double tf = postingsEnum.freq();
                    tfidf = tf * idf;
                }
                // print docid : term = "tfidf"
                System.out.println(MessageFormat.format("docid : {0}, term : {1} = tfidf : {2}", i, term, tfidf));
            }
        }

    }

    // bm25 similarity, get top 5 docs
    public static ScoreDoc[] getBM25Scores(IndexSearcher searcher, Query query) throws IOException {
        searcher.setSimilarity(new BM25Similarity());
        TopDocs docs = searcher.search(query, 5);
        ScoreDoc[] hits = docs.scoreDocs;
        return hits;
    }

    //tfidf by classic similarity, get top 5 docs
    public static ScoreDoc[] getTFIDFScores(IndexSearcher searcher, Query query) throws IOException {
        searcher.setSimilarity(new ClassicSimilarity());
        TopDocs docs = searcher.search(query, 5);
        ScoreDoc[] hits = docs.scoreDocs;
        return hits;
    }

    public static void printScores(ScoreDoc[] hits, IndexSearcher searcher) throws IOException {
        for (ScoreDoc hit : hits) {
            int docid = hit.doc;
            Document doc = searcher.doc(docid);
            String content = doc.get("content");
            float score = hit.score;
            System.out.println("\n" + score + " : " + content);
        }

    }

}
