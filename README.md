


## Inference

準備環境
```
pip install -r requirements.txt 
```

指定目標任務與進化方法，並選擇欲執行的步驟
其中 `main_init()` 由 `for_pop_init()` 與 `for_pop_contr()` 兩個步驟組成
```
if __name__=="__main__":
    task = "TREC"
    evolvers = ["EvoDE", "CoEvo2"]

    # for_pop_init("TREC")             <-- step 1-1
    # for_pop_contr("TREC")            <-- step 1-2
    # main_init([task])                <-- step 1
    main_experiment(task, evolvers)    <-- step 2
```

run
```
python main.py
```
