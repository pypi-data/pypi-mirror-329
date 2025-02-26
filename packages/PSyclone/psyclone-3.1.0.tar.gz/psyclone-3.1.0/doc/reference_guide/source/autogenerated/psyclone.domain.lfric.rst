=========================
``psyclone.domain.lfric``
=========================

.. automodule:: psyclone.domain.lfric

   .. contents::
      :local:


Submodules
==========

.. toctree::

   psyclone.domain.lfric.algorithm
   psyclone.domain.lfric.arg_index_to_metadata_index
   psyclone.domain.lfric.arg_ordering
   psyclone.domain.lfric.function_space
   psyclone.domain.lfric.kern_call_acc_arg_list
   psyclone.domain.lfric.kern_call_arg_list
   psyclone.domain.lfric.kern_call_invoke_arg_list
   psyclone.domain.lfric.kern_stub_arg_list
   psyclone.domain.lfric.kernel
   psyclone.domain.lfric.kernel_interface
   psyclone.domain.lfric.lfric_arg_descriptor
   psyclone.domain.lfric.lfric_builtins
   psyclone.domain.lfric.lfric_cell_iterators
   psyclone.domain.lfric.lfric_collection
   psyclone.domain.lfric.lfric_constants
   psyclone.domain.lfric.lfric_dofmaps
   psyclone.domain.lfric.lfric_extract_driver_creator
   psyclone.domain.lfric.lfric_fields
   psyclone.domain.lfric.lfric_halo_depths
   psyclone.domain.lfric.lfric_invoke
   psyclone.domain.lfric.lfric_invoke_schedule
   psyclone.domain.lfric.lfric_invokes
   psyclone.domain.lfric.lfric_kern
   psyclone.domain.lfric.lfric_kern_call_factory
   psyclone.domain.lfric.lfric_kern_metadata
   psyclone.domain.lfric.lfric_loop
   psyclone.domain.lfric.lfric_loop_bounds
   psyclone.domain.lfric.lfric_psy
   psyclone.domain.lfric.lfric_run_time_checks
   psyclone.domain.lfric.lfric_scalar_args
   psyclone.domain.lfric.lfric_stencils
   psyclone.domain.lfric.lfric_symbol_table
   psyclone.domain.lfric.lfric_types
   psyclone.domain.lfric.metadata_to_arguments_rules
   psyclone.domain.lfric.transformations
   psyclone.domain.lfric.utils

.. currentmodule:: psyclone.domain.lfric


Classes
=======

- :py:class:`ArgOrdering`:
  Base class capturing the arguments, type and ordering of data in

- :py:class:`FunctionSpace`:
  Manages the name of a function space. If it is an any_space or

- :py:class:`KernCallAccArgList`:
  Kernel call arguments that need to be declared by OpenACC

- :py:class:`KernCallArgList`:
  Creates the argument list required to call kernel "kern" from the

- :py:class:`KernelInterface`:
  Create the kernel arguments for the supplied kernel as specified by

- :py:class:`KernStubArgList`:
  Creates the argument list required to create and declare the

- :py:class:`LFRicArgDescriptor`:
  This class captures the information specified in one of LFRic API argument

- :py:class:`LFRicCellIterators`:
  Handles all entities required by kernels that operate on cell-columns.

- :py:class:`LFRicCollection`:
  Base class for managing the declaration and initialisation of a

- :py:class:`LFRicConstants`:
  This class stores all LFRic constants. Note that some constants

- :py:class:`LFRicDofmaps`:
  Holds all information on the dofmaps (including column-banded and

- :py:class:`LFRicExtractDriverCreator`:
  This class provides the functionality to create a driver that

- :py:class:`LFRicFields`:
  Manages the declarations for all field arguments required by an Invoke

- :py:class:`LFRicHaloDepths`:
  Manages the declarations for all halo-depth arguments (as needed by

- :py:class:`LFRicInvoke`:
  The LFRic-specific Invoke class. This passes the LFRic-specific

- :py:class:`LFRicInvokes`:
  The LFRic-specific invokes class. This passes the LFRic-specific

- :py:class:`LFRicInvokeSchedule`:
  The LFRic-specific InvokeSchedule sub-class. This passes the LFRic-

- :py:class:`LFRicKern`:
  Stores information about LFRic Kernels as specified by the

- :py:class:`LFRicKernCallFactory`:
  Create the necessary framework for an LFRic kernel call.

- :py:class:`LFRicKernMetadata`:
  Captures the Kernel subroutine code and metadata describing

- :py:class:`LFRicLoop`:
  The LFRic-specific PSyLoop class. This passes the LFRic-specific

- :py:class:`LFRicLoopBounds`:
  Handles all variables required for specifying loop limits within

- :py:class:`LFRicPSy`:
  The LFRic-specific PSy class. This creates an LFRic-specific

- :py:class:`LFRicRunTimeChecks`:
  Handle declarations and code generation for run-time checks. This

- :py:class:`LFRicScalarArgs`:
  Handles the declarations of scalar kernel arguments appearing in either

- :py:class:`LFRicStencils`:
  Stencil information and code generation associated with a PSy-layer

- :py:class:`LFRicSymbolTable`:
  Sub-classes SymbolTable to provide a LFRic-specific implementation.


.. autoclass:: ArgOrdering
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ArgOrdering
      :parts: 1

.. autoclass:: FunctionSpace
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: FunctionSpace
      :parts: 1

.. autoclass:: KernCallAccArgList
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: KernCallAccArgList
      :parts: 1

.. autoclass:: KernCallArgList
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: KernCallArgList
      :parts: 1

.. autoclass:: KernelInterface
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: KernelInterface
      :parts: 1

.. autoclass:: KernStubArgList
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: KernStubArgList
      :parts: 1

.. autoclass:: LFRicArgDescriptor
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicArgDescriptor
      :parts: 1

.. autoclass:: LFRicCellIterators
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicCellIterators
      :parts: 1

.. autoclass:: LFRicCollection
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicCollection
      :parts: 1

.. autoclass:: LFRicConstants
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicConstants
      :parts: 1

.. autoclass:: LFRicDofmaps
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicDofmaps
      :parts: 1

.. autoclass:: LFRicExtractDriverCreator
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicExtractDriverCreator
      :parts: 1

.. autoclass:: LFRicFields
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicFields
      :parts: 1

.. autoclass:: LFRicHaloDepths
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicHaloDepths
      :parts: 1

.. autoclass:: LFRicInvoke
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicInvoke
      :parts: 1

.. autoclass:: LFRicInvokes
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicInvokes
      :parts: 1

.. autoclass:: LFRicInvokeSchedule
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicInvokeSchedule
      :parts: 1

.. autoclass:: LFRicKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicKern
      :parts: 1

.. autoclass:: LFRicKernCallFactory
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicKernCallFactory
      :parts: 1

.. autoclass:: LFRicKernMetadata
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicKernMetadata
      :parts: 1

.. autoclass:: LFRicLoop
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicLoop
      :parts: 1

.. autoclass:: LFRicLoopBounds
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicLoopBounds
      :parts: 1

.. autoclass:: LFRicPSy
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicPSy
      :parts: 1

.. autoclass:: LFRicRunTimeChecks
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicRunTimeChecks
      :parts: 1

.. autoclass:: LFRicScalarArgs
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicScalarArgs
      :parts: 1

.. autoclass:: LFRicStencils
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicStencils
      :parts: 1

.. autoclass:: LFRicSymbolTable
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicSymbolTable
      :parts: 1
