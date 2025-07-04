# 名言集アプリ（azuma-insight）

## 概要
SupabaseとFastAPIを使った名言集アプリ。LINEチャットログから抽出した名言をデータベース化し、テーマ・サブテーマ・タグで分類・検索できます。
スマホからも使えるWebアプリを目指しています。

## 目的
- LINEチャットログから名言を抽出・データベース化
- テーマ・サブテーマ・タグによる自動分類
- 条件に合った名言を引き出す検索機能
- 感想を記録し、分析も行う

## 開発環境
- macOS（Cursorエディタ）
- Python 3.x
- FastAPI
- Supabase
- Git + GitHub

## セットアップ手順
1. 仮想環境の作成
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   ```
2. 必要なライブラリのインストール
   ```bash
   pip install -r requirements.txt
   ```
3. Supabaseプロジェクトの準備
4. .envファイルに接続情報を記載
5. データベース接続テスト

## データベース設計
### quotes（名言）テーブル
- `id`: UUID（主キー）
- `title`: 名言のタイトル
- `text`: 名言の本文
- `author`: 作者（デフォルト: '成幸者への道'）
- `theme`: テーマ（成功・目標、人間関係、学習・成長など）
- `subtheme`: サブテーマ（目標設定、習慣・継続、コミュニケーションなど）
- `tags`: タグ配列（時間、決断、行動、健康、継続など）
- `created_at`: 作成日時

### users（ユーザー）テーブル
- `id`: UUID（主キー）
- `username`: ユーザー名
- `email`: メールアドレス
- `password_hash`: パスワードハッシュ
- `created_at`: 作成日時

### impressions（感想）テーブル
- `id`: UUID（主キー）
- `quote_id`: 名言ID（外部キー）
- `user_id`: ユーザーID（外部キー）
- `impression`: 感想内容
- `created_at`: 作成日時

## データ処理機能

### 1. データ抽出・変換
- `data/export_for_gpt.py`: 名言データを50件ずつCSVに分割
- LINEチャットログから抽出した256件の名言を処理

### 2. 自動分類システム
- `data/improved_classify_quotes.py`: キーワードベースの自動分類
- **テーマ**: 10カテゴリ（成功・目標、人間関係、学習・成長、健康・生活など）
- **サブテーマ**: 10カテゴリ（目標設定、習慣・継続、コミュニケーションなど）
- **タグ**: 20個（時間、決断、行動、健康、継続、自信、勇気など）

### 3. データベース更新
- `data/update_quotes_improved.py`: 分類結果をデータベースに反映

## API機能（レベル2）

### FastAPI REST API
- **起動**: `python run_api.py`
- **ドキュメント**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **バージョン**: 2.0.0

### エンドポイント
- `GET /` - API基本情報・機能一覧
- `GET /quotes` - 引用一覧（高度なフィルタリング・ソート・ページネーション付き）
- `GET /quotes/{id}` - 特定の引用取得
- `POST /quotes` - 新しい引用作成
- `PUT /quotes/{id}` - 引用更新
- `DELETE /quotes/{id}` - 引用削除
- `GET /quotes/search` - 高度なキーワード検索（複数フィールド・AND/OR検索）
- `GET /quotes/tags` - タグベース検索（複数タグ・AND/OR検索）
- `GET /quotes/theme/{theme}` - テーマ別検索
- `GET /quotes/random` - ランダム引用取得
- `GET /stats` - 拡張統計情報

### 高度な機能
- **複数条件フィルタリング**: テーマ、サブテーマ、作者、タグ、日付範囲
- **高度な検索**: 複数フィールド、AND/OR検索、検索対象フィールド指定
- **ソート機能**: 複数フィールド、昇順・降順選択
- **タグ検索**: 複数タグでのAND/OR検索
- **拡張統計**: テーマ別、サブテーマ別、タグ別、作者別、月別統計

### テスト
- `python test_api.py` - API機能テスト

## 外部パッケージ
- supabase-utils（共通Supabase操作ユーティリティ）
  - pip install -e ../supabase-utils で開発用インストール

## TODO
- [x] GitHubリポジトリ作成
- [x] README.md作成
- [x] Supabaseテーブル設計・作成
- [x] supabase-utilsパッケージ化
- [x] 接続テスト実装
- [x] LINEチャットログからの名言抽出
- [x] 名言データのCSV変換・分割
- [x] 自動分類システムの実装
- [x] データベースへの分類結果反映
- [x] FastAPIでAPI作成（レベル2完了）
- [ ] フロントエンド作成
- [ ] ユーザー認証機能
- [ ] 名言検索機能
- [ ] 感想記録機能

## 開発記録
- 2024-07-03: GitHubリポジトリ作成、初期セットアップ
- 2024-07-04: README.md作成、GitHub連携完了
- 2024-07-05: Supabaseテーブル設計・作成、テストデータ投入
- 2024-07-06: supabase-utilsパッケージ化、接続テスト実装
- 2025-07-04: LINEチャットログからの名言抽出・データベース化完了
- 2025-07-04: 自動分類システム実装、256件の名言をテーマ・サブテーマ・タグで分類
- 2025-07-04: FastAPI REST API（レベル1）実装完了、基本的なCRUD操作・検索・統計機能を提供
- 2025-07-04: FastAPI REST API（レベル2）実装完了、高度な検索・フィルタリング・ソート・統計機能を提供

## 工夫・学び
- 仮想環境（venv）は.gitignoreで除外
- requirements.txtで依存管理
- .envで環境変数管理
- dataディレクトリは.gitignoreで除外（機密データ保護）
- キーワードベースの自動分類システムを実装
- CSV分割による大量データの効率的な処理
- Supabase Pythonクライアントの活用
- GitHub認証はPersonal Access Token（PAT）を利用
- コンフリクト解消やrebase、cherry-pickも経験
- printによるデバッグ、エラー時の対処法も記録
- パッケージ修正時は再pip不要（-eオプション）

## データ統計
- **総名言数**: 256件
- **テーマ数**: 10カテゴリ
- **サブテーマ数**: 10カテゴリ
- **タグ数**: 20個
- **データ期間**: 2024年10月〜2025年7月

---

**Supabase＋Python（FastAPI）＋GitHub＋自動分類システムというモダンな開発フローを、大量データ処理や機械学習的アプローチを交えながら着実に構築・運用しています。**