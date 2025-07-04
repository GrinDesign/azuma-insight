# 名言集アプリ（azuma-insight）

## 概要
SupabaseとFastAPIを使った名言集アプリ。名言の登録・検索・感想記録ができます。
スマホからも使えるWebアプリを目指しています。

## 目的
- 名言をデータベース化し、条件に合った名言を引き出す
- 感想を記録し、分析も行う

## 開発環境
- macOS（Cursorエディタ）
- Python 3.x
- FastAPI
- Supabase
- Git + GitHub

## セットアップ手順
1. 仮想環境の作成
2. 必要なライブラリのインストール
3. Supabaseプロジェクトの準備
4. .envファイルに接続情報を記載
5. supabase_test.pyで接続テスト

## データベース設計
- quotes（名言）: id, title, text, author, theme, tags, created_at
- users（ユーザー）: id, username, email, password_hash, created_at
- impressions（感想）: id, quote_id, user_id, impression, created_at

## 外部パッケージ
- supabase-utils（共通Supabase操作ユーティリティ）
  - pip install -e ../supabase-utils で開発用インストール

## TODO
- [x] GitHubリポジトリ作成
- [x] README.md作成
- [x] Supabaseテーブル設計・作成
- [x] supabase-utilsパッケージ化
- [x] 接続テスト実装
- [ ] FastAPIでAPI作成
- [ ] フロントエンド作成
- [ ] ユーザー認証機能
- [ ] 名言検索機能
- [ ] 感想記録機能

## 開発記録
- 2024-07-03: GitHubリポジトリ作成、初期セットアップ
- 2024-07-04: README.md作成、GitHub連携完了
- 2024-07-05: Supabaseテーブル設計・作成、テストデータ投入
- 2024-07-06: supabase-utilsパッケージ化、接続テスト実装

## 工夫・学び
- 仮想環境（venv）は.gitignoreで除外
- requirements.txtで依存管理
- .envで環境変数管理
- GitHub認証はPersonal Access Token（PAT）を利用
- コンフリクト解消やrebase、cherry-pickも経験
- printによるデバッグ、エラー時の対処法も記録
- パッケージ修正時は再pip不要（-eオプション）

---

**Supabase＋Python（FastAPI）＋GitHub＋ユーティリティパッケージ化というモダンな開発フローを、トラブルシュートやベストプラクティスを交えながら着実に構築・運用しています。**