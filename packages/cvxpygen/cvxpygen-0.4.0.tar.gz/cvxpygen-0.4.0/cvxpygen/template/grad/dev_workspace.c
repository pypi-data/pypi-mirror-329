

#include "dev_workspace.h"

cpg_int cpg_osqp_gradient_L_p[5] = {
0,
3,
3,
3,
3,
};

cpg_int cpg_osqp_gradient_L_i[7] = {
1,
2,
3,
0,
0,
0,
0,
};

cpg_float cpg_osqp_gradient_L_x[7] = {
(cpg_float)1.00000000000000000000,
(cpg_float)1.00000000000000000000,
(cpg_float)1.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
};

cpg_csc cpg_osqp_gradient_L = {cpg_osqp_gradient_L_p, cpg_osqp_gradient_L_i, cpg_osqp_gradient_L_x, 3, 4};

cpg_float cpg_osqp_gradient_D[4] = {
(cpg_float)-6.00000000000000000000,
(cpg_float)-7.00000000000000000000,
(cpg_float)-8.00000000000000000000,
(cpg_float)-9.00000000000000000000,
};

cpg_float cpg_osqp_gradient_Dinv[4] = {
(cpg_float)-0.16666666666666666666,
(cpg_float)-0.14257514000000000000,
(cpg_float)-0.12500000000000000000,
(cpg_float)-0.11111111111111111111,
};

cpg_int cpg_osqp_gradient_K_p[5] = {0, 1, 3, 6, 10};

cpg_int cpg_osqp_gradient_K_i[10] = {
    0,
    0, 1,
    0, 1, 2,
    0, 1, 2, 3
};

cpg_float cpg_osqp_gradient_K_x[10] = {
    (cpg_float)-6.00000000000000000000,
    (cpg_float)-6.00000000000000000000, (cpg_float)-13.00000000000000000000,
    (cpg_float)-6.00000000000000000000, (cpg_float)-6.00000000000000000000, (cpg_float)-14.00000000000000000000,
    (cpg_float)-6.00000000000000000000, (cpg_float)-6.00000000000000000000, (cpg_float)-6.00000000000000000000, (cpg_float)-15.00000000000000000000
};


cpg_csc cpg_osqp_gradient_K = {cpg_osqp_gradient_K_p, cpg_osqp_gradient_K_i, cpg_osqp_gradient_K_x, 10, 4};

cpg_float cpg_osqp_gradient_ci[4] = {
0,
1,
2,
3,
};

cpg_float cpg_osqp_gradient_c[4] = {
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
};

cpg_float cpg_osqp_gradient_cx[4] = {
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
};

cpg_float cpg_osqp_gradient_l[4] = {
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
};

cpg_float cpg_osqp_gradient_li[4] = {
0,
1,
2,
3,
};

cpg_float cpg_osqp_gradient_lx[4] = {
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
};

cpg_float cpg_osqp_gradient_w[4] = {
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
};

cpg_float cpg_osqp_gradient_wx[4] = {
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
};

cpg_int cpg_osqp_gradient_wi[4] = {
0,
1,
2,
3
};

// Struct containing primal solution
CPG_OSQP_Grad_t CPG_OSQP_Grad = {
.L = &cpg_osqp_gradient_L,
.D = (cpg_float *) &cpg_osqp_gradient_D,
.Dinv = (cpg_float *) &cpg_osqp_gradient_Dinv,
.K = &cpg_osqp_gradient_K,
.c = (cpg_float *) &cpg_osqp_gradient_c,
.cx = (cpg_float *) &cpg_osqp_gradient_cx,
.ci = (cpg_int *) &cpg_osqp_gradient_ci,
.l = (cpg_float *) &cpg_osqp_gradient_l,
.lx = (cpg_float *) &cpg_osqp_gradient_lx,
.li = (cpg_int *) &cpg_osqp_gradient_li,
.w = (cpg_float *) &cpg_osqp_gradient_w,
.wx = (cpg_float *) &cpg_osqp_gradient_wx,
.wi = (cpg_int *) &cpg_osqp_gradient_wi,
};

