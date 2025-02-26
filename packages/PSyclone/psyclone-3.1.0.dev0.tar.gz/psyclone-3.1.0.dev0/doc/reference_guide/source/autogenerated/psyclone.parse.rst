==================
``psyclone.parse``
==================

.. automodule:: psyclone.parse

   .. contents::
      :local:


Submodules
==========

.. toctree::

   psyclone.parse.algorithm
   psyclone.parse.file_info
   psyclone.parse.kernel
   psyclone.parse.module_info
   psyclone.parse.module_manager
   psyclone.parse.utils

.. currentmodule:: psyclone.parse


Classes
=======

- :py:class:`FileInfo`:
  This class stores mostly cached information about source code:

- :py:class:`ModuleInfo`:
  This class stores mostly memory-cached information about a Fortran

- :py:class:`ModuleManager`:
  This class implements a singleton that manages module


.. autoclass:: FileInfo
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: FileInfo
      :parts: 1

.. autoclass:: ModuleInfo
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ModuleInfo
      :parts: 1

.. autoclass:: ModuleManager
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ModuleManager
      :parts: 1


Exceptions
==========

- :py:exc:`FileInfoFParserError`:
  Triggered when generation of FParser tree failed

- :py:exc:`ModuleInfoError`:
  PSyclone-specific exception for use when an error with the module manager


.. autoexception:: FileInfoFParserError

   .. rubric:: Inheritance
   .. inheritance-diagram:: FileInfoFParserError
      :parts: 1

.. autoexception:: ModuleInfoError

   .. rubric:: Inheritance
   .. inheritance-diagram:: ModuleInfoError
      :parts: 1
