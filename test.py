import tensorflow as tf
print("TensorFlow version:", tf._version_)
print("is_gpu_available:", tf.test.is_gpu_available())
import tensorflow.compiler as tf_cc
print("is TensorRT enabled:", tf_cc.tf2tensorrt._pywrap_py_utils.is_tensorrt_enabled())
print("loaded trt ver:", tf_cc.tf2tensorrt._pywrap_py_utils.get_loaded_tensorrt_version())
print("linked trt ver:", tf_cc.tf2tensorrt._pywrap_py_utils.get_linked_tensorrt_version())
