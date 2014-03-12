Document='
============================
hiking_splitfile.bash
----------------------------
arguments
    |- $filename
(   |- splitnum = 2   )
output
============================
'

# --- arguments ---
NEEDARGNUM=`echo "$Document"|grep -A 100 "arguments"|grep -B 100 "output"|perl -pe 's/^\(.*\n$//'|wc -l`
NEEDARGNUM=$(($NEEDARGNUM-2))
if [ $# -lt $NEEDARGNUM ];then
   echo "$Document"
   exit 1
fi
filename=$1
base=${filename%.*}
base=${base}_split
ext=.${filename##*.}
splitnum=2;if [ $# -ge 2 ];then splitnum=$2;fi

# --- main --- #
linenum=`less $filename|wc -l`
outlinenum=$(($linenum/$splitnum))

splitnum=$(($splitnum-1))
less $filename|tail -n +$(($outlinenum*$splitnum+1)) > ${base}$((splitnum+1))$ext
echo "less $filename|tail -n +$(($outlinenum*$splitnum+1))"
while [ $splitnum -gt 0 ];do
    splitnum=$(($splitnum-1))
    less $filename|tail -n +$(($outlinenum*$splitnum+1))|head -$outlinenum > ${base}$(($splitnum+1))$ext
    echo "less $filename|tail -n +$(($outlinenum*$splitnum+1))|head -$outlinenum"
done