-- Creates a composite index on first character of name and score.
CREATE INDEX idx_name_first_score ON names (name(1), score);
