==========================================
``psyclone.domain.common.transformations``
==========================================

.. automodule:: psyclone.domain.common.transformations

   .. contents::
      :local:


Submodules
==========

.. toctree::

   psyclone.domain.common.transformations.alg_invoke_2_psy_call_trans
   psyclone.domain.common.transformations.alg_trans
   psyclone.domain.common.transformations.kernel_module_inline_trans
   psyclone.domain.common.transformations.raise_psyir_2_alg_trans

.. currentmodule:: psyclone.domain.common.transformations


Classes
=======

- :py:class:`AlgInvoke2PSyCallTrans`:
  Base class to transform (lower) an AlgorithmInvokeCall into a

- :py:class:`AlgTrans`:
  Transform a generic PSyIR representation of the Algorithm layer to

- :py:class:`KernelModuleInlineTrans`:
  Brings the routine being called into the same Container as the call

- :py:class:`RaisePSyIR2AlgTrans`:
  Transform a generic PSyIR representation of an Algorithm-layer


.. autoclass:: AlgInvoke2PSyCallTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: AlgInvoke2PSyCallTrans
      :parts: 1

.. autoclass:: AlgTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: AlgTrans
      :parts: 1

.. autoclass:: KernelModuleInlineTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: KernelModuleInlineTrans
      :parts: 1

.. autoclass:: RaisePSyIR2AlgTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: RaisePSyIR2AlgTrans
      :parts: 1
