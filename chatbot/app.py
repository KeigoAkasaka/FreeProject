
from flask import Flask, render_template, request, jsonify
import os
import cohere
from dotenv import load_dotenv

import requests
from datetime import datetime

# 環境変数を読み込む
load_dotenv()

app = Flask(__name__)

# Cohere APIキーを環境変数から取得
cohere_api_key = os.getenv('COHERE_API_KEY')

if not cohere_api_key:
    raise ValueError("COHERE_API_KEY環境変数が設定されていません。.envファイルを確認してください。")

# Cohereクライアントを初期化
co = cohere.Client(cohere_api_key)

def get_greeting():
    """現在の時刻に基づいて挨拶を返す"""
    hour = datetime.now().hour
    if 5 <= hour < 11:
        return "おはようございます"
    elif 11 <= hour < 18:
        return "こんにちは"
    else:
        return "こんばんは"

def get_weather():
    """Open-Meteo APIを使用して仙台の天気を取得する"""
    try:
        # 仙台の座標: 緯度 38.2682, 経度 140.8694
        url = "https://api.open-meteo.com/v1/forecast?latitude=38.2682&longitude=140.8694&current_weather=true&timezone=Asia%2FTokyo"
        response = requests.get(url)
        data = response.json()
        
        if 'current_weather' in data:
            weather_code = data['current_weather']['weathercode']
            temperature = data['current_weather']['temperature']
            
            # WMO Weather interpretation codes (WW)
            # https://open-meteo.com/en/docs
            weather_map = {
                0: "快晴", 1: "晴れ", 2: "晴れ時々曇り", 3: "曇り",
                45: "霧", 48: "霧氷",
                51: "霧雨", 53: "霧雨", 55: "霧雨",
                61: "雨", 63: "雨", 65: "雨",
                71: "雪", 73: "雪", 75: "雪",
                80: "にわか雨", 81: "にわか雨", 82: "にわか雨",
                95: "雷雨", 96: "雷雨", 99: "雷雨"
            }
            
            weather_desc = weather_map.get(weather_code, "不明")
            return f"現在の仙台の天気は{weather_desc}、気温は{temperature}℃です。"
        else:
            return "天気の取得に失敗しました。"
    except Exception as e:
        return f"天気情報の取得中にエラーが発生しました: {str(e)}"

@app.route('/')
def index():
    """メインページを表示"""
    # 挨拶を悟空風に変更
    greeting = "オッス！オラ悟空！"
    
    # 天気情報を取得して悟空風にアレンジ
    weather_info = get_weather()
    if "天気は" in weather_info:
        weather_info = weather_info.replace("現在の仙台の天気は", "今の仙台の天気は").replace("です。", "だぞ！")
    
    # NHKニュースのRSSから最新ニュースを取得（完全無料、APIキー不要）
    import random
    import feedparser
    news_topic = ""
    
    try:
        # NHKニュースのRSSフィードを取得
        rss_url = "https://www.nhk.or.jp/rss/news/cat0.xml"
        feed = feedparser.parse(rss_url)
        
        if feed.entries:
            # ランダムに1つのニュースを選択
            article = random.choice(feed.entries[:5])  # 最新5件から選択
            title = article.get('title', '')
            if title:
                # 悟空風にアレンジ
                news_topic = f"最近のニュースで「{title}」ってのがあったぞ！"
    except Exception as e:
        print(f"ニュース取得エラー: {e}")
    
    # ニュースが取得できなかった場合のフォールバック
    if not news_topic:
        fallback_topics = [
            "最近、AIがすげぇ進化してるらしいな！オラもビックリだぞ！",
            "円安が進んでるって聞いたぞ！お金のことはよくわかんねぇけどな！",
            "今年も残りわずかだな！おめえは何か目標あるか？",
            "寒くなってきたな！風邪ひかねぇように気をつけろよ！",
            "最近、宇宙開発がすげぇことになってるらしいぞ！オラもワクワクすっぞ！"
        ]
        news_topic = random.choice(fallback_topics)
    
    initial_message = f"{greeting} {weather_info} {news_topic} オラに何か聞きてぇことあっか？"
    
    # スタンプ画像のリストを取得
    stamp_dir = os.path.join(app.static_folder, 'stamp')
    stamps = []
    if os.path.exists(stamp_dir):
        for filename in os.listdir(stamp_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                stamps.append(filename)
    
    # 背景画像をランダムに選択
    import random
    haikei_dir = os.path.join(app.static_folder, 'haikei')
    background_image = None
    if os.path.exists(haikei_dir):
        haikei_files = [f for f in os.listdir(haikei_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
        if haikei_files:
            background_image = 'haikei/' + random.choice(haikei_files)
    
    return render_template('index.html', initial_message=initial_message, stamps=stamps, background_image=background_image)

@app.route('/chat', methods=['POST'])
def chat():
    """チャットメッセージを処理してAIからの応答を返す"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'メッセージが空です'}), 400
        
        # スタンプメッセージの処理
        ai_input_message = user_message
        if user_message.startswith('[STAMP:') and user_message.endswith(']'):
            stamp_filename = user_message[7:-1]
            # ファイル名から拡張子を除いた部分を取得してコンテキストにする
            stamp_name = os.path.splitext(os.path.basename(stamp_filename))[0]
            
            if 'ok' in stamp_name.lower():
                ai_input_message = "（ユーザーが「OK」のスタンプを送信しました）"
            elif 'thanks' in stamp_name.lower():
                ai_input_message = "（ユーザーが「ありがとう」のスタンプを送信しました）"
            elif 'good' in stamp_name.lower():
                ai_input_message = "（ユーザーが「いいね」のスタンプを送信しました）"
            elif 'daijoubu' in stamp_name.lower():
                ai_input_message = "（ユーザーが「大丈夫」のスタンプを送信しました）"
            else:
                ai_input_message = f"（ユーザーが「{stamp_name}」というスタンプを送信しました）"
        
        # Cohere Chat APIを使用して応答を生成
        # 利用可能なモデル: command-a-03-2025, command-r-08-2024, command-r-plus-08-2024
        # 悟空のペルソナをメッセージに含める
        goku_instruction = "あなたはドラゴンボールの孫悟空として返答してください。一人称は「オラ」、相手のことは「おめえ」と呼び、「〜だぞ」「〜だ！」などの語尾を使ってください。敬語は使わないでください。\n\n"
        response = co.chat(
            model='command-a-03-2025',
            message=goku_instruction + ai_input_message,
            max_tokens=300,
            temperature=0.7,
        )
        
        ai_message = response.text.strip()
        
        return jsonify({
            'message': ai_message,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'エラーが発生しました: {str(e)}',
            'status': 'error'
        }), 500

if __name__ == '__main__':
    # ポート5000がmacOSのAirPlay Receiverで使用されている可能性があるため、3000を使用
    app.run(debug=True, host='0.0.0.0', port=3000)

