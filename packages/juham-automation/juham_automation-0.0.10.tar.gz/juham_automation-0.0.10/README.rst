Welcome to Juham™ - Juha's Ultimate Home Automation Masterpiece
================================================================

Project Description
-------------------

This package extends the ``juham_core`` package, providing home automation building blocks that cover most common needs.
It consists of two main sub-modules:

.. image:: _static/images/juham_automation.png
   :alt: Basic automation classes for optimizing energy consumption and minimizing electricity costs.
   :width: 640px
   :align: center  


- ``automation``

  * **spothintafi**: Acquires electricity prices in Finland.
  * **watercirculator**: Automates a water circulator pump based on hot water temperature and motion detection.
  * **hotwateroptimizer**: Controls hot water radiators based on temperature sensors and electricity price data.
  * **energycostcalculator**: Monitors power consumption and electricity prices, and computes the energy balance in euros.


- ``ts``

  * This folder contains time series recorders that listen for Juham™ topics and store the data in a time series database
    for later inspection.


Project Status
--------------

**Current State**: **Pre-Alpha (Status 2)**

All classes have been tested to some extent, and no known bugs have been reported. However, the code still requires work in
terms of design and robustness. For instance, electricity prices are currently hard-coded to use euros, but this should be
configurable to support multiple currencies.


Special Thanks
--------------

This project would not have been possible without the generous support of two exceptional individuals: Teppo K. and Mahi.

Teppo K. provided the initial spark for this project by donating a Raspberry Pi, a temperature sensor, and giving an inspiring
demonstration of his own home automation system—effectively dragging me down the rabbit hole of endless tinkering.

Mahi has been instrumental in translating my half-baked ideas into Python code, offering invaluable support and
encouragement—while also ensuring that every time I thought I was done, I wasn’t.

Because of these two gentlemen, my already minimal spare time dropped into the negatives as I desperately tried to push the
system to some semblance of professionalism.

I’m truly grateful to both—really. 😅
