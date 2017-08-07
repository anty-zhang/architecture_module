# -*- coding: utf-8 -*-
# 图间tensorflow同步程序样例

import time
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import mnist_inference

###################################################################################################
# mnist 数据集相关常数
# 输入层节点数。 对于mnist数据集，这个等于图片的像素
INPUT_NODE = 784
# 输出层的节点数。这个等于类别的数目
OUTPUT_NODE = 10

###################################################################################################
# 配置神经网络参数
# 隐藏层节点数
LAYER1_NODE = 500
# 一个训练batch中的训练数据个数， batch越大，训练越接近梯度下降；batch越小，训练越接近随机梯度下降
BATCH_SIZE = 100
# 基础学习率
LEARNING_RATE_BASE = 0.8
# 学习率衰减率
LEARNING_RATE_DECAY = 0.99
# 描述模型复杂度的正则化项在损失函数中的系数
REGULARIZATION_RATE = 0.0001
# 训练论数
TRAINING_STEPS = 2000
# 滑动平均衰减率
MOVING_AVERAGE_DECAY = 0.99

# 模型保存的路径和文件名。
MODEL_SAVE_PATH = "/data/logs/log_async"
# mnist数据路径
DATA_PATH = "/data/datasets/MNIST_data"

###################################################################################################
# 通过flags指定运行的参数
FLAGS = tf.app.flags.FLAGS
# 指定当前运行的是参数服务器还是计算服务器
# 参数服务器只负责TensorFlow中变量的维护和管理；计算服务器负责每一轮迭代时运行反向传播过程
tf.app.flags.DEFINE_string("job_name", 'worker', '"ps" or "worker"')

# 指定集群中参数服务器地址
tf.app.flags.DEFINE_string("ps_hosts", 'tf-ps0:2222, tf-ps1:2223', 'Comma-separated list of hostname:port '
                                                                   'for the parameter server jobs. e.g. "tf-ps0:2222, tf-ps1:2223"')

# 指定集群中计算服务器地址
tf.app.flags.DEFINE_string(('worker_hosts', 'tf-worker0:2222, tf-worker1:2223', 'Comma-separated list of hostname:port'
                                                                                ' for the worker jobs. e.g. "tf-worker0:2222, tf-worker1:2223"'))

# 指定当前任务ID
# TensorFlow会自动根据参数服务器／计算服务器立标中国年的端口号来启动服务
tf.app.flags.DEFINE_integer('task_id', 0, 'Task ID of the worker/replica running the training.')


###################################################################################################
# 定义TensorFlow的计算图并返回每一轮迭代需要运行的操作
# 和异步类似，唯一的区别在于使用tf.train.SyncReplicasOptimizer处理同步更新
def buidl_model(x, y_, n_workers, is_chief):
	regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)
	y = mnist_inference.inference(x, regularizer)
	global_step = tf.Variable(0, trainable=False)
	
	# 定义损失函数并计算反向传播过程
	cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(y, tf.argmax(y_, 1))
	cross_entropy_mean = tf.reduce_mean(cross_entropy)
	loss = cross_entropy_mean + tf.add_n(tf.get_collection('losses'))
	learning_rate = tf.train.exponential_decay(LEARNING_RATE_BASE, global_step, 60000 / BATCH_SIZE, LEARNING_RATE_DECAY)
	
	# ======================================================================================
	# 通过tf.train.SyncReplicasOptimizer方式实现同步更新
	opt = tf.train.SyncReplicasOptimizer(tf.train.GradientDescentOptimizer(learning_rate),  # 定义基础的优化方法
	                                     replicas_to_aggregate=n_workers,    # 定义每一轮更新需要多少个计算服务器得出的梯度
	                                     total_num_replicas=n_workers,    # 指定总共有多少个计算服务器
	                                     replica_id=FLAGS.task_id    # 指定当前计算服务器的编号
	                                     )
	
	# 定义每一轮迭代需要的操作
	### train_op = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)
	train_op = opt.minimize(loss, global_step=global_step)
	# ======================================================================================
	
	# 定义每一轮迭代需要运行的操作
	if is_chief:
		# 计算变量的滑动平均值
		variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
		variable_averages_op = variable_averages.apply(tf.trainable_variables())
		with tf.control_dependencies(([variable_averages_op, train_op])):
			train_op = tf.no_op()
	return global_step, loss, train_op, opt


###################################################################################################
# 训练分布式深度学习模型的主要过程
def main(argv=None):
	# 解析flags并通过tf.train.ClusterSpec配置TensorFlow集群
	ps_hosts = FLAGS.ps_hosts.split(',')
	worker_hosts = FLAGS.worder_hosts.split(',')
	n_workers = len(worker_hosts)
	cluster = tf.train.ClusterSpec({'ps': ps_hosts, 'worker': worker_hosts})
	
	# 通过ClusterSpec以及当前任务创建Server
	server = tf.train.Server(cluster, job_name=FLAGS.job_name, task_index=FLAGS.task_id)
	
	# 参数服务器只需要管理TensorFlow中的变量，不需要执行训练过程
	# server.join会一直定在这条语句上
	if FLAGS.job_name == 'ps':
		server.join()
	
	# 定义计算服务器需要运行的操作
	# 在所有的计算服务器中有一个是主计算服务器，它除来负责计算反响传播的结果，还负责输出日志和保存模型
	is_chief = (FLAGS.task_id == 0)
	mnist = input_data.read_data_sets(DATA_PATH, one_hot=True)
	
	# 通过tf.train.replica_device_setter来指定执行每一个运算的设备
	# 此函数会自动将所有的参数分配到参数服务器上，而计算分配到当前的计算服务器上
	with tf.device(
			tf.train.replica_device_setter(worker_device="/job:worker/task:%d" % FLAGS.task_id, cluster=cluster)):
		x = tf.placeholder(tf.float32, [None, mnist_inference.INPUT_NODE], name="x-input")
		y_ = tf.placeholder(tf.float32, [None, mnist_inference.OUTPUT_NODE], name="y-input")
		
		# 定义训练模型需要运行的操作
		global_step, loss, train_op, opt = buidl_model(x, y_, n_workers, is_chief)
		
		# 定义用于保存模型的saver
		saver = tf.train.Saver()
		
		# 定义日志输出操作
		summary_op = tf.merge_all_summaries()
		
		# 定义变量初始化操作
		init_op = tf.initialize_all_variables()
		
		# ======================================================================================
		# 在同步模式下，主计算服务器需要协调不同计算服务器计算得到的参数梯度并最终更新参数
		# 在主服务器需要完成一些额外的初始工作
		if is_chief:
			# 定义协调不同计算服务器的队列并定义初始化操作
			chied_queue_runner = opt.get_chief_queue_runner()
			# get_init_tokens_op 中的参数控制对不同计算服务器之间的同步要求
			# get_init_tokens_op的参数大于0时，TensorFlow支持多次使用由同一个个计算服务器的梯度，这样可以缓解计算服务器性能瓶颈问题
			init_tokens_op = opt.get_init_tokens_op(0)
		# ======================================================================================
		
		
		# 通过tf.train.Supervisor管理训练深度学习模型的通用功能
		# tf.train.Supervisor能统一管理队列操作、模型保存、日志输入、会话生成
		sv = tf.train.Supervisor(
			is_chief=is_chief,  # 定义当前计算服务器是否为主计算服务器，只有主计算服务器会保存模型和日志输出
			logdir=MODEL_SAVE_PATH,  # 指定保存模型和输入日志的地址
			init_op=init_op,  # 指定初始化操作
			summary_op=summary_op,  # 指定日志生成操作
			saver=saver,  # 指定用于保存模型的saver
			global_step=global_step,  # 指定昂欠迭代的轮数，这个会用于生成保存模型文件的文件名
			save_model_secs=60,  # 指定保存模型的时间间隔
			save_summaries_secs=60  # 指定日志输出的时间间隔
		)
		
		sess_config = tf.ConfigProto(allow_soft_placement=True, log_device_placement=True)
		
		# 通过tf.train.Supervisor生成会话
		sess = sv.prepare_or_wait_for_session(server.target, config=sess_config)
		
		# ======================================================================================
		# 在主计算服务器上启动协调同步engine的对比了并初始化
		if is_chief:
			sv.start_queue_runners((sess, [chied_queue_runner]))
			sess.run(init_tokens_op)
		# ======================================================================================
		
		step = 0
		start_time = time.time()
		
		# 执行迭代过程
		# 在迭代过程中tf.train.Supervisor会帮助输出日志和保存模型, 所以不需要直接调用这些过程
		while not sv.should_stop():
			xs, ys = mnist.train.next_batch(BATCH_SIZE)
			_, loss_value, global_step_value = sess.run([train_op, loss, global_step], feed_dict={x: xs, y_: ys})
			if global_step_value >= TRAINING_STEPS:
				break
			
			# 每隔一段时间输出训练信息
			if step > 0 and step % 100 == 0:
				duration = time.time() - start_time
				
				# 不同的训练服务器都会更新全局的训练轮数
				# 所以这里使用global_step_value可以直接得到在训练中使用过的batch总数
				sec_per_batch = duration / global_step_value
				format_str = "After %d training steps (%d global steps), loss on training batch is %g. (%.3f sec/batch)"
				print format_str % (step, global_step_value, loss_value, sec_per_batch)
				
				step += 1
	
	sv.stop()


if __name__ == "__main__":
	tf.app.run()

"""
	python dist_tf_mnist_sync.py \
	--job_name='ps' \
	--task_id=0 \
	--ps_hosts='tf-ps0:2222' \
	--worker_hosts='tf-worker0:2222, tf-worder1:2222'

	python dist_tf_mnist_sync.py \
	--job_name='worker' \
	--task_id=0 \
	--ps_host='tf-ps0:2222' \
	--worker_hosts='tf-worker0:2222, tf-worker1:2222'


	python dist_tf_mnist_sync.py \
	--job_name='worker' \
	--task_id=1 \
	--ps_host='tf-ps0:2222' \
	--worker_hosts='tf-worker0:2222, tf-worker1:2222'

"""