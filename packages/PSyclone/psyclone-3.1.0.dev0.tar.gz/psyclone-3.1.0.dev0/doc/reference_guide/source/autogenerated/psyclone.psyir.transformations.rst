==================================
``psyclone.psyir.transformations``
==================================

.. automodule:: psyclone.psyir.transformations

   .. contents::
      :local:


Submodules
==========

.. toctree::

   psyclone.psyir.transformations.acc_kernels_trans
   psyclone.psyir.transformations.acc_update_trans
   psyclone.psyir.transformations.allarrayaccess2loop_trans
   psyclone.psyir.transformations.arrayaccess2loop_trans
   psyclone.psyir.transformations.arrayassignment2loops_trans
   psyclone.psyir.transformations.chunk_loop_trans
   psyclone.psyir.transformations.extract_trans
   psyclone.psyir.transformations.fold_conditional_return_expressions_trans
   psyclone.psyir.transformations.hoist_local_arrays_trans
   psyclone.psyir.transformations.hoist_loop_bound_expr_trans
   psyclone.psyir.transformations.hoist_trans
   psyclone.psyir.transformations.inline_trans
   psyclone.psyir.transformations.intrinsics
   psyclone.psyir.transformations.loop_fuse_trans
   psyclone.psyir.transformations.loop_swap_trans
   psyclone.psyir.transformations.loop_tiling_2d_trans
   psyclone.psyir.transformations.loop_trans
   psyclone.psyir.transformations.omp_loop_trans
   psyclone.psyir.transformations.omp_target_trans
   psyclone.psyir.transformations.omp_task_trans
   psyclone.psyir.transformations.omp_taskwait_trans
   psyclone.psyir.transformations.parallel_loop_trans
   psyclone.psyir.transformations.profile_trans
   psyclone.psyir.transformations.psy_data_trans
   psyclone.psyir.transformations.read_only_verify_trans
   psyclone.psyir.transformations.reference2arrayrange_trans
   psyclone.psyir.transformations.region_trans
   psyclone.psyir.transformations.replace_induction_variables_trans
   psyclone.psyir.transformations.transformation_error
   psyclone.psyir.transformations.value_range_check_trans

.. currentmodule:: psyclone.psyir.transformations


Classes
=======

- :py:class:`ACCKernelsTrans`:
  Enclose a sub-set of nodes from a Schedule within an OpenACC kernels

- :py:class:`ACCUpdateTrans`:
  Examines the supplied Schedule and adds OpenACC "update" directives

- :py:class:`AllArrayAccess2LoopTrans`:
  Provides a transformation from a PSyIR Assignment containing

- :py:class:`ArrayAccess2LoopTrans`:
  Provides a transformation to transform a constant index access to

- :py:class:`ArrayAssignment2LoopsTrans`:
  Provides a transformation from a PSyIR Array Range to a PSyIR

- :py:class:`ChunkLoopTrans`:
  Apply a chunking transformation to a loop (in order to permit a

- :py:class:`ExtractTrans`:
  This transformation inserts an ExtractNode or a node derived

- :py:class:`FoldConditionalReturnExpressionsTrans`:
  Provides a transformation that folds conditional expressions with only

- :py:class:`HoistLocalArraysTrans`:
  This transformation takes a Routine and promotes any local, 'automatic'

- :py:class:`HoistLoopBoundExprTrans`:
  This transformation moves complex bounds expressions out of the loop

- :py:class:`HoistTrans`:
  This transformation takes an assignment and moves it outside of

- :py:class:`InlineTrans`:
  This transformation takes a Call (which may have a return value)

- :py:class:`Abs2CodeTrans`:
  Provides a transformation from a PSyIR ABS Operator node to

- :py:class:`DotProduct2CodeTrans`:
  Provides a transformation from a PSyIR DOT_PRODUCT Operator node to

- :py:class:`Matmul2CodeTrans`:
  Provides a transformation from a PSyIR MATMUL Operator node to

- :py:class:`Max2CodeTrans`:
  Provides a transformation from a PSyIR MAX Intrinsic node to

- :py:class:`Min2CodeTrans`:
  Provides a transformation from a PSyIR MIN Intrinsic node to

- :py:class:`Sign2CodeTrans`:
  Provides a transformation from a PSyIR SIGN intrinsic node to

- :py:class:`Sum2LoopTrans`:
  Provides a transformation from a PSyIR SUM IntrinsicCall node to an

- :py:class:`LoopFuseTrans`:
  Provides a generic loop-fuse transformation to two Nodes in the

- :py:class:`LoopSwapTrans`:
  Provides a loop-swap transformation, e.g.:

- :py:class:`LoopTiling2DTrans`:
  Apply a 2D loop tiling transformation to a loop. For example:

- :py:class:`LoopTrans`:
  This abstract class is a base class for all transformations that act

- :py:class:`Maxval2LoopTrans`:
  Provides a transformation from a PSyIR MAXVAL IntrinsicCall node to

- :py:class:`Minval2LoopTrans`:
  Provides a transformation from a PSyIR MINVAL IntrinsicCall node to

- :py:class:`OMPLoopTrans`:
  Adds an OpenMP directive to parallelise this loop. It can insert different

- :py:class:`OMPTargetTrans`:
  Adds an OpenMP target directive to a region of code.

- :py:class:`OMPTaskTrans`:
  Apply an OpenMP Task Transformation to a Loop. The Loop must

- :py:class:`OMPTaskwaitTrans`:
  Adds zero or more OpenMP Taskwait directives to an OMP parallel region.

- :py:class:`ParallelLoopTrans`:
  Adds an abstract directive (it needs to be specified by sub-classing this

- :py:class:`Product2LoopTrans`:
  Provides a transformation from a PSyIR PRODUCT IntrinsicCall node to

- :py:class:`ProfileTrans`:
  Create a profile region around a list of statements. For

- :py:class:`PSyDataTrans`:
  Create a PSyData region around a list of statements. For

- :py:class:`ReadOnlyVerifyTrans`:
  This transformation inserts a ReadOnlyVerifyNode or a node derived

- :py:class:`Reference2ArrayRangeTrans`:
  Provides a transformation from PSyIR Array Notation (a reference to

- :py:class:`RegionTrans`:
  This abstract class is a base class for all transformations that act

- :py:class:`ReplaceInductionVariablesTrans`:
  Move all supported induction variables out of the loop, and replace

- :py:class:`ValueRangeCheckTrans`:
  This transformation inserts a ValueRangeCheckNode into the PSyIR of a


.. autoclass:: ACCKernelsTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCKernelsTrans
      :parts: 1

.. autoclass:: ACCUpdateTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCUpdateTrans
      :parts: 1

.. autoclass:: AllArrayAccess2LoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: AllArrayAccess2LoopTrans
      :parts: 1

.. autoclass:: ArrayAccess2LoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ArrayAccess2LoopTrans
      :parts: 1

.. autoclass:: ArrayAssignment2LoopsTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ArrayAssignment2LoopsTrans
      :parts: 1

.. autoclass:: ChunkLoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ChunkLoopTrans
      :parts: 1

.. autoclass:: ExtractTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ExtractTrans
      :parts: 1

.. autoclass:: FoldConditionalReturnExpressionsTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: FoldConditionalReturnExpressionsTrans
      :parts: 1

.. autoclass:: HoistLocalArraysTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: HoistLocalArraysTrans
      :parts: 1

.. autoclass:: HoistLoopBoundExprTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: HoistLoopBoundExprTrans
      :parts: 1

.. autoclass:: HoistTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: HoistTrans
      :parts: 1

.. autoclass:: InlineTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: InlineTrans
      :parts: 1

.. autoclass:: Abs2CodeTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Abs2CodeTrans
      :parts: 1

.. autoclass:: DotProduct2CodeTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DotProduct2CodeTrans
      :parts: 1

.. autoclass:: Matmul2CodeTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Matmul2CodeTrans
      :parts: 1

.. autoclass:: Max2CodeTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Max2CodeTrans
      :parts: 1

.. autoclass:: Min2CodeTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Min2CodeTrans
      :parts: 1

.. autoclass:: Sign2CodeTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Sign2CodeTrans
      :parts: 1

.. autoclass:: Sum2LoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Sum2LoopTrans
      :parts: 1

.. autoclass:: LoopFuseTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LoopFuseTrans
      :parts: 1

.. autoclass:: LoopSwapTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LoopSwapTrans
      :parts: 1

.. autoclass:: LoopTiling2DTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LoopTiling2DTrans
      :parts: 1

.. autoclass:: LoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LoopTrans
      :parts: 1

.. autoclass:: Maxval2LoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Maxval2LoopTrans
      :parts: 1

.. autoclass:: Minval2LoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Minval2LoopTrans
      :parts: 1

.. autoclass:: OMPLoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPLoopTrans
      :parts: 1

.. autoclass:: OMPTargetTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPTargetTrans
      :parts: 1

.. autoclass:: OMPTaskTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPTaskTrans
      :parts: 1

.. autoclass:: OMPTaskwaitTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPTaskwaitTrans
      :parts: 1

.. autoclass:: ParallelLoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ParallelLoopTrans
      :parts: 1

.. autoclass:: Product2LoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Product2LoopTrans
      :parts: 1

.. autoclass:: ProfileTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ProfileTrans
      :parts: 1

.. autoclass:: PSyDataTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: PSyDataTrans
      :parts: 1

.. autoclass:: ReadOnlyVerifyTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ReadOnlyVerifyTrans
      :parts: 1

.. autoclass:: Reference2ArrayRangeTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Reference2ArrayRangeTrans
      :parts: 1

.. autoclass:: RegionTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: RegionTrans
      :parts: 1

.. autoclass:: ReplaceInductionVariablesTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ReplaceInductionVariablesTrans
      :parts: 1

.. autoclass:: ValueRangeCheckTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ValueRangeCheckTrans
      :parts: 1


Exceptions
==========

- :py:exc:`TransformationError`:
  Provides a PSyclone-specific error class for errors found during


.. autoexception:: TransformationError

   .. rubric:: Inheritance
   .. inheritance-diagram:: TransformationError
      :parts: 1
