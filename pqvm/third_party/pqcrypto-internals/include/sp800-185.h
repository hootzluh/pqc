#ifndef PQCRYPTO_SP800_185_H
#define PQCRYPTO_SP800_185_H
#include <stddef.h>
void cshake128(unsigned char *out, size_t outlen, const unsigned char *in, size_t inlen,
               const unsigned char *name, size_t namelen,
               const unsigned char *custom, size_t customlen);
#endif

