# -*- coding: utf-8 -*-
import tensorflow as tf


###################################################################################################
# 定义神经网络结构相关的参数
# 输入层节点数。 对于mnist数据集，这个等于图片的像素
INPUT_NODE = 784
# 输出层的节点数。这个等于类别的数目
OUTPUT_NODE = 10
# 隐藏层节点数
LAYER1_NODE = 500


###################################################################################################
# 通过tf.get_variable 函数获取变量。 在训练神经网络时会创建这些变量； 在测试时会通过保存的模型加载这些变量的值
# 可以在变量加载时，将滑动平均变量重命名，所以可以通过同样的名字在训练时使用变量自身，而在测试时使用变量的滑动变量
# 平均值。
# 这个函数也会将变量的正则化损失加入损失集合
def get_weight_variable(shape, regularizer):
	weights = tf.get_variable("weights", shape, initializer=tf.truncated_normal_initializer(stddev=0.1))
	# 当给出了正则化生成函数时，将当前变量的正则化损失加入名字为losses的集合
	if regularizer:
		tf.add_to_collection("losses", regularizer(weights))
	return weights


###################################################################################################
# 辅助函数，给定了神经网络的输入和所有参数，计算神经网络前向传播结果
# 使用relu激活函数实现了去线性化， 实现了三层全连接神经网络
def inference(input_tensor, regularizer):
	# 声明第一层神经网络的变量并完成前向传播过程
	with tf.variable_scope('layer1'):
		weights = get_weight_variable([INPUT_NODE, LAYER1_NODE], regularizer)
		biases = tf.get_variable("biases", [LAYER1_NODE], initializer=tf.constant_initializer(0.0))
		layer1 = tf.nn.relu(tf.matmul(input_tensor, weights) + biases)
	
	# 声明第二层神经网络的变量并完成前向传播过程
	with tf.variable_scope('layer2'):
		weights = get_weight_variable([LAYER1_NODE, OUTPUT_NODE], regularizer)
		biases = tf.get_variable("biases", [OUTPUT_NODE], initializer=tf.constant_initializer(0.0))
		layer2 = tf.matmul(layer1, weights) + biases
	return layer2
