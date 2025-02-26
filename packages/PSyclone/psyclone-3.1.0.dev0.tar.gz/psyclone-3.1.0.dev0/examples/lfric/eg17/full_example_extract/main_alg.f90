PROGRAM main
  USE main_psy, ONLY: invoke_testkern_w0
  USE main_psy, ONLY: invoke_initialise_fields
  USE global_mesh_base_mod, ONLY: global_mesh_base_type
  USE mesh_mod, ONLY: mesh_type, PLANE
  USE partition_mod, ONLY: partition_type, partitioner_planar, partitioner_interface
  USE extrusion_mod, ONLY: uniform_extrusion_type
  USE function_space_mod, ONLY: function_space_type
  USE fs_continuity_mod, ONLY: W0, W1, W2, W2V, W2H
  USE field_mod, ONLY: field_type
  USE constants_mod, ONLY: r_def, i_def, l_def
  USE log_mod, ONLY: LOG_LEVEL_ALWAYS
  IMPLICIT NONE
  TYPE(global_mesh_base_type), TARGET :: global_mesh
  CLASS(global_mesh_base_type), POINTER :: global_mesh_ptr
  TYPE(partition_type) :: partition
  TYPE(mesh_type), TARGET :: mesh
  TYPE(uniform_extrusion_type), TARGET :: extrusion
  TYPE(uniform_extrusion_type), POINTER :: extrusion_ptr
  TYPE(function_space_type), TARGET :: vector_space
  TYPE(function_space_type), POINTER :: vector_space_ptr
  PROCEDURE(partitioner_interface), POINTER :: partitioner_ptr
  TYPE(field_type) :: field1, field2
  TYPE(field_type) :: chi(3)
  INTEGER(KIND = i_def) :: lfric_fs = W0
  INTEGER(KIND = i_def) :: element_order_h = 1
  INTEGER(KIND = i_def) :: element_order_v = 1
  INTEGER(KIND = i_def) :: ndata_sz
  REAL(KIND = r_def) :: one
  LOGICAL(KIND = l_def) :: some_logical
  INTEGER :: i, ierr
  global_mesh = global_mesh_base_type()
  global_mesh_ptr => global_mesh
  partitioner_ptr => partitioner_planar
  partition = partition_type(global_mesh_ptr, partitioner_ptr, 1, 1, 0, 0, 1)
  extrusion = uniform_extrusion_type(0.0_r_def, 100.0_r_def, 5)
  extrusion_ptr => extrusion
  mesh = mesh_type(global_mesh_ptr, partition, extrusion_ptr)
  WRITE(*, *) "Mesh has", mesh % get_nlayers(), "layers."
  ndata_sz = 1
  vector_space = function_space_type(mesh, element_order_h, element_order_v, lfric_fs, ndata_sz)
  vector_space_ptr => vector_space
  DO i = 1, 3
    CALL chi(i) % initialise(vector_space = vector_space_ptr, name = "chi")
  END DO
  CALL field1 % initialise(vector_space = vector_space_ptr, name = "field1")
  CALL field2 % initialise(vector_space = vector_space_ptr, name = "field2")
  one = 1.0_r_def
  CALL invoke_initialise_fields(field1, field2, one)
  some_logical = .FALSE.
  CALL invoke_testkern_w0(field1, field2, chi, some_logical)
  CALL field1 % log_minmax(LOG_LEVEL_ALWAYS, "minmax of field1")
END PROGRAM main