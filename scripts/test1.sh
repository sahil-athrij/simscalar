sim-fast >compress.txt 2>compresssim.txt   $SS95/compress95.ss  <$SSIN/compress.in
sim-fast >swim.txt 2>swimsim.txt   $SS95/swim.ss  <$SSIN/swim.in &
sim-cache >perl.txt  $SS95/perl.ss $SSIN/charcount $SSIN/all_grep_words
