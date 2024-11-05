package org.example;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.CharArraySet;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.Tokenizer;
import org.apache.lucene.analysis.core.StopFilter;
import org.apache.lucene.analysis.core.WhitespaceTokenizer;
import org.apache.lucene.analysis.custom.CustomAnalyzer;
import org.apache.lucene.analysis.standard.StandardTokenizer;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.example.entity.OurAnalyzer;

import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

public class Main {
    public static void main(String[] args) throws Exception {

        String sample_text = "Today is sunny. She is a sunny girl. To be or not to be. She is in Berlin today.\n" +
                "Sunny Berlin! Berlin is always exciting!";

        String[] stopWords = {"was", "is", "in", "to", "be"};

        // P01 a
        System.out.println("Standard Tokenizer:");
        printTokens(new StandardTokenizer(), sample_text);

        System.out.println("Whitespace Tokenizer:");
        printTokens(new WhitespaceTokenizer(), sample_text);

        // P01 b
        System.out.println("Analyzer and StopwordFilter:");

        applyStandardAnalyzerAndStopFilter(new StandardTokenizer(), sample_text, stopWords);

        //P01 c
        System.out.println("\nCustom Analyzer:");
        customAnalyzer(sample_text, stopWords);

    }

    /**
     * Assignment P01 a
     */
    public static void printTokens (Tokenizer t, String s){
        try {
            t.setReader(new StringReader(s));
            t.reset(); // set token pointer to start of the input

            // CharTermAttribute holds the tokens
            CharTermAttribute charTermAttr = t.addAttribute(CharTermAttribute.class);

            while (t.incrementToken()) System.out.print(charTermAttr.toString() + ',');

        }catch (IOException e){
            e.printStackTrace();
        }
        System.out.println();
    }

    /**
     * Assignment P01 b
     */
    public static void applyStandardAnalyzerAndStopFilter (Tokenizer t, String text, String[] stopArr) throws Exception{
        List<String> arr = Arrays.asList(stopArr);
        CharArraySet stopWords = new CharArraySet(arr, true);

        t.setReader(new StringReader(text));

        TokenStream tokenStream = new StopFilter(t, stopWords);

        tokenStream.reset();
        CharTermAttribute charTermAttr = tokenStream.getAttribute(CharTermAttribute.class);

        while (tokenStream.incrementToken())
            System.out.print(charTermAttr.toString() + ",");
    }

    /**
     * Assignment P01 c
     */
    public static void customAnalyzer (String text, String arr []) throws Exception{

        Analyzer a = new OurAnalyzer(arr);
        TokenStream ts = a.tokenStream("field", new StringReader(text));
        CharTermAttribute attr = ts.addAttribute(CharTermAttribute.class);
        ts.reset();
        while (ts.incrementToken())
            System.out.print(attr.toString() + ",");
    }
}