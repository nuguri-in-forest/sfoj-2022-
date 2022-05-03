#!/bin/bash

# cur directory : ./Judger
# ./compile_cxx.sh <file_name>
# ./compile_cxx.sh abc

OPTIONS="-ansi -fno-asm -O2 -Wall -lm --static"
CC="g++"
FILENAME=${1}

cp ./shield/shield.cpp /tmp/$FILENAME/`echo $FILENAME`_shield.cpp
echo "#include</tmp/"$FILENAME"/`echo $FILENAME.cpp`>" >> /tmp/$FILENAME/`echo $FILENAME`_shield.cpp
$CC /tmp/$FILENAME/`echo $FILENAME`_shield.cpp $OPTIONS -o /tmp/$FILENAME/$FILENAME >/dev/null

exit $?