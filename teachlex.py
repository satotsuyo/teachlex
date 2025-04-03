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
                elif category == "中学校":
                    textbooks = ["BS", "HWG", "NH", "NC", "OW", "SS"]

                if category in ["小学校", "中学校"]:
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
