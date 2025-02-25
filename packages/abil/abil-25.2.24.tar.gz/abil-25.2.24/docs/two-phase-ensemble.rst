2-phase Ensemble 
****************

YAML example
~~~~~~~~~~~~

Before running the model, model specifications need to be defined in a YAML file. 
For a detailed explanation of each parameter see :ref:`yaml explained`.

The YAML file of a 2-phase model used in this example is provided below.
Note that compared to a 1-phase regressor model, the hyper-parameters for the classifier also need to be specified.

.. literalinclude:: ../../../tests/2-phase.yml
   :language: yaml

Running the model
~~~~~~~~~~~~~~~~~
After specifying the model configuration in the relevant YAML file, we can use the Abil API
to 1) tune the model, evaluating the model performance across different hyper-parameter values and then 
selecting the best configuration 2) predict in-sample and out-of-sample observations based on the optimal
hyper-parameter configuration identified in the first step 3) conduct post-processing such as exporting
relevant performance metrics, spatially or temporally integrated target estimates, and diversity metrics.


Loading dependencies
^^^^^^^^^^^^^^^^^^^^

Before running the Python script we need to import all relevant Python packages.
For instructions on how to install these packages, see :ref:`dependencies install`
and the Abil :ref:`install instructions`.

.. code-block:: python

    #load dependencies:
    import numpy as np
    from yaml import load
    from yaml import CLoader as Loader
    from abil.tune import tune
    from abil.predict import predict
    from abil.post import post
    from abil.utils import example_data 
    import os


Defining paths
^^^^^^^^^^^^^^

After loading the required packages we need to define our file paths.
Note that this is operating system specific, as Unix and Mac use '/' while for Windows '\' is used.

.. tab-set::

    .. tab-item:: Unix/MacOS

        .. code-block:: python

            #define root directory:
            os.chdir('/home/phyto-2/Abil/')  

            #load configuration yaml:
            with open('./tests/2-phase.yml', 'r') as f:
                model_config = load(f, Loader=Loader)


    .. tab-item:: Windows

        .. code-block:: python

             #define root directory:
            os.chdir('.\Abil\')  

            #load configuration yaml:
            with open('.\tests\2-phase.yml', 'r') as f:
                model_config = load(f, Loader=Loader)

Creating example data
^^^^^^^^^^^^^^^^^^^^^

In this example we will look at coccolithophore observations from the Bermuda Atlantic Time Series (BATS).
These observations were extracted from the `CASCADE database <https://doi.org/10.5281/zenodo.12797197>`_ and combined with environmental data from `World Ocean Atlas <https://www.ncei.noaa.gov/products/world-ocean-atlas>`_ and xyz.

.. literalinclude:: ../../examples/2-phase.py
   :lines: 14-15
   :language: python


Plotting observations
---------------------

.. image:: ../../examples/observational_data.png
   :alt: 2-phase model example plot

Plotting environmental data
----------------------------
.. image:: ../../examples/environmental_data.png
   :alt: 2-phase model example plot

Training the model
^^^^^^^^^^^^^^^^^^

Next we train our model. Note that depending on the number of hyper-parameters specified in the
YAML file this can be computationally very expensive and it recommended to do this on a HPC system. 

.. code-block:: python

    #train your model:
    m = tune(X_train, y, model_config)
    m.train(model="rf")

Making predictions
^^^^^^^^^^^^^^^^^^

After training our model we can make predictions on a new dataset (X_predict):

.. code-block:: python

    #predict your model:
    m = predict(X_train=X_train, y=y, X_predict=X_predict, 
        model_config=model_config, n_jobs=2)
    m.make_prediction()

Post-processing
^^^^^^^^^^^^^^^

Finally, we conduct the post-processing.

.. code-block:: python

    #post:
    targets = np.array([target_name])
    def do_post(statistic)
        m = post(X_train, y, X_predict, model_config, statistic, datatype="poc")
        
        m.estimate_applicability()
        m.estimate_carbon("pg poc")
        m.total()

        m.merge_performance(model="ens") 
        m.merge_performance(model="xgb")
        m.merge_performance(model="rf")
        m.merge_performance(model="knn")

        m.merge_parameters(model="rf")
        m.merge_parameters(model="xgb")
        m.merge_parameters(model="knn")

        m.merge_env()
        m.merge_obs("test",targets)

        m.export_ds("test")
        m.export_csv("test")

        vol_conversion = 1e3 #L-1 to m-3
        integ = m.integration(m, vol_conversion=vol_conversion)
        integ.integrated_totals(targets, monthly=True)
        integ.integrated_totals(targets)

    do_post(statistic="mean")
    do_post(statistic="median")
    do_post(statistic="std")
    do_post(statistic="ci95_UL")
    do_post(statistic="ci95_LL")