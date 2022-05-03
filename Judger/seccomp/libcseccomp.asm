# check if arch is X86_64
A = arch
A == ARCH_X86_64 ? next : dead
A = sys_number
A >= 0x40000000 ? dead : next
A == read ? ok : next
A == fstat ? ok : next
A == mmap ? ok : next
A == mprotect ? ok : next
A == munmap ? ok : next
A == uname ? ok : next
A == arch_prctl ? ok : next
A == brk ? ok : next
A == access ? ok : next
A == exit_group ? ok : next
A == close ? ok : next
A == readlink ? ok : next
A == sysinfo ? ok : next
A == write ? ok : next
A == writev ? ok : next
A == lseek ? ok : next
A == clock_gettime ? ok : next
return KILL
ok:
return ALLOW
dead:
return KILL	