#!/bin/bash
# radiolink_scanner.sh - Zaměření na frekvence používané pro radioreléové spoje

LOG_DIR="$HOME/radiolink_logs"
mkdir -p $LOG_DIR

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Známé rozsahy pro radioreléové spoje České telekomunikace
RANGES=(
  "330M:400M:100k"   # Starší analogové spoje
  "400M:420M:100k"   # Utility frekvence
  "1.35G:1.5G:250k"  # L-band spoje
)

echo "Skenování frekvenčních rozsahů radioreléových spojů"
echo "Výsledky budou uloženy do: $LOG_DIR"

for range in "${RANGES[@]}"; do
  echo "Skenuji rozsah: $range"
  OUTPUT_FILE="$LOG_DIR/radiolink_${range//[:.]/}_${TIMESTAMP}.csv"
  
  rtl_power -f $range -g 40 -i 30 -e 600s $OUTPUT_FILE
  
  # Najdi Top 5 nejsilnějších signálů v tomto rozsahu
  echo "Top 5 signálů v rozsahu $range:"
  awk -F, "NR>1 {if (\$7 > -70) print \$2 \"MHz: \" \$7 \"dB\"}" $OUTPUT_FILE | sort -nr -k2 | head -5
  
  echo "----------------------------------------"
done
