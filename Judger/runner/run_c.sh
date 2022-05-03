#!/bin/bash

# usage : ./run_c.sh <TMP_PATH> <problem_path> <MEMORY_LIMIT> <TIME_LIMIT> <OUTPUT_LIMIT> <TC_cnt> <EXEFILE>
#       : ./run_c.sh /tmp/1234 /home/sfoj/problem/1000 10000 1 10000 2 /tmp/1234/1234

UN=sindo
DIFFTOOL=diff
PASSEDTESTS=0

DIFFOPTION="" # default

DIFFARGUMENT=""
if [[ "$DIFFOPTION" != "identical" && "$DIFFOPTION" != "ignore" ]]; then
	DIFFARGUMENT=$DIFFOPTION
fi

TMP_PATH=${1}
shift

PROBLEMPATH=${1}
shift

MEMORY_LIMIT=${1}
shift

TIME_LIMIT=${1}
shift

# TIME_LIMITINT=${1}
# shift

OUTPUT_LIMIT=${1}
shift

TST=$((${1}))
shift

EXECFILE=${1}
shift

DEBUG=false
if $DEBUG; then
	echo "[*] checking args"
	echo "TMP_PATH : " $TMP_PATH
	echo "PROBLEMPATH : " $PROBLEMPATH
	echo "MEMORY_LIMIT : " $MEMORY_LIMIT
	echo "TIME_LIMIT : " $TIME_LIMIT
	# echo "TIME_LIMITINT : " $TIME_LIMITINT
	echo "OUTPUT_LIMIT : " $OUTPUT_LIMIT
	echo "TST : " $TST
	echo "EXECFILE : " $EXECFILE
	echo '[*] done'
fi

err=$TMP_PATH/err
out=$TMP_PATH/out
correct=$TMP_PATH/correct
if $DEBUG; then
	echo "err : " $err
	echo "out : " $out
fi

# For testing
if [ -d "$TMP_PATH" ]; then
  ### Take action if $TMP_PATH exists ###
  echo "Directory Exists : ${TMP_PATH}/..." >> $err
else
  ###  Control will jump here if $TMP_PATH does NOT exists ###
  echo "Error: ${TMP_PATH} not found. Create New Directory" >> $err
  mkdir $TMP_PATH
fi

# for((i=1;i<=TST;i++)); do
# 	if [ -f "$out$i" ]; then
# 		rm $out$i
# 	fi
# done

if [ -f "$err" ]; then
	echo "err exists.." >> $err
	rm $err
	touch $err
else
	touch $err
fi

if [ -f "$out" ]; then
	echo "out exists.." >> $err
	rm $out
	touch $out
else
	touch $out
fi

if [ -f "$correct" ]; then
	rm $correct
	touch $correct
else
	touch $correct
fi

OUTPUT="{\"RESULT\":{"
for((i=1;i<=TST;i++)); do
	
	IN=$PROBLEMPATH/TC/$i.in
	# ulimit -v $((MEMORY_LIMIT+10000))
	# ulimit -m $((MEMORY_LIMIT+10000))
	# ulimit -s $((MEMORY_LIMIT+10000))
	# ulimit -t $((TIME_LIMIT))

	# echo "sudo -u sindo timeout -s9 $((TIME_LIMIT*2)) ./timeouts --just-kill -l $OUTPUT_LIMIT -t $TIME_LIMIT -m $MEMORY_LIMIT -outdir=$out -errdir=$err $EXECFILE <$IN >>$out 2>>$err"
	# sudo -u sindo timeout -s9 $((TIME_LIMIT*2)) ./timeouts --just-kill -l $OUTPUT_LIMIT -t $TIME_LIMIT -m $MEMORY_LIMIT -outdir=$out -errdir=$err $EXECFILE <$IN >>$out 2>>$err
	
	if $DEBUG; then
		echo "bash -c \"timeout ${TIME_LIMIT}s $EXECFILE <$IN >>$out.tmp 2>>$err\"" >> $err
	fi
	bash -c "timeout ${TIME_LIMIT}s $EXECFILE <$IN >$out.tmp 2>>$err"
	# $EXECFILE <$IN >>$out.tmp 2>>$err
	EXITCODE=$?

	# echo -e "sudo -u sindo timeout -s9 $((TIMELIMITINT*2)) $CMD <$IN >out 2>err" >>/home/hu/Desktop/log
	# KILL all processes of another_user (A process may still be alive!)
	# If you are running codes as another_user, also uncomment this line:
	# sudo -u sindo pkill -9 -u sindo

	# ./runcode.sh $MEMORY_LIMIT $TIME_LIMITINT $PROBLEMPATH/TC/$i.in "./timeout --just-kill -l $OUTLIMIT -t $TIME_LIMIT -m $MEMORY_LIMIT $EXEFILE"
	# #$TIMEOUT ./$FILENAME <$PROBLEMPATH/TC/$i.in >out 2>/dev/null
	
	echo "EXIT : "$EXITCODE  >> $err
	echo "" >> $err
	# mv thetemp out

	if [ $EXITCODE -eq 124 ]; then
		OUTPUT="${OUTPUT}\"${i}\":\"Time Limit Exceeded\"}, \"SCORE\":0}"
		# echo "Time Limit Exceeded"
		echo $OUTPUT
		exit 0
	fi

	if [ $EXITCODE -eq 136 ]; then
		OUTPUT="${OUTPUT}\"${i}\":\"Runtime Error( Floating point exception )\"}, \"SCORE\":0}"
		# echo "Runtime Error( Floating point exception )"
		echo $OUTPUT
		exit 0
	fi

	if [ $EXITCODE -eq 139 ]; then
		OUTPUT="${OUTPUT}\"${i}\":\"Runtile Error\"}, \"SCORE\":0}"
		# echo "Runtime Error"
		echo $OUTPUT
		exit 0
	fi

	if [ $EXITCODE -eq 159 ]; then
		OUTPUT="${OUTPUT}\"${i}\":\"Bad System Call\"}, \"SCORE\":0}"
		# echo "Bad System Call"
		echo $OUTPUT
		exit 0
	fi

	ACCEPTED=false
	if [ $EXITCODE -eq 0 ]; then
		# checking correctness of output
		# cp $PROBLEMPATH/TC/$i.out $TMP_PATH
		
		# # Add a newline at the end of both files
		tr -d '\n' <$out.tmp >$out 2>/dev/null && mv $out $out.tmp
		tr -d '\n' <$PROBLEMPATH/TC/$i.out >$correct.tmp 2>/dev/null

		sed 's/^[ \t]*//;s/[ \t]*$//' <$out.tmp >$out 2>/dev/null
		sed 's/^[ \t]*//;s/[ \t]*$//' <$correct.tmp >$correct 2>/dev/null
		# echo $PROBLEMPATH/TC/$i.out >> $err
		# echo $out >> $err
		# echo $correct >> $err

		# Compare output files
		echo "$DIFFTOOL $DIFFARGUMENT $out $correct >/dev/null 2>/dev/null" >> $err
		$DIFFTOOL $DIFFARGUMENT $out $correct >/dev/null 2>/dev/null
		if [ $? -eq 0 ]; then
			ACCEPTED=true
		fi
	fi
	
	if $ACCEPTED; then
		if [ $i -eq $TST ]; then
			OUTPUT="${OUTPUT}\"${i}\":\"ACCEPTED\"}, \"SCORE\":"
		else
			OUTPUT="${OUTPUT}\"${i}\":\"ACCEPTED\", "
		fi
		
		((PASSEDTESTS=$PASSEDTESTS+1))
	else
		if [ $i -eq $TST ]; then
			OUTPUT="${OUTPUT}\"${i}\":\"WRONG\"}, \"SCORE\":"
		else
			OUTPUT="${OUTPUT}\"${i}\":\"WRONG\", "
		fi
	fi

done

((SCORE=PASSEDTESTS*100/TST)) # give score from 10,000

echo $SCORE >> $err

OUTPUT="${OUTPUT}${SCORE}}"
if [ $SCORE -eq 100 ]; then
	echo $OUTPUT
else
	echo $OUTPUT
	# $PASSEDTESTS/$TST-"($SCORE%)"
fi
