#include "ocp/StageOCPApplication.hpp"
#include "ocp/StageOCP.hpp"
#include <limits>
#include "../casadi_codegen.h"
double inf = std::numeric_limits<double>::infinity();
#include "../problem_information.h"
#include <memory>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
using namespace fatrop;

fatrop::StageOCPRockit create()
{
#define INSTANTIATE_EVAL_CAS_GEN(FUNCTION_NAME) \
    EvalCasGen(&FUNCTION_NAME##_incref, &FUNCTION_NAME##_decref, &FUNCTION_NAME##_checkout, &FUNCTION_NAME##_release, &FUNCTION_NAME##_n_in, &FUNCTION_NAME##_n_out, &FUNCTION_NAME##_sparsity_in, &FUNCTION_NAME##_sparsity_out, &FUNCTION_NAME##_work, &FUNCTION_NAME)
    return fatrop::StageOCPRockit(
        MACRO_nu,
        MACRO_nx,
        MACRO_ngI,
        MACRO_ng,
        MACRO_ngF,
        MACRO_ng_ineqI,
        MACRO_ng_ineq,
        MACRO_ng_ineqF,
        MACRO_n_stage_params,
        MACRO_n_global_params,
        MACRO_K,
        INSTANTIATE_EVAL_CAS_GEN(BAbt),
        INSTANTIATE_EVAL_CAS_GEN(bk),
        INSTANTIATE_EVAL_CAS_GEN(RSQrqtI),
        INSTANTIATE_EVAL_CAS_GEN(rqI),
        INSTANTIATE_EVAL_CAS_GEN(RSQrqt),
        INSTANTIATE_EVAL_CAS_GEN(rqk),
        INSTANTIATE_EVAL_CAS_GEN(RSQrqtF),
        INSTANTIATE_EVAL_CAS_GEN(rqF),
        INSTANTIATE_EVAL_CAS_GEN(GgtI),
        INSTANTIATE_EVAL_CAS_GEN(gI),
        INSTANTIATE_EVAL_CAS_GEN(Ggt),
        INSTANTIATE_EVAL_CAS_GEN(g),
        INSTANTIATE_EVAL_CAS_GEN(GgtF),
        INSTANTIATE_EVAL_CAS_GEN(gF),
        INSTANTIATE_EVAL_CAS_GEN(GgineqIt),
        INSTANTIATE_EVAL_CAS_GEN(gineqI),
        INSTANTIATE_EVAL_CAS_GEN(Ggineqt),
        INSTANTIATE_EVAL_CAS_GEN(gineq),
        INSTANTIATE_EVAL_CAS_GEN(GgineqFt),
        INSTANTIATE_EVAL_CAS_GEN(gineqF),
        INSTANTIATE_EVAL_CAS_GEN(LI),
        INSTANTIATE_EVAL_CAS_GEN(Lk),
        INSTANTIATE_EVAL_CAS_GEN(LF),
        std::vector<double>(MACRO_bounds_L),
        std::vector<double>(MACRO_bounds_U),
        std::vector<double>(MACRO_stage_params),
        std::vector<double>(MACRO_global_params),
        std::vector<double>(MACRO_initial_u),
        std::vector<double>(MACRO_initial_x));
}

int main()
{
    auto app = std::make_shared<StageOCPApplication>(std::make_shared<StageOCPRockit>(create()));
    app -> build();
    app -> optimize();
    return 0;
}