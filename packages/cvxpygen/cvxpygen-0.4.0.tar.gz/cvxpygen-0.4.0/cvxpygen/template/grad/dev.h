#ifndef DEV_H
#define DEV_H

#include "dev_workspace.h"

// Function to insert a non-zero entry into the sparse matrix
extern void insert_nonzero(cpg_csc *L, cpg_int row, cpg_int col);

// Function to insert a non-zero entry with a value into the sparse matrix
extern void insert_nonzero_and_value(cpg_csc *L, cpg_int row, cpg_int col, cpg_float value);

// Function to remove a non-zero entry from the sparse matrix
extern void remove_nonzero(cpg_csc *L, cpg_int row, cpg_int col);

// Function to perform symbolic LDL update
extern void symbolic_ldl_update(cpg_csc *L, cpg_int *w_indices, cpg_int w_size, cpg_int offset);

// Function to perform symbolic LDL downdate
extern void symbolic_ldl_downdate(cpg_csc *L, cpg_int *w_indices, cpg_int w_size, cpg_int offset);

// Function to perform rank-1 update
extern void cpg_rank_1_update(cpg_int sigma, cpg_int offset);

// Function to delete a column in the LDL factorization
extern void cpg_ldl_delete(cpg_int index);

// Function to add a column in the LDL factorization
extern void cpg_ldl_add(cpg_int index);

#endif // DEV_H
