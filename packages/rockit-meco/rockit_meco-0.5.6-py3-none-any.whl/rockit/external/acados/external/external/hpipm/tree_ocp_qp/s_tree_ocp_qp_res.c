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

#include <blasfeo_target.h>
#include <blasfeo_common.h>
#include <blasfeo_s_aux.h>
#include <blasfeo_s_blas.h>

#include <hpipm_tree.h>
#include <hpipm_s_tree_ocp_qp_dim.h>
#include <hpipm_s_tree_ocp_qp_res.h>
#include <hpipm_aux_mem.h>



#define BLASFEO_VECEL BLASFEO_SVECEL



#define AXPY blasfeo_saxpy
#define CREATE_STRVEC blasfeo_create_svec
#define DOT blasfeo_sdot
#define GEMV_DIAG blasfeo_sgemv_d
#define GEMV_NT blasfeo_sgemv_nt
#define UNPACK_VEC blasfeo_unpack_svec
#define TREE_OCP_QP_DIM s_tree_ocp_qp_dim
#define TREE_OCP_QP_RES s_tree_ocp_qp_res
#define TREE_OCP_QP_RES_WS s_tree_ocp_qp_res_ws
#define REAL float
#define SIZE_STRVEC blasfeo_memsize_svec
#define STRMAT blasfeo_smat
#define STRVEC blasfeo_svec
#define SYMV_L blasfeo_ssymv_l
#define TREE_OCP_QP s_tree_ocp_qp
#define TREE_OCP_QP_SOL s_tree_ocp_qp_sol
#define VECAD_SP blasfeo_svecad_sp
#define VECCP blasfeo_sveccp
#define VECEX_SP blasfeo_svecex_sp
#define VECMULACC blasfeo_svecmulacc
#define VECMULDOT blasfeo_svecmuldot
#define VECNRM_INF blasfeo_svecnrm_inf



#define TREE_OCP_QP_RES_MEMSIZE s_tree_ocp_qp_res_memsize
#define TREE_OCP_QP_RES_CREATE s_tree_ocp_qp_res_create
#define TREE_OCP_QP_RES_WS_MEMSIZE s_tree_ocp_qp_res_ws_memsize
#define TREE_OCP_QP_RES_WS_CREATE s_tree_ocp_qp_res_ws_create
#define TREE_OCP_QP_RES_GET_ALL s_tree_ocp_qp_res_get_all
#define TREE_OCP_QP_RES_COMPUTE s_tree_ocp_qp_res_compute
#define TREE_OCP_QP_RES_COMPUTE_INF_NORM s_tree_ocp_qp_res_compute_inf_norm
#define TREE_OCP_QP_RES_COMPUTE_LIN s_tree_ocp_qp_res_compute_lin



#include "x_tree_ocp_qp_res.c"


