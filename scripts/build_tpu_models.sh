#!/bin/bash
curl -LO https://github.com/google-coral/test_data/raw/master/mobilenet_v2_1.0_224_quant_edgetpu.tflite
mv mobilenet_v2_1.0_224_quant_edgetpu.tflite backend/models/ocr_edgetpu.tflite
