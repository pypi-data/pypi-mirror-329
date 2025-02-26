==========================
``psyclone.psyir.symbols``
==========================

.. automodule:: psyclone.psyir.symbols

   .. contents::
      :local:


Submodules
==========

.. toctree::

   psyclone.psyir.symbols.containersymbol
   psyclone.psyir.symbols.data_type_symbol
   psyclone.psyir.symbols.datasymbol
   psyclone.psyir.symbols.datatypes
   psyclone.psyir.symbols.generic_interface_symbol
   psyclone.psyir.symbols.interfaces
   psyclone.psyir.symbols.intrinsic_symbol
   psyclone.psyir.symbols.routinesymbol
   psyclone.psyir.symbols.symbol
   psyclone.psyir.symbols.symbol_table
   psyclone.psyir.symbols.typed_symbol

.. currentmodule:: psyclone.psyir.symbols


Classes
=======

- :py:class:`ArgumentInterface`:
  Captures the interface to a Symbol that is accessed as a routine

- :py:class:`ArrayType`:
  Describes an array datatype. Can be an array of intrinsic types (e.g.

- :py:class:`AutomaticInterface`:
  The symbol is declared without attributes. Its data will live

- :py:class:`CommonBlockInterface`:
  A symbol declared in the local scope but acts as a global that

- :py:class:`ContainerSymbol`:
  Symbol that represents a reference to a Container. The reference

- :py:class:`DataSymbol`:
  Symbol identifying a data element. It contains information about:

- :py:class:`DataType`:
  Abstract base class from which all types are derived.

- :py:class:`DataTypeSymbol`:
  Symbol identifying a user-defined type (e.g. a derived type in Fortran).

- :py:class:`DefaultModuleInterface`:
  The symbol contains data declared in a module scope without additional

- :py:class:`GenericInterfaceSymbol`:
  Symbol identifying a generic interface that maps to a number of

- :py:class:`ImportInterface`:
  Describes the interface to a Symbol that is imported from an

- :py:class:`IntrinsicSymbol`:
  Symbol identifying a callable intrinsic routine.

- :py:class:`NoType`:
  Indicates that the associated symbol has an empty type (equivalent

- :py:class:`PreprocessorInterface`:
  The symbol exists in the file through compiler macros or preprocessor

- :py:class:`RoutineSymbol`:
  Symbol identifying a callable routine.

- :py:class:`ScalarType`:
  Describes a scalar datatype (and its precision).

- :py:class:`StaticInterface`:
  The symbol contains data that is kept alive through the execution

- :py:class:`StructureType`:
  Describes a 'structure' or 'derived' datatype that is itself composed

- :py:class:`Symbol`:
  Generic Symbol item for the Symbol Table and PSyIR References.

- :py:class:`SymbolTable`:
  Encapsulates the symbol table and provides methods to add new

- :py:class:`TypedSymbol`:
  Abstract base class for those Symbols that have an associated datatype.

- :py:class:`UnsupportedFortranType`:
  Indicates that a Fortran declaration is not supported by the PSyIR.

- :py:class:`UnknownInterface`:
  We have a symbol with a declaration but PSyclone does not support its

- :py:class:`UnsupportedType`:
  Indicates that a variable declaration is not supported by the PSyIR.

- :py:class:`UnresolvedInterface`:
  We have a symbol but we don't know where it is declared. 

- :py:class:`UnresolvedType`:
  Indicates that the type declaration has not been found yet. 


.. autoclass:: ArgumentInterface
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ArgumentInterface
      :parts: 1

.. autoclass:: ArrayType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ArrayType
      :parts: 1

.. autoclass:: AutomaticInterface
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: AutomaticInterface
      :parts: 1

.. autoclass:: CommonBlockInterface
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: CommonBlockInterface
      :parts: 1

.. autoclass:: ContainerSymbol
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ContainerSymbol
      :parts: 1

.. autoclass:: DataSymbol
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DataSymbol
      :parts: 1

.. autoclass:: DataType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DataType
      :parts: 1

.. autoclass:: DataTypeSymbol
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DataTypeSymbol
      :parts: 1

.. autoclass:: DefaultModuleInterface
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DefaultModuleInterface
      :parts: 1

.. autoclass:: GenericInterfaceSymbol
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GenericInterfaceSymbol
      :parts: 1

.. autoclass:: ImportInterface
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ImportInterface
      :parts: 1

.. autoclass:: IntrinsicSymbol
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: IntrinsicSymbol
      :parts: 1

.. autoclass:: NoType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: NoType
      :parts: 1

.. autoclass:: PreprocessorInterface
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: PreprocessorInterface
      :parts: 1

.. autoclass:: RoutineSymbol
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: RoutineSymbol
      :parts: 1

.. autoclass:: ScalarType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ScalarType
      :parts: 1

.. autoclass:: StaticInterface
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: StaticInterface
      :parts: 1

.. autoclass:: StructureType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: StructureType
      :parts: 1

.. autoclass:: Symbol
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Symbol
      :parts: 1

.. autoclass:: SymbolTable
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: SymbolTable
      :parts: 1

.. autoclass:: TypedSymbol
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: TypedSymbol
      :parts: 1

.. autoclass:: UnsupportedFortranType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: UnsupportedFortranType
      :parts: 1

.. autoclass:: UnknownInterface
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: UnknownInterface
      :parts: 1

.. autoclass:: UnsupportedType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: UnsupportedType
      :parts: 1

.. autoclass:: UnresolvedInterface
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: UnresolvedInterface
      :parts: 1

.. autoclass:: UnresolvedType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: UnresolvedType
      :parts: 1


Exceptions
==========

- :py:exc:`SymbolError`:
  PSyclone-specific exception for use with errors relating to the Symbol and


.. autoexception:: SymbolError

   .. rubric:: Inheritance
   .. inheritance-diagram:: SymbolError
      :parts: 1


Variables
=========

- :py:data:`BOOLEAN_TYPE`
- :py:data:`CHARACTER_TYPE`
- :py:data:`INTEGER_TYPE`
- :py:data:`INTEGER_SINGLE_TYPE`
- :py:data:`INTEGER_DOUBLE_TYPE`
- :py:data:`INTEGER4_TYPE`
- :py:data:`INTEGER8_TYPE`
- :py:data:`REAL_TYPE`
- :py:data:`REAL_SINGLE_TYPE`
- :py:data:`REAL_DOUBLE_TYPE`
- :py:data:`REAL4_TYPE`
- :py:data:`REAL8_TYPE`

.. autodata:: BOOLEAN_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x774937e2e270>

.. autodata:: CHARACTER_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x774937e2e690>

.. autodata:: INTEGER_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x774937e2d760>

.. autodata:: INTEGER_SINGLE_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x774937e2d8b0>

.. autodata:: INTEGER_DOUBLE_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x774937e2d640>

.. autodata:: INTEGER4_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x774937e2dbe0>

.. autodata:: INTEGER8_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x774937e2e000>

.. autodata:: REAL_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x774937e2d790>

.. autodata:: REAL_SINGLE_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x774937e2d7f0>

.. autodata:: REAL_DOUBLE_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x774937e2d7c0>

.. autodata:: REAL4_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x774937e2d880>

.. autodata:: REAL8_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x774937e2d820>
