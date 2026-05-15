CREATE TABLE IF NOT EXISTS nexus_curated.dim_calendar (
  calendar_date  DATE         NOT NULL,
  year           SMALLINT     NOT NULL,
  month          TINYINT      NOT NULL,
  day            TINYINT      NOT NULL,
  day_of_week    TINYINT      NOT NULL,
  is_weekend     TINYINT(1)   NOT NULL,
  quarter        TINYINT      NOT NULL,
  _run_id        CHAR(36)     NOT NULL,
  _source_cut    VARCHAR(64)  NOT NULL,
  _release_tag   VARCHAR(64)  NOT NULL,
  _certified_at  DATETIME(6)  NOT NULL,
  PRIMARY KEY (calendar_date)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE IF NOT EXISTS nexus_curated.dim_currency (
  currency_code  CHAR(3)       NOT NULL,
  rate_date      DATE          NOT NULL,
  rate_to_hkd    DECIMAL(18,8) NOT NULL,
  _run_id        CHAR(36)      NOT NULL,
  _source_cut    VARCHAR(64)   NOT NULL,
  _release_tag   VARCHAR(64)   NOT NULL,
  _certified_at  DATETIME(6)   NOT NULL,
  PRIMARY KEY (currency_code, rate_date)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE IF NOT EXISTS nexus_curated.ref_codelist (
  list_name      VARCHAR(80)  NOT NULL,
  source_code    VARCHAR(80)  NOT NULL,
  canonical_code VARCHAR(80)  NOT NULL,
  description    VARCHAR(255),
  _run_id        CHAR(36)     NOT NULL,
  _source_cut    VARCHAR(64)  NOT NULL,
  _release_tag   VARCHAR(64)  NOT NULL,
  _certified_at  DATETIME(6)  NOT NULL,
  PRIMARY KEY (list_name, source_code)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
