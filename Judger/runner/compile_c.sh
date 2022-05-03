#!/bin/bash

# cur directory : ./Judger
# ./compile_c.sh <file_name>
# ./compile_c.sh abc

OPTIONS="-ansi -fno-asm -O2 -Wall -lm --static"
CC="gcc"
FILENAME=${1}

cp ./shield/shield.c /tmp/$FILENAME/`echo $FILENAME`_shield.c
echo "#include</tmp/"$FILENAME"/`echo $FILENAME.c`>" >> /tmp/$FILENAME/`echo $FILENAME`_shield.c
$CC /tmp/$FILENAME/`echo $FILENAME`_shield.c $OPTIONS -o /tmp/$FILENAME/$FILENAME >/dev/null

exit $?