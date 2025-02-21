/*
 * Fatrop - A fast trajectory optimization solver
 * Copyright (C) 2022, 2023 Lander Vanroye, KU Leuven. All rights reserved.
 *
 * This file is part of Fatrop.
 *
 * Fatrop is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Fatrop is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with Fatrop.  If not, see <http://www.gnu.org/licenses/>. */
#ifndef ALBBUILDERINCLUDED
#define ALBBUILDERINCLUDED
// #include "NLPAlg.hpp"
#include "FatropAlg.hpp"
#include "fatrop/auxiliary/Common.hpp"
namespace fatrop
{
    class AlgBuilder
    {
    public:
        void build_fatrop_algorithm_objects(const std::shared_ptr<FatropNLP> &nlp,
                                            const std::shared_ptr<FatropOptions> &fatropparams,
                                            std::shared_ptr<FatropData> &fatropdata,
                                            std::shared_ptr<Journaller> &journaller)
        {
            if (fatropprinter_ == nullptr)
            {
                fatropprinter_ = std::make_shared<FatropPrinter>();
            }
            fatropdata = std::make_shared<FatropData>(nlp->get_nlp_dims(), fatropparams, fatropprinter_);
            journaller = std::make_shared<Journaller>(fatropparams->maxiter + 1, fatropprinter_);
            fatropdata_ = fatropdata; // keep this around for building the algorithm
            journaller_ = journaller;
            nlp_ = nlp;
            fatropoptions_ = fatropparams;
        }
        void set_printer(const std::shared_ptr<FatropPrinter> &printer)
        {
            fatropprinter_ = printer;
        }
        std::shared_ptr<FatropAlg> build_algorithm()
        {
            // TODO unsafe if maxiter is changed during application
            std::shared_ptr<Filter> filter = std::make_shared<Filter>(fatropoptions_->maxiter + 1);
            std::shared_ptr<LineSearch> linesearch = std::make_shared<BackTrackingLineSearch>(fatropoptions_, nlp_, fatropdata_, filter, journaller_, fatropprinter_);
            return std::make_shared<FatropAlg>(nlp_, fatropdata_, fatropoptions_, filter, linesearch, journaller_, fatropprinter_);
        }

    private:
        std::shared_ptr<FatropNLP> nlp_;
        std::shared_ptr<FatropOptions> fatropoptions_;
        std::shared_ptr<FatropData> fatropdata_;
        std::shared_ptr<Journaller> journaller_;
        std::shared_ptr<FatropPrinter> fatropprinter_;
    };
};

#endif // ALBBUILDERINCLUDED