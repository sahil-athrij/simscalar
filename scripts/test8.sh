sim-outorder -fastfwd 1000000 >compress9.txt 2>compresssim9.txt   $SS95/compress95.ss  <$SSIN/compress.in
sim-outorder -fastfwd 1000000 >swim9.txt 2>swimsim9.txt   $SS95/swim.ss  <$SSIN/swim.in &
sim-outorder -fastfwd 1000000 >perl9.txt 2>perlsim9.txt $SS95/perl.ss $SSIN/charcount $SSIN/all_grep_words
