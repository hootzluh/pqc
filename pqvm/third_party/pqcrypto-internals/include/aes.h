#ifndef PQCRYPTO_AES_H
#define PQCRYPTO_AES_H
void aes256ctr_prf(unsigned char *out, unsigned long outlen, const unsigned char key[32], const unsigned char nonce[12]);
#endif

