sim-outorder >compress2.txt 2>compresssim2.txt   $SS95/compress95.ss  <$SSIN/compress.in
sim-outorder >swim2.txt 2>swimsim2.txt $SS95/swim.ss  <$SSIN/swim.in
sim-outorder >perl2.txt 2>perlsim2.txt $SS95/perl.ss $SSIN/charcount $SSIN/all_grep_words
