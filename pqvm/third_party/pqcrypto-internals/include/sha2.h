#ifndef PQCRYPTO_SHA2_H
#define PQCRYPTO_SHA2_H
#include <stddef.h>
void sha256(unsigned char *out, const unsigned char *in, size_t inlen);
void sha512(unsigned char *out, const unsigned char *in, size_t inlen);
#endif

