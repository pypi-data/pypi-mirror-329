MODULE test_alg_mod
  IMPLICIT NONE
  PUBLIC
  CONTAINS
  SUBROUTINE test_alg(mesh, chi, panel_id)
    USE test_alg_mod_psy, ONLY: invoke_0
    USE constants_mod, ONLY: i_def, r_def
    USE field_mod, ONLY: field_type
    USE finite_element_config_mod, ONLY: element_order_h, element_order_v
    USE fs_continuity_mod, ONLY: w1, w2, w3
    USE function_space_collection_mod, ONLY: function_space_collection
    USE function_space_mod, ONLY: function_space_type
    USE mesh_mod, ONLY: mesh_type
    TYPE(mesh_type), POINTER, INTENT(IN) :: mesh
    TYPE(field_type), DIMENSION(3), INTENT(IN), OPTIONAL :: chi
    TYPE(field_type), INTENT(IN), OPTIONAL :: panel_id
    TYPE(function_space_type), POINTER :: vector_space_w1_ptr
    TYPE(function_space_type), POINTER :: vector_space_w2_ptr
    TYPE(function_space_type), POINTER :: vector_space_w3_ptr
    REAL(KIND = r_def) :: rscalar_1
    TYPE(field_type) :: field_2
    TYPE(field_type) :: field_3
    TYPE(field_type) :: field_4
    TYPE(field_type) :: field_5
    vector_space_w1_ptr => function_space_collection % get_fs(mesh, element_order_h, element_order_v, w1)
    vector_space_w2_ptr => function_space_collection % get_fs(mesh, element_order_h, element_order_v, w2)
    vector_space_w3_ptr => function_space_collection % get_fs(mesh, element_order_h, element_order_v, w3)
    CALL field_2 % initialise(vector_space = vector_space_w1_ptr, name = 'field_2')
    CALL field_3 % initialise(vector_space = vector_space_w2_ptr, name = 'field_3')
    CALL field_4 % initialise(vector_space = vector_space_w2_ptr, name = 'field_4')
    CALL field_5 % initialise(vector_space = vector_space_w3_ptr, name = 'field_5')
    rscalar_1 = 1_i_def
    CALL invoke_0(field_2, field_3, field_4, field_5, rscalar_1)
  END SUBROUTINE test_alg
END MODULE test_alg_mod