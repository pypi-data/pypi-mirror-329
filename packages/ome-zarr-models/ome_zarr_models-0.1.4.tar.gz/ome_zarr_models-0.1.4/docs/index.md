# ome-zarr-models

A Python package that provides validation and a Pythonic interface for OME-Zarr datasets.

## Installing

```sh
pip install ome-zarr-models
```

or

```sh
conda install -c conda-forge ome-zarr-models
```

## Getting started

Useful places to get started are:

- [The tutorial](tutorial.py), which gives a worked example of using this package
- [How do I?](how-to.md), which explains how to do common tasks
- [The API reference](api/index.md), which explains how this package is structured

## Design

This package has been designed with the following guiding principles:

- Strict adherence to the [OME-Zarr specification](https://ngff.openmicroscopy.org/), with the goal of being a reference implementation.
- A usable set of Python classes for reading, writing, and interacting with OME-Zarr metadata.
- The ability to work with multiple versions of the OME-Zarr spec at the same time.
- Array reading and writing operations are out of scope.

## Getting help

Developers of this package are active on our [Zulip chat channel](https://imagesc.zulipchat.com/#narrow/channel/469152-ome-zarr-models-py), which is a great place for asking questions and getting help.

## Known issues

- Because of the way this package is structured, it can't currently distinguish
  between values that are present but set to `null` in saved metadata, and
  fields that are not present.
- We do not currently validate [`bioformats2raw` metadata](https://ngff.openmicroscopy.org/0.4/index.html#bf2raw)
  This is because it is transitional, and we have decided to put time into implementing other
  parts of the specification. We would welcome a pull request to add this functionality though!

### OME-Zarr 0.5

_Note:_ support for OME-Zarr 0.5 is not complete, but when it is the following issues will apply:

- Since the first release of OME-Zarr 0.5 (commit [8a0f886](https://github.com/ome/ngff/tree/8a0f886aac791060e329874b624126d3530c2b6f)), the specification has edited without the version number in OME-Zarr datasets being changed.
  A diff between the 'current' 0.5 specification and 'original' 0.5 specification [can be seen here](https://github.com/ome/ngff/compare/0.5.0...main#diff-6e0c0575683d2ac5c07564e6828e9c71ae3b93b6eacc36575055150af6c5ef73).
  As an implementation we have no way of knowing which version of the specification data that contains version "0.5" was written to, so **we have chosen to validate against the original release of OME-Zarr 0.5** (commit [8a0f886](https://github.com/ome/ngff/tree/8a0f886aac791060e329874b624126d3530c2b6f)). As of writing, this means `ome-zarr-models` does not validate omero metadata, and does not require that the "dimension_names" attribute to be present in multiscale Zarr array metadata.
- For labels, [the OME-Zarr specification says](https://ngff.openmicroscopy.org/0.5/index.html#labels-md) "Intermediate groups between "labels" and the images within it are allowed, but these MUST NOT contain metadata.". Because it is not clear what "metadata" means in this sentence, we do not validate this part of the specification.

## Versioning

`ome-zarr-models` has a major.minor versioning scheme where:

- The major version is incremented when support for a new version of the OME-Zarr specification is added, or a breaking change is made to the package.
- The minor version is incremented for any other changes (e.g., documentation improvements, bug fixes, new features)

Minor versions are released often with new improvements and bugfixes.

Before version 1.0 is released, the version number will be 0.major.minor, and version 1.0 will be released when support for version 0.5 of the OME-Zarr specification is complete.

## Roadmap

- Writing metadata after creation/modification.
- Support for OME-Zarr version 0.5.
- Emitting warnings when data violates "SHOULD" statements in the specification.
- Want to see a feature? See [the contributing guide](contributing.md)!
