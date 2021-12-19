import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import math


# %%

## DATA WITHOUT ATTACKS
## https://www.kaggle.com/cicdataset/cicids2017
from database import Database
from logger import Logger

db = Database()
logger = Logger(db)

class DetectionMemory:
    gt_df = None
    test_df = None


def detection_click(file, type_of_detection):
    logger.log_a_logxd('LOG', f'anomaly-detection({file}, {type_of_detection})')
    if DetectionMemory.gt_df is None:
        try:
            DetectionMemory.gt_df = pd.read_csv('../data/Monday-WorkingHours.pcap_ISCX.csv', sep=',', encoding='UTF8')
        except:
            logger.log_a_logxd('ERROR',
                               f'anomaly-detection({file}, {type_of_detection}) - did not find the ground truth data file, or it could not be read',
                               if_print=True)
            return
        logger.log_a_logxd('LOG', f'anomaly-detection({file}, {type_of_detection}) - loaded ground truth data')
    try:
        DetectionMemory.test_df = pd.read_csv(file, sep=',', encoding='UTF8')
    except:
        logger.log_a_logxd('ERROR',
                           f'anomaly-detection({file}, {type_of_detection}) - no such file as {file} or it could not be read',
                           if_print=True)
        return
    logger.log_a_logxd('LOG', f'anomaly-detection({file}, {type_of_detection}) - loaded test data', if_print=True)
    if type_of_detection == 'flow_duration':
        find_anomaly_in_flow_duration(DetectionMemory.gt_df, DetectionMemory.test_df)
    elif type_of_detection == 'unique_ports':
        find_anomaly_in_unique_ports(DetectionMemory.gt_df, DetectionMemory.test_df)
    elif type_of_detection == 'high_difference':
        logger.log_a_logxd('LOG', f'anomaly-detection({file}, {type_of_detection}) - Calculating all possible analytics - this may take a while', if_print=True)
        gt_analytics = calculate_overall_analytics(DetectionMemory.gt_df)
        compare_overall_analytics(DetectionMemory.test_df, gt_analytics)
    else:
        logger.log_a_logxd('ERROR', f'anomaly-detection({file}, {type_of_detection}) - No such type of detection as {type_of_detection}', if_print=True)
    logger.log_a_logxd('LOG',
                       f'anomaly-detection({file}, {type_of_detection}) - Analysis is done',
                       if_print=True)


def flow_duration_analytics(data_frame):
    analytics_dict = {}
    flow_duration = data_frame[' Flow Duration']
    analytics_dict['flow_duration_mean'] = np.mean(flow_duration)
    analytics_dict['dur_0_200'] = 0
    analytics_dict['dur_200_1000'] = 0
    analytics_dict['dur_1000_100000'] = 0
    analytics_dict['dur_100000_1000000'] = 0
    analytics_dict['dur_1000000_100000000'] = 0
    analytics_dict['dur_100000000_more'] = 0
    analytics_dict['sum'] = sum(flow_duration)
    for dur in flow_duration:
        if dur <= 200:
            analytics_dict['dur_0_200'] += 1
        elif dur <= 1000:
            analytics_dict['dur_200_1000'] += 1
        elif dur <= 100000:
            analytics_dict['dur_1000_100000'] += 1
        elif dur <= 1000000:
            analytics_dict['dur_100000_1000000'] += 1
        elif dur <= 100000000:
            analytics_dict['dur_1000000_100000000'] += 1
        else:
            analytics_dict['dur_100000000_more'] += 1
    return analytics_dict


def get_unique_ports(gt_df, test_df):
    unique_ports = {'gt': gt_df[' Destination Port'].unique(), 'test': test_df[' Destination Port'].unique()}
    return unique_ports


def find_anomaly_in_unique_ports(gt_data, test_data):
    unique_ports = get_unique_ports(gt_data, test_data)
    for port in unique_ports['test']:
        if port not in unique_ports['gt']:
            logger.log_a_logxd('ALERT', f'find_anomaly_in_unique_ports(gt_data, test_data) - port={port} present in tested data but not in ground truth data', if_print=True)


def calculate_overall_analytics(data_frame):
    res_dict = {}
    for key in data_frame:
        try:
            res_dict[key] = np.mean(data_frame[key])
        except:
            pass
    return res_dict


def compare_overall_analytics(test_frame, gt_analytics):
    for key in test_frame:
        try:
            if 0.1 * gt_analytics[key] > np.mean(test_frame[key]):
                logger.log_a_logxd('ALERT',
                                   f'compare_overall_analytics(test_frame, gt_analytics) - {key} values are a lot smaller in tested data', if_print=True)
            elif np.mean(test_frame[key]) > 1.9 * gt_analytics[key]:
                logger.log_a_logxd('ALERT',
                                   f'compare_overall_analytics(test_frame, gt_analytics) - {key} values are a lot bigger in tested data', if_print=True)
        except:
            logger.log_a_logxd('ERROR',
                               f'compare_overall_analytics(test_frame, gt_analytics) - unable to fetch results for key:{key}', if_print=True)


def normalize_test_data(gt_analysis, test_analysis):
    normalized_test_analysis = {}
    for key in test_analysis:
        if key != 'sum' and key != 'flow_duration_mean':
            normalized_test_analysis[key] = test_analysis[key] * (gt_analysis['sum']/test_analysis['sum'])
        else:
            normalized_test_analysis[key] = test_analysis[key]
    return normalized_test_analysis

def find_anomaly_in_flow_duration(gt_data, test_data):
    gt_analysis = flow_duration_analytics(gt_data)
    test_analysis = flow_duration_analytics(test_data)
    # normalize test data
    test_analysis = normalize_test_data(gt_analysis, test_analysis)
    for key in gt_analysis:
        if gt_analysis[key] * 0.5 > test_analysis[key]:
            logger.log_a_logxd('ALERT',
                               f'find_anomaly_in_flow_duration(gt_data, test_data) - amount of packets in section {key} in tested data is a lot smaller than in ground truth data', if_print=True)
        if test_analysis[key] > gt_analysis[key] * 1.5:
            logger.log_a_logxd('ALERT',
                               f'find_anomaly_in_flow_duration(gt_data, test_data) - amount of packets in section {key} in tested data is a lot bigger than in ground truth data', if_print=True)
