package org.example.Assignment2;

import org.apache.lucene.analysis.custom.CustomAnalyzer;
import org.apache.lucene.document.Document;

import org.apache.lucene.search.*;
import org.apache.lucene.store.Directory;

import org.apache.lucene.document.FieldType;
import org.apache.lucene.document.Field;
import org.apache.lucene.store.RAMDirectory;
import org.apache.lucene.util.BytesRef;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.index.*;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.queryparser.classic.ParseException;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;


public class Assignment2 {
    public static void main(String[] args) throws Exception {

        Analyzer analyzer = CustomAnalyzer.builder().withTokenizer("standard").addTokenFilter("lowercase").build();

        Directory index = new RAMDirectory();
        IndexWriterConfig config = new IndexWriterConfig(analyzer);
        IndexWriter content = new IndexWriter(index, config);


        String[] docs = "Today is sunny. She is a sunny girl. To be or not to be. She is in Berlin today. Sunny Berlin! Berlin is always exciting!".split("[\\.!]");
        for(String doc: docs){
            documentWriter(content, doc);
        }

        content.close();

        // Implementation of 4.1
        String query = "sunny AND exciting";
        createIndexAndIntersect(analyzer, query, index);

        createIndexAndIntersect(analyzer, "to AND be", index);

        String query1 = "sunny";
        String query2 = "to";

        IndexReader reader = DirectoryReader.open(index);
        printPostingList(query1, reader, docs.length);
        printPostingList(query2, reader, docs.length);

    }

    //Create Inverted Index
    private static void documentWriter(IndexWriter indexWriter, String str) throws Exception {
        FieldType fieldType = new FieldType();
        Document document = new Document();
        fieldType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS_AND_OFFSETS);
        fieldType.setStored(true);
        fieldType.setStoreTermVectors(true);
        fieldType.setStoreTermVectorPositions(true);
        fieldType.setStoreTermVectorPayloads(true);
        fieldType.setStoreTermVectorOffsets(true);
        document.add(new Field("Input", str, fieldType));
        indexWriter.addDocument(document);
    }

    public static void createIndexAndIntersect(Analyzer analyzer, String query, Directory index) throws Exception{
        int occurrenceInDoc = 100, counter =0;
        Query queryParser = new QueryParser("Input", analyzer).parse(query);

        IndexReader indexReader = DirectoryReader.open(index);
        IndexSearcher indexSearcher = new IndexSearcher(indexReader);
        TopScoreDocCollector topScoreDocCollector = TopScoreDocCollector.create(occurrenceInDoc);
        indexSearcher.search(queryParser, topScoreDocCollector);
        ScoreDoc[] occurrence = topScoreDocCollector.topDocs().scoreDocs;

        for (ScoreDoc scoreDoc : occurrence) {
            counter++;
            int docId = scoreDoc.doc;
            System.out.printf("Both of the terms \"%s\" occur in document: %s %n", query, docId);
        }
        if(counter == 0)
            System.out.println("There are no occurrence of the words: "+ query);
    }

    //Assignment 2 b
    public static void printPostingList(String query, IndexReader indexReader, int noOfDocuments) throws Exception {

        System.out.printf("Printing Posting List for \"%s\" :\n", query);
        Term term = new Term("Input", query);
        long totalFrequency = indexReader.totalTermFreq(term);
        long documentFrequency = indexReader.docFreq(term);
        System.out.printf("[%s : %s : %s]", query, totalFrequency, documentFrequency);

        for (int i = 0; i < noOfDocuments; i++) {
            Terms vector = indexReader.getTermVector(i, "Input");
            TermsEnum iterator = vector.iterator();
            BytesRef termFromIndex;
            PostingsEnum postings = null;

            while ((termFromIndex = iterator.next()) != null) {
                postings = iterator.postings(postings, PostingsEnum.ALL);
                if (termFromIndex.equals(term.bytes())) {
                    postings.nextDoc();
                    long termFrequency = iterator.totalTermFreq();
                    ArrayList<Integer> positions = new ArrayList<>();
                    for (int j = 0; j < termFrequency; j++)
                        positions.add(postings.nextPosition());
                    System.out.printf(" -> [ %s : %s : %s ]", i, termFrequency, positions);
                }
            }

        }
        System.out.println();
    }

}

