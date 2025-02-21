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



hpipm_size_t TREE_OCP_QP_RES_MEMSIZE(struct TREE_OCP_QP_DIM *dim)
	{

	// loop index
	int ii, idx;

	// extract ocp qp size
	int Nn = dim->Nn;
	int *nx = dim->nx;
	int *nu = dim->nu;
	int *nb = dim->nb;
	int *ng = dim->ng;
	int *ns = dim->ns;

	// compute core qp size
	int nvt = 0;
	int net = 0;
	int nct = 0;
	for(ii=0; ii<Nn; ii++)
		{
		nvt += nx[ii]+nu[ii]+2*ns[ii];
		nct += 2*nb[ii]+2*ng[ii]+2*ns[ii];
		}
	for(ii=0; ii<Nn-1; ii++)
		{
		idx = ii+1;
		net += nx[idx];
		}

	hpipm_size_t size = 0;

	size += 3*Nn*sizeof(struct STRVEC); // res_g res_d res_m
	size += 3*(Nn-1)*sizeof(struct STRVEC); // res_b

	size += 1*SIZE_STRVEC(nvt); // res_g
	size += 1*SIZE_STRVEC(net); // res_b
	size += 2*SIZE_STRVEC(nct); // res_d res_m

	size = (size+63)/64*64; // make multiple of typical cache line size
	size += 1*64; // align once to typical cache line size

	return size;

	}



void TREE_OCP_QP_RES_CREATE(struct TREE_OCP_QP_DIM *dim, struct TREE_OCP_QP_RES *res, void *mem)
	{

	// loop index
	int ii, idx;

	// zero memory (to avoid corrupted memory like e.g. NaN)
	hpipm_size_t memsize = TREE_OCP_QP_RES_MEMSIZE(dim);
	hpipm_zero_memset(memsize, mem);

	// extract ocp qp size
	int Nn = dim->Nn;
	int *nx = dim->nx;
	int *nu = dim->nu;
	int *nb = dim->nb;
	int *ng = dim->ng;
	int *ns = dim->ns;

	// compute core qp size
	int nvt = 0;
	int net = 0;
	int nct = 0;
	for(ii=0; ii<Nn; ii++)
		{
		nvt += nx[ii]+nu[ii]+2*ns[ii];
		nct += 2*nb[ii]+2*ng[ii]+2*ns[ii];
		}
	for(ii=0; ii<Nn-1; ii++)
		{
		idx = ii+1;
		net += nx[idx];
		}


	// vector struct
	struct STRVEC *sv_ptr = (struct STRVEC *) mem;

	res->res_g = sv_ptr;
	sv_ptr += Nn;
	res->res_b = sv_ptr;
	sv_ptr += Nn-1;
	res->res_d = sv_ptr;
	sv_ptr += Nn;
	res->res_m = sv_ptr;
	sv_ptr += Nn;


	// align to typical cache line size
	hpipm_size_t s_ptr = (hpipm_size_t) sv_ptr;
	s_ptr = (s_ptr+63)/64*64;


	// void stuf
	char *c_ptr = (char *) s_ptr;

	CREATE_STRVEC(nvt, res->res_g, c_ptr);
	c_ptr += SIZE_STRVEC(nvt);

	CREATE_STRVEC(net, res->res_b, c_ptr);
	c_ptr += SIZE_STRVEC(net);

	CREATE_STRVEC(nct, res->res_d, c_ptr);
	c_ptr += SIZE_STRVEC(nct);

	CREATE_STRVEC(nct, res->res_m, c_ptr);
	c_ptr += SIZE_STRVEC(nct);

	// alias
	//
	c_ptr = (char *) res->res_g->pa;
	for(ii=0; ii<Nn; ii++)
		{
		CREATE_STRVEC(nu[ii]+nx[ii]+2*ns[ii], res->res_g+ii, c_ptr);
		c_ptr += nu[ii]*sizeof(REAL);
		c_ptr += nx[ii]*sizeof(REAL);
		c_ptr += ns[ii]*sizeof(REAL);
		c_ptr += ns[ii]*sizeof(REAL);
		}
	//
	c_ptr = (char *) res->res_b->pa;
	for(ii=0; ii<Nn-1; ii++)
		{
		idx = ii+1;
		CREATE_STRVEC(nx[idx], res->res_b+ii, c_ptr);
		c_ptr += (nx[idx])*sizeof(REAL);
		}
	//
	c_ptr = (char *) res->res_d->pa;
	for(ii=0; ii<Nn; ii++)
		{
		CREATE_STRVEC(2*nb[ii]+2*ng[ii]+2*ns[ii], res->res_d+ii, c_ptr);
		c_ptr += nb[ii]*sizeof(REAL);
		c_ptr += ng[ii]*sizeof(REAL);
		c_ptr += nb[ii]*sizeof(REAL);
		c_ptr += ng[ii]*sizeof(REAL);
		c_ptr += ns[ii]*sizeof(REAL);
		c_ptr += ns[ii]*sizeof(REAL);
		}
	//
	c_ptr = (char *) res->res_m->pa;
	for(ii=0; ii<Nn; ii++)
		{
		CREATE_STRVEC(2*nb[ii]+2*ng[ii]+2*ns[ii], res->res_m+ii, c_ptr);
		c_ptr += nb[ii]*sizeof(REAL);
		c_ptr += ng[ii]*sizeof(REAL);
		c_ptr += nb[ii]*sizeof(REAL);
		c_ptr += ng[ii]*sizeof(REAL);
		c_ptr += ns[ii]*sizeof(REAL);
		c_ptr += ns[ii]*sizeof(REAL);
		}



	res->dim = dim;

	res->memsize = memsize; //MEMSIZE_TREE_OCP_QP_RES(dim);


#if defined(RUNTIME_CHECKS)
	if(c_ptr > ((char *) mem) + res->memsize)
		{
#ifdef EXT_DEP
		printf("\ncreate_tree_ocp_qp_res: outside memory bounds!\n\n");
#endif
		exit(1);
		}
#endif


	return;

	}



hpipm_size_t TREE_OCP_QP_RES_WS_MEMSIZE(struct TREE_OCP_QP_DIM *dim)
	{

	// loop index
	int ii, idx;

	// extract ocp qp size
	int Nn = dim->Nn;
	int *nx = dim->nx;
	int *nu = dim->nu;
	int *nb = dim->nb;
	int *ng = dim->ng;
	int *ns = dim->ns;

	// compute core qp size and max size
	int nbM = 0;
	int ngM = 0;
	int nsM = 0;
	for(ii=0; ii<Nn; ii++)
		{
		nbM = nb[ii]>nbM ? nb[ii] : nbM;
		ngM = ng[ii]>ngM ? ng[ii] : ngM;
		nsM = ns[ii]>nsM ? ns[ii] : nsM;
		}

	hpipm_size_t size = 0;

	size += 3*sizeof(struct STRVEC); // 2*tmp_nbgM tmp_nsM

	size += 2*SIZE_STRVEC(nbM+ngM); // tmp_nbgM
	size += 1*SIZE_STRVEC(nsM); // tmp_nsM

	size = (size+63)/64*64; // make multiple of typical cache line size
	size += 1*64; // align once to typical cache line size

	return size;

	}



void TREE_OCP_QP_RES_WS_CREATE(struct TREE_OCP_QP_DIM *dim, struct TREE_OCP_QP_RES_WS *ws, void *mem)
	{

	// loop index
	int ii, idx;

	// zero memory (to avoid corrupted memory like e.g. NaN)
	hpipm_size_t memsize = TREE_OCP_QP_RES_WS_MEMSIZE(dim);
	hpipm_zero_memset(memsize, mem);

	// extract ocp qp size
	int Nn = dim->Nn;
	int *nx = dim->nx;
	int *nu = dim->nu;
	int *nb = dim->nb;
	int *ng = dim->ng;
	int *ns = dim->ns;


	// compute core qp size and max size
	int nbM = 0;
	int ngM = 0;
	int nsM = 0;
	for(ii=0; ii<Nn; ii++)
		{
		nbM = nb[ii]>nbM ? nb[ii] : nbM;
		ngM = ng[ii]>ngM ? ng[ii] : ngM;
		nsM = ns[ii]>nsM ? ns[ii] : nsM;
		}


	// vector struct
	struct STRVEC *sv_ptr = (struct STRVEC *) mem;

	ws->tmp_nbgM = sv_ptr;
	sv_ptr += 2;
	ws->tmp_nsM = sv_ptr;
	sv_ptr += 1;


	// align to typical cache line size
	hpipm_size_t s_ptr = (hpipm_size_t) sv_ptr;
	s_ptr = (s_ptr+63)/64*64;


	// void stuf
	char *c_ptr = (char *) s_ptr;


	CREATE_STRVEC(nbM+ngM, ws->tmp_nbgM+0, c_ptr);
	c_ptr += (ws->tmp_nbgM+0)->memsize;

	CREATE_STRVEC(nbM+ngM, ws->tmp_nbgM+1, c_ptr);
	c_ptr += (ws->tmp_nbgM+1)->memsize;

	CREATE_STRVEC(nsM, ws->tmp_nsM+0, c_ptr);
	c_ptr += (ws->tmp_nsM+0)->memsize;

	ws->memsize = memsize; //MEMSIZE_TREE_OCP_QP_RES(dim);


#if defined(RUNTIME_CHECKS)
	if(c_ptr > ((char *) mem) + ws->memsize)
		{
#ifdef EXT_DEP
		printf("\ncreate_tree_ocp_qp_res_workspace: outside memory bounds!\n\n");
#endif
		exit(1);
		}
#endif


	return;

	}



void TREE_OCP_QP_RES_GET_ALL(struct TREE_OCP_QP_RES *res, REAL **res_r, REAL **res_q, REAL **res_ls, REAL **res_us, REAL **res_b, REAL **res_d_lb, REAL **res_d_ub, REAL **res_d_lg, REAL **res_d_ug, REAL **res_d_ls, REAL **res_d_us, REAL **res_m_lb, REAL **res_m_ub, REAL **res_m_lg, REAL **res_m_ug, REAL **res_m_ls, REAL **res_m_us)
	{

	int Nn = res->dim->Nn;
	int *nx = res->dim->nx;
	int *nu = res->dim->nu;
	int *nb = res->dim->nb;
	int *ng = res->dim->ng;
	int *ns = res->dim->ns;

	int ii, idx;

	for(ii=0; ii<Nn; ii++)
		{
		// cost
		UNPACK_VEC(nu[ii], res->res_g+ii, 0, res_r[ii], 1);
		UNPACK_VEC(nx[ii], res->res_g+ii, nu[ii], res_q[ii], 1);

		// box constraints
		if(nb[ii]>0)
			{
			UNPACK_VEC(nb[ii], res->res_d+ii, 0, res_d_lb[ii], 1);
			UNPACK_VEC(nb[ii], res->res_d+ii, nb[ii]+ng[ii], res_d_ub[ii], 1);
			UNPACK_VEC(nb[ii], res->res_m+ii, 0, res_m_lb[ii], 1);
			UNPACK_VEC(nb[ii], res->res_m+ii, nb[ii]+ng[ii], res_m_ub[ii], 1);
			}

		// general constraints
		if(ng[ii]>0)
			{
			UNPACK_VEC(ng[ii], res->res_d+ii, nb[ii], res_d_lg[ii], 1);
			UNPACK_VEC(ng[ii], res->res_d+ii, 2*nb[ii]+ng[ii], res_d_ug[ii], 1);
			UNPACK_VEC(ng[ii], res->res_m+ii, nb[ii], res_m_lg[ii], 1);
			UNPACK_VEC(ng[ii], res->res_m+ii, 2*nb[ii]+ng[ii], res_m_ug[ii], 1);
			}

		// soft constraints
		if(ns[ii]>0)
			{
			UNPACK_VEC(ns[ii], res->res_g+ii, nu[ii]+nx[ii], res_ls[ii], 1);
			UNPACK_VEC(ns[ii], res->res_g+ii, nu[ii]+nx[ii]+ns[ii], res_us[ii], 1);
			UNPACK_VEC(ns[ii], res->res_d+ii, 2*nb[ii]+2*ng[ii], res_d_ls[ii], 1);
			UNPACK_VEC(ns[ii], res->res_d+ii, 2*nb[ii]+2*ng[ii]+ns[ii], res_d_us[ii], 1);
			UNPACK_VEC(ns[ii], res->res_m+ii, 2*nb[ii]+2*ng[ii], res_m_ls[ii], 1);
			UNPACK_VEC(ns[ii], res->res_m+ii, 2*nb[ii]+2*ng[ii]+ns[ii], res_m_us[ii], 1);
			}
		}
	
	for(ii=0; ii<Nn-1; ii++)
		{
		// dynamics
		idx = ii+1;
		UNPACK_VEC(nx[idx], res->res_b+ii, 0, res_b[ii], 1);
		}

	return;

	}



void TREE_OCP_QP_RES_COMPUTE(struct TREE_OCP_QP *qp, struct TREE_OCP_QP_SOL *qp_sol, struct TREE_OCP_QP_RES *res, struct TREE_OCP_QP_RES_WS *ws)
	{

	struct tree *ttree = qp->dim->ttree;
	
	// loop index
	int ii, jj;

	int nkids, idxkid;

	//
	int Nn = qp->dim->Nn;
	int *nx = qp->dim->nx;
	int *nu = qp->dim->nu;
	int *nb = qp->dim->nb;
	int *ng = qp->dim->ng;
	int *ns = qp->dim->ns;

	int nct = 0;
	for(ii=0; ii<Nn; ii++)
		nct += 2*nb[ii]+2*ng[ii]+2*ns[ii];

	REAL nct_inv = 1.0/nct;


	struct STRMAT *BAbt = qp->BAbt;
	struct STRMAT *RSQrq = qp->RSQrq;
	struct STRMAT *DCt = qp->DCt;
	struct STRVEC *b = qp->b;
	struct STRVEC *rqz = qp->rqz;
	struct STRVEC *d = qp->d;
	struct STRVEC *m = qp->m;
	int **idxb = qp->idxb;
	struct STRVEC *Z = qp->Z;
	int **idxs_rev = qp->idxs_rev;

	struct STRVEC *ux = qp_sol->ux;
	struct STRVEC *pi = qp_sol->pi;
	struct STRVEC *lam = qp_sol->lam;
	struct STRVEC *t = qp_sol->t;

	struct STRVEC *res_g = res->res_g;
	struct STRVEC *res_b = res->res_b;
	struct STRVEC *res_d = res->res_d;
	struct STRVEC *res_m = res->res_m;

	struct STRVEC *tmp_nbgM = ws->tmp_nbgM;
	struct STRVEC *tmp_nsM = ws->tmp_nsM;

	int nx0, nx1, nu0, nu1, nb0, ng0, ns0, idx;

	//
	REAL mu = 0.0;
	res->obj = 0.0;

	// loop over nodes
	for(ii=0; ii<Nn; ii++)
		{

		nx0 = nx[ii];
		nu0 = nu[ii];
		nb0 = nb[ii];
		ng0 = ng[ii];
		ns0 = ns[ii];

//		SYMV_L(nu0+nx0, 1.0, RSQrq+ii, 0, 0, ux+ii, 0, 1.0, rqz+ii, 0, res_g+ii, 0);
		SYMV_L(nu0+nx0, 1.0, RSQrq+ii, 0, 0, ux+ii, 0, 2.0, rqz+ii, 0, res_g+ii, 0);
		res->obj += 0.5*DOT(nu0+nx0, res_g+ii, 0, ux+ii, 0);
		AXPY(nu0+nx0, -1.0, rqz+ii, 0, res_g+ii, 0, res_g+ii, 0);

		// if not root
		if(ii>0)
			AXPY(nx0, -1.0, pi+(ii-1), 0, res_g+ii, nu0, res_g+ii, nu0);

		if(nb0+ng0>0)
			{
			AXPY(nb0+ng0, -1.0, lam+ii, 0, lam+ii, nb0+ng0, tmp_nbgM+0, 0);
			AXPY(2*nb0+2*ng0,  1.0, d+ii, 0, t+ii, 0, res_d+ii, 0);
			// box
			if(nb0>0)
				{
				VECAD_SP(nb0, 1.0, tmp_nbgM+0, 0, idxb[ii], res_g+ii, 0);
				VECEX_SP(nb0, 1.0, idxb[ii], ux+ii, 0, tmp_nbgM+1, 0);
				}
			// general
			if(ng0>0)
				{
				GEMV_NT(nu0+nx0, ng0, 1.0, 1.0, DCt+ii, 0, 0, tmp_nbgM+0, nb[ii], ux+ii, 0, 1.0, 0.0, res_g+ii, 0, tmp_nbgM+1, nb0, res_g+ii, 0, tmp_nbgM+1, nb0);
				}

			AXPY(nb0+ng0, -1.0, tmp_nbgM+1, 0, res_d+ii, 0, res_d+ii, 0);
			AXPY(nb0+ng0,  1.0, tmp_nbgM+1, 0, res_d+ii, nb0+ng0, res_d+ii, nb0+ng0);
			}
		if(ns0>0)
			{
			// res_g
//			GEMV_DIAG(2*ns0, 1.0, Z+ii, 0, ux+ii, nu0+nx0, 1.0, rqz+ii, nu0+nx0, res_g+ii, nu0+nx0);
			GEMV_DIAG(2*ns0, 1.0, Z+ii, 0, ux+ii, nu0+nx0, 2.0, rqz+ii, nu0+nx0, res_g+ii, nu0+nx0);
			res->obj += 0.5*DOT(2*ns0, res_g+ii, nu0+nx0, ux+ii, nu0+nx0);
			AXPY(2*ns0, -1.0, rqz+ii, nu0+nx0, res_g+ii, nu0+nx0, res_g+ii, nu0+nx0);

			AXPY(2*ns0, -1.0, lam+ii, 2*nb0+2*ng0, res_g+ii, nu0+nx0, res_g+ii, nu0+nx0);
			for(jj=0; jj<nb0+ng0; jj++)
				{
				idx = idxs_rev[ii][jj];
				if(idx!=-1)
					{
					BLASFEO_VECEL(res_g+ii, nu0+nx0+idx) -= BLASFEO_VECEL(lam+ii, jj);
					BLASFEO_VECEL(res_g+ii, nu0+nx0+ns0+idx) -= BLASFEO_VECEL(lam+ii, nb0+ng0+jj);
					// res_d
					BLASFEO_VECEL(res_d+ii, jj) -= BLASFEO_VECEL(ux+ii, nu0+nx0+idx);
					BLASFEO_VECEL(res_d+ii, nb0+ng0+jj) -= BLASFEO_VECEL(ux+ii, nu0+nx0+ns0+idx);
					}
				}
			AXPY(2*ns0, -1.0, ux+ii, nu0+nx0, t+ii, 2*nb0+2*ng0, res_d+ii, 2*nb0+2*ng0);
			AXPY(2*ns0, 1.0, d+ii, 2*nb0+2*ng0, res_d+ii, 2*nb0+2*ng0, res_d+ii, 2*nb0+2*ng0);
			}

		// work on kids
		nkids = (ttree->root+ii)->nkids;
		for(jj=0; jj<nkids; jj++)
			{

			idxkid = (ttree->root+ii)->kids[jj];

			nu1 = nu[idxkid];
			nx1 = nx[idxkid];

			AXPY(nx1, -1.0, ux+idxkid, nu1, b+idxkid-1, 0, res_b+idxkid-1, 0);

			GEMV_NT(nu0+nx0, nx1, 1.0, 1.0, BAbt+idxkid-1, 0, 0, pi+idxkid-1, 0, ux+ii, 0, 1.0, 1.0, res_g+ii, 0, res_b+idxkid-1, 0, res_g+ii, 0, res_b+idxkid-1, 0);

			}

		mu += VECMULDOT(2*nb0+2*ng0+2*ns0, lam+ii, 0, t+ii, 0, res_m+ii, 0);
		AXPY(2*nb0+2*ng0+2*ns0, -1.0, m+ii, 0, res_m+ii, 0, res_m+ii, 0);

		}

	res->res_mu = mu*nct_inv;

	return;

	}



void TREE_OCP_QP_RES_COMPUTE_LIN(struct TREE_OCP_QP *qp, struct TREE_OCP_QP_SOL *qp_sol, struct TREE_OCP_QP_SOL *qp_step, struct TREE_OCP_QP_RES *res, struct TREE_OCP_QP_RES_WS *ws)
	{

	struct tree *ttree = qp->dim->ttree;
	
	// loop index
	int ii, jj;

	int nkids, idxkid;

	//
	int Nn = qp->dim->Nn;
	int *nx = qp->dim->nx;
	int *nu = qp->dim->nu;
	int *nb = qp->dim->nb;
	int *ng = qp->dim->ng;
	int *ns = qp->dim->ns;

	struct STRMAT *BAbt = qp->BAbt;
	struct STRMAT *RSQrq = qp->RSQrq;
	struct STRMAT *DCt = qp->DCt;
	struct STRVEC *b = qp->b;
	struct STRVEC *rqz = qp->rqz;
	struct STRVEC *d = qp->d;
	struct STRVEC *m = qp->m;
	int **idxb = qp->idxb;
	struct STRVEC *Z = qp->Z;
	int **idxs_rev = qp->idxs_rev;

	struct STRVEC *ux = qp_step->ux;
	struct STRVEC *pi = qp_step->pi;
	struct STRVEC *lam = qp_step->lam;
	struct STRVEC *t = qp_step->t;

	struct STRVEC *Lam = qp_sol->lam;
	struct STRVEC *T = qp_sol->t;

	struct STRVEC *res_g = res->res_g;
	struct STRVEC *res_b = res->res_b;
	struct STRVEC *res_d = res->res_d;
	struct STRVEC *res_m = res->res_m;

	struct STRVEC *tmp_nbgM = ws->tmp_nbgM;
	struct STRVEC *tmp_nsM = ws->tmp_nsM;

	int nx0, nx1, nu0, nu1, nb0, ng0, ns0, idx;

	//
	REAL mu = 0.0;

	// loop over nodes
	for(ii=0; ii<Nn; ii++)
		{

		nx0 = nx[ii];
		nu0 = nu[ii];
		nb0 = nb[ii];
		ng0 = ng[ii];
		ns0 = ns[ii];

		SYMV_L(nu0+nx0, 1.0, RSQrq+ii, 0, 0, ux+ii, 0, 1.0, rqz+ii, 0, res_g+ii, 0);

		// if not root
		if(ii>0)
			AXPY(nx0, -1.0, pi+(ii-1), 0, res_g+ii, nu0, res_g+ii, nu0);

		if(nb0+ng0>0)
			{
			AXPY(nb0+ng0, -1.0, lam+ii, 0, lam+ii, nb0+ng0, tmp_nbgM+0, 0);
			AXPY(2*nb0+2*ng0,  1.0, d+ii, 0, t+ii, 0, res_d+ii, 0);
			// box
			if(nb0>0)
				{
				VECAD_SP(nb0, 1.0, tmp_nbgM+0, 0, idxb[ii], res_g+ii, 0);
				VECEX_SP(nb0, 1.0, idxb[ii], ux+ii, 0, tmp_nbgM+1, 0);
				}
			// general
			if(ng0>0)
				{
				GEMV_NT(nu0+nx0, ng0, 1.0, 1.0, DCt+ii, 0, 0, tmp_nbgM+0, nb[ii], ux+ii, 0, 1.0, 0.0, res_g+ii, 0, tmp_nbgM+1, nb0, res_g+ii, 0, tmp_nbgM+1, nb0);
				}

			AXPY(nb0+ng0, -1.0, tmp_nbgM+1, 0, res_d+ii, 0, res_d+ii, 0);
			AXPY(nb0+ng0,  1.0, tmp_nbgM+1, 0, res_d+ii, nb0+ng0, res_d+ii, nb0+ng0);
			}
		if(ns0>0)
			{
			// res_g
			GEMV_DIAG(2*ns0, 1.0, Z+ii, 0, ux+ii, nu0+nx0, 1.0, rqz+ii, nu0+nx0, res_g+ii, nu0+nx0);
			AXPY(2*ns0, -1.0, lam+ii, 2*nb0+2*ng0, res_g+ii, nu0+nx0, res_g+ii, nu0+nx0);
			for(jj=0; jj<nb0+ng0; jj++)
				{
				idx = idxs_rev[ii][jj];
				if(idx!=-1)
					{
					BLASFEO_VECEL(res_g+ii, nu0+nx0+idx) -= BLASFEO_VECEL(lam+ii, jj);
					BLASFEO_VECEL(res_g+ii, nu0+nx0+ns0+idx) -= BLASFEO_VECEL(lam+ii, nb0+ng0+jj);
					// res_d
					BLASFEO_VECEL(res_d+ii, jj) -= BLASFEO_VECEL(ux+ii, nu0+nx0+idx);
					BLASFEO_VECEL(res_d+ii, nb0+ng0+jj) -= BLASFEO_VECEL(ux+ii, nu0+nx0+ns0+idx);
					}
				}
			AXPY(2*ns0, -1.0, ux+ii, nu0+nx0, t+ii, 2*nb0+2*ng0, res_d+ii, 2*nb0+2*ng0);
			AXPY(2*ns0, 1.0, d+ii, 2*nb0+2*ng0, res_d+ii, 2*nb0+2*ng0, res_d+ii, 2*nb0+2*ng0);
			}

		// work on kids
		nkids = (ttree->root+ii)->nkids;
		for(jj=0; jj<nkids; jj++)
			{

			idxkid = (ttree->root+ii)->kids[jj];

			nu1 = nu[idxkid];
			nx1 = nx[idxkid];

			AXPY(nx1, -1.0, ux+idxkid, nu1, b+idxkid-1, 0, res_b+idxkid-1, 0);

			GEMV_NT(nu0+nx0, nx1, 1.0, 1.0, BAbt+idxkid-1, 0, 0, pi+idxkid-1, 0, ux+ii, 0, 1.0, 1.0, res_g+ii, 0, res_b+idxkid-1, 0, res_g+ii, 0, res_b+idxkid-1, 0);

			}

		VECCP(2*nb0+2*ng0+2*ns0, m+ii, 0, res_m+ii, 0);
		VECMULACC(2*nb0+2*ng0+2*ns0, Lam+ii, 0, t+ii, 0, res_m+ii, 0);
		VECMULACC(2*nb0+2*ng0+2*ns0, lam+ii, 0, T+ii, 0, res_m+ii, 0);

		}

	return;

	}



void TREE_OCP_QP_RES_COMPUTE_INF_NORM(struct TREE_OCP_QP_RES *res)
	{

	struct TREE_OCP_QP_DIM *dim = res->dim;
	int Nn = dim->Nn;
	int *nx = dim->nx;
	int *nu = dim->nu;
	int *nb = dim->nb;
	int *ng = dim->ng;
	int *ns = dim->ns;

	int ii, idx;

	int nv = 0;
	int ne = 0;
	int nc = 0;

	for(ii=0; ii<Nn; ii++)
		{
		nv += nu[ii]+nx[ii]+2*ns[ii];
		nc += 2*nb[ii]+2*ng[ii]+2*ns[ii];
		}
	for(ii=0; ii<Nn-1; ii++)
		{
		idx = ii+1;
		ne += nx[idx];
		}

	// compute infinity norm
	VECNRM_INF(nv, res->res_g, 0, res->res_max+0);
	VECNRM_INF(ne, res->res_b, 0, res->res_max+1);
	VECNRM_INF(nc, res->res_d, 0, res->res_max+2);
	VECNRM_INF(nc, res->res_m, 0, res->res_max+3);

	return;

	}




