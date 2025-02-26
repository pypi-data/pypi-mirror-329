  MODULE other_alg_mod_psy
    USE constants_mod, ONLY: r_def, i_def
    USE field_mod, ONLY: field_type, field_proxy_type
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_0(chksum1, field_1)
      USE scalar_mod, ONLY: scalar_type
      USE profile_psy_data_mod, ONLY: profile_PSyDataType
      USE mesh_mod, ONLY: mesh_type
      REAL(KIND=r_def), intent(out) :: chksum1
      TYPE(field_type), intent(in) :: field_1
      TYPE(scalar_type) global_sum
      INTEGER(KIND=i_def) df
      TYPE(profile_PSyDataType), target, save :: profile_psy_data
      INTEGER(KIND=i_def) loop0_start, loop0_stop
      REAL(KIND=r_def), pointer, dimension(:) :: field_1_data => null()
      TYPE(field_proxy_type) field_1_proxy
      INTEGER(KIND=i_def) max_halo_depth_mesh
      TYPE(mesh_type), pointer :: mesh => null()
      !
      ! Initialise field and/or operator proxies
      !
      field_1_proxy = field_1%get_proxy()
      field_1_data => field_1_proxy%data
      !
      ! Create a mesh object
      !
      mesh => field_1_proxy%vspace%get_mesh()
      max_halo_depth_mesh = mesh%get_halo_depth()
      !
      ! Set-up all of the loop bounds
      !
      loop0_start = 1
      loop0_stop = field_1_proxy%vspace%get_last_dof_owned()
      !
      ! Call kernels and communication routines
      !
      CALL profile_psy_data%PreStart("other_alg_mod_psy", "invoke_0-x_innerproduct_x-r0", 0, 0)
      !$acc enter data copyin(field_1_data)
      !
      !$acc kernels
      !
      ! Zero summation variables
      !
      chksum1 = 0.0_r_def
      !
      DO df = loop0_start, loop0_stop, 1
        ! Built-in: X_innerproduct_X (real-valued field)
        chksum1 = chksum1 + field_1_data(df) * field_1_data(df)
      END DO
      !$acc end kernels
      global_sum%value = chksum1
      chksum1 = global_sum%get_sum()
      CALL profile_psy_data%PostEnd
      !
    END SUBROUTINE invoke_0
  END MODULE other_alg_mod_psy