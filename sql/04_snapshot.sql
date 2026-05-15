-- Append-only snapshot table for in-force policy report.
-- No UPDATE/DELETE grants should be given to the pipeline application user on this schema.
CREATE TABLE IF NOT EXISTS nexus_snapshot.rpt_policy_in_force (
  -- Snapshot metadata (added by publisher.py)
  snapshot_id    CHAR(36)     NOT NULL,
  report_name    VARCHAR(120) NOT NULL,
  run_id         CHAR(36)     NOT NULL,
  source_cut     VARCHAR(64)  NOT NULL,
  release_tag    VARCHAR(64)  NOT NULL,
  approver       VARCHAR(120),
  snapshotted_at DATETIME(6)  NOT NULL,
  -- Report payload columns (extend as the curated policy dataset is defined)
  policy_id      INT          NOT NULL,
  product_code   VARCHAR(40),
  status         VARCHAR(40),
  inception_date DATE,
  -- Composite PK: allows multiple snapshots of the same policy across releases
  PRIMARY KEY (snapshot_id, policy_id),
  INDEX idx_report_cut (report_name, source_cut),
  INDEX idx_release (release_tag)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
