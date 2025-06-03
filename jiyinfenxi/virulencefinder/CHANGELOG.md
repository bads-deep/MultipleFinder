# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.1.0] - 2024-12-05

### Added

- Sub-database category to the json output file. The "ref_database" entry in the "seq_regions" entries, will now contain the name of the database followed by a colon followed by the specific sub-database the region in question was found. Ex.: "VirulenceFinder-2.0.0:virulence_ecoli"

### Changed

- dependencies to only include cgecore >= 2.0.0 and not cgelib.

## [3.0.2] - 2024-09-19

### Fixed

- Issue with only providing a single fastq file.

## [3.0.1] - 2024-06-28

### Fixed

- Crash when not providing a path to blastn, but relying on availability in PATH.

## [3.0.0] - 2024-06-06

### Added

- biopython to dependencies
- Several environmental variables for VirulenceFinder settings (see README.md).
- New method for calling VirulenceFinder if installed via pip "python -m virulencefinder -h"

### Changed

- Refactoring
- Recommended installation method for VirulenceFinder. See README.md.
- json output file to contain all output results and enable the user to specify a path for the file.
- Dockerfile will now create an image that includes the databases. The image will also become available on Docker Hub.

### Deprecated

- The previous json format has been replaced by a new standardized one. The corrresponding output file (default name: data.json) will be removed in the next major update. Instead use the json output file that uses the new format (first entry is "type: software_result").
- It is no longer recommended to clone the repository of VirulenceFinder, unless you are a developer. Instead install via pip or Docker is recommended.
- The flag "-ifa" will in the next major update not be supported. Instead use "--inputfasta".
- The flag "-ifq" will in the next major update not be supported. Instead use "--inputfastq".
- The flag "-tmp" will in the next major update not be supported. Instead use "--tmp_dir".
- The flag "-db_vir_kma" will in the next major update not be supported. Instead use "--db_path_vir_kma".
