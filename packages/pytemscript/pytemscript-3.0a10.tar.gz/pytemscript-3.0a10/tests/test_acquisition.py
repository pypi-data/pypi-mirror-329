import argparse
import logging
from typing import Optional, List
import numpy as np
import math

from pytemscript.microscope import Microscope
from pytemscript.utils.enums import *
from pytemscript.modules.extras import Image


def print_stats(image: Image,
                binning: int,
                exp_time: float,
                interactive: bool = False) -> None:
    """ Calculate statistics about the image and display it.
    :param image: Image object
    :param binning: Input binning
    :param exp_time: Input exposure time
    :param interactive: Show plot and other stats
    """
    img = image.data
    metadata = image.metadata

    print("Metadata: ", metadata)

    if 'TimeStamp' in metadata:
        assert int(metadata['Binning.Width']) == binning
        assert math.isclose(float(metadata['ExposureTime']), exp_time, abs_tol=0.01)

    assert img.shape[1] == metadata["width"]
    assert img.shape[0] == metadata["height"]

    if interactive:
        import matplotlib.pyplot as plt

        print("\tMean: ", np.mean(image.data))
        vmin = np.percentile(image.data, 3)
        vmax = np.percentile(image.data, 97)
        print("\tStdDev: ", np.std(image.data))

        logging.getLogger("matplotlib").setLevel(logging.INFO)

        plt.imshow(image.data, interpolation="nearest", cmap="gray",
                   vmin=vmin, vmax=vmax)
        print("\tStdDev: ", np.std(image.data))
        plt.colorbar()
        plt.suptitle(image.name)
        plt.ion()
        plt.show()
        plt.pause(1.0)


def camera_acquire(microscope: Microscope,
                   cam_name: str,
                   exp_time: float,
                   binning: int,
                   **kwargs) -> None:
    """ Acquire a test TEM image and check output metadata.
    :param microscope: Microscope object
    :param cam_name: Camera / detector name
    :param exp_time: Exposure time
    :param binning: Input binning
    :param kwargs: Keyword arguments
    """

    image = microscope.acquisition.acquire_tem_image(cam_name,
                                                     size=AcqImageSize.FULL,
                                                     exp_time=exp_time,
                                                     binning=binning,
                                                     **kwargs)
    if image is not None:
        print_stats(image, binning, exp_time)
        image.save(fn="test_image_%s.mrc" % cam_name, overwrite=True)
        image.save(fn="test_image_%s.tif" % cam_name, overwrite=True)


def detector_acquire(microscope: Microscope,
                     cam_name: str,
                     dwell_time: float,
                     binning: int,
                     **kwargs) -> None:
    """ Acquire a test STEM image.
    :param microscope: Microscope object
    :param cam_name: Camera / detector name
    :param dwell_time: Dwell time
    :param binning: Input binning
    :param kwargs: Keyword arguments
    """
    image = microscope.acquisition.acquire_stem_image(cam_name,
                                                      size=AcqImageSize.FULL,
                                                      dwell_time=dwell_time,
                                                      binning=binning,
                                                      **kwargs)
    print_stats(image, binning, dwell_time)
    image.save(fn="test_image_%s.tiff" % cam_name, overwrite=True)


def main(argv: Optional[List] = None) -> None:
    """ Testing acquisition functions. """
    parser = argparse.ArgumentParser(
        description="This test can use local or remote client. In the latter case "
                    "pytemscript-server must be already running",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-t", "--type", type=str,
                        choices=["direct", "socket", "zmq", "grpc"],
                        default="direct",
                        help="Connection type: direct, socket, zmq or grpc")
    parser.add_argument("-p", "--port", type=int, default=39000,
                        help="Specify port on which the server is listening")
    parser.add_argument("--host", type=str, default='127.0.0.1',
                        help="Specify host address on which the server is listening")
    parser.add_argument("-d", "--debug", dest="debug",
                        default=False, action='store_true',
                        help="Enable debug mode")
    args = parser.parse_args(argv)

    microscope = Microscope(connection=args.type, host=args.host,
                            port=args.port, debug=args.debug)

    print("Starting acquisition tests, connection: %s" % args.type)

    cameras = microscope.detectors.cameras
    print("Available detectors:\n", cameras)

    if "BM-Ceta" in cameras:
        camera_acquire(microscope, "BM-Ceta", exp_time=1, binning=2)
    if "BM-Falcon" in cameras:
        camera_acquire(microscope, "BM-Falcon", exp_time=0.5, binning=2)
        camera_acquire(microscope, "BM-Falcon", exp_time=3, binning=1,
                       align_image=True, electron_counting=True,
                       frame_ranges=[(1, 2), (2, 3)])

    if microscope.stem.is_available:
        microscope.stem.enable()
        detectors = microscope.detectors.stem_detectors
        if "BF" in detectors:
            detector_acquire(microscope, "BF", dwell_time=1e-5, binning=2)
        microscope.stem.disable()


if __name__ == '__main__':
    main()
