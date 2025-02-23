
#ifndef CPG_OSQP_GRAD_TYPES_H
# define CPG_OSQP_GRAD_TYPES_H

typedef float cpg_float;
typedef int cpg_int;

typedef struct {
  cpg_int      *p;
  cpg_int      *i;
  cpg_float    *x;
  cpg_int      nnz;
  cpg_int      n;
} cpg_csc;

// Derivative data
typedef struct {
  cpg_int      *a;         // Bound indicator (-1 for lower bound, 1 for upper bound, 0 for no bound)
  cpg_csc      *L;         // Lower triangular factor of K
  cpg_float    *D;         // Diagonal factor of K
  cpg_float    *Dinv;      // Inverse of D
  cpg_float    *P;         // Permutation P, represented as index array
  cpg_float    *Pinv;      // Inverse of permutation P, represented as index array
  cpg_csc      *K;         // KKT matrix
  cpg_float    *c;         // Vector used in update
  cpg_int      *ci;        // Sparse vector used in update
  cpg_float    *cx;        // Sparse vector used in update
  cpg_float    *w;         // Vector used in update
  cpg_int      *wi;        // Sparse vector used in update
  cpg_float    *wx;        // Sparse vector used in update
  cpg_float    *l;         // Vector used in update
  cpg_int      *li;        // Sparse vector used in update
  cpg_float    *lx;        // Sparse vector used in update
  cpg_float    *dx;        // Gradient in x
  cpg_float    *r;         // rhs / solution of linear system
  cpg_float    *rp;        // permuted rhs / solution of linear system
  cpg_float    *dq;        // Gradient in q
  cpg_float    *dl;        // Gradient in l
  cpg_float    *du;        // Gradient in u
  cpg_csc      *dP;        // Gradient in P
  cpg_csc      *dA;        // Gradient in A
} CPG_OSQP_Grad_t;

#endif // ifndef CPG_OSQP_GRAD_TYPES_H

extern CPG_OSQP_Grad_t CPG_OSQP_Grad;
extern cpg_int n;
extern cpg_int N;
