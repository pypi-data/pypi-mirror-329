Watermeter plugin for Juham™
=============================

Description
-----------

A web camera and AI-based water meter solution for Juham™ home automation.

This package includes two different water meter implementations:

* Tesseract OCR and OpenCV solution for reading and interpreting water meter digits.
  This class requires further work to be truly useful. My Raspberry Pi didn't have enough disk
  space, so I decided to set this aside for now.

* A simple class that compares subsequent images to measure differences. The greater the difference between images,
  the more the arrows and digits on the water meter have changed, indicating water consumption.
  This solution also uploads the images to a specified FTP site when water consumption is detected,
  allowing homeowners to inspect the water meter visually. While this solution doesn’t provide exact water
  consumption readings, it is highly reliable for detecting leaks. Just ensure that spiders or other potentially moving
  objects don't obstruct the camera's view of the water meter.  
  

.. image:: _static/images/watermeter_diff.png
   :alt: Web camera based water meter leak detector based on comparison of subsequent images
   :width: 640px
   :align: center  


Getting Started
---------------

### Installation

1. Prerequisities

In order to use the first solution you need Tesseract OCR to read the digits. To install Tesseract:

.. code-block:: bash

      sudo apt install tesseract-ocr

If you are on Windows, visit the Tesseract GitHub repository, or Download a precompiled Windows binary from UB Mannheim.

2. Install 

   .. code-block:: bash

      pip install juham_watermeter


2. Configure

To adjust update interval and other attributes edit `WaterMeter.json` configuration file.

