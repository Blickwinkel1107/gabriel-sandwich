#
# Cloudlet Infrastructure for Mobile Computing
#   - Task Assistance
#
#   Author: Zhuo Chen <zhuoc@cs.cmu.edu>
#           Roger Iyengar <iyengar@cmu.edu>
#
#   Copyright (C) 2011-2019 Carnegie Mellon University
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import numpy as np
import logging
from gabriel_server import cognitive_engine
from gabriel_protocol import gabriel_pb2
import instruction_pb2
import instructions
import sys
import os
import cv2
import asyncio

from migrate_lib import migrate_api
from migrate_lib.protocol import app_state_pb2

faster_rcnn_root = os.getenv('FASTER_RCNN_ROOT', '.')
sys.path.append(os.path.join(faster_rcnn_root, "tools"))
import _init_paths  # this is necessary
from fast_rcnn.config import cfg as faster_rcnn_config
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
sys.path.append(os.path.join(faster_rcnn_root, "python"))
import caffe


PROTOTXT = 'model/faster_rcnn_test.pt'
CAFFEMODEL = 'model/model.caffemodel'

IMAGE_MAX_WH = 640  # Max image width and height

CONF_THRESH = 0.5
NMS_THRESH = 0.3

CLASS_IDX_LIMIT = instructions.BREAD + 1  # Bread has largest index


if not os.path.isfile(CAFFEMODEL):
    raise IOError(('{:s} not found.').format(CAFFEMODEL))


faster_rcnn_config.TEST.HAS_RPN = True  # Use RPN for proposals

logger = logging.getLogger(__name__)


class SandwichEngine(cognitive_engine.Engine):
    def __init__(self, cpu_only):
        if cpu_only:
            caffe.set_mode_cpu()
        else:
            caffe.set_mode_gpu()

            # 0 is the default GPU ID
            caffe.set_device(0)
            faster_rcnn_config.GPU_ID = 0

        self.net = caffe.Net(PROTOTXT, CAFFEMODEL, caffe.TEST)

        # Warmup on a dummy image
        img = 128 * np.ones((300, 500, 3), dtype=np.uint8)
        for i in range(2):
            _, _= im_detect(self.net, img)
        logger.info("Caffe net has been initilized")
        
        self.user_progress = []
        self.video_frames = []
        self.need_migrate_session = False
        self.need_resume = False
        migrate_api.register_extract_state_api(self.extract_state)

    def extract_state(self):
        app_state = app_state_pb2.AppState()
        app_state.user_progress.extend(self.user_progress)
        if instructions.last_effect_update is not None:
            app_state.result_wrapper.CopyFrom(instructions.last_effect_update)
        return app_state.SerializeToString()

    def _detect_object(self, img):
        scores, boxes = im_detect(self.net, img)

        det_for_class = {}
        # Start from 1 because 0 is the background
        for cls_idx in range(1, CLASS_IDX_LIMIT):
            cls_boxes = boxes[:, 4 * cls_idx : 4 * (cls_idx + 1)]
            cls_scores = scores[:, cls_idx]

            # dets: detected results, each line is in
            #       [x1, y1, x2, y2, confidence] format
            dets = np.hstack((cls_boxes, cls_scores[:, np.newaxis])).astype(
                np.float32)

            # non maximum suppression
            keep = nms(dets, NMS_THRESH)
            dets = dets[keep, :]

            for det in dets:
                if det[-1] >= CONF_THRESH:
                    det_for_class[cls_idx] = det
                    break  # We only want one object

        return det_for_class

    def handle_migrate(self, from_migrate):
        logger.info("from_migrate: %s" % from_migrate)
        asyncio.get_event_loop().run_until_complete(migrate_api.send_state())
        
    def handle_merge(self, bytes_obj):
        old_state = self.user_progress
        new_state_obj = app_state_pb2.AppState().FromString(bytes_obj)
        self.user_progress = new_state_obj.user_progress
        logger.info("Merge State: %s ---> %s" % (old_state, self.user_progress))
        instructions.last_effect_update = new_state_obj.result_wrapper
        self.need_resume = True
        
    def handle_finish_merge(self):
        # logger.info("Finish merged, Clean State: %s ---> %s" % (self.user_progress, []))
        logger.info("Finish merged, Clean State")
        self.user_progress = []
        self.need_migrate_session = True
        
    def handle_client_disconnect(self):
        if self.user_progress == []:
            return
        logger.info("Disconnected, Clean State")
        self.user_progress = []
    
    def _send_client_migrate_packet(self, from_client):
        result_wrapper = gabriel_pb2.ResultWrapper()
        result_wrapper.frame_id = from_client.frame_id
        result_wrapper.status = gabriel_pb2.ResultWrapper.Status.SUCCESS
        result_wrapper.ClearField('engine_fields')
        result = gabriel_pb2.ResultWrapper.Result()
        result.engine_name = migrate_api.MIGRATE_ADDRESS
        result_wrapper.results.append(result)
        logger.info("MIGRATE user_progress TO ANOTHER SERVER!")
        return result_wrapper
    
    def handle(self, from_client):
        # logger.info("frame_id: %s" % from_client.frame_id)
        if self.need_migrate_session:
            self.need_migrate_session = False
            return self._send_client_migrate_packet(from_client)
            
        if from_client.payload_type != gabriel_pb2.PayloadType.IMAGE:
            return cognitive_engine.wrong_input_format_error(
                from_client.frame_id)

        engine_fields = cognitive_engine.unpack_engine_fields(
            instruction_pb2.EngineFields, from_client)
        
        logger.info("engine_fields\n%s" % engine_fields)
        user_state_name = instruction_pb2.Sandwich.State.Name(engine_fields.sandwich.state)
        # logger.info("user_progress from client %s" % user_state_name)
        # drop additional frames after migration
        # if user_state_name == 'START' and not self.need_resume:
        #     logger.info("Reset State: %s ---> %s" % (self.user_progress, []))
        #     self.user_progress = []
        if len(self.user_progress) == 0 and user_state_name != 'START':
            return self._send_client_migrate_packet(from_client)
        if len(self.user_progress) == 0\
            or (user_state_name != "START" and self.user_progress[-1] != user_state_name):
            self.user_progress.append(user_state_name)
            logger.info("user_progress: %s" % self.user_progress)
            logger.info("Update State: %s" % self.user_progress)

        img_array = np.asarray(bytearray(from_client.payload), dtype=np.int8)
        img = cv2.imdecode(img_array, -1)
        
        # save video frame per interval (15fps)
        # self.video_frames.append(img)
        # if from_client.frame_id % 50 == 0:
        #     logger.info("video frames size: %d B" % self.video_frames.__sizeof__()) # byte
        # write to folder. only for checking, quality isn't important
        # cv2.imwrite('./video_frames/%d.jpg' % from_client.frame_id, img, [cv2.IMWRITE_JPEG_QUALITY, 100])

        if max(img.shape) > IMAGE_MAX_WH:
            resize_ratio = float(IMAGE_MAX_WH) / max(img.shape[0], img.shape[1])

            img = cv2.resize(img, (0, 0), fx=resize_ratio, fy=resize_ratio,
                             interpolation=cv2.INTER_AREA)
            det_for_class = self._detect_object(img)
            for class_idx in det_for_class:
                det_for_class[class_idx][:4] /= resize_ratio
        else:
            det_for_class = self._detect_object(img)

        # logger.info("object detection result: %s", det_for_class)
        # if engine_fields.sandwich.state == instruction_pb2.Sandwich.State.
        if engine_fields.sandwich.state == instruction_pb2.Sandwich.State.START and self.user_progress[-1] != 'START' and self.need_resume:
            self.need_resume = False
            engine_fields.sandwich.state = instruction_pb2.Sandwich.State.Value(self.user_progress[-1])
            logger.info("Resume user_progress!")
            result_wrapper = instructions.last_effect_update
        else:
            engine_fields.sandwich.state = instruction_pb2.Sandwich.State.Value(self.user_progress[-1])
            result_wrapper = instructions.get_instruction(
                engine_fields, det_for_class)
        result_wrapper.frame_id = from_client.frame_id
        result_wrapper.status = gabriel_pb2.ResultWrapper.Status.SUCCESS
        # if self.user_progress[-1] == 'LETTUCE':  # test!
        #     print('xxxxxxxxxxxxxxxxxxx')
        #     result_wrapper.ClearField('engine_fields')
        if len(result_wrapper.results) != 0:
            logger.info("result_wrapper.results[1]\n%s" % result_wrapper.results[1])

        return result_wrapper
