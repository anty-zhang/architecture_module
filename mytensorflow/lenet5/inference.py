# -*- coding: utf-8 -*-
import tensorflow as tf


# 配置神经网络参数
INPUT_NODE = 784
OUTPUT_NODE = 10
IMAGE_SIZE = 28
NUM_CHANNELS = 1
NUM_LABELS = 10

# 第一层卷基层的尺寸和深度
CONV1_SIZE = 5
CONV1_DEEP = 32

# 第二层卷基层的尺寸和深度
CONV2_SIZE = 5
CONV2_DEEP = 64

# 全连接节点个数
FC_SIZE = 521


def inference(input_tensor, train, regularizer):
	"""
	desc: 1. 定义卷机神经网络的前向传播过程
		2. dropout方法可以进一步提升模型的可靠性并防止过拟合（只在训练时使用）
	:param input_tensor:
	:param train: 用于区分训练过程还是测试过程
	:param regularizer:
	:return:
	"""
	
	# 声明第一层卷机神经网络并实现前向传播过程
	# 通过使用不同的命名空间来隔离不同的变量
	# 和标准的LeNet-5模型不同，此处定义的卷基层输入为28*28*1的原始LSTM图片像素。因为使用全0填充，所以输出为28*28*32的矩阵
	with tf.variable_scope('layer1-conv1'):
		conv1_weight = tf.get_variable("weight", [CONV1_SIZE, CONV1_SIZE, NUM_CHANNELS, CONV1_DEEP],
		                               initializer=tf.truncated_normal_initializer(stddev=0.1))
		conv1_bias = tf.get_variable("bias", [CONV1_DEEP], initializer=tf.constant_initializer(0.0))
		
		# 使用边长为5，深度为32的过滤器，过滤器移动的步长为1，且使用全0填充
		conv1 = tf.nn.conv2d(input_tensor, conv1_weight, strides=[1, 1, 1, 1], padding='SAME')
		relu1 = tf.nn.relu(tf.nn.bias_add(conv1, conv1_bias))
		
	# 第二层池化层前向传播过程
	# 池化层过滤器选择2*2，使用全零填充并且移动步长为2
	# 输入为28*28*32，输出为14*14*32
	with tf.name_scope('layer2-pool1'):
		pool1 = tf.nn.max_pool(relu1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
	
	# 第三层卷基层的前向传播过程
	# 使用过滤器为5*5*64，过滤器移动步长为1，使用全零填充
	# 输入矩阵为14*14*32，输出矩阵为14*14*64
	with tf.variable_scope('layer3-conv2'):
		conv2_weight = tf.get_variable("weight", [CONV2_SIZE, CONV2_SIZE, CONV1_DEEP, CONV2_DEEP],
		                               initializer=tf.truncated_normal_initializer(stddev=0.1))
		conv2_bias = tf.get_variable("bias", [CONV2_DEEP], initializer=tf.constant_initializer(0.0))
	

