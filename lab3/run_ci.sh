#!/usr/bin/env bash
pylint decrypt.py --output-format=json > pylint_report.json
pylint decrypt.py --reports=y --score=y
pylint_res=$?
python3 -m unittest -v
tests_res=$?
if [[ $pylint_res -eq 0 && $tests_res -eq 0 ]]; then
  echo "OK"
else
  echo "Имеются ошибки"
fi
