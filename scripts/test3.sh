sim-outorder -bpred:2lev 1 512 4 0 >compress4.txt 2>compresssim4.txt   $SS95/compress95.ss  <$SSIN/compress.in
sim-outorder -bpred:2lev 1 512 4 0 >swim4.txt 2>swimsim4.txt   $SS95/swim.ss  <$SSIN/swim.in &
sim-outorder -bpred:2lev 1 512 4 0 >perl4.txt 2>perlsim4.txt $SS95/perl.ss $SSIN/charcount $SSIN/all_grep_words
