### "prep"
mv run-example.yaml dexy.yaml

### "dexy-without-setup"
dexy

### "setup"
dexy setup

### "dexy"
dexy

### "show-hidden-files"
ls .dexy

### "info"
dexy info -expr hello

### "data-info"
dexy datas -alias generic

### "datas"
dexy datas

### "data-info-ws"
dexy info -expr hello.txt -ws
