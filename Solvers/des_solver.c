#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define LB32_MASK 0x00000001
#define LB64_MASK 0x0000000000000001
#define L64_MASK 0x00000000ffffffff
#define H64_MASK 0xffffffff00000000

/* Tables not changed from your original code */

/* Initial Permutation Table */
static uint8_t IP[64] = { 58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7 };
static uint8_t PI[64] = { 40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25 };
/* Expansion table */
static uint8_t E[48] = { 32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1 };
/* Post S-Box permutation */
static uint8_t P[32] = { 16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25 };
/* The S-Box tables */
static uint8_t S[8][64] = { {14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7, 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8, 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0, 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13}, {15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10, 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5, 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15, 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9}, {10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8, 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1, 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7, 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12}, {7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15, 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9, 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4, 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14}, {2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9, 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6, 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14, 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3}, {12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11, 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8, 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6, 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13}, {4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1, 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6, 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2, 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12}, {13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7, 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2, 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8, 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11} };
/* Iteration Shift Array */
static uint8_t iteration_shift[] = {1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1};
/* Permuted Choice 1 Table */
static uint8_t PC1[56] = { 57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4 };
/* Permuted Choice 2 Table */
static uint8_t PC2[48] = { 14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32 };

uint64_t des(uint64_t input, uint64_t key, char mode) {
    /* Variable declarations */
    uint_fast8_t i, j;
    uint_fast8_t row, column;
    uint32_t C = 0, D = 0;
    uint32_t L = 0, R = 0;
    uint32_t s_output = 0, f_function_res = 0, temp = 0;
    uint64_t sub_key[16] = {0}, s_input = 0;
    uint64_t permuted_choice_1 = 0, permuted_choice_2 = 0;
    uint64_t init_perm_res = 0, inv_init_perm_res = 0, pre_output = 0;

    // Initial permutation
    for (i = 0; i < 64; i++) {
        init_perm_res <<= 1;
        init_perm_res |= (input >> (64 - IP[i])) & LB64_MASK;
    }
    L = (uint32_t)(init_perm_res >> 32) & L64_MASK;
    R = (uint32_t)init_perm_res & L64_MASK;

    // Initial key schedule calculation
    for (i = 0; i < 56; i++) {
        permuted_choice_1 <<= 1;
        permuted_choice_1 |= (key >> (64 - PC1[i])) & LB64_MASK;
    }
    C = (uint32_t)((permuted_choice_1 >> 28) & 0x000000000fffffff);
    D = (uint32_t)(permuted_choice_1 & 0x000000000fffffff);

    /* Calculation of the 16 keys */
    for (i = 0; i < 16; i++) {
        /* Key schedule: shifting Ci and Di */
        C = 0x0fffffff & (C << iteration_shift[i]) | (C >> (28 - iteration_shift[i]));
        D = 0x0fffffff & (D << iteration_shift[i]) | (D >> (28 - iteration_shift[i]));

        permuted_choice_2 = (((uint64_t)C) << 28) | (uint64_t)D;
        for (j = 0; j < 48; j++) {
            sub_key[i] <<= 1;
            sub_key[i] |= (permuted_choice_2 >> (56 - PC2[j])) & LB64_MASK;
        }
    }

    /* Encryption process starts here */
    for (i = 0; i < 16; i++) {
        /* Expansion (E) operation */
        s_input = 0;
        for (j = 0; j < 48; j++) {
            s_input <<= 1;
            s_input |= (uint64_t)((R >> (32 - E[j])) & LB32_MASK);
        }
        
        /* XOR with key */
        s_input = s_input ^ sub_key[i]; // No decryption mode; removed for optimization
        
        /* S-Boxes */
        s_output = 0;
        for (j = 0; j < 8; j++) {
            row = (char)((s_input & (0x0000840000000000 >> 6 * j)) >> 42 - 6 * j);
            row = (row >> 4) | (row & 0x01);
            column = (char)((s_input & (0x0000780000000000 >> 6 * j)) >> 43 - 6 * j);
            s_output <<= 4;
            s_output |= (uint32_t)(S[j][16 * row + column] & 0x0f);
        }

        /* Permutation (P) operation */
        f_function_res = 0;
        for (j = 0; j < 32; j++) {
            f_function_res <<= 1;
            f_function_res |= (s_output >> (32 - P[j])) & LB32_MASK;
        }
        
        /* Swap and combine */
        temp = R;
        R = L ^ f_function_res;
        L = temp;
    }

    /* Pre-output: combine R and L (reversed) */
    pre_output = (((uint64_t)R) << 32) | (uint64_t)L;

    /* Final permutation (inverse initial permutation) */
    for (i = 0; i < 64; i++) {
        inv_init_perm_res <<= 1;
        inv_init_perm_res |= (pre_output >> (64 - PI[i])) & LB64_MASK;
    }

    return inv_init_perm_res;
}
int main(int argc, char *argv[]) {

    // Convert hexadecimal strings to uint64_t
    uint64_t key, plaintext;
    sscanf(argv[1], "%llx", &key);
    sscanf(argv[2], "%llx", &plaintext);

    // Call des function with the provided key, plaintext, and 'e' for encryption mode
    uint64_t ciphertext = des(plaintext, key, 'e');

    printf("%016llx\n", ciphertext);
    // Print the result

    return 0;
}