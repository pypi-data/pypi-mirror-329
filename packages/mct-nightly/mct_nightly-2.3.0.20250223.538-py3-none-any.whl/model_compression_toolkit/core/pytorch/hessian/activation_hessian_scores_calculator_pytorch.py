# Copyright 2023 Sony Semiconductor Israel, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from typing import List

import numpy as np
import torch
from torch import autograd
from tqdm import tqdm

from model_compression_toolkit.constants import MIN_HESSIAN_ITER, HESSIAN_COMP_TOLERANCE, HESSIAN_NUM_ITERATIONS
from model_compression_toolkit.core.common import Graph
from model_compression_toolkit.core.common.hessian import HessianScoresRequest, HessianScoresGranularity
from model_compression_toolkit.core.pytorch.back2framework.float_model_builder import FloatPyTorchModelBuilder
from model_compression_toolkit.core.pytorch.hessian.hessian_scores_calculator_pytorch import \
    HessianScoresCalculatorPytorch
from model_compression_toolkit.core.pytorch.utils import torch_tensor_to_numpy
from model_compression_toolkit.logger import Logger


class ActivationHessianScoresCalculatorPytorch(HessianScoresCalculatorPytorch):
    """
    Pytorch implementation of the Hessian approximation scores Calculator for activations.
    """
    def __init__(self,
                 graph: Graph,
                 input_images: List[torch.Tensor],
                 fw_impl,
                 hessian_scores_request: HessianScoresRequest,
                 num_iterations_for_approximation: int = HESSIAN_NUM_ITERATIONS):
        """
        Args:
            graph: Computational graph for the float model.
            input_images: List of input images for the computation.
            fw_impl: Framework-specific implementation for Hessian approximation scores computation.
            hessian_scores_request: Configuration request for which to compute the Hessian approximation scores.
            num_iterations_for_approximation: Number of iterations to use when approximating the Hessian scores.

        """
        super(ActivationHessianScoresCalculatorPytorch, self).__init__(graph=graph,
                                                                       input_images=input_images,
                                                                       fw_impl=fw_impl,
                                                                       hessian_scores_request=hessian_scores_request,
                                                                       num_iterations_for_approximation=num_iterations_for_approximation)

    def forward_pass(self):
        model_output_nodes = [ot.node for ot in self.graph.get_outputs()]

        if len([n for n in self.hessian_request.target_nodes if n in model_output_nodes]) > 0:
            Logger.critical("Activation Hessian approximation cannot be computed for model outputs. "
                            "Exclude output nodes from Hessian request targets.")

        grad_model_outputs = self.hessian_request.target_nodes + model_output_nodes
        model, _ = FloatPyTorchModelBuilder(graph=self.graph, append2output=grad_model_outputs).build_model()
        model.eval()

        # Run model inference
        # Set inputs to track gradients during inference
        for input_tensor in self.input_images:
            input_tensor.requires_grad_()
            input_tensor.retain_grad()

        outputs = model(*self.input_images)

        if len(outputs) != len(grad_model_outputs):  # pragma: no cover
            Logger.critical(f"Mismatch in expected and actual model outputs for activation Hessian approximation. "
                            f"Expected {len(grad_model_outputs)} outputs, received {len(outputs)}.")

        # Extracting the intermediate activation tensors and the model real output.
        # Note that we do not allow computing Hessian for output nodes, so there shouldn't be an overlap.
        num_target_nodes = len(self.hessian_request.target_nodes)
        # Extract activation tensors of nodes for which we want to compute Hessian
        target_activation_tensors = outputs[:num_target_nodes]
        # Extract the model outputs
        output_tensors = outputs[num_target_nodes:]

        # Concat outputs
        # First, we need to unfold all outputs that are given as list, to extract the actual output tensors
        output = self.concat_tensors(output_tensors)
        return output, target_activation_tensors

    def compute(self) -> List[np.ndarray]:
        """
        Compute the scores that are based on the approximation of the Hessian w.r.t the requested target nodes' activations.

        Returns:
            List[np.ndarray]: Scores based on the approximated Hessian for the requested nodes.
        """
        output, target_activation_tensors = self.forward_pass()

        if self.hessian_request.granularity == HessianScoresGranularity.PER_TENSOR:
            hessian_scores = self._compute_per_tensor(output, target_activation_tensors)
        elif self.hessian_request.granularity == HessianScoresGranularity.PER_OUTPUT_CHANNEL:
            hessian_scores = self._compute_per_channel(output, target_activation_tensors)
        else:
            raise NotImplementedError(f'{self.hessian_request.granularity} is not supported')    # pragma: no cover

        # Convert results to list of numpy arrays
        hessian_results = [torch_tensor_to_numpy(h) for h in hessian_scores]
        return hessian_results

    def _compute_per_tensor(self, output, target_activation_tensors):
        assert self.hessian_request.granularity == HessianScoresGranularity.PER_TENSOR
        ipts_hessian_approx_scores = [torch.tensor([0.0], requires_grad=True, device=output.device)
                                      for _ in range(len(target_activation_tensors))]
        prev_mean_results = None
        for j in tqdm(range(self.num_iterations_for_approximation), "Hessian random iterations"):  # Approximation iterations
            # Getting a random vector
            v = self._generate_random_vectors_batch(output.shape, output.device)
            f_v = torch.sum(v * output)
            for i, ipt_tensor in enumerate(target_activation_tensors):  # Per Interest point activation tensor
                # Computing the hessian-approximation scores by getting the gradient of (output * v)
                hess_v = autograd.grad(outputs=f_v,
                                       inputs=ipt_tensor,
                                       retain_graph=True,
                                       allow_unused=True)[0]

                if hess_v is None:
                    # In case we have an output node, which is an interest point, but it is not differentiable,
                    # we consider its Hessian to be the initial value 0.
                    continue  # pragma: no cover

                # Mean over all dims but the batch (CXHXW for conv)
                hessian_approx_scores = torch.sum(hess_v ** 2.0, dim=tuple(d for d in range(1, len(hess_v.shape))))

                # Update node Hessian approximation mean over random iterations
                ipts_hessian_approx_scores[i] = (j * ipts_hessian_approx_scores[i] + hessian_approx_scores) / (j + 1)

            # If the change to the maximal mean Hessian approximation is insignificant we stop the calculation
            if j > MIN_HESSIAN_ITER:
                if prev_mean_results is not None:
                    new_mean_res = torch.mean(torch.stack(ipts_hessian_approx_scores), dim=1)
                    relative_delta_per_node = (torch.abs(new_mean_res - prev_mean_results) /
                                               (torch.abs(new_mean_res) + 1e-6))
                    max_delta = torch.max(relative_delta_per_node)
                    if max_delta < HESSIAN_COMP_TOLERANCE:
                        break
            prev_mean_results = torch.mean(torch.stack(ipts_hessian_approx_scores), dim=1)

        # add extra dimension to preserve previous behaviour
        ipts_hessian_approx_scores = [torch.unsqueeze(t, -1) for t in ipts_hessian_approx_scores]
        return ipts_hessian_approx_scores

    def _compute_per_channel(self, output, target_activation_tensors):
        assert self.hessian_request.granularity == HessianScoresGranularity.PER_OUTPUT_CHANNEL
        ipts_hessian_approx_scores = [torch.tensor(0.0, requires_grad=True, device=output.device)
                                      for _ in range(len(target_activation_tensors))]

        for j in tqdm(range(self.num_iterations_for_approximation), "Hessian random iterations"):  # Approximation iterations
            v = self._generate_random_vectors_batch(output.shape, output.device)
            f_v = torch.sum(v * output)
            for i, ipt_tensor in enumerate(target_activation_tensors):  # Per Interest point activation tensor
                hess_v = autograd.grad(outputs=f_v,
                                       inputs=ipt_tensor,
                                       retain_graph=True)[0]
                hessian_approx_scores = hess_v ** 2
                rank = len(hess_v.shape)
                if rank > 2:
                    hessian_approx_scores = torch.mean(hessian_approx_scores, dim=tuple(range(2, rank)))

                # Update node Hessian approximation mean over random iterations
                ipts_hessian_approx_scores[i] = (j * ipts_hessian_approx_scores[i] + hessian_approx_scores) / (j + 1)

        return ipts_hessian_approx_scores
