#!/usr/bin/env python3

import numpy as np
import os
import sys
import tensorflow as tf
import cv2 as cv


print("-----------import done------------")
# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_FROZEN_GRAPH = os.path.join('ssd_mobilenet_v1_coco_2017_11_17', 'frozen_inference_graph.pb')

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('protobuf', 'name_map')

# list of the images to run with object detection
PATH_TO_TEST_IMAGES_DIR = 'test_images'
TEST_IMAGE_PATHS = [os.path.join(PATH_TO_TEST_IMAGES_DIR, "{}".format(i)) for i in os.listdir(PATH_TO_TEST_IMAGES_DIR) ]

category_index={}
def create_category_index_from_labelmap(label_file):
    global category_index
    with open(label_file) as f:
        return eval(f.read())

category_index=create_category_index_from_labelmap(PATH_TO_LABELS)

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')


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

colors=[(0,0,255), (0,255,0), (255,0,0), (0,255,255), (255,0,255), (255,255,0)]
for image_path in TEST_IMAGE_PATHS:
    image = cv.imread(image_path, cv.IMREAD_COLOR)
    image_np = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    # Actual detection.
    output_dict = run_inference_for_single_image(image_np, detection_graph)
    print("-------output_dict--------")
    #print(output_dict)
    print("-------output_dict--------")
    #print(type(output_dict['detection_classes']))
    px,py=image_np.shape[:2]
    for index in range(output_dict["num_detections"]):
        if output_dict["detection_scores"][index] < 0.5:
            break
        print("score is {} class is {}".format(output_dict["detection_scores"][index],\
                category_index[output_dict["detection_classes"][index]]))
        color=colors[output_dict["detection_classes"][index]%6]
        pt1=[int(px*output_dict['detection_boxes'][index][0]), int(py*output_dict['detection_boxes'][index][1])]
        pt2=[int(px*output_dict['detection_boxes'][index][2]), int(py*output_dict['detection_boxes'][index][3])]
        pt1.reverse()
        pt2.reverse()
        cv.rectangle(image_np, tuple(pt1), tuple(pt2), color, 2)
        text="{}:{}%".format(category_index[output_dict["detection_classes"][index]], \
                             int(output_dict["detection_scores"][index]*100))
        ret,baseline=cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 1, 1 )
        fillp1=(pt1[0], pt1[1]-ret[1])
        fillp2=(pt1[0]+ret[0], pt1[1])
        cv.rectangle(image_np, fillp1, fillp2, color, -1)
        cv.putText(image_np, text, tuple(pt1), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 1)
    cv.namedWindow("img", cv.WINDOW_NORMAL)
    cv.resizeWindow("img", py, px)
    cv.imshow("img", cv.cvtColor(image_np, cv.COLOR_RGB2BGR))
    cv.waitKey()
