#!/usr/bin/env python3
"""
Azuma Insight Quotes API 起動スクリプト
"""

import uvicorn
from api.main import app

if __name__ == "__main__":
    print("🚀 Azuma Insight Quotes API を起動中...")
    print("📖 API ドキュメント: http://localhost:8000/docs")
    print("🔍 ReDoc: http://localhost:8000/redoc")
    print("🌐 API ベースURL: http://localhost:8000")
    print("=" * 50)
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 開発用: ファイル変更時に自動リロード
        log_level="info"
    ) 