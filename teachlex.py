import streamlit as st
import pandas as pd
import spacy

# SpaCyの英語モデルをロード
nlp = spacy.load("en_core_web_sm")

# 小学校、中学校、高等学校英語コミュニケーション、高等学校論理表現のCSVファイルのURL
CSV_URL_E = "http://hirosakieigo.weblike.jp/satoclass/material/webapp/vocabdata_E.csv"
CSV_URL_J = "http://hirosakieigo.weblike.jp/satoclass/material/webapp/vocabdata_J.csv"
CSV_URL_HE = "http://hirosakieigo.weblike.jp/satoclass/material/webapp/vocabdata_HE.csv"
CSV_URL_HL = "http://hirosakieigo.weblike.jp/satoclass/material/webapp/vocabdata_HL.csv"

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df_e = load_data(CSV_URL_E)
df_j = load_data(CSV_URL_J)
df_he = load_data(CSV_URL_HE)
df_hl = load_data(CSV_URL_HL)

st.title("TeachLex Scope")
st.markdown("""
<p style="font-size:16px;">
小学校から高等学校の英語の教科書の使用状況をお知らせします。
</p>
""", unsafe_allow_html=True)

# レイアウト設定
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 単語を検索")
    word = st.text_input("単語を入力してください", "")

# 単語のlemmaを取得する関数
def get_lemma(input_word):
    doc = nlp(input_word)
    return doc[0].lemma_  # 最初の単語のlemmaを返す

with col2:
    if word:  # テキストボックスに入力があった場合のみ処理を実行
        lemma_word = get_lemma(word)  # 入力された単語をlemmaに変換
        st.write(f"入力された単語: {word} → lemma形式: {lemma_word}")

        # 小学校の教科書の使用状況
        result_e = df_e[df_e["単語"] == lemma_word]
        if not result_e.empty:
            st.subheader("小学校の教科書の使用状況")
            st.markdown(f"<p style='font-weight:normal;'>頻度: <b style='font-size:18px;'>{result_e['頻度'].values[0]}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-weight:normal;'>語彙レベル: <b style='font-size:18px;'>{result_e['語彙レベル'].values[0]}</b></p>", unsafe_allow_html=True)

            textbooks = ["R2", "BS", "HWG", "NH", "NC", "OW", "SS"]
            states = ['〇' if result_e[book].values[0] else '×' for book in textbooks]

            data_e = pd.DataFrame([textbooks, states], index=["教科書名", "使用の有無"])
            st.table(data_e)
        else:
            st.warning("入力された単語は小学校のリストに含まれていません。")

        # 中学校の教科書の使用状況
        result_j = df_j[df_j["単語"] == lemma_word]
        if not result_j.empty:
            st.subheader("中学校の教科書の使用状況")
            st.markdown(f"<p style='font-weight:normal;'>頻度: <b style='font-size:18px;'>{result_j['頻度'].values[0]}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-weight:normal;'>語彙レベル: <b style='font-size:18px;'>{result_j['語彙レベル'].values[0]}</b></p>", unsafe_allow_html=True)

            textbooks = ["BS", "HWG", "NH", "NC", "OW", "SS"]
            states = ['〇' if result_j[book].values[0] else '×' for book in textbooks]

            data_j = pd.DataFrame([textbooks, states], index=["教科書名", "使用の有無"])
            st.table(data_j)
        else:
            st.warning("入力された単語は中学校のリストに含まれていません。")

        # 高等学校英語コミュニケーション
        result_he = df_he[df_he["単語"] == lemma_word]
        if not result_he.empty:
            st.markdown("---")
            st.subheader("高等学校英語コミュニケーションの使用状況")
            st.markdown(f"<p style='font-weight:normal;'>語彙レベル: <b style='font-size:18px;'>{result_he['語彙レベル'].values[0]}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-weight:normal;'>頻度: <b style='font-size:18px;'>{int(result_he['ARF'].values[0])}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-weight:normal;'>使用教科書数: <b style='font-size:18px;'>{int(result_he['使用教科書数'].values[0])}</b></p>", unsafe_allow_html=True)
        else:
            st.warning("入力された単語は英語コミュニケーションのリストに含まれていません。")

        # 高等学校論理表現
        result_hl = df_hl[df_hl["単語"] == lemma_word]
        if not result_hl.empty:
            st.markdown("---")
            st.subheader("高等学校論理表現の使用状況")
            st.markdown(f"<p style='font-weight:normal;'>語彙レベル: <b style='font-size:18px;'>{result_hl['語彙レベル'].values[0]}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-weight:normal;'>頻度: <b style='font-size:18px;'>{int(result_hl['ARF'].values[0])}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-weight:normal;'>使用教科書数: <b style='font-size:18px;'>{int(result_hl['使用教科書数'].values[0])}</b></p>", unsafe_allow_html=True)
        else:
            st.warning("入力された単語は論理表現のリストに含まれていません。")
    else:
        st.warning("ここに結果が表示されます")
