  MODULE main_psy
    USE constants_mod, ONLY: r_def, i_def
    USE field_mod, ONLY: field_type, field_proxy_type
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_initialise_fields(field1, field2)
      USE mesh_mod, ONLY: mesh_type
      TYPE(field_type), intent(in) :: field1, field2
      INTEGER(KIND=i_def) df
      INTEGER(KIND=i_def) loop1_start, loop1_stop
      INTEGER(KIND=i_def) loop0_start, loop0_stop
      REAL(KIND=r_def), pointer, dimension(:) :: field2_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: field1_data => null()
      TYPE(field_proxy_type) field1_proxy, field2_proxy
      INTEGER(KIND=i_def) max_halo_depth_mesh
      TYPE(mesh_type), pointer :: mesh => null()
      !
      ! Initialise field and/or operator proxies
      !
      field1_proxy = field1%get_proxy()
      field1_data => field1_proxy%data
      field2_proxy = field2%get_proxy()
      field2_data => field2_proxy%data
      !
      ! Create a mesh object
      !
      mesh => field1_proxy%vspace%get_mesh()
      max_halo_depth_mesh = mesh%get_halo_depth()
      !
      ! Set-up all of the loop bounds
      !
      loop0_start = 1
      loop0_stop = field1_proxy%vspace%get_last_dof_owned()
      loop1_start = 1
      loop1_stop = field2_proxy%vspace%get_last_dof_owned()
      !
      ! Call kernels and communication routines
      !
      DO df = loop0_start, loop0_stop, 1
        ! Built-in: setval_c (set a real-valued field to a real scalar value)
        field1_data(df) = 0.0_r_def
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL field1_proxy%set_dirty()
      !
      DO df = loop1_start, loop1_stop, 1
        ! Built-in: setval_c (set a real-valued field to a real scalar value)
        field2_data(df) = 1.0_r_def
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL field2_proxy%set_dirty()
      !
      !
    END SUBROUTINE invoke_initialise_fields
    SUBROUTINE invoke_testkern_w0(field1, field2)
      USE testkern_w0_kernel_mod, ONLY: testkern_w0_code
      USE mesh_mod, ONLY: mesh_type
      TYPE(field_type), intent(in) :: field1, field2
      INTEGER(KIND=i_def) cell
      INTEGER(KIND=i_def) loop0_start, loop0_stop
      INTEGER(KIND=i_def) nlayers_field1
      REAL(KIND=r_def), pointer, dimension(:) :: field2_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: field1_data => null()
      TYPE(field_proxy_type) field1_proxy, field2_proxy
      INTEGER(KIND=i_def), pointer :: map_w0(:,:) => null()
      INTEGER(KIND=i_def) ndf_w0, undf_w0
      INTEGER(KIND=i_def) max_halo_depth_mesh
      TYPE(mesh_type), pointer :: mesh => null()
      !
      ! Initialise field and/or operator proxies
      !
      field1_proxy = field1%get_proxy()
      field1_data => field1_proxy%data
      field2_proxy = field2%get_proxy()
      field2_data => field2_proxy%data
      !
      ! Initialise number of layers
      !
      nlayers_field1 = field1_proxy%vspace%get_nlayers()
      !
      ! Create a mesh object
      !
      mesh => field1_proxy%vspace%get_mesh()
      max_halo_depth_mesh = mesh%get_halo_depth()
      !
      ! Look-up dofmaps for each function space
      !
      map_w0 => field1_proxy%vspace%get_whole_dofmap()
      !
      ! Initialise number of DoFs for w0
      !
      ndf_w0 = field1_proxy%vspace%get_ndf()
      undf_w0 = field1_proxy%vspace%get_undf()
      !
      ! Set-up all of the loop bounds
      !
      loop0_start = 1
      loop0_stop = mesh%get_last_halo_cell(1)
      !
      ! Call kernels and communication routines
      !
      IF (field1_proxy%is_dirty(depth=1)) THEN
        CALL field1_proxy%halo_exchange(depth=1)
      END IF
      IF (field2_proxy%is_dirty(depth=1)) THEN
        CALL field2_proxy%halo_exchange(depth=1)
      END IF
      DO cell = loop0_start, loop0_stop, 1
        CALL testkern_w0_code(nlayers_field1, field1_data, field2_data, ndf_w0, undf_w0, map_w0(:,cell))
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL field1_proxy%set_dirty()
      !
      !
    END SUBROUTINE invoke_testkern_w0
  END MODULE main_psy