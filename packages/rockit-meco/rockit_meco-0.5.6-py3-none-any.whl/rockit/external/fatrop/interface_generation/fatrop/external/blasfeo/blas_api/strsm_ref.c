/**************************************************************************************************
*                                                                                                 *
* This file is part of BLASFEO.                                                                   *
*                                                                                                 *
* BLASFEO -- BLAS for embedded optimization.                                                      *
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

#include <blasfeo_common.h>
#include <blasfeo_s_blasfeo_api.h>
#include <blasfeo_s_kernel.h>




#define SINGLE_PRECISION



#if ( defined(BLAS_API) & defined(MF_PANELMAJ) )
#define TRSM_LLNN blasfeo_cm_strsm_llnn
#define TRSM_LLNU blasfeo_cm_strsm_llnu
#define TRSM_LLTN blasfeo_cm_strsm_lltn
#define TRSM_LLTU blasfeo_cm_strsm_lltu
#define TRSM_LUNN blasfeo_cm_strsm_lunn
#define TRSM_LUNU blasfeo_cm_strsm_lunu
#define TRSM_LUTN blasfeo_cm_strsm_lutn
#define TRSM_LUTU blasfeo_cm_strsm_lutu
#define TRSM_RLNN blasfeo_cm_strsm_rlnn
#define TRSM_RLNU blasfeo_cm_strsm_rlnu
#define TRSM_RLTN blasfeo_cm_strsm_rltn
#define TRSM_RLTU blasfeo_cm_strsm_rltu
#define TRSM_RUNN blasfeo_cm_strsm_runn
#define TRSM_RUNU blasfeo_cm_strsm_runu
#define TRSM_RUTN blasfeo_cm_strsm_rutn
#define TRSM_RUTU blasfeo_cm_strsm_rutu
#define MAT blasfeo_cm_smat
#else
#define TRSM_LLNN blasfeo_strsm_llnn
#define TRSM_LLNU blasfeo_strsm_llnu
#define TRSM_LLTN blasfeo_strsm_lltn
#define TRSM_LLTU blasfeo_strsm_lltu
#define TRSM_LUNN blasfeo_strsm_lunn
#define TRSM_LUNU blasfeo_strsm_lunu
#define TRSM_LUTN blasfeo_strsm_lutn
#define TRSM_LUTU blasfeo_strsm_lutu
#define TRSM_RLNN blasfeo_strsm_rlnn
#define TRSM_RLNU blasfeo_strsm_rlnu
#define TRSM_RLTN blasfeo_strsm_rltn
#define TRSM_RLTU blasfeo_strsm_rltu
#define TRSM_RUNN blasfeo_strsm_runn
#define TRSM_RUNU blasfeo_strsm_runu
#define TRSM_RUTN blasfeo_strsm_rutn
#define TRSM_RUTU blasfeo_strsm_rutu
#define MAT blasfeo_smat
#endif
#define REAL float



#if defined(FORTRAN_BLAS_API)
#define TRSM strsm_
#else
#define TRSM blasfeo_blas_strsm
#endif




#include "xtrsm_ref.c"


