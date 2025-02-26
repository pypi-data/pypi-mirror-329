  MODULE main_psy
    USE constants_mod, ONLY: r_def, i_def
    USE field_mod, ONLY: field_type, field_proxy_type
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_initialise_fields(field1, field2)
      USE profile_psy_data_mod, ONLY: profile_PSyDataType
      USE mesh_mod, ONLY: mesh_type
      TYPE(field_type), intent(in) :: field1, field2
      INTEGER(KIND=i_def) df
      TYPE(profile_PSyDataType), target, save :: profile_psy_data
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
      CALL profile_psy_data%PreStart("main_psy", "invoke_initialise_fields-r0", 0, 0)
      !$acc enter data copyin(field1_data,field2_data)
      !
      !$acc kernels
      DO df = loop0_start, loop0_stop, 1
        ! Built-in: setval_c (set a real-valued field to a real scalar value)
        field1_data(df) = 0.1_r_def
      END DO
      !$acc end kernels
      !
      ! Set halos dirty/clean for fields modified in the above loop(s)
      !
      CALL field1_proxy%set_dirty()
      !
      ! End of set dirty/clean section for above loop(s)
      !
      !$acc kernels
      DO df = loop1_start, loop1_stop, 1
        ! Built-in: setval_c (set a real-valued field to a real scalar value)
        field2_data(df) = 0.2_r_def
      END DO
      !$acc end kernels
      !
      ! Set halos dirty/clean for fields modified in the above loop(s)
      !
      CALL field2_proxy%set_dirty()
      !
      ! End of set dirty/clean section for above loop(s)
      !
      CALL profile_psy_data%PostEnd
      !
    END SUBROUTINE invoke_initialise_fields
    SUBROUTINE invoke_testkern_w0(field1, field2)
      USE testkern_w0_kernel_0_mod, ONLY: testkern_w0_0_code
      USE profile_psy_data_mod, ONLY: profile_PSyDataType
      USE mesh_mod, ONLY: mesh_type
      TYPE(field_type), intent(in) :: field1, field2
      INTEGER(KIND=i_def) cell
      INTEGER(KIND=i_def) colour
      TYPE(profile_PSyDataType), target, save :: profile_psy_data
      INTEGER(KIND=i_def) loop1_start
      INTEGER(KIND=i_def) loop0_start, loop0_stop
      INTEGER(KIND=i_def) nlayers_field1
      REAL(KIND=r_def), pointer, dimension(:) :: field2_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: field1_data => null()
      TYPE(field_proxy_type) field1_proxy, field2_proxy
      INTEGER(KIND=i_def), pointer :: map_w0(:,:) => null()
      INTEGER(KIND=i_def) ndf_w0, undf_w0
      INTEGER(KIND=i_def), allocatable :: last_halo_cell_all_colours(:,:)
      INTEGER(KIND=i_def) ncolour
      INTEGER(KIND=i_def), pointer :: cmap(:,:)
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
      ! Get the colourmap
      !
      ncolour = mesh%get_ncolours()
      cmap => mesh%get_colour_map()
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
      ! Initialise mesh properties
      !
      last_halo_cell_all_colours = mesh%get_last_halo_cell_all_colours()
      !
      ! Set-up all of the loop bounds
      !
      loop0_start = 1
      loop0_stop = ncolour
      loop1_start = 1
      !
      ! Call kernels and communication routines
      !
      CALL profile_psy_data%PreStart("main_psy", "invoke_testkern_w0-testkern_w0_code-r1", 0, 0)
      IF (field1_proxy%is_dirty(depth=1)) THEN
        CALL field1_proxy%halo_exchange(depth=1)
      END IF
      IF (field2_proxy%is_dirty(depth=1)) THEN
        CALL field2_proxy%halo_exchange(depth=1)
      END IF
      !$acc enter data copyin(field1_data,field2_data,map_w0,ndf_w0,nlayers_field1,undf_w0)
      !
      DO colour = loop0_start, loop0_stop, 1
        !$acc kernels
        DO cell = loop1_start, last_halo_cell_all_colours(colour,1), 1
          CALL testkern_w0_0_code(nlayers_field1, field1_data, field2_data, ndf_w0, undf_w0, map_w0(:,cmap(colour,cell)))
        END DO
        !$acc end kernels
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL field1_proxy%set_dirty()
      !
      CALL profile_psy_data%PostEnd
      !
    END SUBROUTINE invoke_testkern_w0
    SUBROUTINE invoke_2(field2, chksm)
      USE profile_psy_data_mod, ONLY: profile_PSyDataType
      USE mesh_mod, ONLY: mesh_type
      REAL(KIND=r_def), intent(in) :: chksm
      TYPE(field_type), intent(in) :: field2
      INTEGER(KIND=i_def) df
      TYPE(profile_PSyDataType), target, save :: profile_psy_data
      INTEGER(KIND=i_def) loop0_start, loop0_stop
      REAL(KIND=r_def), pointer, dimension(:) :: field2_data => null()
      TYPE(field_proxy_type) field2_proxy
      INTEGER(KIND=i_def) max_halo_depth_mesh
      TYPE(mesh_type), pointer :: mesh => null()
      !
      ! Initialise field and/or operator proxies
      !
      field2_proxy = field2%get_proxy()
      field2_data => field2_proxy%data
      !
      ! Create a mesh object
      !
      mesh => field2_proxy%vspace%get_mesh()
      max_halo_depth_mesh = mesh%get_halo_depth()
      !
      ! Set-up all of the loop bounds
      !
      loop0_start = 1
      loop0_stop = field2_proxy%vspace%get_last_dof_owned()
      !
      ! Call kernels and communication routines
      !
      CALL profile_psy_data%PreStart("main_psy", "invoke_2-setval_c-r2", 0, 0)
      !$acc enter data copyin(field2_data)
      !
      !$acc kernels
      DO df = loop0_start, loop0_stop, 1
        ! Built-in: setval_c (set a real-valued field to a real scalar value)
        field2_data(df) = chksm
      END DO
      !$acc end kernels
      !
      ! Set halos dirty/clean for fields modified in the above loop(s)
      !
      CALL field2_proxy%set_dirty()
      !
      ! End of set dirty/clean section for above loop(s)
      !
      CALL profile_psy_data%PostEnd
      !
    END SUBROUTINE invoke_2
  END MODULE main_psy