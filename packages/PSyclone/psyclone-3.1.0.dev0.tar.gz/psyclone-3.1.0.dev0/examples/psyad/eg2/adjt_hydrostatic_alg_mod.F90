MODULE adjt_hydrostatic_alg_mod
  IMPLICIT NONE
  PUBLIC
  CONTAINS
  SUBROUTINE adjt_hydrostatic_alg(mesh, chi, panel_id)
    USE adjt_hydrostatic_alg_mod_psy, ONLY: invoke_1
    USE adjt_hydrostatic_alg_mod_psy, ONLY: invoke_0
    USE constants_mod, ONLY: i_def, r_def
    USE field_mod, ONLY: field_type
    USE finite_element_config_mod, ONLY: element_order_h, element_order_v
    USE fs_continuity_mod, ONLY: w2, w3, wtheta
    USE function_space_collection_mod, ONLY: function_space_collection
    USE function_space_mod, ONLY: function_space_type
    USE log_mod, ONLY: log_event, log_level_error, log_level_info, log_scratch_space
    USE mesh_mod, ONLY: mesh_type
    USE quadrature_rule_gaussian_mod, ONLY: quadrature_rule_gaussian_type
    USE quadrature_xyoz_mod, ONLY: quadrature_xyoz_type
    USE setop_random_kernel_mod, ONLY: setop_random_kernel_type
    REAL(KIND = r_def), PARAMETER :: overall_tolerance = 1500.0_r_def
    TYPE(mesh_type), POINTER, INTENT(IN) :: mesh
    TYPE(field_type), DIMENSION(3), INTENT(IN), OPTIONAL :: chi
    TYPE(field_type), INTENT(IN), OPTIONAL :: panel_id
    TYPE(function_space_type), POINTER :: vector_space_w2_ptr
    TYPE(function_space_type), POINTER :: vector_space_w3_ptr
    TYPE(function_space_type), POINTER :: vector_space_wtheta_ptr
    TYPE(field_type) :: r_u
    TYPE(field_type) :: exner
    TYPE(field_type) :: theta
    TYPE(field_type), DIMENSION(3) :: moist_dyn_fac
    TYPE(field_type) :: ls_exner
    TYPE(field_type) :: ls_theta
    TYPE(field_type), DIMENSION(3) :: ls_moist_dyn_fac
    REAL(KIND = r_def) :: cp
    TYPE(quadrature_xyoz_type) :: qr_xyoz
    TYPE(quadrature_rule_gaussian_type) :: quadrature_rule
    REAL(KIND = r_def) :: cp_input
    TYPE(field_type) :: r_u_input
    TYPE(field_type) :: exner_input
    TYPE(field_type) :: theta_input
    TYPE(field_type), DIMENSION(3) :: moist_dyn_fac_input
    TYPE(field_type) :: ls_exner_input
    TYPE(field_type) :: ls_theta_input
    TYPE(field_type), DIMENSION(3) :: ls_moist_dyn_fac_input
    REAL(KIND = r_def) :: r_u_inner_prod
    REAL(KIND = r_def) :: exner_inner_prod
    REAL(KIND = r_def) :: theta_inner_prod
    REAL(KIND = r_def), DIMENSION(3) :: moist_dyn_fac_inner_prod
    REAL(KIND = r_def) :: ls_exner_inner_prod
    REAL(KIND = r_def) :: ls_theta_inner_prod
    REAL(KIND = r_def), DIMENSION(3) :: ls_moist_dyn_fac_inner_prod
    REAL(KIND = r_def) :: inner1
    REAL(KIND = r_def) :: r_u_r_u_input_inner_prod
    REAL(KIND = r_def) :: exner_exner_input_inner_prod
    REAL(KIND = r_def) :: theta_theta_input_inner_prod
    REAL(KIND = r_def), DIMENSION(3) :: moist_dyn_fac_moist_dyn_fac_input_inner_prod
    REAL(KIND = r_def) :: ls_exner_ls_exner_input_inner_prod
    REAL(KIND = r_def) :: ls_theta_ls_theta_input_inner_prod
    REAL(KIND = r_def), DIMENSION(3) :: ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod
    REAL(KIND = r_def) :: inner2
    REAL(KIND = r_def) :: MachineTol
    REAL(KIND = r_def) :: relative_diff
    vector_space_w2_ptr => function_space_collection % get_fs(mesh, element_order_h, element_order_v, w2)
    vector_space_w3_ptr => function_space_collection % get_fs(mesh, element_order_h, element_order_v, w3)
    vector_space_wtheta_ptr => function_space_collection % get_fs(mesh, element_order_h, element_order_v, wtheta)
    CALL r_u % initialise(vector_space = vector_space_w2_ptr, name = 'r_u')
    CALL exner % initialise(vector_space = vector_space_w3_ptr, name = 'exner')
    CALL theta % initialise(vector_space = vector_space_wtheta_ptr, name = 'theta')
    CALL moist_dyn_fac(1_i_def) % initialise(vector_space = vector_space_wtheta_ptr, name = 'moist_dyn_fac')
    CALL moist_dyn_fac(2_i_def) % initialise(vector_space = vector_space_wtheta_ptr, name = 'moist_dyn_fac')
    CALL moist_dyn_fac(3_i_def) % initialise(vector_space = vector_space_wtheta_ptr, name = 'moist_dyn_fac')
    CALL ls_exner % initialise(vector_space = vector_space_w3_ptr, name = 'ls_exner')
    CALL ls_theta % initialise(vector_space = vector_space_wtheta_ptr, name = 'ls_theta')
    CALL ls_moist_dyn_fac(1_i_def) % initialise(vector_space = vector_space_wtheta_ptr, name = 'ls_moist_dyn_fac')
    CALL ls_moist_dyn_fac(2_i_def) % initialise(vector_space = vector_space_wtheta_ptr, name = 'ls_moist_dyn_fac')
    CALL ls_moist_dyn_fac(3_i_def) % initialise(vector_space = vector_space_wtheta_ptr, name = 'ls_moist_dyn_fac')
    qr_xyoz = quadrature_xyoz_type(element_order_h + 3, element_order_h + 3, element_order_v + 3, quadrature_rule)
    CALL r_u_input % initialise(vector_space = vector_space_w2_ptr, name = 'r_u_input')
    CALL exner_input % initialise(vector_space = vector_space_w3_ptr, name = 'exner_input')
    CALL theta_input % initialise(vector_space = vector_space_wtheta_ptr, name = 'theta_input')
    CALL moist_dyn_fac_input(1_i_def) % initialise(vector_space = vector_space_wtheta_ptr, name = 'moist_dyn_fac_input')
    CALL moist_dyn_fac_input(2_i_def) % initialise(vector_space = vector_space_wtheta_ptr, name = 'moist_dyn_fac_input')
    CALL moist_dyn_fac_input(3_i_def) % initialise(vector_space = vector_space_wtheta_ptr, name = 'moist_dyn_fac_input')
    CALL ls_exner_input % initialise(vector_space = vector_space_w3_ptr, name = 'ls_exner_input')
    CALL ls_theta_input % initialise(vector_space = vector_space_wtheta_ptr, name = 'ls_theta_input')
    CALL ls_moist_dyn_fac_input(1_i_def) % initialise(vector_space = vector_space_wtheta_ptr, name = 'ls_moist_dyn_fac_input')
    CALL ls_moist_dyn_fac_input(2_i_def) % initialise(vector_space = vector_space_wtheta_ptr, name = 'ls_moist_dyn_fac_input')
    CALL ls_moist_dyn_fac_input(3_i_def) % initialise(vector_space = vector_space_wtheta_ptr, name = 'ls_moist_dyn_fac_input')
    CALL RANDOM_NUMBER(cp)
    cp_input = cp
    r_u_inner_prod = 0.0_r_def
    exner_inner_prod = 0.0_r_def
    theta_inner_prod = 0.0_r_def
    moist_dyn_fac_inner_prod(1_i_def) = 0.0_r_def
    moist_dyn_fac_inner_prod(2_i_def) = 0.0_r_def
    moist_dyn_fac_inner_prod(3_i_def) = 0.0_r_def
    ls_exner_inner_prod = 0.0_r_def
    ls_theta_inner_prod = 0.0_r_def
    ls_moist_dyn_fac_inner_prod(1_i_def) = 0.0_r_def
    ls_moist_dyn_fac_inner_prod(2_i_def) = 0.0_r_def
    ls_moist_dyn_fac_inner_prod(3_i_def) = 0.0_r_def
    CALL invoke_0(r_u, r_u_input, exner, exner_input, theta, theta_input, moist_dyn_fac(1_i_def), moist_dyn_fac_input(1_i_def), &
&moist_dyn_fac(2_i_def), moist_dyn_fac_input(2_i_def), moist_dyn_fac(3_i_def), moist_dyn_fac_input(3_i_def), ls_exner, &
&ls_exner_input, ls_theta, ls_theta_input, ls_moist_dyn_fac(1_i_def), ls_moist_dyn_fac_input(1_i_def), ls_moist_dyn_fac(2_i_def), &
&ls_moist_dyn_fac_input(2_i_def), ls_moist_dyn_fac(3_i_def), ls_moist_dyn_fac_input(3_i_def), moist_dyn_fac, ls_moist_dyn_fac, cp, &
&r_u_inner_prod, exner_inner_prod, theta_inner_prod, moist_dyn_fac_inner_prod(1_i_def), moist_dyn_fac_inner_prod(2_i_def), &
&moist_dyn_fac_inner_prod(3_i_def), ls_exner_inner_prod, ls_theta_inner_prod, ls_moist_dyn_fac_inner_prod(1_i_def), &
&ls_moist_dyn_fac_inner_prod(2_i_def), ls_moist_dyn_fac_inner_prod(3_i_def), qr_xyoz)
    inner1 = 0.0_r_def
    inner1 = inner1 + cp * cp
    inner1 = inner1 + r_u_inner_prod
    inner1 = inner1 + exner_inner_prod
    inner1 = inner1 + theta_inner_prod
    inner1 = inner1 + moist_dyn_fac_inner_prod(1_i_def)
    inner1 = inner1 + moist_dyn_fac_inner_prod(2_i_def)
    inner1 = inner1 + moist_dyn_fac_inner_prod(3_i_def)
    inner1 = inner1 + ls_exner_inner_prod
    inner1 = inner1 + ls_theta_inner_prod
    inner1 = inner1 + ls_moist_dyn_fac_inner_prod(1_i_def)
    inner1 = inner1 + ls_moist_dyn_fac_inner_prod(2_i_def)
    inner1 = inner1 + ls_moist_dyn_fac_inner_prod(3_i_def)
    r_u_r_u_input_inner_prod = 0.0_r_def
    exner_exner_input_inner_prod = 0.0_r_def
    theta_theta_input_inner_prod = 0.0_r_def
    moist_dyn_fac_moist_dyn_fac_input_inner_prod(1_i_def) = 0.0_r_def
    moist_dyn_fac_moist_dyn_fac_input_inner_prod(2_i_def) = 0.0_r_def
    moist_dyn_fac_moist_dyn_fac_input_inner_prod(3_i_def) = 0.0_r_def
    ls_exner_ls_exner_input_inner_prod = 0.0_r_def
    ls_theta_ls_theta_input_inner_prod = 0.0_r_def
    ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod(1_i_def) = 0.0_r_def
    ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod(2_i_def) = 0.0_r_def
    ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod(3_i_def) = 0.0_r_def
    CALL invoke_1(r_u, exner, theta, moist_dyn_fac, ls_exner, ls_theta, ls_moist_dyn_fac, cp, r_u_r_u_input_inner_prod, r_u_input, &
&exner_exner_input_inner_prod, exner_input, theta_theta_input_inner_prod, theta_input, &
&moist_dyn_fac_moist_dyn_fac_input_inner_prod(1_i_def), moist_dyn_fac(1_i_def), moist_dyn_fac_input(1_i_def), &
&moist_dyn_fac_moist_dyn_fac_input_inner_prod(2_i_def), moist_dyn_fac(2_i_def), moist_dyn_fac_input(2_i_def), &
&moist_dyn_fac_moist_dyn_fac_input_inner_prod(3_i_def), moist_dyn_fac(3_i_def), moist_dyn_fac_input(3_i_def), &
&ls_exner_ls_exner_input_inner_prod, ls_exner_input, ls_theta_ls_theta_input_inner_prod, ls_theta_input, &
&ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod(1_i_def), ls_moist_dyn_fac(1_i_def), ls_moist_dyn_fac_input(1_i_def), &
&ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod(2_i_def), ls_moist_dyn_fac(2_i_def), ls_moist_dyn_fac_input(2_i_def), &
&ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod(3_i_def), ls_moist_dyn_fac(3_i_def), ls_moist_dyn_fac_input(3_i_def), qr_xyoz)
    inner2 = 0.0_r_def
    inner2 = inner2 + cp * cp_input
    inner2 = inner2 + r_u_r_u_input_inner_prod
    inner2 = inner2 + exner_exner_input_inner_prod
    inner2 = inner2 + theta_theta_input_inner_prod
    inner2 = inner2 + moist_dyn_fac_moist_dyn_fac_input_inner_prod(1_i_def)
    inner2 = inner2 + moist_dyn_fac_moist_dyn_fac_input_inner_prod(2_i_def)
    inner2 = inner2 + moist_dyn_fac_moist_dyn_fac_input_inner_prod(3_i_def)
    inner2 = inner2 + ls_exner_ls_exner_input_inner_prod
    inner2 = inner2 + ls_theta_ls_theta_input_inner_prod
    inner2 = inner2 + ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod(1_i_def)
    inner2 = inner2 + ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod(2_i_def)
    inner2 = inner2 + ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod(3_i_def)
    MachineTol = SPACING(MAX(ABS(inner1), ABS(inner2)))
    relative_diff = ABS(inner1 - inner2) / MachineTol
    IF (relative_diff < overall_tolerance) THEN
      WRITE(log_scratch_space, *) "PASSED tl_hydrostatic_kernel_type:", inner1, inner2, relative_diff
      CALL log_event(log_scratch_space, log_level_info)
    ELSE
      WRITE(log_scratch_space, *) "FAILED tl_hydrostatic_kernel_type:", inner1, inner2, relative_diff
      CALL log_event(log_scratch_space, log_level_error)
    END IF
  END SUBROUTINE adjt_hydrostatic_alg
END MODULE adjt_hydrostatic_alg_mod