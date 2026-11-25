# Decision Log

| Date       | Decision                                                         | Why                                                                                                                                                |
| ---------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-11-24 | Use uv instead of pip                                            | Faster installs, reproducible lockfile                                                                                                             |
| 2026-11-24 | Use Python 3.14                                                  | Already installed; works with all libraries                                                                                                        |
| 2026-11-24 | Use the "Variety-wise Daily Market Prices" dataset (35985678...) | The "Current Daily Price" dataset only holds today's data; this one goes back to 2009                                                              |
| 2026-11-25 | Send a browser-like User-Agent header                            | data.gov.in returned 502 to the default python-requests User-Agent                                                                                 |
| 2026-11-25 | PAGE_SIZE = 1000                                                 | Tested with a 3M-row query: offset 0 and 1000 both returned 1000 rows. One call per commodity per day, so ~1,460 calls for 2 years × 2 commodities |
