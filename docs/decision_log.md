# Decision Log

| Date       | Decision                                                         | Why                                                                                   |
| ---------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| 2026-11-24 | Use uv instead of pip                                            | Faster installs, reproducible lockfile                                                |
| 2026-11-24 | Use Python 3.14                                                  | Already installed; works with all libraries                                           |
| 2026-11-24 | Use the "Variety-wise Daily Market Prices" dataset (35985678...) | The "Current Daily Price" dataset only holds today's data; this one goes back to 2009 |
| 2026-11-25 | Send a browser-like User-Agent header                            | data.gov.in returned 502 to the default python-requests User-Agent                    |
