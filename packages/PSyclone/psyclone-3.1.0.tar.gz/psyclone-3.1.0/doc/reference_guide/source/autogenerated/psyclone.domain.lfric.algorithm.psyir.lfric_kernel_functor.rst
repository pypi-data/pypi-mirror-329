==============================================================
``psyclone.domain.lfric.algorithm.psyir.lfric_kernel_functor``
==============================================================

.. automodule:: psyclone.domain.lfric.algorithm.psyir.lfric_kernel_functor

   .. contents::
      :local:

.. currentmodule:: psyclone.domain.lfric.algorithm.psyir.lfric_kernel_functor


Classes
=======

- :py:class:`LFRicBuiltinFunctor`:
  Base class which all LFRic builtins subclass. Contains a builtin call,

- :py:class:`LFRicKernelFunctor`:
  Object containing a call to a user-provided LFRic kernel, a description

- :py:class:`LFRicBuiltinFunctorFactory`:
  This class is a singleton which generates and stores a Functor class for


.. autoclass:: LFRicBuiltinFunctor
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicBuiltinFunctor
      :parts: 1

.. autoclass:: LFRicKernelFunctor
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicKernelFunctor
      :parts: 1

.. autoclass:: LFRicBuiltinFunctorFactory
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicBuiltinFunctorFactory
      :parts: 1
