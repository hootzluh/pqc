EVM Precompile Specification (Scaffold)

Addresses
- To be assigned per chain; recommend contiguous range (e.g., 0x0000..0x000F)

Encoding
- Input: simple TLV
  - T: 1 byte primitive identifier (e.g., 0x01 mlkem.encap, 0x02 mlkem.decap, 0x11 mldsa.sign, 0x12 mldsa.verify, etc.)
  - L: 4 bytes big-endian length of V
  - V: payload bytes
- Output: TLV with status + data

Gas Model
- base_gas + per_byte * input_len + per_variant factor
- Exact numbers to be calibrated with benches.

Determinism
- No host RNG; KATs supply seeds via input V when required.

