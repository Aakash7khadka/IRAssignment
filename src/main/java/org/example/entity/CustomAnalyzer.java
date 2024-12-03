package org.example.entity;

import org.apache.lucene.analysis.*;
import org.apache.lucene.analysis.en.PorterStemFilter;
import org.apache.lucene.analysis.standard.StandardTokenizer;

import java.util.Arrays;

public class CustomAnalyzer extends Analyzer {


    @Override
    protected TokenStreamComponents createComponents(String s) {
        StandardTokenizer tokenizer = new StandardTokenizer();

        TokenStream ts = new LowerCaseFilter(tokenizer);
        return new TokenStreamComponents(tokenizer, ts);
    }


}
