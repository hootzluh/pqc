ML-KEM (FIPS 203) Known Answer Test vectors

Expected layout (drop official .req/.rsp files here):

- mlkem512/
  - PQCkemKAT_1632.req
  - PQCkemKAT_1632.rsp
- mlkem768/
  - PQCkemKAT_2400.req
  - PQCkemKAT_2400.rsp
- mlkem1024/
  - PQCkemKAT_3168.req
  - PQCkemKAT_3168.rsp

Notes:
- These are the finalized ML-KEM vectors corresponding to FIPS 203 (not the older Kyber Round 3 KATs).
- Our pqvm KAT runner looks here first. If these files are absent, ML-KEM KATs are skipped.
- Source: NIST ML-KEM FIPS 203 KATs. If you have a tarball or path to the official set, place the files as above.
- If you want me to vendor them into the repo, confirm and I’ll fetch and add them.

