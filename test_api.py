#!/usr/bin/env python3
"""
Azuma Insight Quotes API テストスクリプト
"""

import requests
import json
from datetime import datetime

# API ベースURL
BASE_URL = "http://localhost:8000"

def test_api():
    """APIの基本機能をテスト"""
    print("🧪 Azuma Insight Quotes API テスト開始")
    print("=" * 50)
    
    # 1. ルートエンドポイント
    print("1. ルートエンドポイントテスト")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ ステータス: {response.status_code}")
        print(f"📄 レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ エラー: {e}")
    print()
    
    # 2. 統計情報
    print("2. 統計情報テスト")
    try:
        response = requests.get(f"{BASE_URL}/stats")
        print(f"✅ ステータス: {response.status_code}")
        stats = response.json()
        print(f"📊 総引用数: {stats['total_quotes']}")
        print(f"🏷️ テーマ別件数: {json.dumps(stats['themes'], indent=2, ensure_ascii=False)}")
        print(f"📅 日付範囲: {stats['date_range']}")
    except Exception as e:
        print(f"❌ エラー: {e}")
    print()
    
    # 3. 引用一覧取得
    print("3. 引用一覧取得テスト")
    try:
        response = requests.get(f"{BASE_URL}/quotes?limit=5")
        print(f"✅ ステータス: {response.status_code}")
        quotes = response.json()
        print(f"📝 取得件数: {len(quotes)}")
        if quotes:
            print(f"📄 最初の引用: {quotes[0]['title']}")
            print(f"📝 内容: {quotes[0]['text'][:50]}...")
    except Exception as e:
        print(f"❌ エラー: {e}")
    print()
    
    # 4. ランダム引用取得
    print("4. ランダム引用取得テスト")
    try:
        response = requests.get(f"{BASE_URL}/quotes/random")
        print(f"✅ ステータス: {response.status_code}")
        quote = response.json()
        print(f"🎲 ランダム引用: {quote['title']}")
        print(f"📝 内容: {quote['text'][:50]}...")
    except Exception as e:
        print(f"❌ エラー: {e}")
    print()
    
    # 5. 検索機能テスト
    print("5. 検索機能テスト")
    try:
        response = requests.get(f"{BASE_URL}/quotes/search?q=人生&limit=3")
        print(f"✅ ステータス: {response.status_code}")
        results = response.json()
        print(f"🔍 検索結果件数: {len(results) if isinstance(results, list) else 0}")
        if isinstance(results, list) and results:
            for i, quote in enumerate(results[:2], 1):
                print(f"  {i}. {quote['title']}")
                print(f"     {quote['text'][:30]}...")
        else:
            print("  検索結果なし")
    except Exception as e:
        print(f"❌ エラー: {e}")
    print()
    
    # 6. テーマ別検索テスト
    print("6. テーマ別検索テスト")
    try:
        response = requests.get(f"{BASE_URL}/quotes/theme/人生&limit=3")
        print(f"✅ ステータス: {response.status_code}")
        results = response.json()
        print(f"🏷️ テーマ別結果件数: {len(results)}")
    except Exception as e:
        print(f"❌ エラー: {e}")
    print()
    
    print("🎉 テスト完了!")

if __name__ == "__main__":
    test_api() 