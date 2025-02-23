
#include <stdio.h>
#include <math.h>
#include "cpg_osqp_grad_workspace_dev.h"

const cpg_int n = 3;
const cpg_int N = 6;
cpg_float cpg_grad_a, cpg_grad_a_bar, cpg_grad_gamma;


void cpg_rank_1_update(cpg_int sigma, cpg_int offset) {
    
    cpg_int i, j;
    
    cpg_grad_a = 1.0;

    // Perform rank-1 update in place
    for (j = offset; j < N; j++) {
        cpg_grad_a_bar = cpg_grad_a + sigma * CPG_OSQP_Grad.w[j] * CPG_OSQP_Grad.w[j] * CPG_OSQP_Grad.Dinv[j];
        cpg_grad_gamma = CPG_OSQP_Grad.w[j] * CPG_OSQP_Grad.Dinv[j] / cpg_grad_a_bar;
        CPG_OSQP_Grad.D[j] *= cpg_grad_a_bar / cpg_grad_a;
        CPG_OSQP_Grad.Dinv[j] = 1.0 / CPG_OSQP_Grad.D[j];
        cpg_grad_a = cpg_grad_a_bar;
        for (i = j + 1; i < N; i++) {
            CPG_OSQP_Grad.w[i] -= CPG_OSQP_Grad.w[j] * CPG_OSQP_Grad.L->x[CPG_OSQP_Grad.L->p[j] + i - j - 1];
            CPG_OSQP_Grad.L->x[CPG_OSQP_Grad.L->p[j] + i - j - 1] += sigma * cpg_grad_gamma * CPG_OSQP_Grad.w[i];
        }
    }

}


void cpg_ldl_delete(cpg_int index) {

    cpg_int i, j;

    // Set w
    for (i = 0; i < N - index - 1; i++) {
        CPG_OSQP_Grad.w[index + 1 + i] = CPG_OSQP_Grad.L->x[CPG_OSQP_Grad.L->p[index] + i] * sqrt(-CPG_OSQP_Grad.D[index]);
    }

    // Set index-th row and column of L to zero
    for (i = 0; i < index; i++) {
        CPG_OSQP_Grad.L->x[CPG_OSQP_Grad.L->p[i] + index - i - 1] = 0.0;
    }
    for (i = 0; i < N - index - 1; i++) {
        CPG_OSQP_Grad.L->x[CPG_OSQP_Grad.L->p[index] + i] = 0.0;
    }

    // Set (index, index)-th entry of L and D to 1.0
    //CPG_OSQP_Grad.L->[index + k] = 1.0;
    CPG_OSQP_Grad.D[index] = 1.0;
    CPG_OSQP_Grad.Dinv[index] = 1.0;

    // Update lower right part
    cpg_rank_1_update(-1, index + 1);

}


void cpg_ldl_add(cpg_int index) {

    cpg_int i, j, k;

    // Solve upper left triangular system
    for (i = 0; i < N; i++) {
        CPG_OSQP_Grad.c[i] = CPG_OSQP_Grad.K[i + index * N];
    }
    for (i = 0; i < index; i++) {
        CPG_OSQP_Grad.c[i] *= CPG_OSQP_Grad.Dinv[i];
        for (j = i + 1; j < index; j++) {
            CPG_OSQP_Grad.c[j] -= CPG_OSQP_Grad.L->x[CPG_OSQP_Grad.L->p[i] + j - i - 1] * CPG_OSQP_Grad.D[i] * CPG_OSQP_Grad.c[i];
        }
    }

    // Udpate D and L, first part
    CPG_OSQP_Grad.D[index] = CPG_OSQP_Grad.c[index];
    for (i = 0; i < index; i++) {
        CPG_OSQP_Grad.D[index] -= CPG_OSQP_Grad.c[i] * CPG_OSQP_Grad.c[i] * CPG_OSQP_Grad.D[i];
    }
    CPG_OSQP_Grad.Dinv[index] = 1.0 / CPG_OSQP_Grad.D[index];
    for (i = 0; i < index; i++) {
        CPG_OSQP_Grad.L->x[CPG_OSQP_Grad.L->p[i] + index - i - 1] = CPG_OSQP_Grad.c[i];
    }
    k = index * (2 * N - 1 - index) / 2;
    for (i = index + 1; i < N; i++) {
        k = CPG_OSQP_Grad.L->p[index] + i - index - 1;
        CPG_OSQP_Grad.L->x[k] = CPG_OSQP_Grad.c[i];
        for (j = 0; j < index; j++) {
            CPG_OSQP_Grad.L->x[k] -= CPG_OSQP_Grad.L->x[CPG_OSQP_Grad.L->p[j] + i - j - 1] * CPG_OSQP_Grad.D[j] * CPG_OSQP_Grad.c[j];
        }
        CPG_OSQP_Grad.L->x[k] *= CPG_OSQP_Grad.Dinv[index];
    }

    // Set w
    for (i = 0; i < N - index - 1; i++) {
        CPG_OSQP_Grad.w[index + 1 + i] = CPG_OSQP_Grad.L->x[CPG_OSQP_Grad.L->p[index] + i] * sqrt(-CPG_OSQP_Grad.D[index]);
    }

    // Update D and L, second part
    cpg_rank_1_update(1, index + 1);

}

/*
def ldl(A):
    
    n = A.shape[0]
    L = np.zeros_like(A)
    D = np.zeros(n)
    
    for i in range(n):
        for j in range(i):
            sum_LDLT = np.dot(L[i, :j], L[j, :j] * D[:j])
            L[i, j] = (A[i, j] - sum_LDLT) / D[j]
        
        sum_LDLT = np.dot(L[i, :i], L[i, :i] * D[:i])
        D[i] = A[i, i] - sum_LDLT
        L[i, i] = 1
    
    return L, np.diag(D)
*/
void cpg_ldl() {
    cpg_int i, j, k;
    cpg_float sum_LDLT;
    CPG_OSQP_Grad.D[0] = CPG_OSQP_Grad.K[0];
    CPG_OSQP_Grad.Dinv[0] = 1.0 / CPG_OSQP_Grad.D[0];
    for (i = 1; i < N; i++) {
        for (j = 0; j < i; j++) {
            sum_LDLT = 0.0;
            for (k = 0; k < j; k++) {
                sum_LDLT += CPG_OSQP_Grad.L->x[CPG_OSQP_Grad.L->p[k] + i - k - 1] * CPG_OSQP_Grad.L->x[CPG_OSQP_Grad.L->p[k] + j - k - 1] * CPG_OSQP_Grad.D[k];
            }
            CPG_OSQP_Grad.L->x[CPG_OSQP_Grad.L->p[j] + i - j - 1] = (CPG_OSQP_Grad.K[i + j * N] - sum_LDLT) * CPG_OSQP_Grad.Dinv[j];
        }
        sum_LDLT = 0.0;
        for (k = 0; k < i; k++) {
            sum_LDLT += CPG_OSQP_Grad.L->x[CPG_OSQP_Grad.L->p[k] + i - k - 1] * CPG_OSQP_Grad.L->x[CPG_OSQP_Grad.L->p[k] + i - k - 1] * CPG_OSQP_Grad.D[k];
        }
        CPG_OSQP_Grad.D[i] = CPG_OSQP_Grad.K[i + i * N] - sum_LDLT;
        CPG_OSQP_Grad.Dinv[i] = 1.0 / CPG_OSQP_Grad.D[i];
    }
}

int main() {

    cpg_int i, j;

    cpg_ldl_delete(3);
    // print L (stored in CSC format) and D
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            if (j < i) {
                printf("%f ", CPG_OSQP_Grad.L->x[CPG_OSQP_Grad.L->p[j] + i - j - 1]);
            } else if (j == i) {
                printf("1 ");
            } else {
                printf("0 ");
            }
        }
        printf("\n");
    }
    printf("\n");
    for (i = 0; i < N; i++) {
        printf("%f ", CPG_OSQP_Grad.D[i]);
    }
    printf("\n\n");
    cpg_ldl_add(3);
    // print L and D
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            if (j < i) {
                printf("%f ", CPG_OSQP_Grad.L->x[CPG_OSQP_Grad.L->p[j] + i - j - 1]);
            } else if (j == i) {
                printf("1 ");
            } else {
                printf("0 ");
            }
        }
        printf("\n");
    }
    printf("\n");
    for (i = 0; i < N; i++) {
        printf("%f ", CPG_OSQP_Grad.D[i]);
    }
    printf("\n\n");

    cpg_ldl();
    // print L and D
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            if (j < i) {
                printf("%f ", CPG_OSQP_Grad.L->x[CPG_OSQP_Grad.L->p[j] + i - j - 1]);
            } else if (j == i) {
                printf("1 ");
            } else {
                printf("0 ");
            }
        }
        printf("\n");
    }
    printf("\n");
    for (i = 0; i < N; i++) {
        printf("%f ", CPG_OSQP_Grad.D[i]);
    }
    printf("\n\n");

    return 0;
}