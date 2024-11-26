package org.example.Assignment3;
import org.apache.lucene.analysis.TokenFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;

import java.io.IOException;
import java.util.LinkedList;
import java.util.Objects;
import java.util.Queue;
public class Assignment3 {

    public static void main(String[] args) throws Exception {
        String text = "Today is sunny. She is a sunny girl. To be or not to be. She is in Berlin today. Sunny Berlin! Berlin is always exciting!";

        TokenStream tokenStream = new CustomTokenizer(text);
        TokenStream biwordFilter = new BiwordFilter(tokenStream);

        biwordFilter.reset();
        CharTermAttribute attr = biwordFilter.addAttribute(CharTermAttribute.class);
        while (biwordFilter.incrementToken()) {
            System.out.println(attr.toString());
        }
        biwordFilter.close();

        // b
        String nytext = "New York University";
        String falsePos = "It is New York. There is the York University";
        checkBiWords(nytext, falsePos);

        String postext = "New York Max";
        String posPos = "It is New York. There is the York University";
        checkBiWords(posPos, postext);



    }

    public static void checkBiWords(String query, String document) throws Exception {
        LinkedList queryBiWords = buildBiWordList(query);
        LinkedList documentBiWords = buildBiWordList(document);

        System.out.println("False Positive Index:"+documentBiWords.toString());
        System.out.println("Query Index:"+queryBiWords.toString());
        boolean contains = true;
        for(Object s : queryBiWords){
            if(!documentBiWords.contains(s)) contains = false;
        }

        if (contains){
            System.out.println("Result: Positive");
        }else{
            System.out.println("Result: Negative");
        }
    }

    public static LinkedList<String> buildBiWordList (String text) throws Exception{
        TokenStream tokenStream = new CustomTokenizer(text);
        TokenStream biwordFilter = new BiwordFilter(tokenStream);
        LinkedList<String> list = new LinkedList<String>();

        biwordFilter.reset();
        CharTermAttribute attr = biwordFilter.addAttribute(CharTermAttribute.class);
        while (biwordFilter.incrementToken()) {
            list.add(attr.toString());
        }
        biwordFilter.close();
        return list;
    }

    static class BiwordFilter extends TokenFilter {
        private final CharTermAttribute termAttr;
        private final LinkedList<String> biwordList;
        private String previousToken;

        protected BiwordFilter(TokenStream input) {
            super(input);
            termAttr = addAttribute(CharTermAttribute.class);
            biwordList = new LinkedList<>();
            previousToken = null;
        }

        @Override
        public boolean incrementToken() throws IOException {
            while (input.incrementToken()) {
                String currentToken = termAttr.toString();
                if (previousToken != null) biwordList.add(previousToken + " " + currentToken);
                previousToken = currentToken;

                if (!biwordList.isEmpty()) {
                    termAttr.setEmpty();
                    termAttr.append(biwordList.removeFirst());
                    return true;
                }
            }
            return false;
        }

        @Override
        public void reset() throws IOException {
            super.reset();
            biwordList.clear();
            previousToken = null;
        }
    }

    static class CustomTokenizer extends TokenStream {
        private CharTermAttribute termAttr;
        private String tokens[];
        private int pos = 0;

        public CustomTokenizer(String text) {
            tokens = text.replaceAll("[\\.!]","").toLowerCase().split("\\s+");
            termAttr  = addAttribute(CharTermAttribute.class);
        }

        @Override
        public boolean incrementToken() {
            if (pos >= tokens.length) return false;
            clearAttributes();
            termAttr.append(tokens[pos]);
            pos++;
            return true;
        }
    }
}
