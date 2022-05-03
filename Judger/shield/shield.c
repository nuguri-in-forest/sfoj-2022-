#include <linux/seccomp.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/prctl.h>

static __attribute__ ((constructor)) void install_seccomp() {
  static unsigned char filter[] = {32,0,0,0,4,0,0,0,21,0,0,21,62,0,0,192,32,0,0,0,0,0,0,0,53,0,19,0,0,0,0,64,21,0,17,0,0,0,0,0,21,0,16,0,5,0,0,0,21,0,15,0,9,0,0,0,21,0,14,0,10,0,0,0,21,0,13,0,11,0,0,0,21,0,12,0,63,0,0,0,21,0,11,0,158,0,0,0,21,0,10,0,12,0,0,0,21,0,9,0,21,0,0,0,21,0,8,0,231,0,0,0,21,0,7,0,3,0,0,0,21,0,6,0,89,0,0,0,21,0,5,0,99,0,0,0,21,0,4,0,1,0,0,0,21,0,3,0,20,0,0,0,21,0,2,0,8,0,0,0,21,0,1,0,228,0,0,0,6,0,0,0,0,0,0,0,6,0,0,0,0,0,255,127,6,0,0,0,0,0,0,0};
  struct prog {
    unsigned short len;
    unsigned char *filter;
  } rule = {
    .len = sizeof(filter) >> 3,
    .filter = filter
  };
  if(prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) < 0) { perror("prctl(PR_SET_NO_NEW_PRIVS)"); exit(2); }
  if(prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &rule) < 0) { perror("prctl(PR_SET_SECCOMP)"); exit(2); }
}
