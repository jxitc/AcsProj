# java -cp weka.jar weka.filters.unsupervised.attribute.StringToWordVector \
# -W 25000 -L -N 0 -stemmer weka.core.stemmers.LovinsStemmer -M 10 \
# -tokenizer "weka.core.tokenizers.WordTokenizer \
# -delimiters \" \\r\\n\\t.,;:\\\'\\\"()?!\"" \
# -i /home/xj229/data/7nat_lvl123_6000each_bf.arff \
# -o /home/xj229/data/7nat_lvl123_6000each_bog.arff
java -cp $7 weka.filters.unsupervised.attribute.StringToWordVector \
-W $1 $2 -N 0 -stemmer $3 -M $4 \
-tokenizer "weka.core.tokenizers.WordTokenizer \
-delimiters \" \\r\\n\\t.,;:\\\'\\\"()?!\"" \
-i $5 \
-o $6
