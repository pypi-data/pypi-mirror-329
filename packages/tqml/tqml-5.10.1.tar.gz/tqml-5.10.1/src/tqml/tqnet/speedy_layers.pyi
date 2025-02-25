from _typeshed import Incomplete
from functools import cached_property as cached_property
from torch import nn
from tqml.tqnet._speedy_qml import cnot_perms as cnot_perms, had_big as had_big, had_medium as had_medium, had_small as had_small, paulix_perms as paulix_perms, rz_eigenvals as rz_eigenvals, tensor_product as tensor_product
from tqml.tqnet.exceptions import DimensionException as DimensionException

class SpeedyLayer(nn.Module):
    in_features: Incomplete
    n_qubits: Incomplete
    depth: Incomplete
    measurement_mode: Incomplete
    rotation: Incomplete
    entangling: Incomplete
    measure: Incomplete
    hw_efficient: Incomplete
    device: Incomplete
    out_features: int
    def __init__(self, in_features, n_qubits, depth, measurement_mode: str = 'None', rotation: str = 'Z', entangling: str = 'strong', measure: str = 'Y', hw_efficient: bool = False, device: Incomplete | None = None) -> None: ...
    @cached_property
    def H(self): ...
    @cached_property
    def sqrtZ(self): ...
    @cached_property
    def binary_matrix(self, ones: bool = True): ...
    @cached_property
    def cnot_ring(self): ...
    @cached_property
    def cnot_incomplete_ring(self): ...
    @cached_property
    def cnot_even_meas(self): ...
    @cached_property
    def init_state(self): ...
    def meas(self, phi): ...
    def had(self, phi): ...
    def rz(self, phi, eigenvals): ...
    def rx(self, phi, eigenvals): ...
    def ry(self, phi, eigenvals): ...
    def bel_forward(self, phi, eigenvals_w): ...
    def sel_forward(self, phi, eigenvals_w): ...

class SpeedyQDI(SpeedyLayer):
    embedding_layers: Incomplete
    embed_rot: Incomplete
    entangler_forward: Incomplete
    weights: Incomplete
    def __init__(self, in_features, n_qubits, depth, measurement_mode: str = 'None', rotation: str = 'Z', entangling: str = 'strong', measure: str = 'Y', hw_efficient: bool = False, device: Incomplete | None = None) -> None: ...
    def forward(self, x): ...
    def extra_repr(self) -> str: ...

class SpeedyQLSTM(nn.Module):
    n_inputs: Incomplete
    hidden_size: Incomplete
    concat_size: Incomplete
    n_qubits: Incomplete
    depth: Incomplete
    measurement_mode: Incomplete
    rotation: Incomplete
    entangling: Incomplete
    measure: Incomplete
    embedding_layers: Incomplete
    batch_first: Incomplete
    bidirectional: Incomplete
    inversward: Incomplete
    device: Incomplete
    inputs_dim: Incomplete
    VQC: Incomplete
    clayer_out: Incomplete
    W_h: Incomplete
    W_x: Incomplete
    directward_layer: Incomplete
    inversward_layer: Incomplete
    def __init__(self, input_size, hidden_size, n_qubits: int = 4, depth: int = 1, measurement_mode: str = 'None', rotation: str = 'Z', entangling: str = 'basic', measure: str = 'Y', embedding_layers: int = 1, batch_first: bool = True, bidirectional: bool = False, inversward: bool = False, device: Incomplete | None = None) -> None: ...
    def forward(self, x, init_states: Incomplete | None = None): ...

class SpeedyHLSTM(nn.Module):
    hidden_layers: Incomplete
    input_size: Incomplete
    hidden_size: Incomplete
    num_classes: Incomplete
    type: Incomplete
    lstm: Incomplete
    linear: Incomplete
    qlayer: Incomplete
    def __init__(self, num_classes, input_size, hidden_size, hidden_layers, nn_type: str = 'Classic', qubits: Incomplete | None = None, depth: Incomplete | None = None, rotation: str = 'X', entangling: str = 'basic', measure: str = 'Z', device: Incomplete | None = None) -> None: ...
    def forward(self, y): ...

class SpeedyPQN(SpeedyLayer):
    embedding_layers: Incomplete
    embed_rot: Incomplete
    entangler_forward: Incomplete
    weights: Incomplete
    out_features: Incomplete
    def __init__(self, in_features, n_qubits, depth, measurement_mode: str = 'None', rotation: str = 'Z', entangling: str = 'strong', measure: str = 'Y', hw_efficient: bool = False, device: Incomplete | None = None) -> None: ...
    def forward(self, x): ...
    def extra_repr(self) -> str: ...

class SpeedyVQ(SpeedyLayer):
    embed_rot: Incomplete
    entangler_forward: Incomplete
    weights: Incomplete
    def __init__(self, in_features, depth, measurement_mode: str = 'None', rotation: str = 'Z', entangling: str = 'strong', measure: str = 'Y', hw_efficient: bool = False, device: Incomplete | None = None) -> None: ...
    def forward(self, x): ...

class SpeedyEFQ(SpeedyLayer):
    embedding_layers: Incomplete
    embed_rot: Incomplete
    entangler_forward: Incomplete
    weights: Incomplete
    def __init__(self, in_features, n_qubits, depth, measurement_mode: str = 'None', rotation: str = 'Z', entangling: str = 'strong', measure: str = 'Y', hw_efficient: bool = False, device: Incomplete | None = None) -> None: ...
    def forward(self, x): ...
    def extra_repr(self) -> str: ...

class SpeedyPHN(SpeedyLayer):
    quantum: Incomplete
    hidden_size: Incomplete
    out_features: Incomplete
    weights: Incomplete
    embedding_layers: Incomplete
    classical: Incomplete
    last: Incomplete
    def __init__(self, in_features, n_qubits, depth, hidden_size, measurement_mode: str = 'None', rotation: str = 'Z', entangling: str = 'strong', measure: str = 'Y', hw_efficient: bool = False, device: Incomplete | None = None) -> None: ...
    def forward(self, x): ...

class SpeedyGeneral(SpeedyLayer):
    embedding_layers: Incomplete
    reuploads: Incomplete
    variational_layers: Incomplete
    embed_rot: Incomplete
    entangler_forward: Incomplete
    weights: Incomplete
    def __init__(self, in_features, n_qubits, depth: int = 1, reuploads: int = 1, measurement_mode: str = 'None', rotation: str = 'Z', entangling: str = 'strong', measure: str = 'Y', hw_efficient: bool = False, device: Incomplete | None = None) -> None: ...
    def forward(self, x): ...

class SpeedyDressed(SpeedyLayer):
    reuploads: Incomplete
    hidden_dim: Incomplete
    out_features: Incomplete
    pre_q_linear: Incomplete
    quantum: Incomplete
    q_weights: Incomplete
    embedding_layers: Incomplete
    post_q_linear: Incomplete
    def __init__(self, in_features, n_qubits, depth: int = 1, reuploads: int = 1, hidden_dim: Incomplete | None = None, out_features: Incomplete | None = None, measurement_mode: str = 'None', rotation: str = 'Z', entangling: str = 'strong', measure: str = 'Y', hw_efficient: bool = False, device: Incomplete | None = None, classical_bias: bool = False) -> None: ...
    def forward(self, x): ...

class SpeedySoft(SpeedyLayer):
    embedding_layers: Incomplete
    reuploads: Incomplete
    variational_layers: Incomplete
    embed_rot: Incomplete
    weights_r: Incomplete
    weights_i: Incomplete
    def __init__(self, in_features, n_qubits, reuploads: int = 1, measurement_mode: str = 'None', rotation: str = 'Z', measure: str = 'Y', hw_efficient: bool = False, device: Incomplete | None = None) -> None: ...
    def get_soft_unitaries(self): ...
    def is_unitary_model(self, atol: float = 0.0001): ...
    def regularization(self, scaler: int = 1): ...
    def forward(self, x): ...
