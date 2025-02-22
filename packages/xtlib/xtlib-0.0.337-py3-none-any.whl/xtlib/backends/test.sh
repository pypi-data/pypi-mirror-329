        # define the duration function (for a running log timer)
        duration() {
        diff=$(( $(date -u +%s) - $XT_STARTED))')
        if [ $diff -gt 72000 ]; then echo $(echo "scale=2; $diff/72000" | bc) days ;
        elif [ $diff -gt 3600 ]; then echo $(echo "scale=2; $diff/3600" | bc) hrs  ;
        elif [ $diff -gt 60 ]; then echo $(echo "scale=2; $diff/60" | bc) mins  ; 
        else echo $diff secs ; fi }