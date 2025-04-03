import streamlit as st
import pandas as pd
import spacy
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
import nltk

# 必要なデータをダウンロード
nltk.download('wordnet')
nltk.download('omw-1.4')

# レンマタイザの初期化
lemmatizer = WordNetLemmatizer()

# SpaCyの英語モデルをロード
@st.cache_data
def load_nlp_model():
    return spacy.load("en_core_web_sm")

nlp = load_nlp_model()

# CSVファイルのURLリスト
CSV_URLS = {
    "小学校": "http://hirosakieigo.weblike.jp/satoclass/material/webapp/vocabdata_E.csv",
    "中学校": "http://hirosakieigo.weblike.jp/satoclass/material/webapp/vocabdata_J.csv",
    "高等学校英語コミュニケーション": "http://hirosakieigo.weblike.jp/satoclass/material/webapp/vocabdata_HE.csv",
    "高等学校論理表現": "http://hirosakieigo.weblike.jp/satoclass/material/webapp/vocabdata_HL.csv",
}

TEXT_URLS = {
    "小学校": "http://hirosakieigo.weblike.jp/appdvlp/txtbk/ES.txt",
    "中学校": "http://hirosakieigo.weblike.jp/appdvlp/txtbk/JHS.txt",
    "高等学校英語コミュニケーション": "http://hirosakieigo.weblike.jp/appdvlp/txtbk/EC.txt",
    "高等学校論理表現": "http://hirosakieigo.weblike.jp/appdvlp/txtbk/LE.txt",
}

# データをロードする関数
@st.cache_data
def load_data(url):
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"データの読み込みに失敗しました: {url}\nエラー: {str(e)}")
        return pd.DataFrame()  # 空のDataFrameを返す

# データのロード
dataframes = {key: load_data(url) for key, url in CSV_URLS.items()}

st.title("TeachLex Scope")
st.markdown("""<p style="font-size:16px;">小学校から高等学校の英語の教科書の使用状況をお知らせします。</p>""", unsafe_allow_html=True)

# 3カラムのレイアウト設定
col1, col2, col3 = st.columns([2, 4, 4])

with col1:
    st.markdown("### 単語を検索")
    word = st.text_input("単語を入力してください", "")

# 単語のlemmaを取得する関数
def get_lemma(input_word):
    doc = nlp(input_word)
    return doc[0].lemma_ if doc else input_word  # 最初の単語のlemmaを返す

with col2:
    if word:
        lemma_word = get_lemma(word)
        st.write(f"入力された単語: {word} → lemma形式: {lemma_word}")

        # 各カテゴリーのデータ処理
        for category, df in dataframes.items():
            if df.empty:
                continue
            result = df[df["単語"] == lemma_word]
            if not result.empty:
                st.subheader(f"{category}の教科書の使用状況")

                # 特定の条件でテーブルを作成
                if category == "小学校":
                    textbooks = ["R2", "BS", "HWG", "NH", "NC", "OW", "SS"]
                    states = ['〇' if result[book].values[0] else '×' for book in textbooks]
                    data_table = pd.DataFrame([textbooks, states], index=["教科書名", "使用の有無"])
                    st.table(data_table)
                
                elif category == "中学校":
                    textbooks = ["BS", "HWG", "NH", "NC", "OW", "SS"]
                    states = ['〇' if result[book].values[0] else '×' for book in textbooks]
                    data_table = pd.DataFrame([textbooks, states], index=["教科書名", "使用の有無"])
                    st.table(data_table)

                # 共通の情報を表示
                for col in ["頻度", "語彙レベル", "使用教科書数", "ARF"]:
                    if col in result.columns:
                        st.markdown(f"<p style='font-weight:normal;'>{col}: <b style='font-size:18px;'>{result[col].values[0]}</b></p>", unsafe_allow_html=True)
                st.markdown("---")
            else:
                st.warning(f"入力された単語は{category}のリストに含まれていません。")
    else:
        st.info("単語を入力すると、ここに結果が表示されます。")

# ワードクラウドの生成と表示
with col3:
    if word:
        st.markdown("### ワードクラウド")
        for category, text_url in TEXT_URLS.items():
            response = requests.get(text_url)
            if response.status_code == 200:
                text = response.text
            else:
                st.error(f"エラー: {category} のテキストデータを取得できませんでした。")
                continue

            # テキストを単語に分割して原形に変換
            words = [lemmatizer.lemmatize(word.lower()) for word in text.split()]
            context_words = []
            for idx, w in enumerate(words):
                if w == lemma_word:
                    # 前後3語を取得（範囲外の場合を考慮）
                    start = max(0, idx - 3)
                    end = min(len(words), idx + 4)
                    context_words.extend(words[start:idx] + words[idx+1:end])

            # 周辺語をスペースで連結してテキスト化
            context_text = " ".join(context_words)

            # context_text が空の場合の処理
            if not context_text:
                st.warning(f"'{word}' に関連する語が見つかりませんでした（{category}）。")
                continue

            # ワードクラウドを生成
            word_cloud = WordCloud(width=300, height=300, background_color='white', max_words=200).generate(context_text)

            # ワードクラウドを表示
            st.markdown(f"#### {category}")
            st.image(word_cloud.to_array(), use_container_width=True)
