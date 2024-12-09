prepare environment
```
pip install -r requirements.txt 
```

select desired step
```
if __name__=="__main__":
    # for_pop_init("TREC")                          <-- step 1-1
    # for_pop_contr("TREC")                         <-- step 1-2
    # main_init(["CR"])                             <-- step 1
    main_experiment("MR", ["EvoDE", "CoEvo2"])      <-- step 2
```

run
```
python main.py
```