# -*- coding: utf-8 -*-

from rwkvfla.modules.convolution import (ImplicitLongConvolution, LongConvolution,
                                     ShortConvolution)
from rwkvfla.modules.fused_bitlinear import BitLinear, FusedBitLinear
from rwkvfla.modules.fused_cross_entropy import FusedCrossEntropyLoss
from rwkvfla.modules.fused_kl_div import FusedKLDivLoss
from rwkvfla.modules.fused_linear_cross_entropy import FusedLinearCrossEntropyLoss
from rwkvfla.modules.fused_norm_gate import (FusedLayerNormSwishGate,
                                         FusedLayerNormSwishGateLinear,
                                         FusedRMSNormSwishGate,
                                         FusedRMSNormSwishGateLinear)
from rwkvfla.modules.layernorm import (GroupNorm, GroupNormLinear, LayerNorm,
                                   LayerNormLinear, RMSNorm, RMSNormLinear)
from rwkvfla.modules.mlp import GatedMLP
from rwkvfla.modules.rotary import RotaryEmbedding

__all__ = [
    'ImplicitLongConvolution', 'LongConvolution', 'ShortConvolution',
    'BitLinear', 'FusedBitLinear',
    'FusedCrossEntropyLoss', 'FusedLinearCrossEntropyLoss', 'FusedKLDivLoss',
    'GroupNorm', 'GroupNormLinear', 'LayerNorm', 'LayerNormLinear', 'RMSNorm', 'RMSNormLinear',
    'FusedLayerNormSwishGate', 'FusedLayerNormSwishGateLinear', 'FusedRMSNormSwishGate', 'FusedRMSNormSwishGateLinear',
    'GatedMLP',
    'RotaryEmbedding'
]
