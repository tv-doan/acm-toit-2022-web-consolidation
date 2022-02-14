CREATE TABLE base_pages_extracted(
  "base_page" TEXT,
  "asset_url" TEXT,
  "asset_content_type" TEXT,
  "asset_cdn" TEXT,
  "object_size" TEXT,
  "total_time" TEXT,
  "dns_time" TEXT,
  "connect_time" TEXT,
  "ssl_time" TEXT,
  "ttfb" TEXT,
  "download_time" TEXT,
  "protocol" TEXT,
  "securityDetails" TEXT,
  "ip_addr" TEXT
);

attach '[...PATH...]/httparchive_processed/2020-01/assets.db' as extract_from;
BEGIN;
INSERT INTO base_pages_extracted SELECT * FROM extract_from.assets WHERE base_page == asset_url;
COMMIT;
detach extract_from;