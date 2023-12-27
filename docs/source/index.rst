.. geographic-data-visualisation documentation master file, created by
   sphinx-quickstart on Mon Dec 27 10:27:45 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Air Pollution on Poland Map App documentation
============================================

This app visualise different types of gases responsible for air pollution on the Poland Map. You can choose 6 different gases to visualize their intensity
in different voivodeships: carbon dioxide, methane, nitrous oxide, sulfur dioxide, nitric oxide,carbon monoxide. The app includes app, panel to choose configuration
of data and panels to calculate the average over the years and in different areas.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Getting started
===============

To run the app you need to download whole github repository to which link is below.
Then install all the requirements from ``requirements.txt`` file in root catalog by doing the following:::

   pip install -r requirements.txt

Finally, run ``app.py`` in ```scr``` catalog using the command below: ::

   python app.py

and it generates the link which allows you to open the app in the browser.
The explanation of each function can be found at Github repository below each function in docstrings.

Links
==================

* Github repository: https://github.com/marczef/geographic-data-visualisation
* :ref:`search`