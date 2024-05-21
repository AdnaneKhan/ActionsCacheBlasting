# ActionsCacheBlasting

Proof-of-concept code for research into GitHub Actions Cache poisoning. All of this is considered working as intended by GitHub.

You can find more details on my [blog post](https://wordpress.com/post/adnanthekhan.com/454) covering GitHub Actions cache poisoning.

## What is it?

This repository contains code to:

* Exfiltrate the CacheServerUrl Actions Runtime token from a workflow (for example one that runs on `pull_request_target` and checks out user-controlled code). The URL and token is valid for **6 hours**, even if the workflow you exfiltrated it from only runs for a few seconds. There is no way for the repository maintainer to revoke this token.
* Use the CacheServerUrl and token to write arbitrary values to the repository's GitHub Actions cache to user-controlled cache keys and versions.

## How to Poison?

GitHub Actions Cache entries are typically `zstd` compressed archives. You can create one by running:

`tar --zstd -cf poisoned_cache.tzstd cache/contents/here`

If there is a cache hit then the cache restore action will just extract the archive. If the cache is poisoned you can over-write arbitrary files (ideally a script or something else that the workflow calls after restoring the cache). 

If an injection point is not clear, then [Boost Security's LOTP](https://boostsecurityio.github.io/lotp/) is a great resource for finding which files to overwrite to gain arbitrary execution in a workflow.

If you cannot find an injection point, then you can probably replace the `action.yml` file for an action used after the cache restore step. I have not done this personally but it is viable given that all GitHub Actions used by a workflow are downloaded at initiation and stored on the runner's filesystem.

## Disclaimer 

All code is provided for research and educational purposes only. You are responsible for using this for research and authorized security testing work only.
