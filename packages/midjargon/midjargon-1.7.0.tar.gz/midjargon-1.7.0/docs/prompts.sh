cat ./prompts.txt | while read p; do
    echo "======"
    echo $p
    python -m midjargon mj "$p" -j
done
