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

開始實驗
```
python main.py
```

## 模組說明

本專案的目錄結構涵蓋了多個核心模組，這些模組負責實驗執行、指令生成、以及評分等部分。以下是目錄結構與主要模組的詳細介紹：
1. **主程式 (`main.py`)**

    作為系統的執行檔，透過調整主程式入口的內容，系統可根據需求選擇進行的優化任務與階段，提供靈活的運行方式。

1. **配置模組 (`config.ini`)**

    包含專案所需的超參數，如模型名稱及API網址 (例：`http://{host}`)。

1. **需求檔 (`requirement.txt`)**

    列出專案運行所需的所有Python套件及其版本，方便開發者快速配置運行環境。

1. **模型模組 (`utils/`)**

    這是系統的核心邏輯模組，包含了演化方法、評分方式、.....等等。主要文件如下：

    - **進化方法 (`method_update/`)**

        - **抽象基底類別：`population_updater.py`**

            提示群可藉由這種類別進行優化。類別中包含新提示生成 (`get_distinct_new_propmt`) 、評分方法 (`evaluate`) 、格式化提示群 (`formulate_population`)。並指定各優化方式須涵蓋的抽象方法，包括選擇父提示 (`sample_prompt`) 、更新提示群 (`update`) 、優化流程 (`f`)。

        - **實現類別：`evo_prompt.py`**

            基於不同進化策略實現抽象方法。其中，`EvoGA` 和 `EvoDE` 為基準進化類別，而本系統的核心為執行提示優化的 `CoEvo2` 及建立對比提示群的 `EvoGA4Contr`。

    - **評分 (`get_score/`)**

        - **抽象基底類別：`judge_abstract.py`**

            提供模型在特定「提示與資料集」組合下的評估框架，包括呼叫 LLM (`get_reply`)  和實驗設計 (`experiment`)  等方法，並針對不同任務（如分類問題或開放問答）定義抽象方法，如LLM問答方式 (`method`) 和回答擷取 (`extract_answer`)。

        - **實現類別：`judge_cls.py`**

            專為分類任務設計，實現了上述抽象方法，並新增「關鍵字—標籤」轉換器 (`set_switch_keyword`)  提升處理靈活性。

    - **建立指令 (`ttl_prompt/`)**

        - **模板：`template/`**

            包含三個模板檔案，用於生成新提示或評分提示時的LLM指令，這些模板以格式化字串（f-string）呈現，便於重複使用。

        - **抽象基底類別：`get_prompt.py`**

            該類別提供指令生成的框架，包含三大步驟：「確認模板 (`get_template_default`) 」、「確認佔位符 (`get_ttl_key`) 」與「生成指令 (create_prompt) 」。其中，第一步「確認模板」為抽象方法，允許根據使用場景靈活定義不同的模板選擇邏輯，確保框架在各種應用情境下具備高度的可擴展性。

        - **實現類別：prompt_4_deal_task.py**

            針對評分任務實現，除了繼承基底類別的功能外，新增了範例學習方法 (`create_few_shot`)，以提升 LLM 處理能力。

1. **資料模組  (`dataset/`)**

    每個任務對應一個資料夾，內含專屬的訓練與測試資料集。訓練資料約 200 筆，測試資料介於 300 至 500 筆之間。

1. **提示模組  (`prompt/`)**

    該模組包含三個子資料夾：`raw/`、`population_init/`、`contr/`，每個子資料夾內設有針對各任務的專屬資料夾，統一管理提示相關資源。

1. **結果  (`record/`)**

    所有進化實驗的結果均存放於此資料夾，便於後續分析與比較


## Code Strucutre

```python
.
├── dataset
│   ├── AGNews
│   │   └── seed5_200
│   │       └── seed5_200.json
│   ...
│   └── TREC
│       └── seed5_200
│           └── seed5_200.json
├── prompt
│   ├── contr
│   │   ├── AGNews
│   │   │  └── test.json
│   │   ...
│   │   └── TREC
│   │      └── test.json
│   │
│   │── population_init
│   │   ├── AGNews
│   │   │  └── test.json
│   │   ...
│   │   └── TREC
│   │      └── test.json
│   │
│   └── raw
│       ├── AGNews
│       │  └── test.json
│       ...
│       └── TREC
│          └── test.json
│
├── record
│   ├── {experiment_name}
│   │   ├── {experiment_time}
│   │   │   ├── {evolver_name}
│   │   │   │   ├── {iteration_0}
│   │   │   │   ├── {iteration_1}
│   │   │   │   ...
│   │   │   │
│   │   │   ├── {evolver_name}
│   │   │   │   ├── {iteration_0}
│   │   │   │   ├── {iteration_1}
│   │   │   │   ...
│   │   │   │
│   │   └── {experiment_time}
|
├── utils



```
