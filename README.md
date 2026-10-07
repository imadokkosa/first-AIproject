# 4.PDFに質問しよう（後編）
- RetrievalはDBｋら文脈を判断し、Promptの指示を読み込んで、ChatGPT APIを呼び出して回答を行う便利なメソッド
- RetrieverはRetrievalQAがベクトルDBの検索をする。
- Retriever(search_type)ではsimilarityはベクトルDBの距離関数で類似度を計算、mmrは回答の重複を防ぐためにレスポンス内の似ている構文を削除する。similarity_score_thresholdは類似度の閾値設定
- Retriever(search_kwargs)ではkが検索にヒットする文書の数設定、score_thresholdはsimilarity_score_thresholdとセットで類似度設定、filterは各データでmetadataを設定することで、取得する文脈を調整できる。
- ConversationalRetrievalChainを使えば質問の回答の後にその内容を組み込んでさらに質問できる。

# 3.PDFに質問しよう（前編）
- Text Splitter で文章を分割。検索精度の向上、トークン削減、ハルシネーション防止が目的。
- 文章分割後、エンベディングを行う。言葉の数値化のことである。距離による類似度判定、表記ゆれ対応のために行う。
- promptでAIへ指示を出せる。
- エンベディングをした後、情報をベクトルDBに載せる。今回はQdrantというメソッドを決める。ベクトルDBはエンベディングを行う際にベクトルDB内にある複数のエンベディングから類似性のあるものを高速で検索できる。

## ページ遷移
-  st.sidebar.radio("Go to", ["A", "B"])でサイドバーにAとBに移動するラジオボタンが表示させる。
- if文で画面にそのページを表示させるかを決める。

## PDFのuploadと読み取り
- データのuploadをする際はst.file_uploader()で出来る。かっこの中に任意のパラメーターを入力することで挙動をコントロールする。今回は拡張子を指定するtypeでpdfを指定した。
- PdfReaderでPDFファイルの読み取りができる。langchainにはDocument Loaderという汎用的な読み取りメソッドがあるがあまり使われない。

# 2.初めてのAIアプリを作ろう
- LLMはinvoke()で呼び出す
- Wedページの本文を取得するにはBeautifulSoupを使う。
- エラー対処はとりあえずexcept:st.write('something wrong')で行う
- containerを使うとUIが整理される
- response.encoding = response.apparent_encodingで自動でサイトの文字コードを推測してくれる。ただし、統計的推理なので精度は低い。



# 1. 最初のAIチャットアプリを作ろう

## Streamlit と LangChain の役割
- Streamlit：UIを作る。ユーザー入力とAI出力の橋渡し。
- LangChain：OpenAI API に最適化された質問を投げて返答を生成する。

## アプリの処理の流れ
1. AIモデルの準備
2. ページレイアウト設定
3. チャット履歴の初期化
4. ユーザー入力の受付
5. AIによる返答生成
6. チャット履歴の表示

## 重要ポイント
- `.env` を読み込むために `load_dotenv()` が必要
- `st.session_state` でチャット履歴を保持する
- `st.chat_input()` でユーザー入力を受け付ける
- `llm.invoke()` でAIモデルを呼び出す（最新LangChain仕様）
- `st.chat_message()` と `st.markdown()` でチャット画面を表示する