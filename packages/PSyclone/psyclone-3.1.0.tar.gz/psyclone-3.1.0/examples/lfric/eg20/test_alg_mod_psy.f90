  MODULE test_alg_mod_psy
    USE constants_mod, ONLY: r_def, i_def
    USE field_mod, ONLY: field_type, field_proxy_type
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_0(field_2, field_3, field_4, field_5, rscalar_1)
      USE testkern_mod, ONLY: testkern_code
      USE mesh_mod, ONLY: mesh_type
      REAL(KIND=r_def), intent(in) :: rscalar_1
      TYPE(field_type), intent(in) :: field_2, field_3, field_4, field_5
      INTEGER(KIND=i_def) cell
      INTEGER(KIND=i_def) df
      INTEGER(KIND=i_def) loop4_start, loop4_stop
      INTEGER(KIND=i_def) loop3_start, loop3_stop
      INTEGER(KIND=i_def) loop2_start, loop2_stop
      INTEGER(KIND=i_def) loop1_start, loop1_stop
      INTEGER(KIND=i_def) loop0_start, loop0_stop
      INTEGER(KIND=i_def) nlayers_field_2
      REAL(KIND=r_def), pointer, dimension(:) :: field_5_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: field_4_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: field_3_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: field_2_data => null()
      TYPE(field_proxy_type) field_2_proxy, field_3_proxy, field_4_proxy, field_5_proxy
      INTEGER(KIND=i_def), pointer :: map_w1(:,:) => null(), map_w2(:,:) => null(), map_w3(:,:) => null()
      INTEGER(KIND=i_def) ndf_aspc1_field_2, undf_aspc1_field_2, ndf_aspc1_field_3, undf_aspc1_field_3, ndf_aspc1_field_4, &
&undf_aspc1_field_4, ndf_aspc1_field_5, undf_aspc1_field_5, ndf_w1, undf_w1, ndf_w2, undf_w2, ndf_w3, undf_w3
      INTEGER(KIND=i_def) max_halo_depth_mesh
      TYPE(mesh_type), pointer :: mesh => null()
      !
      ! Initialise field and/or operator proxies
      !
      field_2_proxy = field_2%get_proxy()
      field_2_data => field_2_proxy%data
      field_3_proxy = field_3%get_proxy()
      field_3_data => field_3_proxy%data
      field_4_proxy = field_4%get_proxy()
      field_4_data => field_4_proxy%data
      field_5_proxy = field_5%get_proxy()
      field_5_data => field_5_proxy%data
      !
      ! Initialise number of layers
      !
      nlayers_field_2 = field_2_proxy%vspace%get_nlayers()
      !
      ! Create a mesh object
      !
      mesh => field_2_proxy%vspace%get_mesh()
      max_halo_depth_mesh = mesh%get_halo_depth()
      !
      ! Look-up dofmaps for each function space
      !
      map_w1 => field_2_proxy%vspace%get_whole_dofmap()
      map_w2 => field_3_proxy%vspace%get_whole_dofmap()
      map_w3 => field_5_proxy%vspace%get_whole_dofmap()
      !
      ! Initialise number of DoFs for aspc1_field_2
      !
      ndf_aspc1_field_2 = field_2_proxy%vspace%get_ndf()
      undf_aspc1_field_2 = field_2_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_field_3
      !
      ndf_aspc1_field_3 = field_3_proxy%vspace%get_ndf()
      undf_aspc1_field_3 = field_3_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_field_4
      !
      ndf_aspc1_field_4 = field_4_proxy%vspace%get_ndf()
      undf_aspc1_field_4 = field_4_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_field_5
      !
      ndf_aspc1_field_5 = field_5_proxy%vspace%get_ndf()
      undf_aspc1_field_5 = field_5_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for w1
      !
      ndf_w1 = field_2_proxy%vspace%get_ndf()
      undf_w1 = field_2_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for w2
      !
      ndf_w2 = field_3_proxy%vspace%get_ndf()
      undf_w2 = field_3_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for w3
      !
      ndf_w3 = field_5_proxy%vspace%get_ndf()
      undf_w3 = field_5_proxy%vspace%get_undf()
      !
      ! Set-up all of the loop bounds
      !
      loop0_start = 1
      loop0_stop = field_2_proxy%vspace%get_last_dof_owned()
      loop1_start = 1
      loop1_stop = field_3_proxy%vspace%get_last_dof_owned()
      loop2_start = 1
      loop2_stop = field_4_proxy%vspace%get_last_dof_owned()
      loop3_start = 1
      loop3_stop = field_5_proxy%vspace%get_last_dof_owned()
      loop4_start = 1
      loop4_stop = mesh%get_last_halo_cell(1)
      !
      ! Call kernels and communication routines
      !
      DO df = loop0_start, loop0_stop, 1
        ! Built-in: setval_c (set a real-valued field to a real scalar value)
        field_2_data(df) = 1.0_r_def
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL field_2_proxy%set_dirty()
      !
      DO df = loop1_start, loop1_stop, 1
        ! Built-in: setval_c (set a real-valued field to a real scalar value)
        field_3_data(df) = 1.0_r_def
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL field_3_proxy%set_dirty()
      !
      DO df = loop2_start, loop2_stop, 1
        ! Built-in: setval_c (set a real-valued field to a real scalar value)
        field_4_data(df) = 1.0_r_def
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL field_4_proxy%set_dirty()
      !
      DO df = loop3_start, loop3_stop, 1
        ! Built-in: setval_c (set a real-valued field to a real scalar value)
        field_5_data(df) = 1.0_r_def
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL field_5_proxy%set_dirty()
      !
      CALL field_2_proxy%halo_exchange(depth=1)
      CALL field_3_proxy%halo_exchange(depth=1)
      CALL field_4_proxy%halo_exchange(depth=1)
      CALL field_5_proxy%halo_exchange(depth=1)
      DO cell = loop4_start, loop4_stop, 1
        CALL testkern_code(nlayers_field_2, rscalar_1, field_2_data, field_3_data, field_4_data, field_5_data, ndf_w1, undf_w1, &
&map_w1(:,cell), ndf_w2, undf_w2, map_w2(:,cell), ndf_w3, undf_w3, map_w3(:,cell))
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL field_2_proxy%set_dirty()
      !
      !
    END SUBROUTINE invoke_0
  END MODULE test_alg_mod_psy