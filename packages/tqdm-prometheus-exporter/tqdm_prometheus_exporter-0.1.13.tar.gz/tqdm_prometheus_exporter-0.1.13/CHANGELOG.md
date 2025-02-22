# [0.1.13](https://github.com/arrowed/tqdm-prometheus-exporter/releases/tag/release/0.1.13)

* [606ff5a](https://github.com/arrowed/tqdm-prometheus-exporter/commit/606ff5a) Renamed bump.ps1 to release.ps1
* [d1798e5](https://github.com/arrowed/tqdm-prometheus-exporter/commit/d1798e5) Github releases now include binaries
* [4c88fba](https://github.com/arrowed/tqdm-prometheus-exporter/commit/4c88fba) Provide full version changelog in github release also
* [8d76eec](https://github.com/arrowed/tqdm-prometheus-exporter/commit/8d76eec) Provide hashes for release artifacts
* [478f476](https://github.com/arrowed/tqdm-prometheus-exporter/commit/478f476) Formatting changes to changelog
* [8b24e0d](https://github.com/arrowed/tqdm-prometheus-exporter/commit/8b24e0d) Properly set quiet on the http server so bars dont get interrupted with http logs

## Also available from 

 - [PyPi]({self.pypi_release_url(self.to_version)})

## Release hashes

 - tqdm_prometheus_exporter-0.1.13-py3-none-any.whl
   - md5: `f1273e9a4077856ba0107d816fc55f11`
   - sha256: `63e5c3c54888c836faf9132d484eb39e035c6cdb42e0f44149acc57ea820cddd`
 - tqdm_prometheus_exporter-0.1.13.tar.gz
   - md5: `e0a0af3e4b5d1bcf9c79434911baa8f2`
   - sha256: `d7a6420e85fb68c3a7ca52955b848d51e9b56718da9258da443005facd2a878f`

# [0.1.12](https://github.com/arrowed/tqdm-prometheus-exporter/releases/tag/0.1.12)

- [24aec23](https://github.com/arrowed/tqdm-prometheus-exporter/commit/24aec23) Snapshot identity is optimistically calculated by the first word of the progressbar text and the position of the bar
- [e012306](https://github.com/arrowed/tqdm-prometheus-exporter/commit/e012306) Dont sleep in between queue reads, let the timeout parameter do the work [3]
- [65ac685](https://github.com/arrowed/tqdm-prometheus-exporter/commit/65ac685) Allow bucket names to be overriden [2]
- [5e7da7a](https://github.com/arrowed/tqdm-prometheus-exporter/commit/5e7da7a) Allow metric names to be overridden [2]
- [146241f](https://github.com/arrowed/tqdm-prometheus-exporter/commit/146241f) Added debug mode to validate output remotely
- [952e96c](https://github.com/arrowed/tqdm-prometheus-exporter/commit/952e96c) Added test cases to validate duplication in results is now resolved [1]
- [6d1e856](https://github.com/arrowed/tqdm-prometheus-exporter/commit/6d1e856) Standardised some duplicated test logic
- [e4357dc](https://github.com/arrowed/tqdm-prometheus-exporter/commit/e4357dc) Split bucket name, instance and last seen #1
- [547f6a7](https://github.com/arrowed/tqdm-prometheus-exporter/commit/547f6a7) Updated release scripts to update uv lockfile

# [0.1.11](https://github.com/arrowed/tqdm-prometheus-exporter/releases/tag/0.1.11)

- [011b4fc](https://github.com/arrowed/tqdm-prometheus-exporter/commit/011b4fc) Downgraded python dependency to 3.8. Could possibly go further

# [0.1.10](https://github.com/arrowed/tqdm-prometheus-exporter/releases/tag/0.1.10)

- [69052aa](https://github.com/arrowed/tqdm-prometheus-exporter/commit/69052aa) Refactor main api - Simplified properties now behaviour has been externalised - Allowed api to be picked for use in multiprocessing scenarios
- [2a47553](https://github.com/arrowed/tqdm-prometheus-exporter/commit/2a47553) Moving metric server over to using new BucketManager
- [50b3d6b](https://github.com/arrowed/tqdm-prometheus-exporter/commit/50b3d6b) Cleaning up thread behaviour
- [01ce7f9](https://github.com/arrowed/tqdm-prometheus-exporter/commit/01ce7f9) Monitor now async and no longer enumerates tqdm internal members
- [1f26c83](https://github.com/arrowed/tqdm-prometheus-exporter/commit/1f26c83) Separating bucket management duties
- [6a28026](https://github.com/arrowed/tqdm-prometheus-exporter/commit/6a28026) Renamed `add` to `upsert` to better reflect bucket use
- [72fa6e6](https://github.com/arrowed/tqdm-prometheus-exporter/commit/72fa6e6) No longer hold references to tqdm objects, hold only `TqdmSnapshot` instead
- [3685f6a](https://github.com/arrowed/tqdm-prometheus-exporter/commit/3685f6a) Added test to assert the proxy can be passed around with multiprocessing
- [5b67359](https://github.com/arrowed/tqdm-prometheus-exporter/commit/5b67359) (chore) linted
- [3cd132e](https://github.com/arrowed/tqdm-prometheus-exporter/commit/3cd132e) Added build step to invoke uv to update the uv.lock file such that it can be committed

# [0.1.9](https://github.com/arrowed/tqdm-prometheus-exporter/releases/tag/0.1.9)

- [4bf6d05](https://github.com/arrowed/tqdm-prometheus-exporter/commit/4bf6d05) Formatted release.py
- [3eb92eb](https://github.com/arrowed/tqdm-prometheus-exporter/commit/3eb92eb) Bump version in lockfile
- [56daf12](https://github.com/arrowed/tqdm-prometheus-exporter/commit/56daf12) Run tests. Can be messy on stdout

# [0.1.8](https://github.com/arrowed/tqdm-prometheus-exporter/releases/tag/0.1.8)

- [4e9ae14](https://github.com/arrowed/tqdm-prometheus-exporter/commit/4e9ae14) Dont emit logs to stderr
- [3468173](https://github.com/arrowed/tqdm-prometheus-exporter/commit/3468173) Commit uv lock file as well when releasing
- [8f57ae1](https://github.com/arrowed/tqdm-prometheus-exporter/commit/8f57ae1) Fixed buckets not being accumulated correctly
- [bd750ae](https://github.com/arrowed/tqdm-prometheus-exporter/commit/bd750ae) Logged bucket/instance collecting stats for each iteration

# [0.1.7](https://github.com/arrowed/tqdm-prometheus-exporter/releases/tag/0.1.7)

- [cc36993](https://github.com/arrowed/tqdm-prometheus-exporter/commit/cc36993) Fixed github release details

# [0.1.6](https://github.com/arrowed/tqdm-prometheus-exporter/releases/tag/0.1.6)

- [ef9553e](https://github.com/arrowed/tqdm-prometheus-exporter/commit/ef9553e) Added gh release step
- [e7b03db](https://github.com/arrowed/tqdm-prometheus-exporter/commit/e7b03db) Release [patch] version to 0.1.5

# [0.1.4](https://github.com/arrowed/tqdm-prometheus-exporter/releases/tag/0.1.4)

- [0ec841c](https://github.com/arrowed/tqdm-prometheus-exporter/commit/0ec841c) Added intermediate release type
- [5abbb1f](https://github.com/arrowed/tqdm-prometheus-exporter/commit/5abbb1f) Release [patch] version to 0.1.3

# [0.1.2](https://github.com/arrowed/tqdm-prometheus-exporter/releases/tag/0.1.2)

- [6250aec](https://github.com/arrowed/tqdm-prometheus-exporter/commit/6250aec) Write intermediate content to release/ directory
- [9aab64c](https://github.com/arrowed/tqdm-prometheus-exporter/commit/9aab64c) Only push if allowed
- [babc683](https://github.com/arrowed/tqdm-prometheus-exporter/commit/babc683) Fix release diff naming
- [912cfc0](https://github.com/arrowed/tqdm-prometheus-exporter/commit/912cfc0) Adding version bump utils
- [e8ad6b6](https://github.com/arrowed/tqdm-prometheus-exporter/commit/e8ad6b6) Adding version bump utils
- [c26620a](https://github.com/arrowed/tqdm-prometheus-exporter/commit/c26620a) Fix url in readme
- [dac5257](https://github.com/arrowed/tqdm-prometheus-exporter/commit/dac5257) Moved helper scripts to scripts directory
