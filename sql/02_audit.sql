CREATE TABLE IF NOT EXISTS nexus_raw.job_runs (
  run_id            CHAR(36)                              NOT NULL,
  job_name          VARCHAR(120)                          NOT NULL,
  source_cut        VARCHAR(64)                           NOT NULL,
  release_tag       VARCHAR(64),
  started_at        DATETIME(6)                           NOT NULL,
  completed_at      DATETIME(6),
  row_count_in      INT,
  row_count_out     INT,
  validation_result ENUM('pass', 'fail', 'skip')          NOT NULL DEFAULT 'skip',
  error_detail      TEXT,
  PRIMARY KEY (run_id),
  INDEX idx_job_cut (job_name, source_cut)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
