from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import pandas as pd
import numpy as np
import kss
import matplotlib.pyplot as plt
import seaborn as sns
plt.rc('font', family='Malgun Gothic')

def get_formal_status(df_audio):
    df_only_words = df_audio[df_audio["word"] != "<eps>"]
    lectures = df_only_words["lecture"].unique()

    text_dict = {}
    for lecture in lectures:
        corpus = df_only_words[df_only_words["lecture"] == lecture]["word"]
        text = " ".join(corpus)
        sentences = kss.split_sentences(text)
        text_dict[lecture] = sentences


    model = AutoModelForSequenceClassification.from_pretrained("./Model/formal_model/")
    tokenizer = AutoTokenizer.from_pretrained("./Model/formal_tokenizer/")


    formal_classifier = pipeline(
        task="text-classification",
        model=model,
        tokenizer=tokenizer
    )

    result = []
    for lec, sentences in text_dict.items():
        label = [int(formal_classifier(sentence)[0]["label"][-1]) for sentence in sentences]
        prop = np.mean(label)
        result.append((lec, prop))

    df_formal_status = pd.DataFrame(result, columns=["lecture", "formal_prop"])

    return df_formal_status



def plot_formal_info(df_status):
    idx = np.arange(len(df_status))
    w = 0.15

    plt.figure(figsize = (10, 5))
    plt.bar(idx - 1 * w, df_status['MilkT_formal_prop'], width = w, label="MilkT", color="royalblue")
    plt.bar(idx, df_status['Compare_formal_prop'], width = w, label="Compare", color="orange")
    plt.xticks(ticks=idx, labels=df_status["lecture"])
    plt.title("격식체 비교")
    plt.legend()
    plt.ylabel("존대말 사용 비율")
    plt.xlabel("강의 과목")

    plt.show();
