====================================
``psyclone.psyir.symbols.datatypes``
====================================

.. automodule:: psyclone.psyir.symbols.datatypes

   .. contents::
      :local:

.. currentmodule:: psyclone.psyir.symbols.datatypes


Classes
=======

- :py:class:`UnsupportedType`:
  Indicates that a variable declaration is not supported by the PSyIR.

- :py:class:`UnsupportedFortranType`:
  Indicates that a Fortran declaration is not supported by the PSyIR.

- :py:class:`UnresolvedType`:
  Indicates that the type declaration has not been found yet. 

- :py:class:`ScalarType`:
  Describes a scalar datatype (and its precision).

- :py:class:`ArrayType`:
  Describes an array datatype. Can be an array of intrinsic types (e.g.

- :py:class:`StructureType`:
  Describes a 'structure' or 'derived' datatype that is itself composed


.. autoclass:: UnsupportedType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: UnsupportedType
      :parts: 1

.. autoclass:: UnsupportedFortranType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: UnsupportedFortranType
      :parts: 1

.. autoclass:: UnresolvedType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: UnresolvedType
      :parts: 1

.. autoclass:: ScalarType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ScalarType
      :parts: 1

.. autoclass:: ArrayType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ArrayType
      :parts: 1

.. autoclass:: StructureType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: StructureType
      :parts: 1
