import streamlit as st
import pandas as pd
import spacy

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

col1, col2 = st.columns([1, 2])

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
                for col in ["頻度", "語彙レベル", "使用教科書数", "ARF"]:
                    if col in result.columns:
                        st.markdown(f"<p style='font-weight:normal;'>{col}: <b style='font-size:18px;'>{result[col].values[0]}</b></p>", unsafe_allow_html=True)
                st.markdown("---")
            else:
                st.warning(f"入力された単語は{category}のリストに含まれていません。")
    else:
        st.info("単語を入力すると、ここに結果が表示されます。")
