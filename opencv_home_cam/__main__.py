import argparse
import traceback
import sys
import os
import cv2
import signal
import logging
import logging.config
from opencv_home_cam import OpenCvHomeCam, OpenCvHomeCamException

description = "OpenCV home cam. See README.rst for full documentation"


def signal_handler(signal, frame):

    global hcm

    sys.stderr.write('Signal received!')
    hcm.stop()


def load_options():

    global parsed_args
    parser = argparse.ArgumentParser(prog="opencv_home_cam",
                                     description=description)

    parser.add_argument('-c', '--config-file',
                        help="Configuraton file. Contains configuration "
                             "options for recording, detection and actions.")
    parser.add_argument('-l', '--log-config-file',
                        help="Logging configuraton file. This is the "
                             "configuration for the Python logging "
                             "facility. See the Python documentation "
                             "for more details.")

    parsed_args = parser.parse_args()


def main():
    global parsed_args
    global hcm
    load_options()
    hcm = None

    try:

        if not parsed_args.config_file:
            sys.stderr.write('Missing input config file\n')
            exit(1)

        if parsed_args.log_config_file:
            logging.config.fileConfig(parsed_args.log_config_file)
        else:
            sys.stderr.write("Missing logger configuration.\n"
                             "Default configuration will be used.\n")
            logging.basicConfig(stream=sys.stderr,
                                level=logging.DEBUG,
                                format='%(asctime)s %(message)s')

        logger = logging.getLogger(__name__)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        hcm = OpenCvHomeCam(config_file=parsed_args.config_file)

        hcm.start()
        logger.info("Waiting for OpenCvHomeCam to finish\n")
        hcm.wait()
        logger.info("OpenCvHomeCam finished\n")

    except IOError as err:
        sys.stderr.write('{}\n'.format(err))
    except OpenCvHomeCamException as err:
        sys.stderr.write('{}\n'.format(err))
    except:
        traceback.print_exc()

if __name__ == "__main__":
    main()
