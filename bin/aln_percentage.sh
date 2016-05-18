#!/bin/bash
/usr/local/bin/infoalign -sequence $1 -stdout -auto --noheading | /usr/bin/awk ' { ident += $7 / $3 ; nrow += 1 } END { ident = ident / nrow; print ident}'
