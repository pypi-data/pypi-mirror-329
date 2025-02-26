============================
``psyclone.transformations``
============================

.. automodule:: psyclone.transformations

   .. contents::
      :local:

.. currentmodule:: psyclone.transformations


Classes
=======

- :py:class:`ACCEnterDataTrans`:
  Adds an OpenACC "enter data" directive to a Schedule.

- :py:class:`ACCDataTrans`:
  Add an OpenACC data region around a list of nodes in the PSyIR.

- :py:class:`ACCLoopTrans`:
  Adds an OpenACC loop directive to a loop. This directive must be within

- :py:class:`ACCParallelTrans`:
  Create an OpenACC parallel region by inserting an 'acc parallel'

- :py:class:`ACCRoutineTrans`:
  Transform a kernel or routine by adding a "!$acc routine" directive

- :py:class:`ColourTrans`:
  Apply a colouring transformation to a loop (in order to permit a

- :py:class:`Dynamo0p3AsyncHaloExchangeTrans`:
  Splits a synchronous halo exchange into a halo exchange start and

- :py:class:`Dynamo0p3ColourTrans`:
  Split a Dynamo 0.3 loop over cells into colours so that it can be

- :py:class:`Dynamo0p3KernelConstTrans`:
  Modifies a kernel so that the number of dofs, number of layers and

- :py:class:`Dynamo0p3OMPLoopTrans`:
  LFRic (Dynamo 0.3) specific orphan OpenMP loop transformation. Adds

- :py:class:`Dynamo0p3RedundantComputationTrans`:
  This transformation allows the user to modify a loop's bounds so

- :py:class:`DynamoOMPParallelLoopTrans`:
  Dynamo-specific OpenMP loop transformation. Adds Dynamo specific

- :py:class:`GOceanOMPLoopTrans`:
  GOcean-specific orphan OpenMP loop transformation. Adds GOcean

- :py:class:`GOceanOMPParallelLoopTrans`:
  GOcean specific OpenMP Do loop transformation. Adds GOcean

- :py:class:`KernelImportsToArguments`:
  Transformation that removes any accesses of imported data from the supplied

- :py:class:`MoveTrans`:
  Provides a transformation to move a node in the tree. For

- :py:class:`OMPMasterTrans`:
  Create an OpenMP MASTER region by inserting directives. The most

- :py:class:`OMPParallelLoopTrans`:
  Adds an OpenMP PARALLEL DO directive to a loop.

- :py:class:`OMPParallelTrans`:
  Create an OpenMP PARALLEL region by inserting directives. For

- :py:class:`OMPSingleTrans`:
  Create an OpenMP SINGLE region by inserting directives. The most

- :py:class:`ParallelRegionTrans`:
  Base class for transformations that create a parallel region.


.. autoclass:: ACCEnterDataTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCEnterDataTrans
      :parts: 1

.. autoclass:: ACCDataTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCDataTrans
      :parts: 1

.. autoclass:: ACCLoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCLoopTrans
      :parts: 1

.. autoclass:: ACCParallelTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCParallelTrans
      :parts: 1

.. autoclass:: ACCRoutineTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCRoutineTrans
      :parts: 1

.. autoclass:: ColourTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ColourTrans
      :parts: 1

.. autoclass:: Dynamo0p3AsyncHaloExchangeTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Dynamo0p3AsyncHaloExchangeTrans
      :parts: 1

.. autoclass:: Dynamo0p3ColourTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Dynamo0p3ColourTrans
      :parts: 1

.. autoclass:: Dynamo0p3KernelConstTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Dynamo0p3KernelConstTrans
      :parts: 1

.. autoclass:: Dynamo0p3OMPLoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Dynamo0p3OMPLoopTrans
      :parts: 1

.. autoclass:: Dynamo0p3RedundantComputationTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Dynamo0p3RedundantComputationTrans
      :parts: 1

.. autoclass:: DynamoOMPParallelLoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynamoOMPParallelLoopTrans
      :parts: 1

.. autoclass:: GOceanOMPLoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOceanOMPLoopTrans
      :parts: 1

.. autoclass:: GOceanOMPParallelLoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOceanOMPParallelLoopTrans
      :parts: 1

.. autoclass:: KernelImportsToArguments
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: KernelImportsToArguments
      :parts: 1

.. autoclass:: MoveTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: MoveTrans
      :parts: 1

.. autoclass:: OMPMasterTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPMasterTrans
      :parts: 1

.. autoclass:: OMPParallelLoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPParallelLoopTrans
      :parts: 1

.. autoclass:: OMPParallelTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPParallelTrans
      :parts: 1

.. autoclass:: OMPSingleTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPSingleTrans
      :parts: 1

.. autoclass:: ParallelRegionTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ParallelRegionTrans
      :parts: 1
