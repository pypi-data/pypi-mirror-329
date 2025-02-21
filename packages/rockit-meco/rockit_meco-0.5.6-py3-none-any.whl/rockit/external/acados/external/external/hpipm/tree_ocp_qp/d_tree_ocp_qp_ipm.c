/**************************************************************************************************
*                                                                                                 *
* This file is part of HPIPM.                                                                     *
*                                                                                                 *
* HPIPM -- High-Performance Interior Point Method.                                                *
* Copyright (C) 2019 by Gianluca Frison.                                                          *
* Developed at IMTEK (University of Freiburg) under the supervision of Moritz Diehl.              *
* All rights reserved.                                                                            *
*                                                                                                 *
* The 2-Clause BSD License                                                                        *
*                                                                                                 *
* Redistribution and use in source and binary forms, with or without                              *
* modification, are permitted provided that the following conditions are met:                     *
*                                                                                                 *
* 1. Redistributions of source code must retain the above copyright notice, this                  *
*    list of conditions and the following disclaimer.                                             *
* 2. Redistributions in binary form must reproduce the above copyright notice,                    *
*    this list of conditions and the following disclaimer in the documentation                    *
*    and/or other materials provided with the distribution.                                       *
*                                                                                                 *
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND                 *
* ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED                   *
* WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE                          *
* DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR                 *
* ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES                  *
* (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;                    *
* LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND                     *
* ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT                      *
* (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS                   *
* SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                                    *
*                                                                                                 *
* Author: Gianluca Frison, gianluca.frison (at) imtek.uni-freiburg.de                             *
*                                                                                                 *
**************************************************************************************************/

#include <stdlib.h>
#include <stdio.h>
#ifdef USE_C99_MATH
#include <math.h>
#endif

#include <blasfeo_target.h>
#include <blasfeo_common.h>
#include <blasfeo_d_aux.h>
#include <blasfeo_d_blas.h>

#include <hpipm_d_tree_ocp_qp.h>
#include <hpipm_d_tree_ocp_qp_sol.h>
#include <hpipm_d_tree_ocp_qp_res.h>
#include <hpipm_d_tree_ocp_qp_ipm.h>
#include <hpipm_d_tree_ocp_qp_kkt.h>
#include <hpipm_d_core_qp_ipm.h>
#include <hpipm_d_core_qp_ipm_aux.h>
#include <hpipm_aux_mem.h>



#define BLASFEO_MATEL BLASFEO_DMATEL
#define BLASFEO_VECEL BLASFEO_DVECEL



#define AXPY blasfeo_daxpy
#define BACKUP_RES_M d_backup_res_m
#define COMPUTE_ALPHA_QP d_compute_alpha_qp
#define COMPUTE_CENTERING_CORRECTION_QP d_compute_centering_correction_qp
#define COMPUTE_CENTERING_QP d_compute_centering_qp
#define COMPUTE_MU_AFF_QP d_compute_mu_aff_qp
#define COMPUTE_TAU_MIN_QP d_compute_tau_min_qp
#define CORE_QP_IPM_WORKSPACE d_core_qp_ipm_workspace
#define CREATE_STRMAT blasfeo_create_dmat
#define CREATE_STRVEC blasfeo_create_dvec
#define CREATE_CORE_QP_IPM d_create_core_qp_ipm
#define TREE_OCP_QP_FACT_LQ_SOLVE_KKT_STEP d_tree_ocp_qp_fact_lq_solve_kkt_step
#define TREE_OCP_QP_FACT_SOLVE_KKT_STEP d_tree_ocp_qp_fact_solve_kkt_step
#define TREE_OCP_QP_FACT_SOLVE_KKT_UNCONSTR d_tree_ocp_qp_fact_solve_kkt_unconstr
#define GELQF_WORKSIZE blasfeo_dgelqf_worksize
#define GEMV_T blasfeo_dgemv_t
#define MEMSIZE_CORE_QP_IPM d_memsize_core_qp_ipm
#define REAL double
#define SIZE_STRMAT blasfeo_memsize_dmat
#define SIZE_STRVEC blasfeo_memsize_dvec
#define TREE_OCP_QP_SOLVE_KKT_STEP d_tree_ocp_qp_solve_kkt_step
#define STRMAT blasfeo_dmat
#define STRVEC blasfeo_dvec
#define TREE_OCP_QP d_tree_ocp_qp
#define TREE_OCP_QP_DIM d_tree_ocp_qp_dim
#define TREE_OCP_QP_IPM_ARG d_tree_ocp_qp_ipm_arg
#define HPIPM_MODE hpipm_mode
#define TREE_OCP_QP_IPM_ABS_STEP d_tree_ocp_qp_ipm_abs_step
#define TREE_OCP_QP_IPM_DELTA_STEP d_tree_ocp_qp_ipm_delta_step
#define TREE_OCP_QP_IPM_WS d_tree_ocp_qp_ipm_ws
#define TREE_OCP_QP_RES d_tree_ocp_qp_res
#define TREE_OCP_QP_RES_WS d_tree_ocp_qp_res_ws
#define TREE_OCP_QP_RES_COMPUTE d_tree_ocp_qp_res_compute
#define TREE_OCP_QP_RES_COMPUTE_INF_NORM d_tree_ocp_qp_res_compute_inf_norm
#define TREE_OCP_QP_RES_COMPUTE_LIN d_tree_ocp_qp_res_compute_lin
#define TREE_OCP_QP_RES_CREATE d_tree_ocp_qp_res_create
#define TREE_OCP_QP_RES_MEMSIZE d_tree_ocp_qp_res_memsize
#define TREE_OCP_QP_SOL d_tree_ocp_qp_sol
#define TREE_OCP_QP_SOL_CREATE d_tree_ocp_qp_sol_create
#define TREE_OCP_QP_SOL_MEMSIZE d_tree_ocp_qp_sol_memsize
#define UPDATE_VAR_QP d_update_var_qp
#define VECMUL blasfeo_dvecmul
#define VECMULDOT blasfeo_dvecmuldot
#define VECNRM_INF blasfeo_dvecnrm_inf
#define VECSC blasfeo_dvecsc

// arg
#define TREE_OCP_QP_IPM_ARG_MEMSIZE d_tree_ocp_qp_ipm_arg_memsize
#define TREE_OCP_QP_IPM_ARG_CREATE d_tree_ocp_qp_ipm_arg_create
#define TREE_OCP_QP_IPM_ARG_SET_DEFAULT d_tree_ocp_qp_ipm_arg_set_default
#define TREE_OCP_QP_IPM_ARG_SET_ITER_MAX d_tree_ocp_qp_ipm_arg_set_iter_max
#define TREE_OCP_QP_IPM_ARG_SET_ALPHA_MIN d_tree_ocp_qp_ipm_arg_set_alpha_min
#define TREE_OCP_QP_IPM_ARG_SET_MU0 d_tree_ocp_qp_ipm_arg_set_mu0
#define TREE_OCP_QP_IPM_ARG_SET_TOL_STAT d_tree_ocp_qp_ipm_arg_set_tol_stat
#define TREE_OCP_QP_IPM_ARG_SET_TOL_EQ d_tree_ocp_qp_ipm_arg_set_tol_eq
#define TREE_OCP_QP_IPM_ARG_SET_TOL_INEQ d_tree_ocp_qp_ipm_arg_set_tol_ineq
#define TREE_OCP_QP_IPM_ARG_SET_TOL_COMP d_tree_ocp_qp_ipm_arg_set_tol_comp
#define TREE_OCP_QP_IPM_ARG_SET_REG_PRIM d_tree_ocp_qp_ipm_arg_set_reg_prim
#define TREE_OCP_QP_IPM_ARG_SET_WARM_START d_tree_ocp_qp_ipm_arg_set_warm_start
#define TREE_OCP_QP_IPM_ARG_SET_PRED_CORR d_tree_ocp_qp_ipm_arg_set_pred_corr
#define TREE_OCP_QP_IPM_ARG_SET_COND_PRED_CORR d_tree_ocp_qp_ipm_arg_set_cond_pred_corr
#define TREE_OCP_QP_IPM_ARG_SET_COMP_DUAL_SOL_EQ d_tree_ocp_qp_ipm_arg_set_comp_dual_sol_eq
#define TREE_OCP_QP_IPM_ARG_SET_COMP_RES_EXIT d_tree_ocp_qp_ipm_arg_set_comp_res_exit
#define TREE_OCP_QP_IPM_ARG_SET_LAM_MIN d_tree_ocp_qp_ipm_arg_set_lam_min
#define TREE_OCP_QP_IPM_ARG_SET_T_MIN d_tree_ocp_qp_ipm_arg_set_t_min
#define TREE_OCP_QP_IPM_ARG_SET_TAU_MIN d_tree_ocp_qp_ipm_arg_set_tau_min
#define TREE_OCP_QP_IPM_ARG_SET_SPLIT_STEP d_tree_ocp_qp_ipm_arg_set_split_step
#define TREE_OCP_QP_IPM_ARG_SET_T_LAM_MIN d_tree_ocp_qp_ipm_arg_set_t_lam_min
// ipm
#define TREE_OCP_QP_IPM_WS_MEMSIZE d_tree_ocp_qp_ipm_ws_memsize
#define TREE_OCP_QP_IPM_WS_CREATE d_tree_ocp_qp_ipm_ws_create
#define TREE_OCP_QP_IPM_GET_STATUS d_tree_ocp_qp_ipm_get_status
#define TREE_OCP_QP_IPM_GET_ITER d_tree_ocp_qp_ipm_get_iter
#define TREE_OCP_QP_IPM_GET_MAX_RES_STAT d_tree_ocp_qp_ipm_get_max_res_stat
#define TREE_OCP_QP_IPM_GET_MAX_RES_EQ d_tree_ocp_qp_ipm_get_max_res_eq
#define TREE_OCP_QP_IPM_GET_MAX_RES_INEQ d_tree_ocp_qp_ipm_get_max_res_ineq
#define TREE_OCP_QP_IPM_GET_MAX_RES_COMP d_tree_ocp_qp_ipm_get_max_res_comp
#define TREE_OCP_QP_IPM_GET_OBJ d_tree_ocp_qp_ipm_get_obj
#define TREE_OCP_QP_IPM_GET_STAT d_tree_ocp_qp_ipm_get_stat
#define TREE_OCP_QP_IPM_GET_STAT_M d_tree_ocp_qp_ipm_get_stat_m
#define TREE_OCP_QP_INIT_VAR d_tree_ocp_qp_init_var
#define TREE_OCP_QP_IPM_SOLVE d_tree_ocp_qp_ipm_solve



#include "x_tree_ocp_qp_ipm.c"
