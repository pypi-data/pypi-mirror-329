===================================
``psyclone.domain.lfric.algorithm``
===================================

.. automodule:: psyclone.domain.lfric.algorithm

   .. contents::
      :local:


Submodules
==========

.. toctree::

   psyclone.domain.lfric.algorithm.lfric_alg
   psyclone.domain.lfric.algorithm.psyir

.. currentmodule:: psyclone.domain.lfric.algorithm


Classes
=======

- :py:class:`LFRicAlg`:
  Encapsulates the functionality for generating an LFRic Algorithm

- :py:class:`LFRicAlgorithmInvokeCall`:
  An invoke call from the LFRic Algorithm layer.

- :py:class:`LFRicBuiltinFunctor`:
  Base class which all LFRic builtins subclass. Contains a builtin call,

- :py:class:`LFRicBuiltinFunctorFactory`:
  This class is a singleton which generates and stores a Functor class for

- :py:class:`LFRicFunctor`:
  Base functor class for all LFRic user-supplied and built-in kernels.

- :py:class:`LFRicKernelFunctor`:
  Object containing a call to a user-provided LFRic kernel, a description


.. autoclass:: LFRicAlg
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicAlg
      :parts: 1

.. autoclass:: LFRicAlgorithmInvokeCall
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicAlgorithmInvokeCall
      :parts: 1

.. autoclass:: LFRicBuiltinFunctor
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicBuiltinFunctor
      :parts: 1

.. autoclass:: LFRicBuiltinFunctorFactory
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicBuiltinFunctorFactory
      :parts: 1

.. autoclass:: LFRicFunctor
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicFunctor
      :parts: 1

.. autoclass:: LFRicKernelFunctor
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicKernelFunctor
      :parts: 1
