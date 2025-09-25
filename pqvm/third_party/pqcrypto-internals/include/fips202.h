#ifndef PQCRYPTO_FIPS202_H
#define PQCRYPTO_FIPS202_H
#include <stddef.h>
void shake128(unsigned char *out, size_t outlen, const unsigned char *in, size_t inlen);
void shake256(unsigned char *out, size_t outlen, const unsigned char *in, size_t inlen);
#endif

