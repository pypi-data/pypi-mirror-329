
#include "cpg_osqp_grad_workspace_dev.h"

cpg_int cpg_osqp_gradient_L_p[7] = {
0,
5,
9,
12,
14,
15,
15,
};

cpg_int cpg_osqp_gradient_L_i[15] = {
1,
2,
3,
4,
5,
2,
3,
4,
5,
3,
4,
5,
4,
5,
5,
};

cpg_float cpg_osqp_gradient_L_x[15] = {
(cpg_float)2.00000000000000000000,
(cpg_float)3.00000000000000000000,
(cpg_float)4.00000000000000000000,
(cpg_float)5.00000000000000000000,
(cpg_float)6.00000000000000000000,
(cpg_float)8.00000000000000000000,
(cpg_float)9.00000000000000000000,
(cpg_float)10.00000000000000000000,
(cpg_float)11.00000000000000000000,
(cpg_float)13.00000000000000000000,
(cpg_float)14.00000000000000000000,
(cpg_float)15.00000000000000000000,
(cpg_float)17.00000000000000000000,
(cpg_float)18.00000000000000000000,
(cpg_float)20.00000000000000000000,
};

cpg_csc cpg_osqp_gradient_L = {cpg_osqp_gradient_L_p, cpg_osqp_gradient_L_i, cpg_osqp_gradient_L_x};

cpg_float cpg_osqp_gradient_D[6] = {
(cpg_float)1.00000000000000000000,
(cpg_float)2.00000000000000000000,
(cpg_float)-3.00000000000000000000,
(cpg_float)-4.00000000000000000000,
(cpg_float)-5.00000000000000000000,
(cpg_float)-6.00000000000000000000,
};

cpg_float cpg_osqp_gradient_Dinv[6] = {
(cpg_float)1.00000000000000000000,
(cpg_float)0.50000000000000000000,
(cpg_float)-0.33333333333333333333,
(cpg_float)-0.25000000000000000000,
(cpg_float)-0.20000000000000000000,
(cpg_float)-0.16666666666666666666,
};

cpg_float cpg_osqp_gradient_K[36] = {
(cpg_float)1.0, (cpg_float)2.0, (cpg_float)3.0, (cpg_float)4.0, (cpg_float)5.0, (cpg_float)6.0,
(cpg_float)2.0, (cpg_float)6.0, (cpg_float)22.0, (cpg_float)26.0, (cpg_float)30.0, (cpg_float)34.0,
(cpg_float)3.0, (cpg_float)22.0, (cpg_float)134.0, (cpg_float)117.0, (cpg_float)133.0, (cpg_float)149.0,
(cpg_float)4.0, (cpg_float)26.0, (cpg_float)117.0, (cpg_float)-333.0, (cpg_float)-414.0, (cpg_float)-435.0,
(cpg_float)5.0, (cpg_float)30.0, (cpg_float)133.0, (cpg_float)-414.0, (cpg_float)-1524.0, (cpg_float)-1704.0,
(cpg_float)6.0, (cpg_float)34.0, (cpg_float)149.0, (cpg_float)-435.0, (cpg_float)-1704.0, (cpg_float)-3699.0
};

cpg_float cpg_osqp_gradient_c[6] = {
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
};

cpg_float cpg_osqp_gradient_w[6] = {
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
(cpg_float)0.00000000000000000000,
};

// Struct containing primal solution
CPG_OSQP_Grad_t CPG_OSQP_Grad = {
.L = &cpg_osqp_gradient_L,
.D = (cpg_float *) &cpg_osqp_gradient_D,
.Dinv = (cpg_float *) &cpg_osqp_gradient_Dinv,
.K = (cpg_float *) &cpg_osqp_gradient_K,
.c = (cpg_float *) &cpg_osqp_gradient_c,
.w = (cpg_float *) &cpg_osqp_gradient_w,
};