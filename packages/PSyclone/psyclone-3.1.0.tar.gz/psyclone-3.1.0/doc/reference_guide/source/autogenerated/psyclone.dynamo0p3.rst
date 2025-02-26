======================
``psyclone.dynamo0p3``
======================

.. automodule:: psyclone.dynamo0p3

   .. contents::
      :local:

.. currentmodule:: psyclone.dynamo0p3


Classes
=======

- :py:class:`DynFuncDescriptor03`:
  The Dynamo 0.3 API includes a function-space descriptor as

- :py:class:`DynFunctionSpaces`:
  Handles the declaration and initialisation of all function-space-related

- :py:class:`DynProxies`:
  Handles all proxy-related declarations and initialisation. Unlike other

- :py:class:`DynLMAOperators`:
  Handles all entities associated with Local-Matrix-Assembly Operators.

- :py:class:`DynCMAOperators`:
  Holds all information on the Column-Matrix-Assembly operators

- :py:class:`DynMeshes`:
  Holds all mesh-related information (including colour maps if

- :py:class:`DynInterGrid`:
  Holds information on quantities required by an inter-grid kernel.

- :py:class:`DynBasisFunctions`:
  Holds all information on the basis and differential basis

- :py:class:`DynBoundaryConditions`:
  Manages declarations and initialisation of quantities required by

- :py:class:`DynGlobalSum`:
  Dynamo specific global sum class which can be added to and

- :py:class:`LFRicHaloExchange`:
  LFRic-specific halo exchange class which can be added to and

- :py:class:`LFRicHaloExchangeStart`:
  The start of an asynchronous halo exchange. This is similar to a

- :py:class:`LFRicHaloExchangeEnd`:
  The end of an asynchronous halo exchange. This is similar to a

- :py:class:`HaloDepth`:
  Determines how much of the halo a read to a field accesses (the

- :py:class:`HaloWriteAccess`:
  Determines how much of a field's halo is written to (the halo depth)

- :py:class:`HaloReadAccess`:
  Determines how much of a field's halo is read (the halo depth) and

- :py:class:`FSDescriptor`:
  Provides information about a particular function space used by

- :py:class:`FSDescriptors`:
  Contains a collection of FSDescriptor objects and methods

- :py:class:`LFRicArgStencil`:
  Provides stencil information about an LFRic kernel argument.

- :py:class:`DynKernelArguments`:
  Provides information about Dynamo kernel call arguments

- :py:class:`DynKernelArgument`:
  This class provides information about individual LFRic kernel call

- :py:class:`DynACCEnterDataDirective`:
  Sub-classes ACCEnterDataDirective to provide an API-specific implementation


.. autoclass:: DynFuncDescriptor03
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynFuncDescriptor03
      :parts: 1

.. autoclass:: DynFunctionSpaces
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynFunctionSpaces
      :parts: 1

.. autoclass:: DynProxies
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynProxies
      :parts: 1

.. autoclass:: DynLMAOperators
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynLMAOperators
      :parts: 1

.. autoclass:: DynCMAOperators
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynCMAOperators
      :parts: 1

.. autoclass:: DynMeshes
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynMeshes
      :parts: 1

.. autoclass:: DynInterGrid
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynInterGrid
      :parts: 1

.. autoclass:: DynBasisFunctions
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynBasisFunctions
      :parts: 1

.. autoclass:: DynBoundaryConditions
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynBoundaryConditions
      :parts: 1

.. autoclass:: DynGlobalSum
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynGlobalSum
      :parts: 1

.. autoclass:: LFRicHaloExchange
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicHaloExchange
      :parts: 1

.. autoclass:: LFRicHaloExchangeStart
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicHaloExchangeStart
      :parts: 1

.. autoclass:: LFRicHaloExchangeEnd
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicHaloExchangeEnd
      :parts: 1

.. autoclass:: HaloDepth
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: HaloDepth
      :parts: 1

.. autoclass:: HaloWriteAccess
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: HaloWriteAccess
      :parts: 1

.. autoclass:: HaloReadAccess
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: HaloReadAccess
      :parts: 1

.. autoclass:: FSDescriptor
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: FSDescriptor
      :parts: 1

.. autoclass:: FSDescriptors
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: FSDescriptors
      :parts: 1

.. autoclass:: LFRicArgStencil
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicArgStencil
      :parts: 1

.. autoclass:: DynKernelArguments
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynKernelArguments
      :parts: 1

.. autoclass:: DynKernelArgument
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynKernelArgument
      :parts: 1

.. autoclass:: DynACCEnterDataDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynACCEnterDataDirective
      :parts: 1
