# This file is generated! Do not edit manually! see contrib/genVariants.yaml
import sys
import re
from bob.errors import ParseError

# HW_MATCH is a dictionary associating the supported hardware variants as keys
# to arrays of the supported hardware versions. For example,
# {'42' : ['47', '11']} means hardware variant 42 in versions 47 and 11 is
# supported.
variants = {
  301001 : {
      'Brand' : 'S_VOLKSWAGEN',
      'Container Name' : 'VW_CHN',
      'HW_DISPLAY_VARIANT' : '1280640',
      'HW_ETC_EXTERNAL' : '0',
      'HW_GPS' : '0',
      'HW_MATCH' : {'35': ['9', '10', '11', '12', '13', '14']},
      'HW_RAM_VARIANT' : '6',
      'MU Type' : 'C',
      'Map Variant' : 'CHN',
      'Part Number' : '3GB.035.866',
      'Region' : 'CHINA',
      'SW_A2B' : '0',
      'SW_A2B_MICROPHONES' : '0',
      'SW_ACOUSTICAL_FEEDBACK_CONTROLLER' : '0',
      'SW_AETH_PLATFORM' : 'MQB',
      'SW_BUS_MONITOR' : '1',
      'SW_CAN_PLATFORM' : 'MQB',
      'SW_CIF_DSI' : 'DSI_MQB',
      'SW_CIF_RSI' : 'RSI_MQB',
      'SW_CIF_RSI_SERVICE_REGISTRY_ADDRESS' : '127.0.0.1:443',
      'SW_CSW_ISSW' : 'ISSW_MQB',
      'SW_CURL' : '1',
      'SW_DAB_MRC' : '0',
      'SW_DEV_ACCESS' : '1',
      'SW_DEV_TUNEABLE_WIFI_ADAPTATION_TIMER' : '1',
      'SW_DIAGNOSIS_PLATFORM' : 'CNS_MQB',
      'SW_DM_VERITY' : '0',
      'SW_DOWNGRADE_PROTECTION' : '0',
      'SW_EARLY_PARKING_SOUND' : '0',
      'SW_ESD_FILE_PACKAGE' : 'CNS_MQB',
      'SW_EWS_CONFIGURATION' : 'NO_EWS',
      'SW_EXT_TV_TUNER_ETH' : '0',
      'SW_FIREWALL_CONFIG' : 'Config_MQB',
      'SW_HMI_BRAND' : 'vw',
      'SW_HMI_PROJECT' : 'MQB',
      'SW_HMI_REGION' : 'cn',
      'SW_IPERF' : '1',
      'SW_MULTI_BACKEND_SUPPORT' : '0',
      'SW_NOTIFICATION_ONLINE_STATES' : '0',
      'SW_PING' : '1',
      'SW_POS_OCU_SUPPORT' : '1',
      'SW_RADIO_CONFIGURATION' : 'CONFIG_VW',
      'SW_SECUREBOOT_KEY_SET' : 'cns3-mqb-dummy',
      'SW_SEC_KEY' : 'MQB_Fixed',
      'SW_SPEAKER_LOCALIZATION' : '0',
      'SW_SPEECH_ACTIVATION_CONTROL' : '0',
      'SW_TCPDUMP' : '1',
      'SW_TESTABILITY_SERVICE_ETHERNET' : '1',
      'SW_TRACING_ACTIVE' : '1',
      'SW_TUNER_SETUP_REGION' : 'CHINA',
      'SW_UPDATE_KEY' : 'Developer',
      'SW_WEB_APPS_AUDIO_BROWSER' : '0',
      'SW_WEB_APPS_AUDIO_NODE' : '0',
      'SW_WEB_APPS_IMPLEMENTATION' : 'Version_0',
      'SW_WEB_APPS_INITIAL_CONFIG' : 'VW',
      'Variant Info String' : 'FM3-S-NWBY4-CN-VW-MQB-PC',
      'Variant Name' : 'V01_ZR_PKW_AM_FM_China_SVW_FAWVW',
   },
  301002 : {
      'Brand' : 'VOLKSWAGEN',
      'Container Name' : 'VW_HM',
      'HW_DISPLAY_VARIANT' : '1280640',
      'HW_ETC_EXTERNAL' : '0',
      'HW_GPS' : '1',
      'HW_MATCH' : {'31': ['9', '10', '11', '12', '13', '14']},
      'HW_RAM_VARIANT' : '6',
      'MU Type' : 'H',
      'Map Variant' : 'CHN',
      'Part Number' : '3GB.035.864',
      'Region' : 'HONGKONG_MACAO',
      'SW_A2B' : '0',
      'SW_A2B_MICROPHONES' : '0',
      'SW_ACOUSTICAL_FEEDBACK_CONTROLLER' : '0',
      'SW_AETH_PLATFORM' : 'MQB',
      'SW_BUS_MONITOR' : '1',
      'SW_CAN_PLATFORM' : 'MQB',
      'SW_CIF_DSI' : 'DSI_MQB',
      'SW_CIF_RSI' : 'RSI_MQB',
      'SW_CIF_RSI_SERVICE_REGISTRY_ADDRESS' : '127.0.0.1:443',
      'SW_CSW_ISSW' : 'ISSW_MQB',
      'SW_CURL' : '1',
      'SW_DAB_MRC' : '0',
      'SW_DEV_ACCESS' : '1',
      'SW_DEV_TUNEABLE_WIFI_ADAPTATION_TIMER' : '1',
      'SW_DIAGNOSIS_PLATFORM' : 'CNS_MQB',
      'SW_DM_VERITY' : '0',
      'SW_DOWNGRADE_PROTECTION' : '0',
      'SW_EARLY_PARKING_SOUND' : '0',
      'SW_ESD_FILE_PACKAGE' : 'CNS_MQB',
      'SW_EWS_CONFIGURATION' : 'NO_EWS',
      'SW_EXT_TV_TUNER_ETH' : '0',
      'SW_FIREWALL_CONFIG' : 'Config_MQB',
      'SW_HMI_BRAND' : 'vw',
      'SW_HMI_PROJECT' : 'MQB',
      'SW_HMI_REGION' : 'cn',
      'SW_IPERF' : '1',
      'SW_MULTI_BACKEND_SUPPORT' : '1',
      'SW_NOTIFICATION_ONLINE_STATES' : '0',
      'SW_PING' : '1',
      'SW_POS_OCU_SUPPORT' : '0',
      'SW_RADIO_CONFIGURATION' : 'CONFIG_VW',
      'SW_SECUREBOOT_KEY_SET' : 'cns3-mqb-dummy',
      'SW_SEC_KEY' : 'MQB_Fixed',
      'SW_SPEAKER_LOCALIZATION' : '0',
      'SW_SPEECH_ACTIVATION_CONTROL' : '0',
      'SW_TCPDUMP' : '1',
      'SW_TESTABILITY_SERVICE_ETHERNET' : '1',
      'SW_TRACING_ACTIVE' : '1',
      'SW_TUNER_SETUP_REGION' : 'TAIWAN',
      'SW_UPDATE_KEY' : 'Developer',
      'SW_WEB_APPS_AUDIO_BROWSER' : '0',
      'SW_WEB_APPS_AUDIO_NODE' : '0',
      'SW_WEB_APPS_IMPLEMENTATION' : '0',
      'SW_WEB_APPS_INITIAL_CONFIG' : '0',
      'Variant Info String' : 'FM3-S-NWBY4-HM-VW-MQB-PC',
      'Variant Name' : 'V02_ZR_PKW_AM_FM_HKGMAC_VW',
   },
  301003 : {
      'Brand' : 'VOLKSWAGEN',
      'Container Name' : 'VW_TW',
      'HW_DISPLAY_VARIANT' : '1280640',
      'HW_ETC_EXTERNAL' : '0',
      'HW_GPS' : '1',
      'HW_MATCH' : {'31': ['9', '10', '11', '12', '13', '14']},
      'HW_RAM_VARIANT' : '6',
      'MU Type' : 'T',
      'Map Variant' : 'TW',
      'Part Number' : '3GB.035.877',
      'Region' : 'TAIWAN',
      'SW_A2B' : '0',
      'SW_A2B_MICROPHONES' : '0',
      'SW_ACOUSTICAL_FEEDBACK_CONTROLLER' : '0',
      'SW_AETH_PLATFORM' : 'MQB',
      'SW_BUS_MONITOR' : '1',
      'SW_CAN_PLATFORM' : 'MQB',
      'SW_CIF_DSI' : 'DSI_MQB',
      'SW_CIF_RSI' : 'RSI_MQB',
      'SW_CIF_RSI_SERVICE_REGISTRY_ADDRESS' : '127.0.0.1:443',
      'SW_CSW_ISSW' : 'ISSW_MQB',
      'SW_CURL' : '1',
      'SW_DAB_MRC' : '0',
      'SW_DEV_ACCESS' : '1',
      'SW_DEV_TUNEABLE_WIFI_ADAPTATION_TIMER' : '1',
      'SW_DIAGNOSIS_PLATFORM' : 'CNS_MQB',
      'SW_DM_VERITY' : '0',
      'SW_DOWNGRADE_PROTECTION' : '0',
      'SW_EARLY_PARKING_SOUND' : '0',
      'SW_ESD_FILE_PACKAGE' : 'CNS_MQB',
      'SW_EWS_CONFIGURATION' : 'NO_EWS',
      'SW_EXT_TV_TUNER_ETH' : '0',
      'SW_FIREWALL_CONFIG' : 'Config_MQB',
      'SW_HMI_BRAND' : 'vw',
      'SW_HMI_PROJECT' : 'MQB',
      'SW_HMI_REGION' : 'tw',
      'SW_IPERF' : '1',
      'SW_MULTI_BACKEND_SUPPORT' : '1',
      'SW_NOTIFICATION_ONLINE_STATES' : '0',
      'SW_PING' : '1',
      'SW_POS_OCU_SUPPORT' : '1',
      'SW_RADIO_CONFIGURATION' : 'CONFIG_VW',
      'SW_SECUREBOOT_KEY_SET' : 'cns3-mqb-dummy',
      'SW_SEC_KEY' : 'MQB_Fixed',
      'SW_SPEAKER_LOCALIZATION' : '0',
      'SW_SPEECH_ACTIVATION_CONTROL' : '0',
      'SW_TCPDUMP' : '1',
      'SW_TESTABILITY_SERVICE_ETHERNET' : '1',
      'SW_TRACING_ACTIVE' : '1',
      'SW_TUNER_SETUP_REGION' : 'TAIWAN',
      'SW_UPDATE_KEY' : 'Developer',
      'SW_WEB_APPS_AUDIO_BROWSER' : '0',
      'SW_WEB_APPS_AUDIO_NODE' : '0',
      'SW_WEB_APPS_IMPLEMENTATION' : '0',
      'SW_WEB_APPS_INITIAL_CONFIG' : '0',
      'Variant Info String' : 'FM3-S-NWBY4-TW-VW-MQB-PC',
      'Variant Name' : 'V03_ZR_PKW_AM_FM_Taiwan_VW',
   },
  301004 : {
      'Brand' : 'SKODA',
      'Container Name' : 'SK_TW',
      'HW_DISPLAY_VARIANT' : '1280640',
      'HW_ETC_EXTERNAL' : '0',
      'HW_GPS' : '1',
      'HW_MATCH' : {'31': ['9', '10', '11', '12', '13', '14']},
      'HW_RAM_VARIANT' : '6',
      'MU Type' : 'T',
      'Map Variant' : 'TW',
      'Part Number' : '3VD.035.877',
      'Region' : 'TAIWAN',
      'SW_A2B' : '0',
      'SW_A2B_MICROPHONES' : '0',
      'SW_ACOUSTICAL_FEEDBACK_CONTROLLER' : '0',
      'SW_AETH_PLATFORM' : 'MQB',
      'SW_BUS_MONITOR' : '1',
      'SW_CAN_PLATFORM' : 'MQB',
      'SW_CIF_DSI' : 'DSI_MQB',
      'SW_CIF_RSI' : 'RSI_MQB',
      'SW_CIF_RSI_SERVICE_REGISTRY_ADDRESS' : '127.0.0.1:443',
      'SW_CSW_ISSW' : 'ISSW_MQB',
      'SW_CURL' : '1',
      'SW_DAB_MRC' : '0',
      'SW_DEV_ACCESS' : '1',
      'SW_DEV_TUNEABLE_WIFI_ADAPTATION_TIMER' : '1',
      'SW_DIAGNOSIS_PLATFORM' : 'CNS_MQB',
      'SW_DM_VERITY' : '0',
      'SW_DOWNGRADE_PROTECTION' : '0',
      'SW_EARLY_PARKING_SOUND' : '0',
      'SW_ESD_FILE_PACKAGE' : 'CNS_MQB',
      'SW_EWS_CONFIGURATION' : 'NO_EWS',
      'SW_EXT_TV_TUNER_ETH' : '0',
      'SW_FIREWALL_CONFIG' : 'Config_MQB',
      'SW_HMI_BRAND' : 'sk',
      'SW_HMI_PROJECT' : 'MQB',
      'SW_HMI_REGION' : 'tw',
      'SW_IPERF' : '1',
      'SW_MULTI_BACKEND_SUPPORT' : '1',
      'SW_NOTIFICATION_ONLINE_STATES' : '0',
      'SW_PING' : '1',
      'SW_POS_OCU_SUPPORT' : '1',
      'SW_RADIO_CONFIGURATION' : 'CONFIG_SK',
      'SW_SECUREBOOT_KEY_SET' : 'cns3-mqb-dummy',
      'SW_SEC_KEY' : 'MQB_Fixed',
      'SW_SPEAKER_LOCALIZATION' : '0',
      'SW_SPEECH_ACTIVATION_CONTROL' : '0',
      'SW_TCPDUMP' : '1',
      'SW_TESTABILITY_SERVICE_ETHERNET' : '1',
      'SW_TRACING_ACTIVE' : '1',
      'SW_TUNER_SETUP_REGION' : 'TAIWAN',
      'SW_UPDATE_KEY' : 'Developer',
      'SW_WEB_APPS_AUDIO_BROWSER' : '0',
      'SW_WEB_APPS_AUDIO_NODE' : '0',
      'SW_WEB_APPS_IMPLEMENTATION' : '0',
      'SW_WEB_APPS_INITIAL_CONFIG' : '0',
      'Variant Info String' : 'FM3-S-NWBY4-TW-SK-MQB-PC',
      'Variant Name' : 'V04_ZR_PKW_AM_FM_Taiwan_SK',
   },
  301005 : {
      'Brand' : 'SKODA',
      'Container Name' : 'SK_CHN',
      'HW_DISPLAY_VARIANT' : '1280640',
      'HW_ETC_EXTERNAL' : '0',
      'HW_GPS' : '0',
      'HW_MATCH' : {'35': ['9', '10', '11', '12', '13', '14']},
      'HW_RAM_VARIANT' : '6',
      'MU Type' : 'C',
      'Map Variant' : 'CHN',
      'Part Number' : '3VD.035.866',
      'Region' : 'CHINA',
      'SW_A2B' : '0',
      'SW_A2B_MICROPHONES' : '0',
      'SW_ACOUSTICAL_FEEDBACK_CONTROLLER' : '0',
      'SW_AETH_PLATFORM' : 'MQB',
      'SW_BUS_MONITOR' : '1',
      'SW_CAN_PLATFORM' : 'MQB',
      'SW_CIF_DSI' : 'DSI_MQB',
      'SW_CIF_RSI' : 'RSI_MQB',
      'SW_CIF_RSI_SERVICE_REGISTRY_ADDRESS' : '127.0.0.1:443',
      'SW_CSW_ISSW' : 'ISSW_MQB',
      'SW_CURL' : '1',
      'SW_DAB_MRC' : '0',
      'SW_DEV_ACCESS' : '1',
      'SW_DEV_TUNEABLE_WIFI_ADAPTATION_TIMER' : '1',
      'SW_DIAGNOSIS_PLATFORM' : 'CNS_MQB',
      'SW_DM_VERITY' : '0',
      'SW_DOWNGRADE_PROTECTION' : '0',
      'SW_EARLY_PARKING_SOUND' : '0',
      'SW_ESD_FILE_PACKAGE' : 'CNS_MQB',
      'SW_EWS_CONFIGURATION' : 'NO_EWS',
      'SW_EXT_TV_TUNER_ETH' : '0',
      'SW_FIREWALL_CONFIG' : 'Config_MQB',
      'SW_HMI_BRAND' : 'sk',
      'SW_HMI_PROJECT' : 'MQB',
      'SW_HMI_REGION' : 'cn',
      'SW_IPERF' : '1',
      'SW_MULTI_BACKEND_SUPPORT' : '1',
      'SW_NOTIFICATION_ONLINE_STATES' : '0',
      'SW_PING' : '1',
      'SW_POS_OCU_SUPPORT' : '1',
      'SW_RADIO_CONFIGURATION' : 'CONFIG_SK',
      'SW_SECUREBOOT_KEY_SET' : 'cns3-mqb-dummy',
      'SW_SEC_KEY' : 'MQB_Fixed',
      'SW_SPEAKER_LOCALIZATION' : '0',
      'SW_SPEECH_ACTIVATION_CONTROL' : '0',
      'SW_TCPDUMP' : '1',
      'SW_TESTABILITY_SERVICE_ETHERNET' : '1',
      'SW_TRACING_ACTIVE' : '1',
      'SW_TUNER_SETUP_REGION' : 'CHINA',
      'SW_UPDATE_KEY' : 'Developer',
      'SW_WEB_APPS_AUDIO_BROWSER' : '0',
      'SW_WEB_APPS_AUDIO_NODE' : '0',
      'SW_WEB_APPS_IMPLEMENTATION' : 'Version_0',
      'SW_WEB_APPS_INITIAL_CONFIG' : 'SK',
      'Variant Info String' : 'FM3-S-NWBY4-CN-SK-MQB-PC',
      'Variant Name' : 'V05_ZR_PKW_AM_FM_China_SK',
   },
  311001 : {
      'Brand' : 'S_VOLKSWAGEN',
      'Container Name' : 'VW_CHN_sec',
      'HW_DISPLAY_VARIANT' : '1280640',
      'HW_ETC_EXTERNAL' : '0',
      'HW_GPS' : '0',
      'HW_MATCH' : {'35': ['9', '10', '11', '12', '13', '14']},
      'HW_RAM_VARIANT' : '6',
      'MU Type' : '0',
      'Map Variant' : 'CHN',
      'Part Number' : '3GB.035.866',
      'Region' : 'CHINA',
      'SW_A2B' : '0',
      'SW_A2B_MICROPHONES' : '0',
      'SW_ACOUSTICAL_FEEDBACK_CONTROLLER' : '0',
      'SW_AETH_PLATFORM' : 'MQB',
      'SW_BUS_MONITOR' : '0',
      'SW_CAN_PLATFORM' : 'MQB',
      'SW_CIF_DSI' : 'DSI_MQB',
      'SW_CIF_RSI' : 'RSI_MQB',
      'SW_CIF_RSI_SERVICE_REGISTRY_ADDRESS' : '127.0.0.1:443',
      'SW_CSW_ISSW' : 'ISSW_MQB',
      'SW_CURL' : '0',
      'SW_DAB_MRC' : '0',
      'SW_DEV_ACCESS' : '0',
      'SW_DEV_TUNEABLE_WIFI_ADAPTATION_TIMER' : '0',
      'SW_DIAGNOSIS_PLATFORM' : 'CNS_MQB',
      'SW_DM_VERITY' : '1',
      'SW_DOWNGRADE_PROTECTION' : '1',
      'SW_EARLY_PARKING_SOUND' : '0',
      'SW_ESD_FILE_PACKAGE' : 'CNS_MQB',
      'SW_EWS_CONFIGURATION' : 'NO_EWS',
      'SW_EXT_TV_TUNER_ETH' : '0',
      'SW_FIREWALL_CONFIG' : 'Config_MQB',
      'SW_HMI_BRAND' : 'vw',
      'SW_HMI_PROJECT' : 'MQB',
      'SW_HMI_REGION' : 'cn',
      'SW_IPERF' : '0',
      'SW_MULTI_BACKEND_SUPPORT' : '0',
      'SW_NOTIFICATION_ONLINE_STATES' : '0',
      'SW_PING' : '0',
      'SW_POS_OCU_SUPPORT' : '1',
      'SW_RADIO_CONFIGURATION' : 'CONFIG_VW',
      'SW_SECUREBOOT_KEY_SET' : 'cns3-mqb-sop1',
      'SW_SEC_KEY' : 'MQB_Variable',
      'SW_SPEAKER_LOCALIZATION' : '0',
      'SW_SPEECH_ACTIVATION_CONTROL' : '0',
      'SW_TCPDUMP' : '0',
      'SW_TESTABILITY_SERVICE_ETHERNET' : '0',
      'SW_TRACING_ACTIVE' : '0',
      'SW_TUNER_SETUP_REGION' : 'CHINA',
      'SW_UPDATE_KEY' : 'Customer',
      'SW_WEB_APPS_AUDIO_BROWSER' : '0',
      'SW_WEB_APPS_AUDIO_NODE' : '0',
      'SW_WEB_APPS_IMPLEMENTATION' : 'Version_0',
      'SW_WEB_APPS_INITIAL_CONFIG' : 'VW',
      'Variant Info String' : 'FM3-S-NWBY4-CN-VW-MQB-PC',
      'Variant Name' : 'V01_ZR_PKW_AM_FM_China_SVW_FAWVW',
   },
  311002 : {
      'Brand' : 'VOLKSWAGEN',
      'Container Name' : 'VW_HM_sec',
      'HW_DISPLAY_VARIANT' : '1280640',
      'HW_ETC_EXTERNAL' : '0',
      'HW_GPS' : '1',
      'HW_MATCH' : {'31': ['9', '10', '11', '12', '13', '14']},
      'HW_RAM_VARIANT' : '6',
      'MU Type' : '0',
      'Map Variant' : 'CHN',
      'Part Number' : '3GB.035.864',
      'Region' : 'HONGKONG_MACAO',
      'SW_A2B' : '0',
      'SW_A2B_MICROPHONES' : '0',
      'SW_ACOUSTICAL_FEEDBACK_CONTROLLER' : '0',
      'SW_AETH_PLATFORM' : 'MQB',
      'SW_BUS_MONITOR' : '0',
      'SW_CAN_PLATFORM' : 'MQB',
      'SW_CIF_DSI' : 'DSI_MQB',
      'SW_CIF_RSI' : 'RSI_MQB',
      'SW_CIF_RSI_SERVICE_REGISTRY_ADDRESS' : '127.0.0.1:443',
      'SW_CSW_ISSW' : 'ISSW_MQB',
      'SW_CURL' : '0',
      'SW_DAB_MRC' : '0',
      'SW_DEV_ACCESS' : '0',
      'SW_DEV_TUNEABLE_WIFI_ADAPTATION_TIMER' : '0',
      'SW_DIAGNOSIS_PLATFORM' : 'CNS_MQB',
      'SW_DM_VERITY' : '1',
      'SW_DOWNGRADE_PROTECTION' : '1',
      'SW_EARLY_PARKING_SOUND' : '0',
      'SW_ESD_FILE_PACKAGE' : 'CNS_MQB',
      'SW_EWS_CONFIGURATION' : 'NO_EWS',
      'SW_EXT_TV_TUNER_ETH' : '0',
      'SW_FIREWALL_CONFIG' : 'Config_MQB',
      'SW_HMI_BRAND' : 'vw',
      'SW_HMI_PROJECT' : 'MQB',
      'SW_HMI_REGION' : 'cn',
      'SW_IPERF' : '0',
      'SW_MULTI_BACKEND_SUPPORT' : '0',
      'SW_NOTIFICATION_ONLINE_STATES' : '0',
      'SW_PING' : '0',
      'SW_POS_OCU_SUPPORT' : '0',
      'SW_RADIO_CONFIGURATION' : 'CONFIG_VW',
      'SW_SECUREBOOT_KEY_SET' : 'cns3-mqb-sop1',
      'SW_SEC_KEY' : 'MQB_Variable',
      'SW_SPEAKER_LOCALIZATION' : '0',
      'SW_SPEECH_ACTIVATION_CONTROL' : '0',
      'SW_TCPDUMP' : '0',
      'SW_TESTABILITY_SERVICE_ETHERNET' : '0',
      'SW_TRACING_ACTIVE' : '0',
      'SW_TUNER_SETUP_REGION' : 'TAIWAN',
      'SW_UPDATE_KEY' : 'Customer',
      'SW_WEB_APPS_AUDIO_BROWSER' : '0',
      'SW_WEB_APPS_AUDIO_NODE' : '0',
      'SW_WEB_APPS_IMPLEMENTATION' : '0',
      'SW_WEB_APPS_INITIAL_CONFIG' : '0',
      'Variant Info String' : 'FM3-S-NWBY4-HM-VW-MQB-PC',
      'Variant Name' : 'V02_ZR_PKW_AM_FM_HKGMAC_VW',
   },
  311003 : {
      'Brand' : 'VOLKSWAGEN',
      'Container Name' : 'VW_TW_sec',
      'HW_DISPLAY_VARIANT' : '1280640',
      'HW_ETC_EXTERNAL' : '0',
      'HW_GPS' : '1',
      'HW_MATCH' : {'31': ['9', '10', '11', '12', '13', '14']},
      'HW_RAM_VARIANT' : '6',
      'MU Type' : '0',
      'Map Variant' : 'TW',
      'Part Number' : '3GB.035.877',
      'Region' : 'TAIWAN',
      'SW_A2B' : '0',
      'SW_A2B_MICROPHONES' : '0',
      'SW_ACOUSTICAL_FEEDBACK_CONTROLLER' : '0',
      'SW_AETH_PLATFORM' : 'MQB',
      'SW_BUS_MONITOR' : '0',
      'SW_CAN_PLATFORM' : 'MQB',
      'SW_CIF_DSI' : 'DSI_MQB',
      'SW_CIF_RSI' : 'RSI_MQB',
      'SW_CIF_RSI_SERVICE_REGISTRY_ADDRESS' : '127.0.0.1:443',
      'SW_CSW_ISSW' : 'ISSW_MQB',
      'SW_CURL' : '0',
      'SW_DAB_MRC' : '0',
      'SW_DEV_ACCESS' : '0',
      'SW_DEV_TUNEABLE_WIFI_ADAPTATION_TIMER' : '0',
      'SW_DIAGNOSIS_PLATFORM' : 'CNS_MQB',
      'SW_DM_VERITY' : '1',
      'SW_DOWNGRADE_PROTECTION' : '1',
      'SW_EARLY_PARKING_SOUND' : '0',
      'SW_ESD_FILE_PACKAGE' : 'CNS_MQB',
      'SW_EWS_CONFIGURATION' : 'NO_EWS',
      'SW_EXT_TV_TUNER_ETH' : '0',
      'SW_FIREWALL_CONFIG' : 'Config_MQB',
      'SW_HMI_BRAND' : 'vw',
      'SW_HMI_PROJECT' : 'MQB',
      'SW_HMI_REGION' : 'tw',
      'SW_IPERF' : '0',
      'SW_MULTI_BACKEND_SUPPORT' : '0',
      'SW_NOTIFICATION_ONLINE_STATES' : '0',
      'SW_PING' : '0',
      'SW_POS_OCU_SUPPORT' : '1',
      'SW_RADIO_CONFIGURATION' : 'CONFIG_VW',
      'SW_SECUREBOOT_KEY_SET' : 'cns3-mqb-sop1',
      'SW_SEC_KEY' : 'MQB_Variable',
      'SW_SPEAKER_LOCALIZATION' : '0',
      'SW_SPEECH_ACTIVATION_CONTROL' : '0',
      'SW_TCPDUMP' : '0',
      'SW_TESTABILITY_SERVICE_ETHERNET' : '0',
      'SW_TRACING_ACTIVE' : '0',
      'SW_TUNER_SETUP_REGION' : 'TAIWAN',
      'SW_UPDATE_KEY' : 'Customer',
      'SW_WEB_APPS_AUDIO_BROWSER' : '0',
      'SW_WEB_APPS_AUDIO_NODE' : '0',
      'SW_WEB_APPS_IMPLEMENTATION' : '0',
      'SW_WEB_APPS_INITIAL_CONFIG' : '0',
      'Variant Info String' : 'FM3-S-NWBY4-TW-VW-MQB-PC',
      'Variant Name' : 'V03_ZR_PKW_AM_FM_Taiwan_VW',
   },
  311004 : {
      'Brand' : 'SKODA',
      'Container Name' : 'SK_TW_sec',
      'HW_DISPLAY_VARIANT' : '1280640',
      'HW_ETC_EXTERNAL' : '0',
      'HW_GPS' : '1',
      'HW_MATCH' : {'31': ['9', '10', '11', '12', '13', '14']},
      'HW_RAM_VARIANT' : '6',
      'MU Type' : '0',
      'Map Variant' : 'TW',
      'Part Number' : '3VD.035.877',
      'Region' : 'TAIWAN',
      'SW_A2B' : '0',
      'SW_A2B_MICROPHONES' : '0',
      'SW_ACOUSTICAL_FEEDBACK_CONTROLLER' : '0',
      'SW_AETH_PLATFORM' : 'MQB',
      'SW_BUS_MONITOR' : '0',
      'SW_CAN_PLATFORM' : 'MQB',
      'SW_CIF_DSI' : 'DSI_MQB',
      'SW_CIF_RSI' : 'RSI_MQB',
      'SW_CIF_RSI_SERVICE_REGISTRY_ADDRESS' : '127.0.0.1:443',
      'SW_CSW_ISSW' : 'ISSW_MQB',
      'SW_CURL' : '0',
      'SW_DAB_MRC' : '0',
      'SW_DEV_ACCESS' : '0',
      'SW_DEV_TUNEABLE_WIFI_ADAPTATION_TIMER' : '0',
      'SW_DIAGNOSIS_PLATFORM' : 'CNS_MQB',
      'SW_DM_VERITY' : '1',
      'SW_DOWNGRADE_PROTECTION' : '1',
      'SW_EARLY_PARKING_SOUND' : '0',
      'SW_ESD_FILE_PACKAGE' : 'CNS_MQB',
      'SW_EWS_CONFIGURATION' : 'NO_EWS',
      'SW_EXT_TV_TUNER_ETH' : '0',
      'SW_FIREWALL_CONFIG' : 'Config_MQB',
      'SW_HMI_BRAND' : 'sk',
      'SW_HMI_PROJECT' : 'MQB',
      'SW_HMI_REGION' : 'tw',
      'SW_IPERF' : '0',
      'SW_MULTI_BACKEND_SUPPORT' : '0',
      'SW_NOTIFICATION_ONLINE_STATES' : '0',
      'SW_PING' : '0',
      'SW_POS_OCU_SUPPORT' : '1',
      'SW_RADIO_CONFIGURATION' : 'CONFIG_SK',
      'SW_SECUREBOOT_KEY_SET' : 'cns3-mqb-sop1',
      'SW_SEC_KEY' : 'MQB_Variable',
      'SW_SPEAKER_LOCALIZATION' : '0',
      'SW_SPEECH_ACTIVATION_CONTROL' : '0',
      'SW_TCPDUMP' : '0',
      'SW_TESTABILITY_SERVICE_ETHERNET' : '0',
      'SW_TRACING_ACTIVE' : '0',
      'SW_TUNER_SETUP_REGION' : 'TAIWAN',
      'SW_UPDATE_KEY' : 'Customer',
      'SW_WEB_APPS_AUDIO_BROWSER' : '0',
      'SW_WEB_APPS_AUDIO_NODE' : '0',
      'SW_WEB_APPS_IMPLEMENTATION' : '0',
      'SW_WEB_APPS_INITIAL_CONFIG' : '0',
      'Variant Info String' : 'FM3-S-NWBY4-TW-SK-MQB-PC',
      'Variant Name' : 'V04_ZR_PKW_AM_FM_Taiwan_SK',
   },
  311005 : {
      'Brand' : 'SKODA',
      'Container Name' : 'SK_CHN_sec',
      'HW_DISPLAY_VARIANT' : '1280640',
      'HW_ETC_EXTERNAL' : '0',
      'HW_GPS' : '0',
      'HW_MATCH' : {'35': ['9', '10', '11', '12', '13', '14']},
      'HW_RAM_VARIANT' : '6',
      'MU Type' : '0',
      'Map Variant' : 'CHN',
      'Part Number' : '3VD.035.866',
      'Region' : 'CHINA',
      'SW_A2B' : '0',
      'SW_A2B_MICROPHONES' : '0',
      'SW_ACOUSTICAL_FEEDBACK_CONTROLLER' : '0',
      'SW_AETH_PLATFORM' : 'MQB',
      'SW_BUS_MONITOR' : '0',
      'SW_CAN_PLATFORM' : 'MQB',
      'SW_CIF_DSI' : 'DSI_MQB',
      'SW_CIF_RSI' : 'RSI_MQB',
      'SW_CIF_RSI_SERVICE_REGISTRY_ADDRESS' : '127.0.0.1:443',
      'SW_CSW_ISSW' : 'ISSW_MQB',
      'SW_CURL' : '0',
      'SW_DAB_MRC' : '0',
      'SW_DEV_ACCESS' : '0',
      'SW_DEV_TUNEABLE_WIFI_ADAPTATION_TIMER' : '0',
      'SW_DIAGNOSIS_PLATFORM' : 'CNS_MQB',
      'SW_DM_VERITY' : '1',
      'SW_DOWNGRADE_PROTECTION' : '1',
      'SW_EARLY_PARKING_SOUND' : '0',
      'SW_ESD_FILE_PACKAGE' : 'CNS_MQB',
      'SW_EWS_CONFIGURATION' : 'NO_EWS',
      'SW_EXT_TV_TUNER_ETH' : '0',
      'SW_FIREWALL_CONFIG' : 'Config_MQB',
      'SW_HMI_BRAND' : 'sk',
      'SW_HMI_PROJECT' : 'MQB',
      'SW_HMI_REGION' : 'cn',
      'SW_IPERF' : '0',
      'SW_MULTI_BACKEND_SUPPORT' : '0',
      'SW_NOTIFICATION_ONLINE_STATES' : '0',
      'SW_PING' : '0',
      'SW_POS_OCU_SUPPORT' : '1',
      'SW_RADIO_CONFIGURATION' : 'CONFIG_SK',
      'SW_SECUREBOOT_KEY_SET' : 'cns3-mqb-sop1',
      'SW_SEC_KEY' : 'MQB_Variable',
      'SW_SPEAKER_LOCALIZATION' : '0',
      'SW_SPEECH_ACTIVATION_CONTROL' : '0',
      'SW_TCPDUMP' : '0',
      'SW_TESTABILITY_SERVICE_ETHERNET' : '0',
      'SW_TRACING_ACTIVE' : '0',
      'SW_TUNER_SETUP_REGION' : 'CHINA',
      'SW_UPDATE_KEY' : 'Customer',
      'SW_WEB_APPS_AUDIO_BROWSER' : '0',
      'SW_WEB_APPS_AUDIO_NODE' : '0',
      'SW_WEB_APPS_IMPLEMENTATION' : 'Version_0',
      'SW_WEB_APPS_INITIAL_CONFIG' : 'SK',
      'Variant Info String' : 'FM3-S-NWBY4-CN-SK-MQB-PC',
      'Variant Name' : 'V05_ZR_PKW_AM_FM_China_SK',
   },
  701001 : {
      'Brand' : 'S_VOLKSWAGEN',
      'Container Name' : '37W-VW_CHN',
      'HW_DISPLAY_VARIANT' : '1560700',
      'HW_ETC_EXTERNAL' : '0',
      'HW_GPS' : '0',
      'HW_MATCH' : {'36': ['12', '13', '14']},
      'HW_RAM_VARIANT' : '6',
      'MU Type' : 'C',
      'Map Variant' : 'CHN',
      'Part Number' : '5HG.035.866',
      'Region' : 'CHINA',
      'SW_A2B' : '1',
      'SW_A2B_MICROPHONES' : '1',
      'SW_ACOUSTICAL_FEEDBACK_CONTROLLER' : '1',
      'SW_AETH_PLATFORM' : 'MQB2020',
      'SW_BUS_MONITOR' : '1',
      'SW_CAN_PLATFORM' : 'MQB2020',
      'SW_CIF_DSI' : 'DSI_37W',
      'SW_CIF_RSI' : 'RSI_37W',
      'SW_CIF_RSI_SERVICE_REGISTRY_ADDRESS' : '127.0.0.1:443',
      'SW_CSW_ISSW' : 'ISSW_37W',
      'SW_CURL' : '1',
      'SW_DAB_MRC' : '0',
      'SW_DEV_ACCESS' : '1',
      'SW_DEV_TUNEABLE_WIFI_ADAPTATION_TIMER' : '1',
      'SW_DIAGNOSIS_PLATFORM' : 'CNS_MQB2020',
      'SW_DM_VERITY' : '0',
      'SW_DOWNGRADE_PROTECTION' : '0',
      'SW_EARLY_PARKING_SOUND' : '1',
      'SW_ESD_FILE_PACKAGE' : 'CNS_37W',
      'SW_EWS_CONFIGURATION' : 'NO_EWS',
      'SW_EXT_TV_TUNER_ETH' : '0',
      'SW_FIREWALL_CONFIG' : 'Config_37W',
      'SW_HMI_BRAND' : 'vw',
      'SW_HMI_PROJECT' : '37W',
      'SW_HMI_REGION' : 'cn',
      'SW_IPERF' : '1',
      'SW_MULTI_BACKEND_SUPPORT' : '1',
      'SW_NOTIFICATION_ONLINE_STATES' : '0',
      'SW_PING' : '1',
      'SW_POS_OCU_SUPPORT' : '0',
      'SW_RADIO_CONFIGURATION' : 'CONFIG_VW',
      'SW_SECUREBOOT_KEY_SET' : 'cns3-mqb-dummy',
      'SW_SEC_KEY' : 'MQ2_Fixed',
      'SW_SPEAKER_LOCALIZATION' : '1',
      'SW_SPEECH_ACTIVATION_CONTROL' : '1',
      'SW_TCPDUMP' : '1',
      'SW_TESTABILITY_SERVICE_ETHERNET' : '1',
      'SW_TRACING_ACTIVE' : '1',
      'SW_TUNER_SETUP_REGION' : 'CHINA',
      'SW_UPDATE_KEY' : 'Developer',
      'SW_WEB_APPS_AUDIO_BROWSER' : '1',
      'SW_WEB_APPS_AUDIO_NODE' : '1',
      'SW_WEB_APPS_IMPLEMENTATION' : 'Version_1',
      'SW_WEB_APPS_INITIAL_CONFIG' : 'VW',
      'Variant Info String' : 'FM3-S-NWBY4-CN-VW-MQ2-PC',
      'Variant Name' : 'V01_ZR_PKW_AM_FM_China_Online',
   },
  701002 : {
      'Brand' : 'VOLKSWAGEN',
      'Container Name' : '37W-VW_HM',
      'HW_DISPLAY_VARIANT' : '1560700',
      'HW_ETC_EXTERNAL' : '0',
      'HW_GPS' : '1',
      'HW_MATCH' : {'32': ['13', '14']},
      'HW_RAM_VARIANT' : '6',
      'MU Type' : 'H',
      'Map Variant' : 'CHN',
      'Part Number' : '5HG.035.864',
      'Region' : 'HONGKONG_MACAO',
      'SW_A2B' : '1',
      'SW_A2B_MICROPHONES' : '1',
      'SW_ACOUSTICAL_FEEDBACK_CONTROLLER' : '1',
      'SW_AETH_PLATFORM' : 'MQB2020',
      'SW_BUS_MONITOR' : '1',
      'SW_CAN_PLATFORM' : 'MQB2020',
      'SW_CIF_DSI' : 'DSI_37W',
      'SW_CIF_RSI' : 'RSI_37W',
      'SW_CIF_RSI_SERVICE_REGISTRY_ADDRESS' : '127.0.0.1:443',
      'SW_CSW_ISSW' : 'ISSW_37W',
      'SW_CURL' : '1',
      'SW_DAB_MRC' : '0',
      'SW_DEV_ACCESS' : '1',
      'SW_DEV_TUNEABLE_WIFI_ADAPTATION_TIMER' : '1',
      'SW_DIAGNOSIS_PLATFORM' : 'CNS_MQB2020',
      'SW_DM_VERITY' : '0',
      'SW_DOWNGRADE_PROTECTION' : '0',
      'SW_EARLY_PARKING_SOUND' : '1',
      'SW_ESD_FILE_PACKAGE' : 'CNS_37W',
      'SW_EWS_CONFIGURATION' : 'NO_EWS',
      'SW_EXT_TV_TUNER_ETH' : '0',
      'SW_FIREWALL_CONFIG' : 'Config_37W',
      'SW_HMI_BRAND' : 'vw',
      'SW_HMI_PROJECT' : '37W',
      'SW_HMI_REGION' : 'cn',
      'SW_IPERF' : '1',
      'SW_MULTI_BACKEND_SUPPORT' : '1',
      'SW_NOTIFICATION_ONLINE_STATES' : '0',
      'SW_PING' : '1',
      'SW_POS_OCU_SUPPORT' : '0',
      'SW_RADIO_CONFIGURATION' : 'CONFIG_VW',
      'SW_SECUREBOOT_KEY_SET' : 'cns3-mqb-dummy',
      'SW_SEC_KEY' : 'MQ2_Fixed',
      'SW_SPEAKER_LOCALIZATION' : '1',
      'SW_SPEECH_ACTIVATION_CONTROL' : '1',
      'SW_TCPDUMP' : '1',
      'SW_TESTABILITY_SERVICE_ETHERNET' : '1',
      'SW_TRACING_ACTIVE' : '1',
      'SW_TUNER_SETUP_REGION' : 'TAIWAN',
      'SW_UPDATE_KEY' : 'Developer',
      'SW_WEB_APPS_AUDIO_BROWSER' : '0',
      'SW_WEB_APPS_AUDIO_NODE' : '0',
      'SW_WEB_APPS_IMPLEMENTATION' : '0',
      'SW_WEB_APPS_INITIAL_CONFIG' : '0',
      'Variant Info String' : 'FM3-S-NWBY4-HM-VW-MQ2-PC',
      'Variant Name' : 'V02_ZR_PKW_AM_FM_HongKongMacao_Offline',
   },
  701003 : {
      'Brand' : 'VOLKSWAGEN',
      'Container Name' : '37W-VW_TW',
      'HW_DISPLAY_VARIANT' : '1560700',
      'HW_ETC_EXTERNAL' : '0',
      'HW_GPS' : '1',
      'HW_MATCH' : {'32': ['13', '14']},
      'HW_RAM_VARIANT' : '6',
      'MU Type' : 'T',
      'Map Variant' : 'TW',
      'Part Number' : '5HG.035.877',
      'Region' : 'TAIWAN',
      'SW_A2B' : '1',
      'SW_A2B_MICROPHONES' : '1',
      'SW_ACOUSTICAL_FEEDBACK_CONTROLLER' : '1',
      'SW_AETH_PLATFORM' : 'MQB2020',
      'SW_BUS_MONITOR' : '1',
      'SW_CAN_PLATFORM' : 'MQB2020',
      'SW_CIF_DSI' : 'DSI_37W',
      'SW_CIF_RSI' : 'RSI_37W',
      'SW_CIF_RSI_SERVICE_REGISTRY_ADDRESS' : '127.0.0.1:443',
      'SW_CSW_ISSW' : 'ISSW_37W',
      'SW_CURL' : '1',
      'SW_DAB_MRC' : '0',
      'SW_DEV_ACCESS' : '1',
      'SW_DEV_TUNEABLE_WIFI_ADAPTATION_TIMER' : '1',
      'SW_DIAGNOSIS_PLATFORM' : 'CNS_MQB2020',
      'SW_DM_VERITY' : '0',
      'SW_DOWNGRADE_PROTECTION' : '0',
      'SW_EARLY_PARKING_SOUND' : '1',
      'SW_ESD_FILE_PACKAGE' : 'CNS_37W',
      'SW_EWS_CONFIGURATION' : 'NO_EWS',
      'SW_EXT_TV_TUNER_ETH' : '0',
      'SW_FIREWALL_CONFIG' : 'Config_37W',
      'SW_HMI_BRAND' : 'vw',
      'SW_HMI_PROJECT' : '37W',
      'SW_HMI_REGION' : 'tw',
      'SW_IPERF' : '1',
      'SW_MULTI_BACKEND_SUPPORT' : '1',
      'SW_NOTIFICATION_ONLINE_STATES' : '0',
      'SW_PING' : '1',
      'SW_POS_OCU_SUPPORT' : '0',
      'SW_RADIO_CONFIGURATION' : 'CONFIG_VW',
      'SW_SECUREBOOT_KEY_SET' : 'cns3-mqb-dummy',
      'SW_SEC_KEY' : 'MQ2_Fixed',
      'SW_SPEAKER_LOCALIZATION' : '1',
      'SW_SPEECH_ACTIVATION_CONTROL' : '1',
      'SW_TCPDUMP' : '1',
      'SW_TESTABILITY_SERVICE_ETHERNET' : '1',
      'SW_TRACING_ACTIVE' : '1',
      'SW_TUNER_SETUP_REGION' : 'TAIWAN',
      'SW_UPDATE_KEY' : 'Developer',
      'SW_WEB_APPS_AUDIO_BROWSER' : '0',
      'SW_WEB_APPS_AUDIO_NODE' : '0',
      'SW_WEB_APPS_IMPLEMENTATION' : '0',
      'SW_WEB_APPS_INITIAL_CONFIG' : '0',
      'Variant Info String' : 'FM3-S-NWBY4-TW-VW-MQ2-PC',
      'Variant Name' : 'V03_ZR_PKW_AM_FM_Taiwan_Offline',
   },
  701004 : {
      'Brand' : 'SKODA',
      'Container Name' : '37W-SK_CHN',
      'HW_DISPLAY_VARIANT' : '1560700',
      'HW_ETC_EXTERNAL' : '0',
      'HW_GPS' : '0',
      'HW_MATCH' : {'36': ['13', '14']},
      'HW_RAM_VARIANT' : '6',
      'MU Type' : 'C',
      'Map Variant' : 'CHN',
      'Part Number' : '5DD.035.866',
      'Region' : 'CHINA',
      'SW_A2B' : '1',
      'SW_A2B_MICROPHONES' : '1',
      'SW_ACOUSTICAL_FEEDBACK_CONTROLLER' : '1',
      'SW_AETH_PLATFORM' : 'MQB2020',
      'SW_BUS_MONITOR' : '1',
      'SW_CAN_PLATFORM' : 'MQB2020',
      'SW_CIF_DSI' : 'DSI_37W',
      'SW_CIF_RSI' : 'RSI_37W',
      'SW_CIF_RSI_SERVICE_REGISTRY_ADDRESS' : '127.0.0.1:443',
      'SW_CSW_ISSW' : 'ISSW_37W',
      'SW_CURL' : '1',
      'SW_DAB_MRC' : '0',
      'SW_DEV_ACCESS' : '1',
      'SW_DEV_TUNEABLE_WIFI_ADAPTATION_TIMER' : '1',
      'SW_DIAGNOSIS_PLATFORM' : 'CNS_MQB2020',
      'SW_DM_VERITY' : '0',
      'SW_DOWNGRADE_PROTECTION' : '0',
      'SW_EARLY_PARKING_SOUND' : '1',
      'SW_ESD_FILE_PACKAGE' : 'CNS_37W',
      'SW_EWS_CONFIGURATION' : 'NO_EWS',
      'SW_EXT_TV_TUNER_ETH' : '0',
      'SW_FIREWALL_CONFIG' : 'Config_37W',
      'SW_HMI_BRAND' : 'sk',
      'SW_HMI_PROJECT' : '37W',
      'SW_HMI_REGION' : 'cn',
      'SW_IPERF' : '1',
      'SW_MULTI_BACKEND_SUPPORT' : '1',
      'SW_NOTIFICATION_ONLINE_STATES' : '0',
      'SW_PING' : '1',
      'SW_POS_OCU_SUPPORT' : '0',
      'SW_RADIO_CONFIGURATION' : 'CONFIG_SK',
      'SW_SECUREBOOT_KEY_SET' : 'cns3-mqb-dummy',
      'SW_SEC_KEY' : 'MQ2_Fixed',
      'SW_SPEAKER_LOCALIZATION' : '1',
      'SW_SPEECH_ACTIVATION_CONTROL' : '1',
      'SW_TCPDUMP' : '1',
      'SW_TESTABILITY_SERVICE_ETHERNET' : '1',
      'SW_TRACING_ACTIVE' : '1',
      'SW_TUNER_SETUP_REGION' : 'CHINA',
      'SW_UPDATE_KEY' : 'Developer',
      'SW_WEB_APPS_AUDIO_BROWSER' : '1',
      'SW_WEB_APPS_AUDIO_NODE' : '1',
      'SW_WEB_APPS_IMPLEMENTATION' : 'Version_1',
      'SW_WEB_APPS_INITIAL_CONFIG' : 'SK',
      'Variant Info String' : 'FM3-S-NWBY4-CN-SK-MQ2-PC',
      'Variant Name' : 'V04_ZR_PKW_AM_FM_China_Online_SK',
   },
  701005 : {
      'Brand' : 'SKODA',
      'Container Name' : '37W-SK_TW',
      'HW_DISPLAY_VARIANT' : '1560700',
      'HW_ETC_EXTERNAL' : '0',
      'HW_GPS' : '1',
      'HW_MATCH' : {'32': ['13', '14']},
      'HW_RAM_VARIANT' : '6',
      'MU Type' : 'T',
      'Map Variant' : 'TW',
      'Part Number' : '5DD.035.877',
      'Region' : 'TAIWAN',
      'SW_A2B' : '1',
      'SW_A2B_MICROPHONES' : '1',
      'SW_ACOUSTICAL_FEEDBACK_CONTROLLER' : '1',
      'SW_AETH_PLATFORM' : 'MQB2020',
      'SW_BUS_MONITOR' : '1',
      'SW_CAN_PLATFORM' : 'MQB2020',
      'SW_CIF_DSI' : 'DSI_37W',
      'SW_CIF_RSI' : 'RSI_37W',
      'SW_CIF_RSI_SERVICE_REGISTRY_ADDRESS' : '127.0.0.1:443',
      'SW_CSW_ISSW' : 'ISSW_37W',
      'SW_CURL' : '1',
      'SW_DAB_MRC' : '0',
      'SW_DEV_ACCESS' : '1',
      'SW_DEV_TUNEABLE_WIFI_ADAPTATION_TIMER' : '1',
      'SW_DIAGNOSIS_PLATFORM' : 'CNS_MQB2020',
      'SW_DM_VERITY' : '0',
      'SW_DOWNGRADE_PROTECTION' : '0',
      'SW_EARLY_PARKING_SOUND' : '1',
      'SW_ESD_FILE_PACKAGE' : 'CNS_37W',
      'SW_EWS_CONFIGURATION' : 'NO_EWS',
      'SW_EXT_TV_TUNER_ETH' : '0',
      'SW_FIREWALL_CONFIG' : 'Config_37W',
      'SW_HMI_BRAND' : 'sk',
      'SW_HMI_PROJECT' : '37W',
      'SW_HMI_REGION' : 'tw',
      'SW_IPERF' : '1',
      'SW_MULTI_BACKEND_SUPPORT' : '1',
      'SW_NOTIFICATION_ONLINE_STATES' : '0',
      'SW_PING' : '1',
      'SW_POS_OCU_SUPPORT' : '0',
      'SW_RADIO_CONFIGURATION' : 'CONFIG_SK',
      'SW_SECUREBOOT_KEY_SET' : 'cns3-mqb-dummy',
      'SW_SEC_KEY' : 'MQ2_Fixed',
      'SW_SPEAKER_LOCALIZATION' : '1',
      'SW_SPEECH_ACTIVATION_CONTROL' : '1',
      'SW_TCPDUMP' : '1',
      'SW_TESTABILITY_SERVICE_ETHERNET' : '1',
      'SW_TRACING_ACTIVE' : '1',
      'SW_TUNER_SETUP_REGION' : 'TAIWAN',
      'SW_UPDATE_KEY' : 'Developer',
      'SW_WEB_APPS_AUDIO_BROWSER' : '0',
      'SW_WEB_APPS_AUDIO_NODE' : '0',
      'SW_WEB_APPS_IMPLEMENTATION' : '0',
      'SW_WEB_APPS_INITIAL_CONFIG' : '0',
      'Variant Info String' : 'FM3-S-NWBY4-TW-SK-MQ2-PC',
      'Variant Name' : 'V05_ZR_PKW_AM_FM_Taiwan_Offline_SK',
   },
  711001 : {
      'Brand' : 'S_VOLKSWAGEN',
      'Container Name' : '37W-VW_CHN_sec',
      'HW_DISPLAY_VARIANT' : '1560700',
      'HW_ETC_EXTERNAL' : '0',
      'HW_GPS' : '0',
      'HW_MATCH' : {'36': ['12', '13', '14']},
      'HW_RAM_VARIANT' : '6',
      'MU Type' : '0',
      'Map Variant' : 'CHN',
      'Part Number' : '5HG.035.866',
      'Region' : 'CHINA',
      'SW_A2B' : '1',
      'SW_A2B_MICROPHONES' : '1',
      'SW_ACOUSTICAL_FEEDBACK_CONTROLLER' : '1',
      'SW_AETH_PLATFORM' : 'MQB2020',
      'SW_BUS_MONITOR' : '0',
      'SW_CAN_PLATFORM' : 'MQB2020',
      'SW_CIF_DSI' : 'DSI_37W',
      'SW_CIF_RSI' : 'RSI_37W',
      'SW_CIF_RSI_SERVICE_REGISTRY_ADDRESS' : '127.0.0.1:443',
      'SW_CSW_ISSW' : 'ISSW_37W',
      'SW_CURL' : '0',
      'SW_DAB_MRC' : '0',
      'SW_DEV_ACCESS' : '0',
      'SW_DEV_TUNEABLE_WIFI_ADAPTATION_TIMER' : '0',
      'SW_DIAGNOSIS_PLATFORM' : 'CNS_MQB2020',
      'SW_DM_VERITY' : '1',
      'SW_DOWNGRADE_PROTECTION' : '1',
      'SW_EARLY_PARKING_SOUND' : '1',
      'SW_ESD_FILE_PACKAGE' : 'CNS_37W',
      'SW_EWS_CONFIGURATION' : 'NO_EWS',
      'SW_EXT_TV_TUNER_ETH' : '0',
      'SW_FIREWALL_CONFIG' : 'Config_37W',
      'SW_HMI_BRAND' : 'vw',
      'SW_HMI_PROJECT' : '37W',
      'SW_HMI_REGION' : 'cn',
      'SW_IPERF' : '0',
      'SW_MULTI_BACKEND_SUPPORT' : '0',
      'SW_NOTIFICATION_ONLINE_STATES' : '0',
      'SW_PING' : '0',
      'SW_POS_OCU_SUPPORT' : '0',
      'SW_RADIO_CONFIGURATION' : 'CONFIG_VW',
      'SW_SECUREBOOT_KEY_SET' : 'cns3-mqb-sop1',
      'SW_SEC_KEY' : 'MQ2_Variable',
      'SW_SPEAKER_LOCALIZATION' : '1',
      'SW_SPEECH_ACTIVATION_CONTROL' : '1',
      'SW_TCPDUMP' : '0',
      'SW_TESTABILITY_SERVICE_ETHERNET' : '0',
      'SW_TRACING_ACTIVE' : '0',
      'SW_TUNER_SETUP_REGION' : 'CHINA',
      'SW_UPDATE_KEY' : 'Customer',
      'SW_WEB_APPS_AUDIO_BROWSER' : '1',
      'SW_WEB_APPS_AUDIO_NODE' : '1',
      'SW_WEB_APPS_IMPLEMENTATION' : 'Version_1',
      'SW_WEB_APPS_INITIAL_CONFIG' : 'VW',
      'Variant Info String' : 'FM3-S-NWBY4-CN-VW-MQ2-PC',
      'Variant Name' : 'V01_ZR_PKW_AM_FM_China_Online',
   },
  711002 : {
      'Brand' : 'VOLKSWAGEN',
      'Container Name' : '37W-VW_HM_sec',
      'HW_DISPLAY_VARIANT' : '1560700',
      'HW_ETC_EXTERNAL' : '0',
      'HW_GPS' : '1',
      'HW_MATCH' : {'32': ['13', '14']},
      'HW_RAM_VARIANT' : '6',
      'MU Type' : '0',
      'Map Variant' : 'CHN',
      'Part Number' : '5HG.035.864',
      'Region' : 'HONGKONG_MACAO',
      'SW_A2B' : '1',
      'SW_A2B_MICROPHONES' : '1',
      'SW_ACOUSTICAL_FEEDBACK_CONTROLLER' : '1',
      'SW_AETH_PLATFORM' : 'MQB2020',
      'SW_BUS_MONITOR' : '0',
      'SW_CAN_PLATFORM' : 'MQB2020',
      'SW_CIF_DSI' : 'DSI_37W',
      'SW_CIF_RSI' : 'RSI_37W',
      'SW_CIF_RSI_SERVICE_REGISTRY_ADDRESS' : '127.0.0.1:443',
      'SW_CSW_ISSW' : 'ISSW_37W',
      'SW_CURL' : '0',
      'SW_DAB_MRC' : '0',
      'SW_DEV_ACCESS' : '0',
      'SW_DEV_TUNEABLE_WIFI_ADAPTATION_TIMER' : '0',
      'SW_DIAGNOSIS_PLATFORM' : 'CNS_MQB2020',
      'SW_DM_VERITY' : '1',
      'SW_DOWNGRADE_PROTECTION' : '1',
      'SW_EARLY_PARKING_SOUND' : '1',
      'SW_ESD_FILE_PACKAGE' : 'CNS_37W',
      'SW_EWS_CONFIGURATION' : 'NO_EWS',
      'SW_EXT_TV_TUNER_ETH' : '0',
      'SW_FIREWALL_CONFIG' : 'Config_37W',
      'SW_HMI_BRAND' : 'vw',
      'SW_HMI_PROJECT' : '37W',
      'SW_HMI_REGION' : 'cn',
      'SW_IPERF' : '0',
      'SW_MULTI_BACKEND_SUPPORT' : '0',
      'SW_NOTIFICATION_ONLINE_STATES' : '0',
      'SW_PING' : '0',
      'SW_POS_OCU_SUPPORT' : '0',
      'SW_RADIO_CONFIGURATION' : 'CONFIG_VW',
      'SW_SECUREBOOT_KEY_SET' : 'cns3-mqb-sop1',
      'SW_SEC_KEY' : 'MQ2_Variable',
      'SW_SPEAKER_LOCALIZATION' : '1',
      'SW_SPEECH_ACTIVATION_CONTROL' : '1',
      'SW_TCPDUMP' : '0',
      'SW_TESTABILITY_SERVICE_ETHERNET' : '0',
      'SW_TRACING_ACTIVE' : '0',
      'SW_TUNER_SETUP_REGION' : 'TAIWAN',
      'SW_UPDATE_KEY' : 'Customer',
      'SW_WEB_APPS_AUDIO_BROWSER' : '0',
      'SW_WEB_APPS_AUDIO_NODE' : '0',
      'SW_WEB_APPS_IMPLEMENTATION' : '0',
      'SW_WEB_APPS_INITIAL_CONFIG' : '0',
      'Variant Info String' : 'FM3-S-NWBY4-HM-VW-MQ2-PC',
      'Variant Name' : 'V02_ZR_PKW_AM_FM_HongKongMacao_Offline',
   },
  711003 : {
      'Brand' : 'VOLKSWAGEN',
      'Container Name' : '37W-VW_TW_sec',
      'HW_DISPLAY_VARIANT' : '1560700',
      'HW_ETC_EXTERNAL' : '0',
      'HW_GPS' : '1',
      'HW_MATCH' : {'32': ['13', '14']},
      'HW_RAM_VARIANT' : '6',
      'MU Type' : '0',
      'Map Variant' : 'TW',
      'Part Number' : '5HG.035.877',
      'Region' : 'TAIWAN',
      'SW_A2B' : '1',
      'SW_A2B_MICROPHONES' : '1',
      'SW_ACOUSTICAL_FEEDBACK_CONTROLLER' : '1',
      'SW_AETH_PLATFORM' : 'MQB2020',
      'SW_BUS_MONITOR' : '0',
      'SW_CAN_PLATFORM' : 'MQB2020',
      'SW_CIF_DSI' : 'DSI_37W',
      'SW_CIF_RSI' : 'RSI_37W',
      'SW_CIF_RSI_SERVICE_REGISTRY_ADDRESS' : '127.0.0.1:443',
      'SW_CSW_ISSW' : 'ISSW_37W',
      'SW_CURL' : '0',
      'SW_DAB_MRC' : '0',
      'SW_DEV_ACCESS' : '0',
      'SW_DEV_TUNEABLE_WIFI_ADAPTATION_TIMER' : '0',
      'SW_DIAGNOSIS_PLATFORM' : 'CNS_MQB2020',
      'SW_DM_VERITY' : '1',
      'SW_DOWNGRADE_PROTECTION' : '1',
      'SW_EARLY_PARKING_SOUND' : '1',
      'SW_ESD_FILE_PACKAGE' : 'CNS_37W',
      'SW_EWS_CONFIGURATION' : 'NO_EWS',
      'SW_EXT_TV_TUNER_ETH' : '0',
      'SW_FIREWALL_CONFIG' : 'Config_37W',
      'SW_HMI_BRAND' : 'vw',
      'SW_HMI_PROJECT' : '37W',
      'SW_HMI_REGION' : 'tw',
      'SW_IPERF' : '0',
      'SW_MULTI_BACKEND_SUPPORT' : '0',
      'SW_NOTIFICATION_ONLINE_STATES' : '0',
      'SW_PING' : '0',
      'SW_POS_OCU_SUPPORT' : '0',
      'SW_RADIO_CONFIGURATION' : 'CONFIG_VW',
      'SW_SECUREBOOT_KEY_SET' : 'cns3-mqb-sop1',
      'SW_SEC_KEY' : 'MQ2_Variable',
      'SW_SPEAKER_LOCALIZATION' : '1',
      'SW_SPEECH_ACTIVATION_CONTROL' : '1',
      'SW_TCPDUMP' : '0',
      'SW_TESTABILITY_SERVICE_ETHERNET' : '0',
      'SW_TRACING_ACTIVE' : '0',
      'SW_TUNER_SETUP_REGION' : 'TAIWAN',
      'SW_UPDATE_KEY' : 'Customer',
      'SW_WEB_APPS_AUDIO_BROWSER' : '0',
      'SW_WEB_APPS_AUDIO_NODE' : '0',
      'SW_WEB_APPS_IMPLEMENTATION' : '0',
      'SW_WEB_APPS_INITIAL_CONFIG' : '0',
      'Variant Info String' : 'FM3-S-NWBY4-TW-VW-MQ2-PC',
      'Variant Name' : 'V03_ZR_PKW_AM_FM_Taiwan_Offline',
   },
  711004 : {
      'Brand' : 'SKODA',
      'Container Name' : '37W-SK_CHN_sec',
      'HW_DISPLAY_VARIANT' : '1560700',
      'HW_ETC_EXTERNAL' : '0',
      'HW_GPS' : '0',
      'HW_MATCH' : {'36': ['13', '14']},
      'HW_RAM_VARIANT' : '6',
      'MU Type' : '0',
      'Map Variant' : 'CHN',
      'Part Number' : '5DD.035.866',
      'Region' : 'CHINA',
      'SW_A2B' : '1',
      'SW_A2B_MICROPHONES' : '1',
      'SW_ACOUSTICAL_FEEDBACK_CONTROLLER' : '1',
      'SW_AETH_PLATFORM' : 'MQB2020',
      'SW_BUS_MONITOR' : '0',
      'SW_CAN_PLATFORM' : 'MQB2020',
      'SW_CIF_DSI' : 'DSI_37W',
      'SW_CIF_RSI' : 'RSI_37W',
      'SW_CIF_RSI_SERVICE_REGISTRY_ADDRESS' : '127.0.0.1:443',
      'SW_CSW_ISSW' : 'ISSW_37W',
      'SW_CURL' : '0',
      'SW_DAB_MRC' : '0',
      'SW_DEV_ACCESS' : '0',
      'SW_DEV_TUNEABLE_WIFI_ADAPTATION_TIMER' : '0',
      'SW_DIAGNOSIS_PLATFORM' : 'CNS_MQB2020',
      'SW_DM_VERITY' : '1',
      'SW_DOWNGRADE_PROTECTION' : '1',
      'SW_EARLY_PARKING_SOUND' : '1',
      'SW_ESD_FILE_PACKAGE' : 'CNS_37W',
      'SW_EWS_CONFIGURATION' : 'NO_EWS',
      'SW_EXT_TV_TUNER_ETH' : '0',
      'SW_FIREWALL_CONFIG' : 'Config_37W',
      'SW_HMI_BRAND' : 'sk',
      'SW_HMI_PROJECT' : '37W',
      'SW_HMI_REGION' : 'cn',
      'SW_IPERF' : '0',
      'SW_MULTI_BACKEND_SUPPORT' : '0',
      'SW_NOTIFICATION_ONLINE_STATES' : '0',
      'SW_PING' : '0',
      'SW_POS_OCU_SUPPORT' : '0',
      'SW_RADIO_CONFIGURATION' : 'CONFIG_SK',
      'SW_SECUREBOOT_KEY_SET' : 'cns3-mqb-sop1',
      'SW_SEC_KEY' : 'MQ2_Variable',
      'SW_SPEAKER_LOCALIZATION' : '1',
      'SW_SPEECH_ACTIVATION_CONTROL' : '1',
      'SW_TCPDUMP' : '0',
      'SW_TESTABILITY_SERVICE_ETHERNET' : '0',
      'SW_TRACING_ACTIVE' : '0',
      'SW_TUNER_SETUP_REGION' : 'CHINA',
      'SW_UPDATE_KEY' : 'Customer',
      'SW_WEB_APPS_AUDIO_BROWSER' : '1',
      'SW_WEB_APPS_AUDIO_NODE' : '1',
      'SW_WEB_APPS_IMPLEMENTATION' : 'Version_1',
      'SW_WEB_APPS_INITIAL_CONFIG' : 'SK',
      'Variant Info String' : 'FM3-S-NWBY4-CN-SK-MQ2-PC',
      'Variant Name' : 'V04_ZR_PKW_AM_FM_China_Online_SK',
   },
  711005 : {
      'Brand' : 'SKODA',
      'Container Name' : '37W-SK_TW_sec',
      'HW_DISPLAY_VARIANT' : '1560700',
      'HW_ETC_EXTERNAL' : '0',
      'HW_GPS' : '1',
      'HW_MATCH' : {'32': ['13', '14']},
      'HW_RAM_VARIANT' : '6',
      'MU Type' : '0',
      'Map Variant' : 'TW',
      'Part Number' : '5DD.035.877',
      'Region' : 'TAIWAN',
      'SW_A2B' : '1',
      'SW_A2B_MICROPHONES' : '1',
      'SW_ACOUSTICAL_FEEDBACK_CONTROLLER' : '1',
      'SW_AETH_PLATFORM' : 'MQB2020',
      'SW_BUS_MONITOR' : '0',
      'SW_CAN_PLATFORM' : 'MQB2020',
      'SW_CIF_DSI' : 'DSI_37W',
      'SW_CIF_RSI' : 'RSI_37W',
      'SW_CIF_RSI_SERVICE_REGISTRY_ADDRESS' : '127.0.0.1:443',
      'SW_CSW_ISSW' : 'ISSW_37W',
      'SW_CURL' : '0',
      'SW_DAB_MRC' : '0',
      'SW_DEV_ACCESS' : '0',
      'SW_DEV_TUNEABLE_WIFI_ADAPTATION_TIMER' : '0',
      'SW_DIAGNOSIS_PLATFORM' : 'CNS_MQB2020',
      'SW_DM_VERITY' : '1',
      'SW_DOWNGRADE_PROTECTION' : '1',
      'SW_EARLY_PARKING_SOUND' : '1',
      'SW_ESD_FILE_PACKAGE' : 'CNS_37W',
      'SW_EWS_CONFIGURATION' : 'NO_EWS',
      'SW_EXT_TV_TUNER_ETH' : '0',
      'SW_FIREWALL_CONFIG' : 'Config_37W',
      'SW_HMI_BRAND' : 'sk',
      'SW_HMI_PROJECT' : '37W',
      'SW_HMI_REGION' : 'tw',
      'SW_IPERF' : '0',
      'SW_MULTI_BACKEND_SUPPORT' : '0',
      'SW_NOTIFICATION_ONLINE_STATES' : '0',
      'SW_PING' : '0',
      'SW_POS_OCU_SUPPORT' : '0',
      'SW_RADIO_CONFIGURATION' : 'CONFIG_SK',
      'SW_SECUREBOOT_KEY_SET' : 'cns3-mqb-sop1',
      'SW_SEC_KEY' : 'MQ2_Variable',
      'SW_SPEAKER_LOCALIZATION' : '1',
      'SW_SPEECH_ACTIVATION_CONTROL' : '1',
      'SW_TCPDUMP' : '0',
      'SW_TESTABILITY_SERVICE_ETHERNET' : '0',
      'SW_TRACING_ACTIVE' : '0',
      'SW_TUNER_SETUP_REGION' : 'TAIWAN',
      'SW_UPDATE_KEY' : 'Customer',
      'SW_WEB_APPS_AUDIO_BROWSER' : '0',
      'SW_WEB_APPS_AUDIO_NODE' : '0',
      'SW_WEB_APPS_IMPLEMENTATION' : '0',
      'SW_WEB_APPS_INITIAL_CONFIG' : '0',
      'Variant Info String' : 'FM3-S-NWBY4-TW-SK-MQ2-PC',
      'Variant Name' : 'V05_ZR_PKW_AM_FM_Taiwan_Offline_SK',
   },
}


def getBrand(args, **kwargs):
    """
    Get Brand

    Returns the Brand for a single system variant.

    Parameters
    ----------
    arg1: string
        System variant string (e.g. '100101')

    Returns
    -------
    string
        Brand (e.g 'VW')
    """
    return variants[int(args[0])]['Brand']

def getRegion(args, **kwargs):
    """
    Get Region

    Returns the Region for a single system variant.

    Parameters
    ----------
    arg1: string
        System variant string (e.g. '100101')

    Returns
    -------
    string
        Region (e.g 'EU')
    """
    return variants[int(args[0])]['Region']

def getFeature(args, **kwargs):
    """
    Get Feature value

    Returns the value of a feature for a single system variant.

    Parameters
    ----------
    arg1: string
        System variant string (e.g. '100101')
    arg2: string
        Feature-Key (e.g. 'SW_HMI_REGION)

    Returns
    -------
    string
        corresponding value (e.g 'EU')
    """
    return variants[int(args[0])][args[1]]

def getUniqueFeatureFromList(args, **kwargs):
    """
    Get Feature value

    Returns the value of a feature for a list of system variants.
    Raises an Error, if different features are defined.

    Parameters
    ----------
    arg1: string
        Comma separated list of System variant strings (e.g.
        '100101,100102,100103')
    arg2: string
        Feature-Key (e.g. 'SW_HMI_REGION)

    Returns
    -------
    string
        corresponding value (e.g 'EU')
    """
    try:
        Features=[]
        for v in args[0].split(','):
           Features.append(variants[int(v)][args[1]])
        if len(set(Features)) == 1:
            return Features[0]
        else:
            raise ParseError("ERROR: multiple features defined for system variant " + str(Features))
    except IndexError as e:
        raise ParseError("Index Error: " + str(e) + " Args:" + str(args))
    except KeyError as e:
        raise ParseError("Key Error: " + str(e) + " Args:" + str(args))
    return "False"

def getVariantInfoString(args, **kwargs):
    """
    Get Variant Info String

    Returns the variant info string for a single system variant.

    Parameters
    ----------
    arg1: string
        System variant string (e.g. '100101')

    Returns
    -------
    string
        Variant Info String (e.g 'FM3-SM-NWBY4-EU-VW-MQB-PC')
    """
    return variants[int(args[0])]['Variant Info String']

def getProjectNo(args, **kwargs):
    '''
    Get Project number related to https://wiki-automotive.server.technisat-digital/x/4wj-Gg

    Parameters
    ----------
    arg1: list of string
        System variant string (e.g. ['100101'])
        Attention: Uses just the first item in list!

    Returns
    -------
    integer
        1 - for PCC MQB
        2 - for PCC 37W
        3 - for CNS
        4 - for LG MQB
        5 - for LG 37W
        6 - for ICAS MEB
    '''
    # reuse this implementation of genVariants.py -> system_variant_info()
    # TODO think about to generate this system number from flag an query a flag here!
    project=int(str(args[0])[:-5])
    return project

def flagIsSet(args,**kwargs):
    """
    Test if a flag is set in a list of system variants.

    These function can be used to select the packages which need to be
    build for a update container.

    Parameters
    ----------
    arg1: string
        Comma separated list of System variant strings (e.g.
        '100101,100102,100103')
    arg2: string
        Name of the flag.
    arg3: string
        Value of the flag.

    Returns
    -------
    string
        True or False
    """

    try:
       for v in args[0].split(','):
          if variants[int(v)][args[1]] == args[2]:
             return "True"
    except IndexError as e:
        raise ParseError("Index Error: " + str(e) + " Args:" + str(args))
    except KeyError as e:
        raise ParseError("Key Error: " + str(e) + " Args:" + str(args))
    return "False"

# arg's: flag=value
def getMatchingVariantStrings(args, **kwargs):
    """
    Get matching varinat strings

    Get a comma seperated list of variant info strings where the flag
    matches some value. This returns a list of all known system varinats.
    The mib3-minfest generatur will filter them out when building the
    release container for a smaller subset of variants.

    These function can be used to add variant informations in a swupdate
    package recipe.

    Parameters
    ----------
    args: string
        Key=Value pair of Flags which should be set in the variant.

    Returns
    -------
    string
        Comma seperated list of variant strings
    """

    ret = ''
    for variantid in sorted(variants.keys()):
       variant = variants[variantid]
       try:
         match = True
         for f in args:
            (flag,sep,value) = f.partition("=")
            if sep != '=':
               raise ParseError("Error: malformed check! " + f)
            regex = re.compile(value)
            _value = variant.get(flag,None)
            if _value is None:
               match=False
            else:
               if not regex.match(_value):
                  match=False
         if match and not variant.get('Variant Info String') in ret:
            ret += variant.get('Variant Info String') + ','
       except IndexError as e:
          raise ParseError("Index Error: " + str(e) + " Args:" + str(args))
       except KeyError as e:
          raise ParseError("Key Error: " + str(e) + " Args:" + str(args))
    return ret[:-1]

# get a list of variant Flags for given Systemvariants
# arg: comma seperated list of systemvariant ID's
# arg: Flags
def queryVariantFlags(args, **kwargs):
    """
    Query for variant flags

    Get a comma seperated list of variant flags for a comma separated
    list of system variants.

    Parameters
    ----------
    arg1: string
        Comma separated list of system variant ID's.
    args: string
        Variant flag

    Returns
    -------
    string
        comma seperated key=value pair for each variant delimited by semi-colon prefixed by systemvariant
        e.g. queryVariantFlags('100104,100116,100119',SW_HMI_REGION,SW_HMI_BRAND) will return:
        100104:SW_HMI_REGION=eu,SW_HMI_BRAND=vw;100116:SW_HMI_REGION=kr,SW_HMI_BRAND=vw;100119:SW_HMI_REGION=tw,SW_HMI_BRAND=vw
    """

    ret = ''
    v = [v for v in args[0].split(',') if v != '']
    for _v in v:
       try:
          variant = variants[int(_v)]
          ret += _v + ':'
          for flag in args[1:]:
             # dictionaries are transfered to bash arrays
             #'HW_MATCH' : {'33': ['9'], '7': ['5', '6', '7', '8']},
             if type(variant[flag]) is dict:
                 ret += flag + '=('
                 for k,v in sorted(variant[flag].items()):
                     ret += '[' + k + ']="'
                     if type(v) is list:
                        ret += ",".join(map(str,v))
                     else:
                        ret += v
                     ret += '" '
                 ret += ')#'
             else:
                ret += flag + '=' + variant[flag] +'#'
          ret = ret[:-1] + ';'
       except IndexError as e:
          raise ParseError("Index Error: " + str(e) + " Args:" + str(args))
       except KeyError as e:
          raise ParseError("Key Error: " + str(e) + " Args:" + str(args))
    return ret[:-1]
manifest = {
    'apiVersion' : "0.2",
    'stringFunctions' : {
        "flagIsSet" : flagIsSet,
        "getBrand" : getBrand,
        "getRegion" : getRegion,
        "getFeature" : getFeature,
        "getUniqueFeatureFromList" : getUniqueFeatureFromList,
        "getVariantInfoString" : getVariantInfoString,
        "getMatchingVariantStrings" : getMatchingVariantStrings,
        "queryVariantFlags" : queryVariantFlags
    }
}