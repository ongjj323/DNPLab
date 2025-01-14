.. _dnpHydration:

=============
dnpHydration
=============

To use the dnpHydration module first create a inputs dictionary named **hydration**,

.. code-block:: python

    import dnplab
    
    Enhancements = # list of signal enhancements
    Enhancement_powers = # list of signal enhancements powers in Watts
    T1 = # list of T1 values in seconds
    T1_powers = # list of T1 values powers in Watts
    
    pars = {} # initialize the input parameters dictionary
    pars['T10'] = # T1(0) value in seconds, i.e. T1 measured with power=0
    pars['T100'] = # T10(0) value in seconds, i.e. T1 measured with SL=0 and power=0
    pars['spin_C'] = # spin concentration in micromolar
    pars['field'] = # magnetic field in mT
    pars['smax_model'] = # choice of smax model, 'tethered' or 'free'
    pars['t1_interp_method'] = # choice of interpolation, 'linear' or 'second_order'
    
    hydration = {
                 'E' : np.array(Enhancements),
                 'E_power' : np.array(Enhancement_powers),
                 'T1' : np.array(T1),
                 'T1_power' : np.array(T1_powers),
                 'T10': pars['T10'],
                 'T100': pars['T100'],
                 'spin_C': pars['spin_C'],
                 'field': pars['field'],
                 'smax_model': pars['smax_model'],
                 't1_interp_method': pars['t1_interp_method']
                }
    

Now create a workspace named **hydration_workspace** and add the dictionary under the key **'hydration_inputs'**,

.. code-block:: python

    hydration_workspace = dnplab.create_workspace()
    hydration_workspace.add('hydration_inputs', hydration)


Pass the **hydration_workspace** to dnpHydration to perform calculations using,

.. code-block:: python

    hydration_results = dnplab.dnpHydration.hydration(hydration_workspace)


The **hydration_results** is a dictionary that has the elements listed in the table below, 

+-------------------+-------------+------------------------------------------------------------------------------------------+
| key               | type        | description                                                                              |
+===================+=============+==========================================================================================+
| uncorrected_Ep    | numpy array | fit to Equation 12 by varying coupling factor and p\ :sub:`1/2`                          |
+-------------------+-------------+------------------------------------------------------------------------------------------+
| uncorrected_xi    | float       | coupling factor from uncorrected_Ep fit (unitless)                                       |
+-------------------+-------------+------------------------------------------------------------------------------------------+
| interpolated_T1   | numpy array | interpolation of T1 measurements                                                         | 
+-------------------+-------------+------------------------------------------------------------------------------------------+
| ksigma_array      | numpy array | left side of Equation 42                                                                 |
+-------------------+-------------+------------------------------------------------------------------------------------------+
| ksigma_fit        | numpy array | fit to Equation 42 by varying κ\ :sub:`σ` and p\ :sub:`1/2`                              |          
+-------------------+-------------+------------------------------------------------------------------------------------------+
| ksigma            | float       | cross-relaxivity, κ\ :sub:`σ`, (s\ :sup:`-1` M\ :sup:`-1`)                               |   
+-------------------+-------------+------------------------------------------------------------------------------------------+
| ksigma_stdd       | float       | standard deviation in κ\ :sub:`σ` (s\ :sup:`-1` M\ :sup:`-1`)                            |
+-------------------+-------------+------------------------------------------------------------------------------------------+
| ksigma_bulk_ratio | float       | ratio of κ\ :sub:`σ` to bulk value (κ\ :sub:`σ,bulk` = 95.4 s\ :sup:`-1` M\ :sup:`-1`).  |
+-------------------+-------------+------------------------------------------------------------------------------------------+
| krho              | float       | self-relaxivity, κ\ :sub:`ρ`, (s\ :sup:`-1` M\ :sup:`-1`)                                | 
+-------------------+-------------+------------------------------------------------------------------------------------------+
| krho_bulk_ratio   | float       | ratio of κ\ :sub:`ρ` to bulk value (κ\ :sub:`ρ,bulk` = 353.4 s\ :sup:`-1` M\ :sup:`-1`)  |          
+-------------------+-------------+------------------------------------------------------------------------------------------+
| klow              | float       | [(5/3)κ\ :sub:`ρ` - (7/3)κ\ :sub:`σ`]   (s\ :sup:`-1` M\ :sup:`-1`)                      |
+-------------------+-------------+------------------------------------------------------------------------------------------+
| klow_bulk_ratio   | float       | ratio of κ\ :sub:`low` to bulk value (κ\ :sub:`low,bulk` = 366 s\ :sup:`-1` M\ :sup:`-1`)|          
+-------------------+-------------+------------------------------------------------------------------------------------------+
| coupling_factor   | float       | κ\ :sub:`σ` / κ\ :sub:`ρ` (unitless)                                                     |   
+-------------------+-------------+------------------------------------------------------------------------------------------+
| tcorr             | float       | translational correlation time, τ\ :sub:`corr` (ps), see Equations. 21-23                |
+-------------------+-------------+------------------------------------------------------------------------------------------+
| tcorr_bulk_ratio  | float       | ratio of τ\ :sub:`corr` to bulk value (τ\ :sub:`corr,bulk` = 54 ps)                      |          
+-------------------+-------------+------------------------------------------------------------------------------------------+
| Dlocal            | float       | local diffusivity, D\ :sub:`local`, (m\ :sup:`2`/s), see Equations 18-20                 |   
+-------------------+-------------+------------------------------------------------------------------------------------------+

If needed, access the results individually as follows,

.. code-block:: python
     
     interpolated_t1 = hydration_results['interpolated_T1']
     ksigma_array = hydration_results['ksigma_array']     
     ksigma = hydration_results['ksigma']
     coupling_factor = hydration_results['coupling_factor']
     etc.

For explanation of 'smax_model' see https://doi.org/10.1039/c0cp02126a. For explanations of 't1_interp_method' options or any of the equations used to calculate the hydration parameters refer to http://dx.doi.org/10.1016/j.pnmrs.2013.06.001 and https://doi.org/10.1016/bs.mie.2018.09.024. Also see the **interpolate_T1** function of :ref:`dnpFit <dnpFit>` for the T\ :sub:`1` (p) interpolation function.
