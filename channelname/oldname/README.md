Date : 2019/01/04

chname_ondtr.txt was taken by 
```
$ t
$ cd k1rack/db
$ less example_rack.db | grep K1 | sed -r 's/^.*\"(.*)\"\)/\1/' > /users/Miyo/kagra-pem/channelname/chname_ondr.txt 
```


chname.txt was taken by
```
$ chans
$ cd daq
$ less K1PEM*.ini | grep -e "^\[K1.*_DQ\]" | sed -r 's/\[(.*)\]/\1/' > /users/Miyo/kagra-pem/channelname/chname.txt
```