cpy a b
dec b
cpy a d
cpy 0 a
mul b d
add d a
cpy 0 c
cpy 0 d
nop
nop
dec b
cpy b c
cpy c d
dec d
inc c
jnz d -2
tgl c
cpy -16 c
jnz 1 c
cpy 70 c
jnz 87 d
inc a
inc d
jnz d -2
inc c
jnz c -5