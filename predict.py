import tensorflow as tf
import numpy as np
import os
from config import *
from data_utils import *
from models.models import *

### SET UP CONFIG FOR PREDICTIONS ###
checkpoint_dir = './deep-cnn/'
test_imgs_dir = './data/demo/' # './data/test/bike/'
test_seq = os.listdir(test_imgs_dir)
test_seq = list(map(lambda x: test_imgs_dir + x, test_seq))
test_seq = [val for val in test_seq if int(val.split('/')[-1].split('.')[0]) % 2 == 0]
dummy_labels = np.random.random((len(test_seq), 3))
input_test_seq = list(zip(test_seq, dummy_labels))

# # Model
graph = tf.Graph()
with graph.as_default():
    # Build model
    # model = Komada(graph, mean, std)
    model_type = CNN

    if model_type is CNN:
        # (train_seq_X, train_seq_Y, valid_seq_X, valid_seq_Y), (mean, std) = process_csv_cnn(filename="./data/train/output/interpolated.csv", val=25) # concatenated interpolated.csv from rosbags
        # test_seq_X, test_seq_Y = read_csv("./data/test/final_example.csv", train=False, cnn=True) # interpolated.csv for testset filled with dummy values
        mean, std = -0.0057757964, 0.26503262

    else:
        # (train_seq_X, valid_seq_X), (mean, std) = process_csv(filename="./data/train/output/interpolated.csv", val=5)
        # train_seq_Y, valid_seq_Y, test_seq_Y = None, None, None
        mean, std = [-0.0057757964, - 0.073793308,
                     15.845663], [0.26503262,  0.76966596, 5.631488]

    model = model_type(graph, mean, std)

    with tf.Session(graph=graph) as session:
        ckpt = tf.train.latest_checkpoint(checkpoint_dir)
        assert ckpt is not None, 'Trying to load an invalid checkpoint!'
        model.saver.restore(sess=session, save_path=ckpt)
        with open("{}-test-predictions".format("./deepcnn_model"), "w") as out:
            _, test_predictions = model.do_epoch(session=session, sequences=input_test_seq, labels=None,  mode='test')
            for img, pred in test_predictions.items():
                # img = img.replace("challenge_2/Test-final/center/", "")
                print("%s,%f" % (img, pred), file=out)
