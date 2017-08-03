# -*- coding: utf-8 -*-

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import inference as letnet5
import os
import numpy as np

# 定义神经网络参数
# 一个训练batch中的训练数据个数， batch越大，训练越接近梯度下降；batch越小，训练越接近随机梯度下降
BATCH_SIZE = 100
# 基础学习率
LEARNING_RATE_BASE = 0.01
# 学习率衰减率
LEARNING_RATE_DECAY = 0.99
# 描述模型复杂度的正则化项在损失函数中的系数
REGULARIZATION_RATE = 0.0001
# 训练论数
TRAINING_STEPS = 6000
# 滑动平均衰减率
MOVING_AVERAGE_DECAY = 0.99

# 定义训练过程
def train(mnist):
	# 定义输入输出为4维矩阵的placeholder
	x = tf.placeholder(tf.float32,
                       [BATCH_SIZE, letnet5.IMAGE_SIZE, letnet5.IMAGE_SIZE, letnet5.NUM_CHANNELS],
                       name="x-input")
	y_ = tf.placeholder(tf.float32, [None, letnet5.OUTPUT_NODE], name="y-input")

	# --------------------------------------------------------------------------------------------
	# 计算L2正则化损失函数
	regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)

	# --------------------------------------------------------------------------------------------
	# 直接使用letnet5中前向传播过程
	y = letnet5.inference(x, False, regularizer)

	# 定义存储训练轮数的变量
	# 此变量不需要计算滑动平均值，所以这里指定这个变量为不可训练的变量
	# 在tensorflow训练神经网络时，一般会将训练轮数的变量指定为不可训练的变量
	global_step = tf.Variable(0, trainable=False)

	# --------------------------------------------------------------------------------------------
	# 定义滑动平均操作
	# 给定滑动平均衰减率和训练轮数的变量，初始化滑动平均类；给定训练轮数的变量可以加快训练早期变量的更新速度
	variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
	# 在所有代表神经网络参数的变量上使用滑动平均（辅助变量不需要）
	# tf.trainable_variables返回的就是图上集合GraphKeys.TRAINABLE_AVERAGES中的元素。这个集合的元素就是所有没有指定
	# trainable=False的参数
	variable_averages_op = variable_averages.apply(tf.trainable_variables())

	# --------------------------------------------------------------------------------------------
	# 定义损失函数
	# 计算交叉熵作为刻画预测值和真实值之间差距的损失函数
	# 当分类问题只有一个正确答案时，可以使用sparse_softmax_cross_entropy_with_logits函数来加速交叉熵计算
	# tf.argmax函数得到正确答案对应的类别编号
	cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(y, labels=tf.argmax(y_, 1))
	# 计算在当前batch中所有样例的交叉熵平均值
	cross_entropy_mean = tf.reduce_mean(cross_entropy)

	loss = cross_entropy_mean + tf.add_n(tf.get_collection('losses'))

	# --------------------------------------------------------------------------------------------
	# 设置指数衰减的学习率
	learning_rate = tf.train.exponential_decay(
			LEARNING_RATE_BASE,  # 基础学习率，随着迭代的进行，更新变量时使用的学习率在这个基础上递减
			global_step,  # 当前迭代的轮数
			mnist.train.num_examples / BATCH_SIZE,  # 总的迭代次数
			LEARNING_RATE_DECAY)  # 学习率递减速度
	# 使用tf.train.GradientDescentOptimizer优化算法来优化损失函数
	# 这里的损失函数包括了交叉熵损失和L2正则化损失
	train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)

	# --------------------------------------------------------------------------------------------
	# 在训练神经网络模型时，每过一遍数据既要通过反向传播算法来更新神经网络中的参数，又要更新每一个参数的滑动平均值
	# 这一过程，tensorflow提供了tf.control_dependecies和tf.group两种机制
	# train_op = tf.group(train_step, variable_averages_op)
	with tf.control_dependencies([train_step, variable_averages_op]):
		train_op = tf.no_op(name='train')

	# --------------------------------------------------------------------------------------------
	# 初始化TensorFlow持久化类
	saver = tf.train.Saver()
	# 初始化会话并开始训练过程
	with tf.Session() as sess:
		tf.initialize_all_variables().run()
		for i in range(TRAINING_STEPS):
			xs, ys = mnist.train.next_batch(BATCH_SIZE)
			reshaped_xs = np.reshape(xs, (BATCH_SIZE, letnet5.IMAGE_SIZE, letnet5.IMAGE_SIZE, letnet5.NUM_CHANNELS))
			_, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x: reshaped_xs, y_: ys})

			# 每1000轮保存一次模型
			if i % 1000 == 0:
				# 输出当前的训练情况
				# 这里只输出轮模型在当前训练batch上的损失函数大小，通过此损失函数大小可以大概了解训练的情况
				print "After %d training step(s), loss on training batch is: %g." % (step, loss_value)
				# 保存当前模型
				# global_step参数可以让没给保存模型的文件末尾加上训练的轮数
# 				saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=global_step)


def main(argv=None):
	mnist = input_data.read_data_sets("/Users/xxx/work5/tensorflow/mnist", one_hot=True)
	train(mnist)

if __name__ == '__main__':
	main()

"""
Extracting /Users/xxx/work5/tensorflow/mnist/train-images-idx3-ubyte.gz
Extracting /Users/xxx/work5/tensorflow/mnist/train-labels-idx1-ubyte.gz
Extracting /Users/xxx/work5/tensorflow/mnist/t10k-images-idx3-ubyte.gz
Extracting /Users/xxx/work5/tensorflow/mnist/t10k-labels-idx1-ubyte.gz
After 1 training step(s), loss on training batch is: 6.79178.
After 1001 training step(s), loss on training batch is: 0.733534.
After 2001 training step(s), loss on training batch is: 0.681419.
After 3001 training step(s), loss on training batch is: 0.659512.
After 4001 training step(s), loss on training batch is: 0.681954.
After 5001 training step(s), loss on training batch is: 0.673535.

real	48m12.839s
user	95m13.749s
sys	12m33.206s
"""
