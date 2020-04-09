Variants Helper and Recipe Fragment Generator
=============================================

Overview
--------

This
[generator](https://git.mib3.technisat-digital/mib3-integration/tsd-recipes-mib3/blob/master/contrib/variants-helper/genVariants.py)
transforms a variant data export from the MIB3 pure::variants model into the
artifacts providing variant information for the build process:

* A fragment for the variant recipe
  [`recipes/zr3-variant.yaml`](https://git.mib3.technisat-digital/mib3-integration/tsd-recipes-mib3/blob/master/recipes/zr3-variant.yaml)

* The variant data provider for the build with bob
  [`plugins/variants-helper.py`](https://git.mib3.technisat-digital/mib3-integration/tsd-recipes-mib3/blob/master/plugins/variants-helper.py)

These artifacts are updated as follows:

* Export actual variant data from pure::variants
* Generate variant information artifacts with `genVariants.py`
* Replace `recipes/zr3-variant.yaml` `multiPackage:` definition with the generated fragment from `zr3-variant.fragment.yaml`
* Replace `plugins/variants-helper.py` with the newly generated file
* Commit, test, and publish (JSON) data exported from pure::variants and
  updated artifacts

The sections below provide more detailled information about some of these steps.


pure::variants Export
---------------------

Most of the variant information for MIB3 ist modelled with pure::variants. The
[model](https://git.mib3.technisat-digital/tip-architecture/tsd.variants.features/tree/develop/MIB3)
and the [export
plugin](https://git.mib3.technisat-digital/tip-architecture/tsd.variants.features/tree/develop/plugins/pcc.purevariants.plugin.integration.transformator)
are hosted in the same repository. Ask [Raphael
Hummel](mailto:raphael.hummel@preh.de) in case of doubt for help with exporting
data.

You might have to configure the export transformations in pure::variants first,
if you have got a fresh installation.


Generator
---------

To get an overview about `genVariants.py`'s options use:
```bash
contrib/variants-helper$ ./genVariants.py --help
```

The generator supports the actual pure::variants JSON export format as well as
the historically used CSV files.


Updating the Variant Recipe
---------------------------

The variant recipe `recipes/zr3-variant.yaml` contains manually crafted entries
at the top and gets manually edited. The generated fragment for this file
replaces the entries for the `multiPackage` key.


Example
-------

Assuming that you have got an actual variant data export in
`variants-data.yaml`, you might generate and update the artifacts as follows:
```bash
contrib/variants-helper$ ./genVariantsAndUpdate --format json *.json

contrib/variants-helper$ ./genNavimapsAndUpdate --format json variants-data.json

contrib/variants-helper$ git add --update :/
contrib/variants-helper$ git commit
```

Extended call to genVariants.py
------------------------------

MASTER-Branches
```bash
./genVariantsAndUpdate --developer-mu-type-override D --customer-mu-type-override 0 --customer-prefix P --developer-prefix E --format json *.json
```

RELEASE-Branches
```bash
./genVariantsAndUpdate --customer-prefix P --developer-prefix E --format json *.json
```



Extended call to genNavimaps.py
------------------------------

MASTER-Branches
```bash
./genNavimapsAndUpdate --developer-mu-type-override D --customer-mu-type-override 0 --customer-prefix P --developer-prefix E --format json variants-data.json
```

RELEASE-Branches
```bash
./genNavimapsAndUpdate --customer-prefix P --developer-prefix E --format json variants-data.json
```
