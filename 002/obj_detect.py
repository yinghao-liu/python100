#!/usr/bin/env python3

import numpy as np
import os
import sys
import tensorflow as tf
import cv2 as cv


print("start-------------------")
# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_FROZEN_GRAPH = 'ssd_mobilenet_v1_coco_2017_11_17' + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

category_index={}
def create_category_index_from_labelmap(label_file):
    global category_index
    with open("protobuf/name_map") as f:
        category_index=eval(f.read())

create_category_index_from_labelmap("protobuf/name_map")

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')



PATH_TO_TEST_IMAGES_DIR = 'test_images'
TEST_IMAGE_PATHS = [os.path.join(PATH_TO_TEST_IMAGES_DIR, 'bend{}.jpg'.format(i)) for i in range(2,3) ]


def run_inference_for_single_image(image, graph):
    with graph.as_default():
        with tf.Session() as sess:
            # Get handles to input and output tensors
            ops = tf.get_default_graph().get_operations()
            all_tensor_names = {output.name for op in ops for output in op.outputs}
            tensor_dict = {}
            for key in [
                'num_detections', 'detection_boxes', 'detection_scores',
                'detection_classes'
            ]:
                tensor_name = key + ':0'
                if tensor_name in all_tensor_names:
                    tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)
                # Follow the convention by adding back the batch dimension

            image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')
            # Run inference
            output_dict = sess.run(tensor_dict, feed_dict={image_tensor: np.expand_dims(image, 0)})
            # all outputs are float32 numpy arrays, so convert types as appropriate
            output_dict['num_detections'] = int(output_dict['num_detections'][0])
            output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.uint8)
            output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
            output_dict['detection_scores'] = output_dict['detection_scores'][0]
        return output_dict


for image_path in TEST_IMAGE_PATHS:
    #image = cv.imread("test_images/cx.jpg", cv.IMREAD_COLOR)
    image = cv.imread("test_images/human.jpg", cv.IMREAD_COLOR)
    #image = cv.imread(image_path, cv.IMREAD_COLOR)
    image_np = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    #image = Image.open("test_images/image1.jpg")
    #image_np = load_image_into_numpy_array(image)
    # the array based representation of the image will be used later in order to prepare the
    # result image with boxes and labels on it.
    print("--------------------------")
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    #image_np_expanded = np.expand_dims(image_np, axis=0)
    # Actual detection.
    output_dict = run_inference_for_single_image(image_np, detection_graph)
    print("-------output_dict--------")
    #print(output_dict)
    print("-------output_dict--------")
    #print(type(output_dict['detection_classes']))
    px,py=image_np.shape[:2]
    pt1=[int(px*output_dict['detection_boxes'][0][0]), int(py*output_dict['detection_boxes'][0][1])]
    pt2=[int(px*output_dict['detection_boxes'][0][2]), int(py*output_dict['detection_boxes'][0][3])]
    pt1.reverse()
    pt2.reverse()
    cv.rectangle(image_np, tuple(pt1), tuple(pt2), (255,0,0))
    cv.namedWindow("img", cv.WINDOW_NORMAL)
    cv.resizeWindow("img", py, px)
    cv.imshow("img", cv.cvtColor(image_np, cv.COLOR_RGB2BGR))
    cv.waitKey()
