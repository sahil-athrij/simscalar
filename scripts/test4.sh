sim-outorder -cache:il1 il1:128:64:4:l -cache:il1lat 4 >compress5.txt 2>compresssim5.txt   $SS95/compress95.ss  <$SSIN/compress.in
sim-outorder -cache:il1 il1:128:64:4:l -cache:il1lat 4 >swim5.txt 2>swimsim5.txt   $SS95/swim.ss  <$SSIN/swim.in &
sim-outorder -cache:il1 il1:128:64:4:l -cache:il1lat 4 >perl5.txt 2>perlsim5.txt $SS95/perl.ss $SSIN/charcount $SSIN/all_grep_words
