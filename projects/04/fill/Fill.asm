@c
M = 0
(MAIN)
    @KBD
    D=M
    @ERASE
    D; JNE
    @FILL
    D; JEQ


    (ERASE)
        @idx
        M=-1
        (LOOP1)
            @idx
            M=M+1
            D=M
            @SCREEN
            A=A+D
            M=0
            @8192
            D=D-A
            @c
            M=D
            @KBD
            D=M
            @FILL
            D; JNE
            @c
            D=M
            @LOOP1
            D;JNE 
        
    
    (FILL)
        @idx
        M=-1
        (LOOP2)
            @idx
            M=M+1
            D=M
            @SCREEN
            A=A+D
            M=-1
            @8192
            D=D-A
            @c
            M=D
            @KBD
            D=M
            @ERASE
            D; JEQ
            @c
            D=M
            @LOOP2
            D;JNE 
    @MAIN
    0;JMP

