# ActionsCacheBlasting

Proof-of-concept code for research into GitHub Actions Cache poisoning. All of this is considered working as intended by GitHub.

I will populate this README with more thorough instructions once a few disclosures wrap up and I release a deep-dive post on my [blog](https://www.adnanthekhan.com)

## What is it?
For now, this repository contains code to:

* Exfiltrate the CacheServerUrl Actions Runtime token from a workflow (for example one that runs on `pull_request_target` and checks out user-controlled code). The URL and token is valid for **6 hours**, even if the workflow you exfiltrated it from only runs for a few seconds. There is no way for the repository maintainer to revoke this token.
* Use the CacheServerUrl and token to write arbitrary values to the repository's GitHub Actions cache to user-controlled cache keys and versions.

## How to Poison?

GitHub Actions Cache entries are typically `zstd` compressed archives. You can create one by running:

`tar --zstd -cf poisoned_cache.tzstd cache/contents/here`

If there is a cache hit then the cache restore action will just extract the archive. If the cache is poisoned you can over-write arbitrary files (ideally a script or someone else that the workflow calls after restoring the cache).

If an injection point is not clear, then [Boost Security's LOTP](https://boostsecurityio.github.io/lotp/) is a great resource for finding which files to overwrite to gain arbitrary execution in a workflow.

## Disclaimer 

All code is provided for research and educational purposes only. You are responsible for using this for research and authorized security research work only.
