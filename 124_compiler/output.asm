
.data
newline: .asciiz "\n"
str_label0: .asciiz "Hello world!"

.text
la $t0, str_label0
li $v0, 4  # Print string syscall
move $a0, $t0
syscall
la $a0, newline
li $v0, 4  # Print newline syscall
syscall

# Exit program
li $v0, 10
syscall
