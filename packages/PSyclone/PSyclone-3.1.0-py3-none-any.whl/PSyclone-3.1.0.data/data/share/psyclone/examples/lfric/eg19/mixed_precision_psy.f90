  MODULE mixed_precision_psy
    USE constants_mod, ONLY: r_tran, r_solver, r_phys, r_def, r_bl, i_def
    USE field_mod, ONLY: field_type, field_proxy_type
    USE r_solver_field_mod, ONLY: r_solver_field_type, r_solver_field_proxy_type
    USE r_tran_field_mod, ONLY: r_tran_field_type, r_tran_field_proxy_type
    USE r_bl_field_mod, ONLY: r_bl_field_type, r_bl_field_proxy_type
    USE r_phys_field_mod, ONLY: r_phys_field_type, r_phys_field_proxy_type
    USE operator_mod, ONLY: operator_type, operator_proxy_type
    USE r_solver_operator_mod, ONLY: r_solver_operator_type, r_solver_operator_proxy_type
    USE r_tran_operator_mod, ONLY: r_tran_operator_type, r_tran_operator_proxy_type
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_0(scalar_r_def, field_r_def, operator_r_def, scalar_r_solver, field_r_solver, operator_r_solver, &
&scalar_r_tran, field_r_tran, operator_r_tran, scalar_r_bl, field_r_bl, scalar_r_phys, field_r_phys)
      USE mixed_kernel_mod, ONLY: mixed_code
      USE mesh_mod, ONLY: mesh_type
      REAL(KIND=r_def), intent(in) :: scalar_r_def
      REAL(KIND=r_solver), intent(in) :: scalar_r_solver
      REAL(KIND=r_tran), intent(in) :: scalar_r_tran
      REAL(KIND=r_bl), intent(in) :: scalar_r_bl
      REAL(KIND=r_phys), intent(in) :: scalar_r_phys
      TYPE(field_type), intent(in) :: field_r_def
      TYPE(r_solver_field_type), intent(in) :: field_r_solver
      TYPE(r_tran_field_type), intent(in) :: field_r_tran
      TYPE(r_bl_field_type), intent(in) :: field_r_bl
      TYPE(r_phys_field_type), intent(in) :: field_r_phys
      TYPE(operator_type), intent(in) :: operator_r_def
      TYPE(r_solver_operator_type), intent(in) :: operator_r_solver
      TYPE(r_tran_operator_type), intent(in) :: operator_r_tran
      INTEGER(KIND=i_def) cell
      INTEGER(KIND=i_def) loop4_start, loop4_stop
      INTEGER(KIND=i_def) loop3_start, loop3_stop
      INTEGER(KIND=i_def) loop2_start, loop2_stop
      INTEGER(KIND=i_def) loop1_start, loop1_stop
      INTEGER(KIND=i_def) loop0_start, loop0_stop
      INTEGER(KIND=i_def) nlayers_field_r_bl, nlayers_field_r_def, nlayers_field_r_phys, nlayers_field_r_solver, &
&nlayers_field_r_tran
      REAL(KIND=r_tran), pointer, dimension(:,:,:) :: operator_r_tran_local_stencil => null()
      TYPE(r_tran_operator_proxy_type) operator_r_tran_proxy
      REAL(KIND=r_solver), pointer, dimension(:,:,:) :: operator_r_solver_local_stencil => null()
      TYPE(r_solver_operator_proxy_type) operator_r_solver_proxy
      REAL(KIND=r_def), pointer, dimension(:,:,:) :: operator_r_def_local_stencil => null()
      TYPE(operator_proxy_type) operator_r_def_proxy
      REAL(KIND=r_phys), pointer, dimension(:) :: field_r_phys_data => null()
      TYPE(r_phys_field_proxy_type) field_r_phys_proxy
      REAL(KIND=r_bl), pointer, dimension(:) :: field_r_bl_data => null()
      TYPE(r_bl_field_proxy_type) field_r_bl_proxy
      REAL(KIND=r_tran), pointer, dimension(:) :: field_r_tran_data => null()
      TYPE(r_tran_field_proxy_type) field_r_tran_proxy
      REAL(KIND=r_solver), pointer, dimension(:) :: field_r_solver_data => null()
      TYPE(r_solver_field_proxy_type) field_r_solver_proxy
      REAL(KIND=r_def), pointer, dimension(:) :: field_r_def_data => null()
      TYPE(field_proxy_type) field_r_def_proxy
      INTEGER(KIND=i_def), pointer :: map_w3(:,:) => null()
      INTEGER(KIND=i_def) ndf_w3, undf_w3, ndf_w0
      INTEGER(KIND=i_def) max_halo_depth_mesh
      TYPE(mesh_type), pointer :: mesh => null()
      !
      ! Initialise field and/or operator proxies
      !
      field_r_def_proxy = field_r_def%get_proxy()
      field_r_def_data => field_r_def_proxy%data
      operator_r_def_proxy = operator_r_def%get_proxy()
      operator_r_def_local_stencil => operator_r_def_proxy%local_stencil
      field_r_solver_proxy = field_r_solver%get_proxy()
      field_r_solver_data => field_r_solver_proxy%data
      operator_r_solver_proxy = operator_r_solver%get_proxy()
      operator_r_solver_local_stencil => operator_r_solver_proxy%local_stencil
      field_r_tran_proxy = field_r_tran%get_proxy()
      field_r_tran_data => field_r_tran_proxy%data
      operator_r_tran_proxy = operator_r_tran%get_proxy()
      operator_r_tran_local_stencil => operator_r_tran_proxy%local_stencil
      field_r_bl_proxy = field_r_bl%get_proxy()
      field_r_bl_data => field_r_bl_proxy%data
      field_r_phys_proxy = field_r_phys%get_proxy()
      field_r_phys_data => field_r_phys_proxy%data
      !
      ! Initialise number of layers
      !
      nlayers_field_r_bl = field_r_bl_proxy%vspace%get_nlayers()
      nlayers_field_r_def = field_r_def_proxy%vspace%get_nlayers()
      nlayers_field_r_phys = field_r_phys_proxy%vspace%get_nlayers()
      nlayers_field_r_solver = field_r_solver_proxy%vspace%get_nlayers()
      nlayers_field_r_tran = field_r_tran_proxy%vspace%get_nlayers()
      !
      ! Create a mesh object
      !
      mesh => field_r_def_proxy%vspace%get_mesh()
      max_halo_depth_mesh = mesh%get_halo_depth()
      !
      ! Look-up dofmaps for each function space
      !
      map_w3 => field_r_def_proxy%vspace%get_whole_dofmap()
      !
      ! Initialise number of DoFs for w3
      !
      ndf_w3 = field_r_def_proxy%vspace%get_ndf()
      undf_w3 = field_r_def_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for w0
      !
      ndf_w0 = operator_r_def_proxy%fs_from%get_ndf()
      !
      ! Set-up all of the loop bounds
      !
      loop0_start = 1
      loop0_stop = mesh%get_last_edge_cell()
      loop1_start = 1
      loop1_stop = mesh%get_last_edge_cell()
      loop2_start = 1
      loop2_stop = mesh%get_last_edge_cell()
      loop3_start = 1
      loop3_stop = mesh%get_last_edge_cell()
      loop4_start = 1
      loop4_stop = mesh%get_last_edge_cell()
      !
      ! Call kernels and communication routines
      !
      DO cell = loop0_start, loop0_stop, 1
        CALL mixed_code(cell, nlayers_field_r_def, scalar_r_def, field_r_def_data, operator_r_def_proxy%ncell_3d, &
&operator_r_def_local_stencil, ndf_w3, undf_w3, map_w3(:,cell), ndf_w0)
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL field_r_def_proxy%set_dirty()
      !
      DO cell = loop1_start, loop1_stop, 1
        CALL mixed_code(cell, nlayers_field_r_solver, scalar_r_solver, field_r_solver_data, operator_r_solver_proxy%ncell_3d, &
&operator_r_solver_local_stencil, ndf_w3, undf_w3, map_w3(:,cell), ndf_w0)
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL field_r_solver_proxy%set_dirty()
      !
      DO cell = loop2_start, loop2_stop, 1
        CALL mixed_code(cell, nlayers_field_r_tran, scalar_r_tran, field_r_tran_data, operator_r_tran_proxy%ncell_3d, &
&operator_r_tran_local_stencil, ndf_w3, undf_w3, map_w3(:,cell), ndf_w0)
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL field_r_tran_proxy%set_dirty()
      !
      DO cell = loop3_start, loop3_stop, 1
        CALL mixed_code(cell, nlayers_field_r_bl, scalar_r_bl, field_r_bl_data, operator_r_tran_proxy%ncell_3d, &
&operator_r_tran_local_stencil, ndf_w3, undf_w3, map_w3(:,cell), ndf_w0)
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL field_r_bl_proxy%set_dirty()
      !
      DO cell = loop4_start, loop4_stop, 1
        CALL mixed_code(cell, nlayers_field_r_phys, scalar_r_phys, field_r_phys_data, operator_r_def_proxy%ncell_3d, &
&operator_r_def_local_stencil, ndf_w3, undf_w3, map_w3(:,cell), ndf_w0)
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL field_r_phys_proxy%set_dirty()
      !
      !
    END SUBROUTINE invoke_0
  END MODULE mixed_precision_psy