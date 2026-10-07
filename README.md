# 2.初めてのAIアプリを作ろう
- LLMはinvoke()で呼び出す
- Wedページの本文を取得するにはBeautifulSoupを使う。
- エラー対処はとりあえずexcept:st.write('something wrong')で行う
- containerを使うとUIが整理される
- response.encoding = response.apparent_encodingで自動でサイトの文字コードを推測してくれる。



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
