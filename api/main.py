from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import date
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from pydantic import BaseModel
import json

# 環境変数を読み込み
load_dotenv()

# Supabaseクライアントの初期化
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")  # .envファイルの変数名に合わせる
supabase: Client = create_client(supabase_url, supabase_key)

app = FastAPI(
    title="Azuma Insight Quotes API",
    description="引用コレクションのためのREST API",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydanticモデル
class QuoteBase(BaseModel):
    title: str
    text: str
    author: Optional[str] = None
    theme: Optional[str] = None
    subtheme: Optional[str] = None
    tags: Optional[str] = None

class QuoteCreate(QuoteBase):
    pass

class QuoteUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    author: Optional[str] = None
    theme: Optional[str] = None
    subtheme: Optional[str] = None
    tags: Optional[str] = None

class Quote(QuoteBase):
    id: str
    created_at: str
    
    class Config:
        from_attributes = True

class QuoteResponse(BaseModel):
    id: str
    title: str
    text: str
    author: Optional[str] = None
    theme: Optional[str] = None
    subtheme: Optional[str] = None
    tags: Optional[list] = None
    created_at: str

class StatsResponse(BaseModel):
    total_quotes: int
    themes: dict
    date_range: dict

# 基本的なCRUD操作

@app.get("/", response_model=dict)
async def root():
    """APIの基本情報を返す"""
    return {
        "message": "Azuma Insight Quotes API",
        "version": "1.0.0",
        "endpoints": {
            "quotes": "/quotes",
            "search": "/quotes/search",
            "random": "/quotes/random",
            "stats": "/stats"
        }
    }

@app.get("/quotes", response_model=List[QuoteResponse])
async def get_quotes(
    limit: int = Query(50, ge=1, le=100, description="取得件数"),
    offset: int = Query(0, ge=0, description="オフセット"),
    theme: Optional[str] = Query(None, description="テーマでフィルタ"),
    date_from: Optional[str] = Query(None, description="開始日 (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="終了日 (YYYY-MM-DD)")
):
    """引用一覧を取得（フィルタリング・ページネーション付き）"""
    try:
        query = supabase.table("quotes").select("*")
        
        # フィルタリング
        if theme:
            query = query.eq("theme", theme)
        if date_from:
            query = query.gte("created_at", date_from)
        if date_to:
            query = query.lte("created_at", date_to)
        
        # ソート（作成日時降順）
        query = query.order("created_at", desc=True)
        
        # ページネーション
        query = query.range(offset, offset + limit - 1)
        
        response = query.execute()
        
        if response.data is None:
            return []
        
        return response.data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"データベースエラー: {str(e)}")

@app.get("/quotes/random", response_model=QuoteResponse)
async def get_random_quote():
    """ランダムな引用を取得"""
    try:
        # 全引用数を取得
        count_response = supabase.table("quotes").select("id", count="exact").execute()
        total_count = count_response.count
        
        if total_count == 0:
            raise HTTPException(status_code=404, detail="引用がありません")
        
        # ランダムなオフセットを生成
        import random
        random_offset = random.randint(0, total_count - 1)
        
        # ランダムな引用を取得
        response = supabase.table("quotes").select("*").range(random_offset, random_offset).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="引用が見つかりません")
        
        return response.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"データベースエラー: {str(e)}")

@app.get("/quotes/{quote_id}", response_model=QuoteResponse)
async def get_quote(quote_id: str):
    """特定の引用を取得"""
    try:
        response = supabase.table("quotes").select("*").eq("id", quote_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="引用が見つかりません")
        
        return response.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"データベースエラー: {str(e)}")

@app.post("/quotes", response_model=QuoteResponse)
async def create_quote(quote: QuoteCreate):
    """新しい引用を作成"""
    try:
        response = supabase.table("quotes").insert(quote.dict()).execute()
        
        if not response.data:
            raise HTTPException(status_code=400, detail="引用の作成に失敗しました")
        
        return response.data[0]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"データベースエラー: {str(e)}")

@app.put("/quotes/{quote_id}", response_model=QuoteResponse)
async def update_quote(quote_id: str, quote: QuoteUpdate):
    """引用を更新"""
    try:
        # 更新データからNoneの値を除外
        update_data = {k: v for k, v in quote.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="更新データがありません")
        
        response = supabase.table("quotes").update(update_data).eq("id", quote_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="引用が見つかりません")
        
        return response.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"データベースエラー: {str(e)}")

@app.delete("/quotes/{quote_id}")
async def delete_quote(quote_id: str):
    """引用を削除"""
    try:
        response = supabase.table("quotes").delete().eq("id", quote_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="引用が見つかりません")
        
        return {"message": "引用が削除されました", "id": quote_id}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"データベースエラー: {str(e)}")

# 検索機能

@app.get("/quotes/search", response_model=List[QuoteResponse])
async def search_quotes(
    q: str = Query(..., description="検索キーワード"),
    limit: int = Query(50, ge=1, le=100, description="取得件数"),
    offset: int = Query(0, ge=0, description="オフセット")
):
    """キーワード検索（タイトル・内容）"""
    try:
        # タイトルまたは内容にキーワードが含まれる引用を検索
        response = supabase.table("quotes").select("*") \
            .or_(f"(title.ilike.*{q}*),(text.ilike.*{q}*)") \
            .order("created_at", desc=True) \
            .range(offset, offset + limit - 1).execute()
        
        if response.data is None:
            return []
        
        return response.data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"検索エラー: {str(e)}")

@app.get("/quotes/theme/{theme}", response_model=List[QuoteResponse])
async def get_quotes_by_theme(
    theme: str,
    limit: int = Query(50, ge=1, le=100, description="取得件数"),
    offset: int = Query(0, ge=0, description="オフセット")
):
    """テーマ別の引用を取得"""
    try:
        response = supabase.table("quotes").select("*").eq("theme", theme).order("created_at", desc=True).range(offset, offset + limit - 1).execute()
        
        if response.data is None:
            return []
        
        return response.data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"データベースエラー: {str(e)}")

# 統計情報

@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """基本統計情報を取得"""
    try:
        # 全引用を取得
        response = supabase.table("quotes").select("*").execute()
        
        if response.data is None:
            return StatsResponse(
                total_quotes=0,
                themes={},
                date_range={"min": None, "max": None}
            )
        
        quotes = response.data
        
        # 統計を計算
        total_quotes = len(quotes)
        
        # テーマ別件数
        themes = {}
        for quote in quotes:
            theme = quote.get("theme", "未分類")
            themes[theme] = themes.get(theme, 0) + 1
        
        # 日付範囲
        dates = [quote["created_at"] for quote in quotes if quote.get("created_at")]
        date_range = {
            "min": min(dates) if dates else None,
            "max": max(dates) if dates else None
        }
        
        return StatsResponse(
            total_quotes=total_quotes,
            themes=themes,
            date_range=date_range
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"統計計算エラー: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 