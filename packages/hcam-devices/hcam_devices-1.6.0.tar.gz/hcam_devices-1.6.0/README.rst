===============================
hcam_devices
===============================


.. image:: https://img.shields.io/pypi/v/hcam_devices.svg
        :target: https://pypi.python.org/pypi/hcam_devices

.. image:: https://img.shields.io/travis/StuartLittlefair/hcam_devices.svg
        :target: https://travis-ci.org/StuartLittlefair/hcam_devices

.. image:: https://readthedocs.org/projects/hcam-devices/badge/?version=latest
        :target: https://hcam-devices.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/StuartLittlefair/hcam_devices/shield.svg
     :target: https://pyup.io/repos/github/StuartLittlefair/hcam_devices/
     :alt: Updates


Hardware Communication for HiPERCAM

The HiPERCAM project necessitates communicating between numerous hardware components, distributed over
a network. ``hcam_devices`` provides a set of tools to allow devices on the network to run and communicate with each
other.

The architecture uses a central WAMP server (e.g. `crossbar <https://crossbar.io>`_) to handle communication
over websockets. Devices on the network publish telemetry regularly to the WAMP server, and any interested party
can subcribe to the telemetry topic to receive updates.

Devices can expose Remote Procedure Calls (RPCs) so that they may be controlled over the network, and also subscribe
to topics, so that settable attributes (e.g the temperature setpoint of a CCD) can be cpontrolled by publishing to those
topics.

Installation
------------

Install with the usual::

 pip install .

or if you don't have root access::

 pip install --user .

Usage
------

First of all, you will need a running WAMP server. I recommend `crossbar <https://crossbar.io>`_. A config file for a crossbar
instance is included with this package in the `data` directory. Once you have your WAMP server up and running, there are several
scripts that you can run.

hwserver
++++++++

This program runs the HiPERCAM peripheral hardware (e.g the CCD peltier controllers, focal plane slide, flow sensors etc).
Running this script will connect these devices to the WAMP server and allow monitoring and control

hwlogger
++++++++

So that the devices (especially the CCD heads) can be monitored off-site, this script subscribes to the CCD telemetry and saves
the hardware state to a persistent off-site `Influx <https://www.influxdata.com>`_ database. That database can be used with third
party tools like `grafana <https://grafana.com>`_ to enable neat dashboards for device monitoring.

hserver
++++++++

The NGC CCD controller is responsible for driving the CCDs, saving exposures etc. For maximum reliability and speed, this device
is connected to the WAMP server and controlled via it's own custom script, `hserver`.

gtcserver
+++++++++

Finally, the external GTC environment (Electronics racks, rotator, telescope offsets etc) are all connected to the WAMP server
using this script.

Control within python
+++++++++++++++++++++

Once these scripts are running, devices can be controlled in Python. This can be done using a WAMP library like `autobahn <https://autobahn.readthedocs.io/en/latest/>`_.
Alternatively, the WAMP server config included provides a simple HTTP interface that can be used as follows:

.. code-block:: python

    from hcam_devices.wamp.utils import call, publish

    # call RPCs
    ngc_status = call('hipercam.NGC.rpc.summary')
    call('hipercam.GTC.rpc.do_offset', raoff=0.05, decoff=0.001)

    # publish to a topic
    publish('hipercam.FocalPlaneSlide.target_position', -50)

Subscribing to device telemetry must be done using a WAMP library for now.

Optional package dependencies
-----------------------------

``hcam_devices`` supports several other tools, such as the finding chart tool ``hfinder`` and the
instrument control GUI ``hdriver``. Most users will need no extra modules installed. However,
If you want to be able to run ``hdriver``, *and* you want full communication with the telescope
whilst running at the GTC, you need to install the CORBA implementation ``omniORBpy``.

Full install instructions are found at the omniORB project `homepage <http://omniorb.sourceforge.net/>`_.
Be sure to install both omniORB and omniORBpy. Also, the omniORBpy module and the lib64 variant must
both be in the ``PYTHONPATH``. Finally, communicating with the GTC requires the installation of
Interface Definition Language (IDL) files, and the python modules compiled from them. Contact S. Littlefair
for these files, which must also be in the ``PYTHONPATH``.

* Free software: MIT license



