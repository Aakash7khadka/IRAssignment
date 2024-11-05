package org.example.entity;

import org.apache.lucene.analysis.*;
import org.apache.lucene.analysis.en.PorterStemFilter;
import org.apache.lucene.analysis.standard.StandardTokenizer;

import java.util.Arrays;

public class OurAnalyzer extends Analyzer {

    private CharArraySet stopWords;

    public OurAnalyzer (String arr[]){
        stopWords = new CharArraySet(Arrays.asList(arr), true);
    }

    @Override
    protected TokenStreamComponents createComponents(String s) {
        StandardTokenizer tokenizer = new StandardTokenizer();

        TokenStream ts = new LowerCaseFilter(tokenizer);
        ts = new StopFilter(ts, stopWords);
        ts = new PorterStemFilter(ts);

        return new TokenStreamComponents(tokenizer, ts);
    }


}
