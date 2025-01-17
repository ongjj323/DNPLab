======================
Introduction to DNPLab
======================

The aim of DNPLab is to provide a turn-key data processing environment for DNP-NMR data. The software package is entirely written in Python and no proprietary software is required.

DNPLab is published under the open-source MIT license.

In the following section, we introduce the intended workflow for processing DNP-NMR data with DNPLab. The DNPLab python package supports data formats of all major NMR platforms.

The general workflow is as follows:

1. Import DNP-NMR Data
2. Create Workspace
3. Process Data
4. Save Data in h5 Format
5. Further Processing and Data Analysis
6. Create Report

A key-feature of DNPLab is creating a workspace. The imported data is stored in a dnpdata object and the first object that is created during the import process is the *raw* object. It contains the raw data from the spectrometer and will be accessible at any time. All processing steps are automatically documented and the entire workspace can be saved as a single file in the h5 format.

Workflow
========

.. figure:: _static/images/dnpLab_workflow.png
    :width: 400
    :alt: dnpLab Workflow
    :align: center

    Overview of the dnpLab Workflow

Importing Data
--------------
The data is imported using the :ref:`dnpImport <dnpImport>`  sub-package. This sub-package calls modules for importing various spectrometer formats (e.g. topspin, vnmrj, prospa, etc.).

The data is imported as a :ref:`dnpdata <dnpData>` object. The dnpdata object is a container for data (values), coordinates for each dimension (coords), dimension labels (dims), and experimental parameters (attrs). In addition, each processing step applied to the data is saved in the dnpdata object (stored as proc_attrs).

The dnpdata object is a flexible data format which can handle N-dimensional data and coordinates together.

Creating a workspace
--------------------
The workspace can be created with the "create_workspace" function in DNPLab. Once the data is imported, it is added to a workspace which is a python dictonary-like class that stores multiple dnpdata objects. A workspace is a collection of dnpdata objects and allows for raw and processed data to be saved in the same h5 file. That way, the raw data is always available, even if the data on the spectrometer does not exist anymore.

Creating a single h5 file has the advantage that data can be easily shared among collaborators.

Processing Data
---------------
The DNPLab workspace has the concept of a "processing_buffer" (typically called proc). The processing buffer specifies the data which is meant for processing. Typically one will add (raw) data to the workspace and copy or move the data to the processing buffer (proc). DNPLab is primarily designed for processing and analyzing DNP-NMR data. Processing DNP-NMR data is performed using the the :ref:`dnpNMR <dnpNMR>` module. 

Saving Data in h5 format
------------------------
Once the data is processed, the entire workspace can be saved in a single file in the h5 format. This is done using the :ref:`dnpSave <dnpSave>` module. The workspace can then be loaded, subsequent processing can be performed and the data can be saved again.