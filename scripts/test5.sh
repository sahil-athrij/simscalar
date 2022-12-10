sim-outorder -cache:il1 il1:64:64:8:l -cache:il1lat 6 >compress6.txt 2>compresssim6.txt   $SS95/compress95.ss  <$SSIN/compress.in
sim-outorder -cache:il1 il1:64:64:8:l -cache:il1lat 6 >swim6.txt 2>swimsim6.txt   $SS95/swim.ss  <$SSIN/swim.in &
sim-outorder -cache:il1 il1:64:64:8:l -cache:il1lat 6 >perl6.txt 2>perlsim6.txt $SS95/perl.ss $SSIN/charcount $SSIN/all_grep_words
