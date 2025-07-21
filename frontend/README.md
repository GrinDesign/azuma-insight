# Azuma Insight Frontend (PWA)

このプロジェクトは [Vite](https://vitejs.dev/) + [React](https://react.dev/) + [TypeScript](https://www.typescriptlang.org/) + [vite-plugin-pwa](https://vite-pwa-org.netlify.app/) で構築されたPWA対応のフロントエンドです。

## 開発サーバー起動

```bash
npm run dev
```

## 本番ビルド

```bash
npm run build
```

## PWAについて
- サービスワーカーによるオフライン対応
- ホーム画面への追加（スマホ/PC）
- manifest.json, アイコン等は `vite.config.ts` で設定

## 依存パッケージ追加

```bash
npm install パッケージ名
```

---

バックエンドAPIとの連携やPWAのカスタマイズは、`vite.config.ts`や`src/`配下を編集してください。
