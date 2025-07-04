CREATE TABLE IF NOT EXISTS users (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    username text NOT NULL,
    email text NOT NULL UNIQUE,
    password_hash text NOT NULL,
    created_at timestamp with time zone DEFAULT timezone('utc', now())
);