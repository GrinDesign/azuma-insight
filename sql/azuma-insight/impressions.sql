CREATE TABLE IF NOT EXISTS impressions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    quote_id uuid NOT NULL REFERENCES quotes(id) ON DELETE CASCADE,
    user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    impression text NOT NULL,
    created_at timestamp with time zone DEFAULT timezone('utc', now())
);