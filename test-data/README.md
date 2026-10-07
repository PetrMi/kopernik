# Reference Test Data

This directory is reserved for representative or synthetic FITS files used to verify Kopernik measurements and assessments.

Reference data should be added deliberately and documented with:

- the origin of the image,
- the property or behaviour it is intended to test,
- any known expected measurement or relationship,
- whether the file may be redistributed with the repository.

Do not commit private, sensitive or redistribution-restricted data.

## Local reference input

`r_pp_ic1805.fit` is supplied locally by the project owner to verify structural
FITS validation and header reporting. Its provenance and redistribution license
have not been established. It is ignored by Git and must not be uploaded or
committed. Header values are reported as declarations, not independently verified
scientific facts. Automated tests use synthetic fixtures instead.
