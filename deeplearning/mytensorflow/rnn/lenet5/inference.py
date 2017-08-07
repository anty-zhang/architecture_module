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
FC_SIZE = 512


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
		conv2 = tf.nn.conv2d(pool1, conv2_weight, strides=[1, 1, 1, 1], padding='SAME')
		relu2 = tf.nn.relu(tf.nn.bias_add(conv2, conv2_bias))

	# 实现第四层迟化层的前向传播过程，和第二层结构一样
	# 迟化层过滤器选择2*2，使用全零填充且移动步长为2
	# 输入矩阵为14*14*64，输出矩阵为7*7*64
	with tf.name_scope("layer4-pool2"):
		pool2 = tf.nn.max_pool(relu2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

	# 第四层池化层输出转为第五层全连接层的数据格式
	# 全连接输入的格式为向量，所以需要将7*7*64的矩阵拉直成一个向量
	# pool2.get_shape函数可以得到第四层输出矩阵的维度而不需要手工计算
	# 每一层神经网络的输入输出都为一个batch矩阵，所以这里得到的维度也包含batch中的数据个数
	pool_shape = pool2.get_shape().as_list()

	# 计算将矩阵拉直成向量之后的长度
	nodes = pool_shape[1] * pool_shape[2] * pool_shape[3]

	# 通过tf.reshape函数将第四层的输出变成一个batch的向量
	reshaped = tf.reshape(pool2, [pool_shape[0], nodes])

	# 声明第五层全连接层的变量并实现前向传播过程
	# 输入矩阵为batch* nodes(3136)，输出为一组长度为512的向量
	# dropout在训练时会随机将部分节点输出为0.
	# dropout可以避免过拟合
	# dropout一般只会在全连接层而不是卷积层或池化层使用
	with tf.variable_scope('layer5-fc1'):
		fc1_weight = tf.get_variable("weight", [nodes, FC_SIZE],initializer=tf.truncated_normal_initializer(stddev=0.1))

		# 只有全连接层的权重需要加入正则化
		if regularizer:
			tf.add_to_collection('losses', regularizer(fc1_weight))
		fc1_bias = tf.get_variable("bias", [FC_SIZE], initializer=tf.constant_initializer(0.1))

		fc1 = tf.nn.relu(tf.matmul(reshaped, fc1_weight) + fc1_bias)
		if train:
			fc1 = tf.nn.dropout(fc1, 0.5)

	# 声明第六层全连接的变量并实现前向传播过程
	# 输出为batch*512，输出为batch*10
	# 这一层的输出经过softmax之后就得了最后的分类结果
	with tf.variable_scope('layer6-fc2'):
		fc2_weight = tf.get_variable("weight", [FC_SIZE, NUM_LABELS], initializer=tf.truncated_normal_initializer(stddev=0.1))

		if regularizer:
			tf.add_to_collection('losses', regularizer(fc2_weight))

		fc2_bias = tf.get_variable('bias', [NUM_LABELS], initializer=tf.constant_initializer(0.1))

		logit = tf.matmul(fc1, fc2_weight) + fc2_bias

	return logit

