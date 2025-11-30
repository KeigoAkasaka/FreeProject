# チャットボットアプリ

FlaskとCohere APIを使用したチャットボットアプリケーションです。

## 機能

- FlaskベースのWebアプリケーション
- Cohere APIを使用したAI応答生成
- ユーザーとAIのメッセージを色分け表示
- モダンで使いやすいUI

## セットアップ方法

### 1. 仮想環境の作成（推奨）

macOSでは、仮想環境を使用することを強く推奨します：

```bash
python3 -m venv venv
```

### 2. 仮想環境の有効化

```bash
source venv/bin/activate
```

仮想環境が有効化されると、プロンプトの前に`(venv)`が表示されます。

### 3. 必要なパッケージのインストール

仮想環境を有効化した状態で、以下のコマンドを実行します：

```bash
pip install -r requirements.txt
```

**注意**: macOSで`pip`コマンドが見つからない場合は、`pip3`または`python3 -m pip`を使用してください。

### 4. 環境変数の設定

1. `.env.example`を`.env`にコピーします：
   ```bash
   cp .env.example .env
   ```

2. `.env`ファイルを開き、CohereのAPIキーを設定します：
   ```
   COHERE_API_KEY=your_actual_cohere_api_key_here
   ```

   CohereのトライアルAPIキーは、[Cohereの公式サイト](https://cohere.com/)から取得できます。

### 5. アプリケーションの起動

**仮想環境を有効化した状態で**、以下のコマンドでアプリケーションを起動します：

```bash
python app.py
```

または

```bash
flask run
```

**注意**: 仮想環境を使用している場合は、起動前に必ず`source venv/bin/activate`を実行してください。

### 6. ブラウザでアクセス

アプリケーションが起動したら、ブラウザで以下のURLにアクセスします：

```
http://localhost:3000
```

**注意**: macOSではポート5000がAirPlay Receiverで使用されている可能性があるため、アプリはポート3000で起動します。

## 使い方

1. ブラウザでアプリケーションを開きます
2. 下部の入力欄にメッセージを入力します
3. 「送信」ボタンをクリックするか、Enterキーを押します
4. AIからの応答が表示されます

## メッセージの色分け

- **ユーザーのメッセージ**: 紫のグラデーション背景（右側に表示）
- **AIのメッセージ**: 白背景（左側に表示）

## トラブルシューティング

### APIキーエラーが表示される場合

- `.env`ファイルが正しく作成されているか確認してください
- APIキーが正しく設定されているか確認してください
- `.env`ファイルがプロジェクトのルートディレクトリにあることを確認してください

### パッケージのインストールエラー

**仮想環境を使用していない場合**、以下のエラーが表示されることがあります：
```
error: externally-managed-environment
```

この場合は、必ず仮想環境を作成して使用してください：

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### `pip`コマンドが見つからない場合

macOSでは、`pip`の代わりに以下を試してください：

```bash
pip3 install -r requirements.txt
```

または

```bash
python3 -m pip install -r requirements.txt
```

## 技術スタック

- **バックエンド**: Flask (Python)
- **AI API**: Cohere
- **フロントエンド**: HTML, CSS, JavaScript

