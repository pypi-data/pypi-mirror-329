TMQ is a framework for training quantization-aware neural networks with an emphasis on ternary
quantization. It uses a differentiable transfer functions on the weights of the following
layer types:
 - Linear
 - Conv2d (both transpose and regular)

The transfer function can be parameterized to range from a simple linear mapping to a soft-staircase
function, which "forces" the weight values to distinct quantization levels over time. 

TMQ-type layers can be used as drop-in replacement into existing models, only requiring minimal change
to the training code, resulting in models that can be compressed significantly.
