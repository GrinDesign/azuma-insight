CREATE TABLE IF NOT EXISTS quotes (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    title text NOT NULL,
    text text NOT NULL,
    author text NOT NULL DEFAULT 'メンター',
    theme text,
    tags text[],
    created_at timestamp with time zone DEFAULT timezone('utc', now())
);