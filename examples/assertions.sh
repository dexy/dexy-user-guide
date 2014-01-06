### "generate"
dexy gen -t assertions -d assertions
cd assertions

### "run-without-assertions"
cp docs-without-assertions.md docs.md
dexy

### "save-results"
mv output/docs.md docs-without-assertions-results.md

### "setup-for-assertions"
cp docs-with-assertions.md docs.md
dexy reset

### "run-with-assertions"
dexy

### "fix-broken-python"
echo "print 'foo'" > broken.py
dexy reset

### "run-with-assertions-again"
dexy
cp output/docs.md docs-with-assertions-results.md

### "list-assertions"
dexy env | grep assert
