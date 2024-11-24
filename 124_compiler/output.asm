.data
x_mem: .word 0
y_mem: .word 0
.text
li $t0, 1
li $t1, 2
add $t2, $t0, $t1
sw $t2, x_mem
li $t3, 2
li $t4, 2
add $t5, $t3, $t4
sw $t5, y_mem
