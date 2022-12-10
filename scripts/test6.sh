sim-outorder -cache:il2 dl2 -cache:dl2 il1:1024:64:16:l -cache:dl2lat 12 >compress7.txt 2>compresssim7.txt   $SS95/compress95.ss  <$SSIN/compress.in
sim-outorder -cache:il2 dl2 -cache:dl2 il1:1024:64:16:l -cache:dl2lat 12 >swim7.txt 2>swimsim7.txt   $SS95/swim.ss  <$SSIN/swim.in &
sim-outorder -cache:il2 dl2 -cache:dl2 il1:1024:64:16:l -cache:dl2lat 12 >perl7.txt 2>perlsim7.txt $SS95/perl.ss $SSIN/charcount $SSIN/all_grep_words
