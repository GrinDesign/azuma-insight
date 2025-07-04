CREATE TABLE quotes (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    title text NOT NULL,
    text text NOT NULL,
    author text NOT NULL DEFAULT '成幸者への道',
    theme text,
    subtheme text,
    tags text[],
    created_at timestamp with time zone DEFAULT timezone('utc', now())
);