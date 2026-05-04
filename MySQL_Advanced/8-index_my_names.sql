-- character of name for faster prefix search
CREATE INDEX idx_name_first ON names (name(1));
