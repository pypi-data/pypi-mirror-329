  MODULE adjt_hydrostatic_alg_mod_psy
    USE constants_mod, ONLY: r_def, i_def
    USE field_mod, ONLY: field_type, field_proxy_type
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_0(r_u, r_u_input, exner, exner_input, theta, theta_input, moist_dyn_fac, moist_dyn_fac_input, &
&moist_dyn_fac_1, moist_dyn_fac_input_1, moist_dyn_fac_2, moist_dyn_fac_input_2, ls_exner, ls_exner_input, ls_theta, &
&ls_theta_input, ls_moist_dyn_fac, ls_moist_dyn_fac_input, ls_moist_dyn_fac_1, ls_moist_dyn_fac_input_1, ls_moist_dyn_fac_2, &
&ls_moist_dyn_fac_input_2, moist_dyn_fac_3, ls_moist_dyn_fac_3, cp, r_u_inner_prod, exner_inner_prod, theta_inner_prod, &
&moist_dyn_fac_inner_prod, moist_dyn_fac_inner_prod_1, moist_dyn_fac_inner_prod_2, ls_exner_inner_prod, ls_theta_inner_prod, &
&ls_moist_dyn_fac_inner_prod, ls_moist_dyn_fac_inner_prod_1, ls_moist_dyn_fac_inner_prod_2, qr_xyoz)
      USE tl_hydrostatic_kernel_mod, ONLY: tl_hydrostatic_code
      USE quadrature_xyoz_mod, ONLY: quadrature_xyoz_type, quadrature_xyoz_proxy_type
      USE function_space_mod, ONLY: BASIS, DIFF_BASIS
      REAL(KIND=r_def), intent(out) :: r_u_inner_prod, exner_inner_prod, theta_inner_prod, moist_dyn_fac_inner_prod, &
&moist_dyn_fac_inner_prod_1, moist_dyn_fac_inner_prod_2, ls_exner_inner_prod, ls_theta_inner_prod, ls_moist_dyn_fac_inner_prod, &
&ls_moist_dyn_fac_inner_prod_1, ls_moist_dyn_fac_inner_prod_2
      REAL(KIND=r_def), intent(in) :: cp
      TYPE(field_type), intent(in) :: r_u, r_u_input, exner, exner_input, theta, theta_input, moist_dyn_fac, moist_dyn_fac_input, &
&moist_dyn_fac_1, moist_dyn_fac_input_1, moist_dyn_fac_2, moist_dyn_fac_input_2, ls_exner, ls_exner_input, ls_theta, &
&ls_theta_input, ls_moist_dyn_fac, ls_moist_dyn_fac_input, ls_moist_dyn_fac_1, ls_moist_dyn_fac_input_1, ls_moist_dyn_fac_2, &
&ls_moist_dyn_fac_input_2, moist_dyn_fac_3(3), ls_moist_dyn_fac_3(3)
      TYPE(quadrature_xyoz_type), intent(in) :: qr_xyoz
      INTEGER(KIND=i_def) cell
      INTEGER(KIND=i_def) df
      INTEGER(KIND=i_def) loop33_start, loop33_stop
      INTEGER(KIND=i_def) loop32_start, loop32_stop
      INTEGER(KIND=i_def) loop31_start, loop31_stop
      INTEGER(KIND=i_def) loop30_start, loop30_stop
      INTEGER(KIND=i_def) loop29_start, loop29_stop
      INTEGER(KIND=i_def) loop28_start, loop28_stop
      INTEGER(KIND=i_def) loop27_start, loop27_stop
      INTEGER(KIND=i_def) loop26_start, loop26_stop
      INTEGER(KIND=i_def) loop25_start, loop25_stop
      INTEGER(KIND=i_def) loop24_start, loop24_stop
      INTEGER(KIND=i_def) loop23_start, loop23_stop
      INTEGER(KIND=i_def) loop22_start, loop22_stop
      INTEGER(KIND=i_def) loop21_start, loop21_stop
      INTEGER(KIND=i_def) loop20_start, loop20_stop
      INTEGER(KIND=i_def) loop19_start, loop19_stop
      INTEGER(KIND=i_def) loop18_start, loop18_stop
      INTEGER(KIND=i_def) loop17_start, loop17_stop
      INTEGER(KIND=i_def) loop16_start, loop16_stop
      INTEGER(KIND=i_def) loop15_start, loop15_stop
      INTEGER(KIND=i_def) loop14_start, loop14_stop
      INTEGER(KIND=i_def) loop13_start, loop13_stop
      INTEGER(KIND=i_def) loop12_start, loop12_stop
      INTEGER(KIND=i_def) loop11_start, loop11_stop
      INTEGER(KIND=i_def) loop10_start, loop10_stop
      INTEGER(KIND=i_def) loop9_start, loop9_stop
      INTEGER(KIND=i_def) loop8_start, loop8_stop
      INTEGER(KIND=i_def) loop7_start, loop7_stop
      INTEGER(KIND=i_def) loop6_start, loop6_stop
      INTEGER(KIND=i_def) loop5_start, loop5_stop
      INTEGER(KIND=i_def) loop4_start, loop4_stop
      INTEGER(KIND=i_def) loop3_start, loop3_stop
      INTEGER(KIND=i_def) loop2_start, loop2_stop
      INTEGER(KIND=i_def) loop1_start, loop1_stop
      INTEGER(KIND=i_def) loop0_start, loop0_stop
      REAL(KIND=r_def), allocatable :: basis_any_w2_qr_xyoz(:,:,:,:), diff_basis_any_w2_qr_xyoz(:,:,:,:), &
&basis_w3_qr_xyoz(:,:,:,:), basis_wtheta_qr_xyoz(:,:,:,:), diff_basis_wtheta_qr_xyoz(:,:,:,:)
      INTEGER(KIND=i_def) dim_any_w2, diff_dim_any_w2, dim_w3, dim_wtheta, diff_dim_wtheta
      REAL(KIND=r_def), pointer :: weights_xy_qr_xyoz(:) => null(), weights_z_qr_xyoz(:) => null()
      INTEGER(KIND=i_def) np_xy_qr_xyoz, np_z_qr_xyoz
      INTEGER(KIND=i_def) nlayers_r_u
      REAL(KIND=r_def), pointer, dimension(:) :: ls_moist_dyn_fac_3_1_data => null(), ls_moist_dyn_fac_3_2_data => null(), &
&ls_moist_dyn_fac_3_3_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: moist_dyn_fac_3_1_data => null(), moist_dyn_fac_3_2_data => null(), &
&moist_dyn_fac_3_3_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: ls_moist_dyn_fac_input_2_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: ls_moist_dyn_fac_2_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: ls_moist_dyn_fac_input_1_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: ls_moist_dyn_fac_1_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: ls_moist_dyn_fac_input_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: ls_moist_dyn_fac_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: ls_theta_input_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: ls_theta_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: ls_exner_input_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: ls_exner_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: moist_dyn_fac_input_2_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: moist_dyn_fac_2_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: moist_dyn_fac_input_1_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: moist_dyn_fac_1_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: moist_dyn_fac_input_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: moist_dyn_fac_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: theta_input_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: theta_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: exner_input_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: exner_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: r_u_input_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: r_u_data => null()
      TYPE(field_proxy_type) r_u_proxy, r_u_input_proxy, exner_proxy, exner_input_proxy, theta_proxy, theta_input_proxy, &
&moist_dyn_fac_proxy, moist_dyn_fac_input_proxy, moist_dyn_fac_1_proxy, moist_dyn_fac_input_1_proxy, moist_dyn_fac_2_proxy, &
&moist_dyn_fac_input_2_proxy, ls_exner_proxy, ls_exner_input_proxy, ls_theta_proxy, ls_theta_input_proxy, ls_moist_dyn_fac_proxy, &
&ls_moist_dyn_fac_input_proxy, ls_moist_dyn_fac_1_proxy, ls_moist_dyn_fac_input_1_proxy, ls_moist_dyn_fac_2_proxy, &
&ls_moist_dyn_fac_input_2_proxy, moist_dyn_fac_3_proxy(3), ls_moist_dyn_fac_3_proxy(3)
      TYPE(quadrature_xyoz_proxy_type) qr_xyoz_proxy
      INTEGER(KIND=i_def), pointer :: map_any_w2(:,:) => null(), map_w3(:,:) => null(), map_wtheta(:,:) => null()
      INTEGER(KIND=i_def) ndf_aspc1_r_u, undf_aspc1_r_u, ndf_aspc1_r_u_input, undf_aspc1_r_u_input, ndf_aspc1_exner, &
&undf_aspc1_exner, ndf_aspc1_exner_input, undf_aspc1_exner_input, ndf_aspc1_theta, undf_aspc1_theta, ndf_aspc1_theta_input, &
&undf_aspc1_theta_input, ndf_aspc1_moist_dyn_fac, undf_aspc1_moist_dyn_fac, ndf_aspc1_moist_dyn_fac_input, &
&undf_aspc1_moist_dyn_fac_input, ndf_aspc1_moist_dyn_fac_1, undf_aspc1_moist_dyn_fac_1, ndf_aspc1_moist_dyn_fac_input_1, &
&undf_aspc1_moist_dyn_fac_input_1, ndf_aspc1_moist_dyn_fac_2, undf_aspc1_moist_dyn_fac_2, ndf_aspc1_moist_dyn_fac_input_2, &
&undf_aspc1_moist_dyn_fac_input_2, ndf_aspc1_ls_exner, undf_aspc1_ls_exner, ndf_aspc1_ls_exner_input, undf_aspc1_ls_exner_input, &
&ndf_aspc1_ls_theta, undf_aspc1_ls_theta, ndf_aspc1_ls_theta_input, undf_aspc1_ls_theta_input, ndf_aspc1_ls_moist_dyn_fac, &
&undf_aspc1_ls_moist_dyn_fac, ndf_aspc1_ls_moist_dyn_fac_input, undf_aspc1_ls_moist_dyn_fac_input, ndf_aspc1_ls_moist_dyn_fac_1, &
&undf_aspc1_ls_moist_dyn_fac_1, ndf_aspc1_ls_moist_dyn_fac_input_1, undf_aspc1_ls_moist_dyn_fac_input_1, &
&ndf_aspc1_ls_moist_dyn_fac_2, undf_aspc1_ls_moist_dyn_fac_2, ndf_aspc1_ls_moist_dyn_fac_input_2, &
&undf_aspc1_ls_moist_dyn_fac_input_2, ndf_any_w2, undf_any_w2, ndf_w3, undf_w3, ndf_wtheta, undf_wtheta
      !
      ! Initialise field and/or operator proxies
      !
      r_u_proxy = r_u%get_proxy()
      r_u_data => r_u_proxy%data
      r_u_input_proxy = r_u_input%get_proxy()
      r_u_input_data => r_u_input_proxy%data
      exner_proxy = exner%get_proxy()
      exner_data => exner_proxy%data
      exner_input_proxy = exner_input%get_proxy()
      exner_input_data => exner_input_proxy%data
      theta_proxy = theta%get_proxy()
      theta_data => theta_proxy%data
      theta_input_proxy = theta_input%get_proxy()
      theta_input_data => theta_input_proxy%data
      moist_dyn_fac_proxy = moist_dyn_fac%get_proxy()
      moist_dyn_fac_data => moist_dyn_fac_proxy%data
      moist_dyn_fac_input_proxy = moist_dyn_fac_input%get_proxy()
      moist_dyn_fac_input_data => moist_dyn_fac_input_proxy%data
      moist_dyn_fac_1_proxy = moist_dyn_fac_1%get_proxy()
      moist_dyn_fac_1_data => moist_dyn_fac_1_proxy%data
      moist_dyn_fac_input_1_proxy = moist_dyn_fac_input_1%get_proxy()
      moist_dyn_fac_input_1_data => moist_dyn_fac_input_1_proxy%data
      moist_dyn_fac_2_proxy = moist_dyn_fac_2%get_proxy()
      moist_dyn_fac_2_data => moist_dyn_fac_2_proxy%data
      moist_dyn_fac_input_2_proxy = moist_dyn_fac_input_2%get_proxy()
      moist_dyn_fac_input_2_data => moist_dyn_fac_input_2_proxy%data
      ls_exner_proxy = ls_exner%get_proxy()
      ls_exner_data => ls_exner_proxy%data
      ls_exner_input_proxy = ls_exner_input%get_proxy()
      ls_exner_input_data => ls_exner_input_proxy%data
      ls_theta_proxy = ls_theta%get_proxy()
      ls_theta_data => ls_theta_proxy%data
      ls_theta_input_proxy = ls_theta_input%get_proxy()
      ls_theta_input_data => ls_theta_input_proxy%data
      ls_moist_dyn_fac_proxy = ls_moist_dyn_fac%get_proxy()
      ls_moist_dyn_fac_data => ls_moist_dyn_fac_proxy%data
      ls_moist_dyn_fac_input_proxy = ls_moist_dyn_fac_input%get_proxy()
      ls_moist_dyn_fac_input_data => ls_moist_dyn_fac_input_proxy%data
      ls_moist_dyn_fac_1_proxy = ls_moist_dyn_fac_1%get_proxy()
      ls_moist_dyn_fac_1_data => ls_moist_dyn_fac_1_proxy%data
      ls_moist_dyn_fac_input_1_proxy = ls_moist_dyn_fac_input_1%get_proxy()
      ls_moist_dyn_fac_input_1_data => ls_moist_dyn_fac_input_1_proxy%data
      ls_moist_dyn_fac_2_proxy = ls_moist_dyn_fac_2%get_proxy()
      ls_moist_dyn_fac_2_data => ls_moist_dyn_fac_2_proxy%data
      ls_moist_dyn_fac_input_2_proxy = ls_moist_dyn_fac_input_2%get_proxy()
      ls_moist_dyn_fac_input_2_data => ls_moist_dyn_fac_input_2_proxy%data
      moist_dyn_fac_3_proxy(1) = moist_dyn_fac_3(1)%get_proxy()
      moist_dyn_fac_3_1_data => moist_dyn_fac_3_proxy(1)%data
      moist_dyn_fac_3_proxy(2) = moist_dyn_fac_3(2)%get_proxy()
      moist_dyn_fac_3_2_data => moist_dyn_fac_3_proxy(2)%data
      moist_dyn_fac_3_proxy(3) = moist_dyn_fac_3(3)%get_proxy()
      moist_dyn_fac_3_3_data => moist_dyn_fac_3_proxy(3)%data
      ls_moist_dyn_fac_3_proxy(1) = ls_moist_dyn_fac_3(1)%get_proxy()
      ls_moist_dyn_fac_3_1_data => ls_moist_dyn_fac_3_proxy(1)%data
      ls_moist_dyn_fac_3_proxy(2) = ls_moist_dyn_fac_3(2)%get_proxy()
      ls_moist_dyn_fac_3_2_data => ls_moist_dyn_fac_3_proxy(2)%data
      ls_moist_dyn_fac_3_proxy(3) = ls_moist_dyn_fac_3(3)%get_proxy()
      ls_moist_dyn_fac_3_3_data => ls_moist_dyn_fac_3_proxy(3)%data
      !
      ! Initialise number of layers
      !
      nlayers_r_u = r_u_proxy%vspace%get_nlayers()
      !
      ! Look-up dofmaps for each function space
      !
      map_any_w2 => r_u_proxy%vspace%get_whole_dofmap()
      map_w3 => exner_proxy%vspace%get_whole_dofmap()
      map_wtheta => theta_proxy%vspace%get_whole_dofmap()
      !
      ! Initialise number of DoFs for aspc1_r_u
      !
      ndf_aspc1_r_u = r_u_proxy%vspace%get_ndf()
      undf_aspc1_r_u = r_u_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_r_u_input
      !
      ndf_aspc1_r_u_input = r_u_input_proxy%vspace%get_ndf()
      undf_aspc1_r_u_input = r_u_input_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_exner
      !
      ndf_aspc1_exner = exner_proxy%vspace%get_ndf()
      undf_aspc1_exner = exner_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_exner_input
      !
      ndf_aspc1_exner_input = exner_input_proxy%vspace%get_ndf()
      undf_aspc1_exner_input = exner_input_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_theta
      !
      ndf_aspc1_theta = theta_proxy%vspace%get_ndf()
      undf_aspc1_theta = theta_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_theta_input
      !
      ndf_aspc1_theta_input = theta_input_proxy%vspace%get_ndf()
      undf_aspc1_theta_input = theta_input_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_moist_dyn_fac
      !
      ndf_aspc1_moist_dyn_fac = moist_dyn_fac_proxy%vspace%get_ndf()
      undf_aspc1_moist_dyn_fac = moist_dyn_fac_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_moist_dyn_fac_input
      !
      ndf_aspc1_moist_dyn_fac_input = moist_dyn_fac_input_proxy%vspace%get_ndf()
      undf_aspc1_moist_dyn_fac_input = moist_dyn_fac_input_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_moist_dyn_fac_1
      !
      ndf_aspc1_moist_dyn_fac_1 = moist_dyn_fac_1_proxy%vspace%get_ndf()
      undf_aspc1_moist_dyn_fac_1 = moist_dyn_fac_1_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_moist_dyn_fac_input_1
      !
      ndf_aspc1_moist_dyn_fac_input_1 = moist_dyn_fac_input_1_proxy%vspace%get_ndf()
      undf_aspc1_moist_dyn_fac_input_1 = moist_dyn_fac_input_1_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_moist_dyn_fac_2
      !
      ndf_aspc1_moist_dyn_fac_2 = moist_dyn_fac_2_proxy%vspace%get_ndf()
      undf_aspc1_moist_dyn_fac_2 = moist_dyn_fac_2_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_moist_dyn_fac_input_2
      !
      ndf_aspc1_moist_dyn_fac_input_2 = moist_dyn_fac_input_2_proxy%vspace%get_ndf()
      undf_aspc1_moist_dyn_fac_input_2 = moist_dyn_fac_input_2_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_ls_exner
      !
      ndf_aspc1_ls_exner = ls_exner_proxy%vspace%get_ndf()
      undf_aspc1_ls_exner = ls_exner_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_ls_exner_input
      !
      ndf_aspc1_ls_exner_input = ls_exner_input_proxy%vspace%get_ndf()
      undf_aspc1_ls_exner_input = ls_exner_input_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_ls_theta
      !
      ndf_aspc1_ls_theta = ls_theta_proxy%vspace%get_ndf()
      undf_aspc1_ls_theta = ls_theta_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_ls_theta_input
      !
      ndf_aspc1_ls_theta_input = ls_theta_input_proxy%vspace%get_ndf()
      undf_aspc1_ls_theta_input = ls_theta_input_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_ls_moist_dyn_fac
      !
      ndf_aspc1_ls_moist_dyn_fac = ls_moist_dyn_fac_proxy%vspace%get_ndf()
      undf_aspc1_ls_moist_dyn_fac = ls_moist_dyn_fac_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_ls_moist_dyn_fac_input
      !
      ndf_aspc1_ls_moist_dyn_fac_input = ls_moist_dyn_fac_input_proxy%vspace%get_ndf()
      undf_aspc1_ls_moist_dyn_fac_input = ls_moist_dyn_fac_input_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_ls_moist_dyn_fac_1
      !
      ndf_aspc1_ls_moist_dyn_fac_1 = ls_moist_dyn_fac_1_proxy%vspace%get_ndf()
      undf_aspc1_ls_moist_dyn_fac_1 = ls_moist_dyn_fac_1_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_ls_moist_dyn_fac_input_1
      !
      ndf_aspc1_ls_moist_dyn_fac_input_1 = ls_moist_dyn_fac_input_1_proxy%vspace%get_ndf()
      undf_aspc1_ls_moist_dyn_fac_input_1 = ls_moist_dyn_fac_input_1_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_ls_moist_dyn_fac_2
      !
      ndf_aspc1_ls_moist_dyn_fac_2 = ls_moist_dyn_fac_2_proxy%vspace%get_ndf()
      undf_aspc1_ls_moist_dyn_fac_2 = ls_moist_dyn_fac_2_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_ls_moist_dyn_fac_input_2
      !
      ndf_aspc1_ls_moist_dyn_fac_input_2 = ls_moist_dyn_fac_input_2_proxy%vspace%get_ndf()
      undf_aspc1_ls_moist_dyn_fac_input_2 = ls_moist_dyn_fac_input_2_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for any_w2
      !
      ndf_any_w2 = r_u_proxy%vspace%get_ndf()
      undf_any_w2 = r_u_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for w3
      !
      ndf_w3 = exner_proxy%vspace%get_ndf()
      undf_w3 = exner_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for wtheta
      !
      ndf_wtheta = theta_proxy%vspace%get_ndf()
      undf_wtheta = theta_proxy%vspace%get_undf()
      !
      ! Look-up quadrature variables
      !
      qr_xyoz_proxy = qr_xyoz%get_quadrature_proxy()
      np_xy_qr_xyoz = qr_xyoz_proxy%np_xy
      np_z_qr_xyoz = qr_xyoz_proxy%np_z
      weights_xy_qr_xyoz => qr_xyoz_proxy%weights_xy
      weights_z_qr_xyoz => qr_xyoz_proxy%weights_z
      !
      ! Allocate basis/diff-basis arrays
      !
      dim_any_w2 = r_u_proxy%vspace%get_dim_space()
      diff_dim_any_w2 = r_u_proxy%vspace%get_dim_space_diff()
      dim_w3 = exner_proxy%vspace%get_dim_space()
      dim_wtheta = theta_proxy%vspace%get_dim_space()
      diff_dim_wtheta = theta_proxy%vspace%get_dim_space_diff()
      ALLOCATE (basis_any_w2_qr_xyoz(dim_any_w2, ndf_any_w2, np_xy_qr_xyoz, np_z_qr_xyoz))
      ALLOCATE (diff_basis_any_w2_qr_xyoz(diff_dim_any_w2, ndf_any_w2, np_xy_qr_xyoz, np_z_qr_xyoz))
      ALLOCATE (basis_w3_qr_xyoz(dim_w3, ndf_w3, np_xy_qr_xyoz, np_z_qr_xyoz))
      ALLOCATE (basis_wtheta_qr_xyoz(dim_wtheta, ndf_wtheta, np_xy_qr_xyoz, np_z_qr_xyoz))
      ALLOCATE (diff_basis_wtheta_qr_xyoz(diff_dim_wtheta, ndf_wtheta, np_xy_qr_xyoz, np_z_qr_xyoz))
      !
      ! Compute basis/diff-basis arrays
      !
      CALL qr_xyoz%compute_function(BASIS, r_u_proxy%vspace, dim_any_w2, ndf_any_w2, basis_any_w2_qr_xyoz)
      CALL qr_xyoz%compute_function(DIFF_BASIS, r_u_proxy%vspace, diff_dim_any_w2, ndf_any_w2, diff_basis_any_w2_qr_xyoz)
      CALL qr_xyoz%compute_function(BASIS, exner_proxy%vspace, dim_w3, ndf_w3, basis_w3_qr_xyoz)
      CALL qr_xyoz%compute_function(BASIS, theta_proxy%vspace, dim_wtheta, ndf_wtheta, basis_wtheta_qr_xyoz)
      CALL qr_xyoz%compute_function(DIFF_BASIS, theta_proxy%vspace, diff_dim_wtheta, ndf_wtheta, diff_basis_wtheta_qr_xyoz)
      !
      ! Set-up all of the loop bounds
      !
      loop0_start = 1
      loop0_stop = undf_aspc1_r_u
      loop1_start = 1
      loop1_stop = undf_aspc1_r_u_input
      loop2_start = 1
      loop2_stop = undf_aspc1_exner
      loop3_start = 1
      loop3_stop = undf_aspc1_exner_input
      loop4_start = 1
      loop4_stop = undf_aspc1_theta
      loop5_start = 1
      loop5_stop = undf_aspc1_theta_input
      loop6_start = 1
      loop6_stop = undf_aspc1_moist_dyn_fac
      loop7_start = 1
      loop7_stop = undf_aspc1_moist_dyn_fac_input
      loop8_start = 1
      loop8_stop = undf_aspc1_moist_dyn_fac_1
      loop9_start = 1
      loop9_stop = undf_aspc1_moist_dyn_fac_input_1
      loop10_start = 1
      loop10_stop = undf_aspc1_moist_dyn_fac_2
      loop11_start = 1
      loop11_stop = undf_aspc1_moist_dyn_fac_input_2
      loop12_start = 1
      loop12_stop = undf_aspc1_ls_exner
      loop13_start = 1
      loop13_stop = undf_aspc1_ls_exner_input
      loop14_start = 1
      loop14_stop = undf_aspc1_ls_theta
      loop15_start = 1
      loop15_stop = undf_aspc1_ls_theta_input
      loop16_start = 1
      loop16_stop = undf_aspc1_ls_moist_dyn_fac
      loop17_start = 1
      loop17_stop = undf_aspc1_ls_moist_dyn_fac_input
      loop18_start = 1
      loop18_stop = undf_aspc1_ls_moist_dyn_fac_1
      loop19_start = 1
      loop19_stop = undf_aspc1_ls_moist_dyn_fac_input_1
      loop20_start = 1
      loop20_stop = undf_aspc1_ls_moist_dyn_fac_2
      loop21_start = 1
      loop21_stop = undf_aspc1_ls_moist_dyn_fac_input_2
      loop22_start = 1
      loop22_stop = r_u_proxy%vspace%get_ncell()
      loop23_start = 1
      loop23_stop = undf_aspc1_r_u
      loop24_start = 1
      loop24_stop = undf_aspc1_exner
      loop25_start = 1
      loop25_stop = undf_aspc1_theta
      loop26_start = 1
      loop26_stop = undf_aspc1_moist_dyn_fac
      loop27_start = 1
      loop27_stop = undf_aspc1_moist_dyn_fac_1
      loop28_start = 1
      loop28_stop = undf_aspc1_moist_dyn_fac_2
      loop29_start = 1
      loop29_stop = undf_aspc1_ls_exner
      loop30_start = 1
      loop30_stop = undf_aspc1_ls_theta
      loop31_start = 1
      loop31_stop = undf_aspc1_ls_moist_dyn_fac
      loop32_start = 1
      loop32_stop = undf_aspc1_ls_moist_dyn_fac_1
      loop33_start = 1
      loop33_stop = undf_aspc1_ls_moist_dyn_fac_2
      !
      ! Call our kernels
      !
      DO df = loop0_start, loop0_stop, 1
        ! Built-in: setval_random (fill a real-valued field with pseudo-random numbers)
        CALL RANDOM_NUMBER(r_u_data(df))
      END DO
      DO df = loop1_start, loop1_stop, 1
        ! Built-in: setval_X (set a real-valued field equal to another such field)
        r_u_input_data(df) = r_u_data(df)
      END DO
      DO df = loop2_start, loop2_stop, 1
        ! Built-in: setval_random (fill a real-valued field with pseudo-random numbers)
        CALL RANDOM_NUMBER(exner_data(df))
      END DO
      DO df = loop3_start, loop3_stop, 1
        ! Built-in: setval_X (set a real-valued field equal to another such field)
        exner_input_data(df) = exner_data(df)
      END DO
      DO df = loop4_start, loop4_stop, 1
        ! Built-in: setval_random (fill a real-valued field with pseudo-random numbers)
        CALL RANDOM_NUMBER(theta_data(df))
      END DO
      DO df = loop5_start, loop5_stop, 1
        ! Built-in: setval_X (set a real-valued field equal to another such field)
        theta_input_data(df) = theta_data(df)
      END DO
      DO df = loop6_start, loop6_stop, 1
        ! Built-in: setval_random (fill a real-valued field with pseudo-random numbers)
        CALL RANDOM_NUMBER(moist_dyn_fac_data(df))
      END DO
      DO df = loop7_start, loop7_stop, 1
        ! Built-in: setval_X (set a real-valued field equal to another such field)
        moist_dyn_fac_input_data(df) = moist_dyn_fac_data(df)
      END DO
      DO df = loop8_start, loop8_stop, 1
        ! Built-in: setval_random (fill a real-valued field with pseudo-random numbers)
        CALL RANDOM_NUMBER(moist_dyn_fac_1_data(df))
      END DO
      DO df = loop9_start, loop9_stop, 1
        ! Built-in: setval_X (set a real-valued field equal to another such field)
        moist_dyn_fac_input_1_data(df) = moist_dyn_fac_1_data(df)
      END DO
      DO df = loop10_start, loop10_stop, 1
        ! Built-in: setval_random (fill a real-valued field with pseudo-random numbers)
        CALL RANDOM_NUMBER(moist_dyn_fac_2_data(df))
      END DO
      DO df = loop11_start, loop11_stop, 1
        ! Built-in: setval_X (set a real-valued field equal to another such field)
        moist_dyn_fac_input_2_data(df) = moist_dyn_fac_2_data(df)
      END DO
      DO df = loop12_start, loop12_stop, 1
        ! Built-in: setval_random (fill a real-valued field with pseudo-random numbers)
        CALL RANDOM_NUMBER(ls_exner_data(df))
      END DO
      DO df = loop13_start, loop13_stop, 1
        ! Built-in: setval_X (set a real-valued field equal to another such field)
        ls_exner_input_data(df) = ls_exner_data(df)
      END DO
      DO df = loop14_start, loop14_stop, 1
        ! Built-in: setval_random (fill a real-valued field with pseudo-random numbers)
        CALL RANDOM_NUMBER(ls_theta_data(df))
      END DO
      DO df = loop15_start, loop15_stop, 1
        ! Built-in: setval_X (set a real-valued field equal to another such field)
        ls_theta_input_data(df) = ls_theta_data(df)
      END DO
      DO df = loop16_start, loop16_stop, 1
        ! Built-in: setval_random (fill a real-valued field with pseudo-random numbers)
        CALL RANDOM_NUMBER(ls_moist_dyn_fac_data(df))
      END DO
      DO df = loop17_start, loop17_stop, 1
        ! Built-in: setval_X (set a real-valued field equal to another such field)
        ls_moist_dyn_fac_input_data(df) = ls_moist_dyn_fac_data(df)
      END DO
      DO df = loop18_start, loop18_stop, 1
        ! Built-in: setval_random (fill a real-valued field with pseudo-random numbers)
        CALL RANDOM_NUMBER(ls_moist_dyn_fac_1_data(df))
      END DO
      DO df = loop19_start, loop19_stop, 1
        ! Built-in: setval_X (set a real-valued field equal to another such field)
        ls_moist_dyn_fac_input_1_data(df) = ls_moist_dyn_fac_1_data(df)
      END DO
      DO df = loop20_start, loop20_stop, 1
        ! Built-in: setval_random (fill a real-valued field with pseudo-random numbers)
        CALL RANDOM_NUMBER(ls_moist_dyn_fac_2_data(df))
      END DO
      DO df = loop21_start, loop21_stop, 1
        ! Built-in: setval_X (set a real-valued field equal to another such field)
        ls_moist_dyn_fac_input_2_data(df) = ls_moist_dyn_fac_2_data(df)
      END DO
      DO cell = loop22_start, loop22_stop, 1
        CALL tl_hydrostatic_code(nlayers_r_u, r_u_data, exner_data, theta_data, moist_dyn_fac_3_1_data, moist_dyn_fac_3_2_data, &
&moist_dyn_fac_3_3_data, ls_exner_data, ls_theta_data, ls_moist_dyn_fac_3_1_data, ls_moist_dyn_fac_3_2_data, &
&ls_moist_dyn_fac_3_3_data, cp, ndf_any_w2, undf_any_w2, map_any_w2(:,cell), basis_any_w2_qr_xyoz, diff_basis_any_w2_qr_xyoz, &
&ndf_w3, undf_w3, map_w3(:,cell), basis_w3_qr_xyoz, ndf_wtheta, undf_wtheta, map_wtheta(:,cell), basis_wtheta_qr_xyoz, &
&diff_basis_wtheta_qr_xyoz, np_xy_qr_xyoz, np_z_qr_xyoz, weights_xy_qr_xyoz, weights_z_qr_xyoz)
      END DO
      !
      ! Zero summation variables
      !
      r_u_inner_prod = 0.0_r_def
      !
      DO df = loop23_start, loop23_stop, 1
        ! Built-in: X_innerproduct_X (real-valued field)
        r_u_inner_prod = r_u_inner_prod + r_u_data(df) * r_u_data(df)
      END DO
      !
      ! Zero summation variables
      !
      exner_inner_prod = 0.0_r_def
      !
      DO df = loop24_start, loop24_stop, 1
        ! Built-in: X_innerproduct_X (real-valued field)
        exner_inner_prod = exner_inner_prod + exner_data(df) * exner_data(df)
      END DO
      !
      ! Zero summation variables
      !
      theta_inner_prod = 0.0_r_def
      !
      DO df = loop25_start, loop25_stop, 1
        ! Built-in: X_innerproduct_X (real-valued field)
        theta_inner_prod = theta_inner_prod + theta_data(df) * theta_data(df)
      END DO
      !
      ! Zero summation variables
      !
      moist_dyn_fac_inner_prod = 0.0_r_def
      !
      DO df = loop26_start, loop26_stop, 1
        ! Built-in: X_innerproduct_X (real-valued field)
        moist_dyn_fac_inner_prod = moist_dyn_fac_inner_prod + moist_dyn_fac_data(df) * moist_dyn_fac_data(df)
      END DO
      !
      ! Zero summation variables
      !
      moist_dyn_fac_inner_prod_1 = 0.0_r_def
      !
      DO df = loop27_start, loop27_stop, 1
        ! Built-in: X_innerproduct_X (real-valued field)
        moist_dyn_fac_inner_prod_1 = moist_dyn_fac_inner_prod_1 + moist_dyn_fac_1_data(df) * moist_dyn_fac_1_data(df)
      END DO
      !
      ! Zero summation variables
      !
      moist_dyn_fac_inner_prod_2 = 0.0_r_def
      !
      DO df = loop28_start, loop28_stop, 1
        ! Built-in: X_innerproduct_X (real-valued field)
        moist_dyn_fac_inner_prod_2 = moist_dyn_fac_inner_prod_2 + moist_dyn_fac_2_data(df) * moist_dyn_fac_2_data(df)
      END DO
      !
      ! Zero summation variables
      !
      ls_exner_inner_prod = 0.0_r_def
      !
      DO df = loop29_start, loop29_stop, 1
        ! Built-in: X_innerproduct_X (real-valued field)
        ls_exner_inner_prod = ls_exner_inner_prod + ls_exner_data(df) * ls_exner_data(df)
      END DO
      !
      ! Zero summation variables
      !
      ls_theta_inner_prod = 0.0_r_def
      !
      DO df = loop30_start, loop30_stop, 1
        ! Built-in: X_innerproduct_X (real-valued field)
        ls_theta_inner_prod = ls_theta_inner_prod + ls_theta_data(df) * ls_theta_data(df)
      END DO
      !
      ! Zero summation variables
      !
      ls_moist_dyn_fac_inner_prod = 0.0_r_def
      !
      DO df = loop31_start, loop31_stop, 1
        ! Built-in: X_innerproduct_X (real-valued field)
        ls_moist_dyn_fac_inner_prod = ls_moist_dyn_fac_inner_prod + ls_moist_dyn_fac_data(df) * ls_moist_dyn_fac_data(df)
      END DO
      !
      ! Zero summation variables
      !
      ls_moist_dyn_fac_inner_prod_1 = 0.0_r_def
      !
      DO df = loop32_start, loop32_stop, 1
        ! Built-in: X_innerproduct_X (real-valued field)
        ls_moist_dyn_fac_inner_prod_1 = ls_moist_dyn_fac_inner_prod_1 + ls_moist_dyn_fac_1_data(df) * ls_moist_dyn_fac_1_data(df)
      END DO
      !
      ! Zero summation variables
      !
      ls_moist_dyn_fac_inner_prod_2 = 0.0_r_def
      !
      DO df = loop33_start, loop33_stop, 1
        ! Built-in: X_innerproduct_X (real-valued field)
        ls_moist_dyn_fac_inner_prod_2 = ls_moist_dyn_fac_inner_prod_2 + ls_moist_dyn_fac_2_data(df) * ls_moist_dyn_fac_2_data(df)
      END DO
      !
      ! Deallocate basis arrays
      !
      DEALLOCATE (basis_any_w2_qr_xyoz, basis_w3_qr_xyoz, basis_wtheta_qr_xyoz, diff_basis_any_w2_qr_xyoz, &
&diff_basis_wtheta_qr_xyoz)
      !
    END SUBROUTINE invoke_0
    SUBROUTINE invoke_1(r_u, exner, theta, moist_dyn_fac, ls_exner, ls_theta, ls_moist_dyn_fac, cp, r_u_r_u_input_inner_prod, &
&r_u_input, exner_exner_input_inner_prod, exner_input, theta_theta_input_inner_prod, theta_input, &
&moist_dyn_fac_moist_dyn_fac_input_inner_prod, moist_dyn_fac_1, moist_dyn_fac_input, &
&moist_dyn_fac_moist_dyn_fac_input_inner_prod_1, moist_dyn_fac_2, moist_dyn_fac_input_1, &
&moist_dyn_fac_moist_dyn_fac_input_inner_prod_2, moist_dyn_fac_3, moist_dyn_fac_input_2, ls_exner_ls_exner_input_inner_prod, &
&ls_exner_input, ls_theta_ls_theta_input_inner_prod, ls_theta_input, ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod, &
&ls_moist_dyn_fac_1, ls_moist_dyn_fac_input, ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod_1, ls_moist_dyn_fac_2, &
&ls_moist_dyn_fac_input_1, ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod_2, ls_moist_dyn_fac_3, ls_moist_dyn_fac_input_2, &
&qr_xyoz)
      USE adj_hydrostatic_kernel_mod, ONLY: adj_hydrostatic_code
      USE quadrature_xyoz_mod, ONLY: quadrature_xyoz_type, quadrature_xyoz_proxy_type
      USE function_space_mod, ONLY: BASIS, DIFF_BASIS
      REAL(KIND=r_def), intent(out) :: r_u_r_u_input_inner_prod, exner_exner_input_inner_prod, theta_theta_input_inner_prod, &
&moist_dyn_fac_moist_dyn_fac_input_inner_prod, moist_dyn_fac_moist_dyn_fac_input_inner_prod_1, &
&moist_dyn_fac_moist_dyn_fac_input_inner_prod_2, ls_exner_ls_exner_input_inner_prod, ls_theta_ls_theta_input_inner_prod, &
&ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod, ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod_1, &
&ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod_2
      REAL(KIND=r_def), intent(in) :: cp
      TYPE(field_type), intent(in) :: r_u, exner, theta, moist_dyn_fac(3), ls_exner, ls_theta, ls_moist_dyn_fac(3), r_u_input, &
&exner_input, theta_input, moist_dyn_fac_1, moist_dyn_fac_input, moist_dyn_fac_2, moist_dyn_fac_input_1, moist_dyn_fac_3, &
&moist_dyn_fac_input_2, ls_exner_input, ls_theta_input, ls_moist_dyn_fac_1, ls_moist_dyn_fac_input, ls_moist_dyn_fac_2, &
&ls_moist_dyn_fac_input_1, ls_moist_dyn_fac_3, ls_moist_dyn_fac_input_2
      TYPE(quadrature_xyoz_type), intent(in) :: qr_xyoz
      INTEGER(KIND=i_def) df
      INTEGER(KIND=i_def) cell
      INTEGER(KIND=i_def) loop11_start, loop11_stop
      INTEGER(KIND=i_def) loop10_start, loop10_stop
      INTEGER(KIND=i_def) loop9_start, loop9_stop
      INTEGER(KIND=i_def) loop8_start, loop8_stop
      INTEGER(KIND=i_def) loop7_start, loop7_stop
      INTEGER(KIND=i_def) loop6_start, loop6_stop
      INTEGER(KIND=i_def) loop5_start, loop5_stop
      INTEGER(KIND=i_def) loop4_start, loop4_stop
      INTEGER(KIND=i_def) loop3_start, loop3_stop
      INTEGER(KIND=i_def) loop2_start, loop2_stop
      INTEGER(KIND=i_def) loop1_start, loop1_stop
      INTEGER(KIND=i_def) loop0_start, loop0_stop
      REAL(KIND=r_def), allocatable :: basis_any_w2_qr_xyoz(:,:,:,:), diff_basis_any_w2_qr_xyoz(:,:,:,:), &
&basis_w3_qr_xyoz(:,:,:,:), basis_wtheta_qr_xyoz(:,:,:,:), diff_basis_wtheta_qr_xyoz(:,:,:,:)
      INTEGER(KIND=i_def) dim_any_w2, diff_dim_any_w2, dim_w3, dim_wtheta, diff_dim_wtheta
      REAL(KIND=r_def), pointer :: weights_xy_qr_xyoz(:) => null(), weights_z_qr_xyoz(:) => null()
      INTEGER(KIND=i_def) np_xy_qr_xyoz, np_z_qr_xyoz
      INTEGER(KIND=i_def) nlayers_r_u
      REAL(KIND=r_def), pointer, dimension(:) :: ls_moist_dyn_fac_input_2_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: ls_moist_dyn_fac_input_1_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: ls_moist_dyn_fac_input_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: ls_theta_input_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: ls_exner_input_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: moist_dyn_fac_input_2_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: moist_dyn_fac_input_1_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: moist_dyn_fac_input_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: theta_input_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: exner_input_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: r_u_input_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: ls_moist_dyn_fac_1_data => null(), ls_moist_dyn_fac_2_data => null(), &
&ls_moist_dyn_fac_3_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: ls_theta_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: ls_exner_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: moist_dyn_fac_1_data => null(), moist_dyn_fac_2_data => null(), &
&moist_dyn_fac_3_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: theta_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: exner_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: r_u_data => null()
      TYPE(field_proxy_type) r_u_proxy, exner_proxy, theta_proxy, moist_dyn_fac_proxy(3), ls_exner_proxy, ls_theta_proxy, &
&ls_moist_dyn_fac_proxy(3), r_u_input_proxy, exner_input_proxy, theta_input_proxy, moist_dyn_fac_1_proxy, &
&moist_dyn_fac_input_proxy, moist_dyn_fac_2_proxy, moist_dyn_fac_input_1_proxy, moist_dyn_fac_3_proxy, &
&moist_dyn_fac_input_2_proxy, ls_exner_input_proxy, ls_theta_input_proxy, ls_moist_dyn_fac_1_proxy, ls_moist_dyn_fac_input_proxy, &
&ls_moist_dyn_fac_2_proxy, ls_moist_dyn_fac_input_1_proxy, ls_moist_dyn_fac_3_proxy, ls_moist_dyn_fac_input_2_proxy
      TYPE(quadrature_xyoz_proxy_type) qr_xyoz_proxy
      INTEGER(KIND=i_def), pointer :: map_any_w2(:,:) => null(), map_w3(:,:) => null(), map_wtheta(:,:) => null()
      INTEGER(KIND=i_def) ndf_any_w2, undf_any_w2, ndf_w3, undf_w3, ndf_wtheta, undf_wtheta, ndf_aspc1_r_u, undf_aspc1_r_u, &
&ndf_aspc1_exner, undf_aspc1_exner, ndf_aspc1_theta, undf_aspc1_theta, ndf_aspc1_moist_dyn_fac_1, undf_aspc1_moist_dyn_fac_1, &
&ndf_aspc1_moist_dyn_fac_2, undf_aspc1_moist_dyn_fac_2, ndf_aspc1_moist_dyn_fac_3, undf_aspc1_moist_dyn_fac_3, ndf_aspc1_ls_exner, &
&undf_aspc1_ls_exner, ndf_aspc1_ls_theta, undf_aspc1_ls_theta, ndf_aspc1_ls_moist_dyn_fac_1, undf_aspc1_ls_moist_dyn_fac_1, &
&ndf_aspc1_ls_moist_dyn_fac_2, undf_aspc1_ls_moist_dyn_fac_2, ndf_aspc1_ls_moist_dyn_fac_3, undf_aspc1_ls_moist_dyn_fac_3
      !
      ! Initialise field and/or operator proxies
      !
      r_u_proxy = r_u%get_proxy()
      r_u_data => r_u_proxy%data
      exner_proxy = exner%get_proxy()
      exner_data => exner_proxy%data
      theta_proxy = theta%get_proxy()
      theta_data => theta_proxy%data
      moist_dyn_fac_proxy(1) = moist_dyn_fac(1)%get_proxy()
      moist_dyn_fac_1_data => moist_dyn_fac_proxy(1)%data
      moist_dyn_fac_proxy(2) = moist_dyn_fac(2)%get_proxy()
      moist_dyn_fac_2_data => moist_dyn_fac_proxy(2)%data
      moist_dyn_fac_proxy(3) = moist_dyn_fac(3)%get_proxy()
      moist_dyn_fac_3_data => moist_dyn_fac_proxy(3)%data
      ls_exner_proxy = ls_exner%get_proxy()
      ls_exner_data => ls_exner_proxy%data
      ls_theta_proxy = ls_theta%get_proxy()
      ls_theta_data => ls_theta_proxy%data
      ls_moist_dyn_fac_proxy(1) = ls_moist_dyn_fac(1)%get_proxy()
      ls_moist_dyn_fac_1_data => ls_moist_dyn_fac_proxy(1)%data
      ls_moist_dyn_fac_proxy(2) = ls_moist_dyn_fac(2)%get_proxy()
      ls_moist_dyn_fac_2_data => ls_moist_dyn_fac_proxy(2)%data
      ls_moist_dyn_fac_proxy(3) = ls_moist_dyn_fac(3)%get_proxy()
      ls_moist_dyn_fac_3_data => ls_moist_dyn_fac_proxy(3)%data
      r_u_input_proxy = r_u_input%get_proxy()
      r_u_input_data => r_u_input_proxy%data
      exner_input_proxy = exner_input%get_proxy()
      exner_input_data => exner_input_proxy%data
      theta_input_proxy = theta_input%get_proxy()
      theta_input_data => theta_input_proxy%data
      moist_dyn_fac_1_proxy = moist_dyn_fac_1%get_proxy()
      moist_dyn_fac_1_data => moist_dyn_fac_1_proxy%data
      moist_dyn_fac_input_proxy = moist_dyn_fac_input%get_proxy()
      moist_dyn_fac_input_data => moist_dyn_fac_input_proxy%data
      moist_dyn_fac_2_proxy = moist_dyn_fac_2%get_proxy()
      moist_dyn_fac_2_data => moist_dyn_fac_2_proxy%data
      moist_dyn_fac_input_1_proxy = moist_dyn_fac_input_1%get_proxy()
      moist_dyn_fac_input_1_data => moist_dyn_fac_input_1_proxy%data
      moist_dyn_fac_3_proxy = moist_dyn_fac_3%get_proxy()
      moist_dyn_fac_3_data => moist_dyn_fac_3_proxy%data
      moist_dyn_fac_input_2_proxy = moist_dyn_fac_input_2%get_proxy()
      moist_dyn_fac_input_2_data => moist_dyn_fac_input_2_proxy%data
      ls_exner_input_proxy = ls_exner_input%get_proxy()
      ls_exner_input_data => ls_exner_input_proxy%data
      ls_theta_input_proxy = ls_theta_input%get_proxy()
      ls_theta_input_data => ls_theta_input_proxy%data
      ls_moist_dyn_fac_1_proxy = ls_moist_dyn_fac_1%get_proxy()
      ls_moist_dyn_fac_1_data => ls_moist_dyn_fac_1_proxy%data
      ls_moist_dyn_fac_input_proxy = ls_moist_dyn_fac_input%get_proxy()
      ls_moist_dyn_fac_input_data => ls_moist_dyn_fac_input_proxy%data
      ls_moist_dyn_fac_2_proxy = ls_moist_dyn_fac_2%get_proxy()
      ls_moist_dyn_fac_2_data => ls_moist_dyn_fac_2_proxy%data
      ls_moist_dyn_fac_input_1_proxy = ls_moist_dyn_fac_input_1%get_proxy()
      ls_moist_dyn_fac_input_1_data => ls_moist_dyn_fac_input_1_proxy%data
      ls_moist_dyn_fac_3_proxy = ls_moist_dyn_fac_3%get_proxy()
      ls_moist_dyn_fac_3_data => ls_moist_dyn_fac_3_proxy%data
      ls_moist_dyn_fac_input_2_proxy = ls_moist_dyn_fac_input_2%get_proxy()
      ls_moist_dyn_fac_input_2_data => ls_moist_dyn_fac_input_2_proxy%data
      !
      ! Initialise number of layers
      !
      nlayers_r_u = r_u_proxy%vspace%get_nlayers()
      !
      ! Look-up dofmaps for each function space
      !
      map_any_w2 => r_u_proxy%vspace%get_whole_dofmap()
      map_w3 => exner_proxy%vspace%get_whole_dofmap()
      map_wtheta => theta_proxy%vspace%get_whole_dofmap()
      !
      ! Initialise number of DoFs for any_w2
      !
      ndf_any_w2 = r_u_proxy%vspace%get_ndf()
      undf_any_w2 = r_u_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for w3
      !
      ndf_w3 = exner_proxy%vspace%get_ndf()
      undf_w3 = exner_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for wtheta
      !
      ndf_wtheta = theta_proxy%vspace%get_ndf()
      undf_wtheta = theta_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_r_u
      !
      ndf_aspc1_r_u = r_u_proxy%vspace%get_ndf()
      undf_aspc1_r_u = r_u_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_exner
      !
      ndf_aspc1_exner = exner_proxy%vspace%get_ndf()
      undf_aspc1_exner = exner_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_theta
      !
      ndf_aspc1_theta = theta_proxy%vspace%get_ndf()
      undf_aspc1_theta = theta_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_moist_dyn_fac_1
      !
      ndf_aspc1_moist_dyn_fac_1 = moist_dyn_fac_1_proxy%vspace%get_ndf()
      undf_aspc1_moist_dyn_fac_1 = moist_dyn_fac_1_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_moist_dyn_fac_2
      !
      ndf_aspc1_moist_dyn_fac_2 = moist_dyn_fac_2_proxy%vspace%get_ndf()
      undf_aspc1_moist_dyn_fac_2 = moist_dyn_fac_2_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_moist_dyn_fac_3
      !
      ndf_aspc1_moist_dyn_fac_3 = moist_dyn_fac_3_proxy%vspace%get_ndf()
      undf_aspc1_moist_dyn_fac_3 = moist_dyn_fac_3_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_ls_exner
      !
      ndf_aspc1_ls_exner = ls_exner_proxy%vspace%get_ndf()
      undf_aspc1_ls_exner = ls_exner_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_ls_theta
      !
      ndf_aspc1_ls_theta = ls_theta_proxy%vspace%get_ndf()
      undf_aspc1_ls_theta = ls_theta_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_ls_moist_dyn_fac_1
      !
      ndf_aspc1_ls_moist_dyn_fac_1 = ls_moist_dyn_fac_1_proxy%vspace%get_ndf()
      undf_aspc1_ls_moist_dyn_fac_1 = ls_moist_dyn_fac_1_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_ls_moist_dyn_fac_2
      !
      ndf_aspc1_ls_moist_dyn_fac_2 = ls_moist_dyn_fac_2_proxy%vspace%get_ndf()
      undf_aspc1_ls_moist_dyn_fac_2 = ls_moist_dyn_fac_2_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_ls_moist_dyn_fac_3
      !
      ndf_aspc1_ls_moist_dyn_fac_3 = ls_moist_dyn_fac_3_proxy%vspace%get_ndf()
      undf_aspc1_ls_moist_dyn_fac_3 = ls_moist_dyn_fac_3_proxy%vspace%get_undf()
      !
      ! Look-up quadrature variables
      !
      qr_xyoz_proxy = qr_xyoz%get_quadrature_proxy()
      np_xy_qr_xyoz = qr_xyoz_proxy%np_xy
      np_z_qr_xyoz = qr_xyoz_proxy%np_z
      weights_xy_qr_xyoz => qr_xyoz_proxy%weights_xy
      weights_z_qr_xyoz => qr_xyoz_proxy%weights_z
      !
      ! Allocate basis/diff-basis arrays
      !
      dim_any_w2 = r_u_proxy%vspace%get_dim_space()
      diff_dim_any_w2 = r_u_proxy%vspace%get_dim_space_diff()
      dim_w3 = exner_proxy%vspace%get_dim_space()
      dim_wtheta = theta_proxy%vspace%get_dim_space()
      diff_dim_wtheta = theta_proxy%vspace%get_dim_space_diff()
      ALLOCATE (basis_any_w2_qr_xyoz(dim_any_w2, ndf_any_w2, np_xy_qr_xyoz, np_z_qr_xyoz))
      ALLOCATE (diff_basis_any_w2_qr_xyoz(diff_dim_any_w2, ndf_any_w2, np_xy_qr_xyoz, np_z_qr_xyoz))
      ALLOCATE (basis_w3_qr_xyoz(dim_w3, ndf_w3, np_xy_qr_xyoz, np_z_qr_xyoz))
      ALLOCATE (basis_wtheta_qr_xyoz(dim_wtheta, ndf_wtheta, np_xy_qr_xyoz, np_z_qr_xyoz))
      ALLOCATE (diff_basis_wtheta_qr_xyoz(diff_dim_wtheta, ndf_wtheta, np_xy_qr_xyoz, np_z_qr_xyoz))
      !
      ! Compute basis/diff-basis arrays
      !
      CALL qr_xyoz%compute_function(BASIS, r_u_proxy%vspace, dim_any_w2, ndf_any_w2, basis_any_w2_qr_xyoz)
      CALL qr_xyoz%compute_function(DIFF_BASIS, r_u_proxy%vspace, diff_dim_any_w2, ndf_any_w2, diff_basis_any_w2_qr_xyoz)
      CALL qr_xyoz%compute_function(BASIS, exner_proxy%vspace, dim_w3, ndf_w3, basis_w3_qr_xyoz)
      CALL qr_xyoz%compute_function(BASIS, theta_proxy%vspace, dim_wtheta, ndf_wtheta, basis_wtheta_qr_xyoz)
      CALL qr_xyoz%compute_function(DIFF_BASIS, theta_proxy%vspace, diff_dim_wtheta, ndf_wtheta, diff_basis_wtheta_qr_xyoz)
      !
      ! Set-up all of the loop bounds
      !
      loop0_start = 1
      loop0_stop = exner_proxy%vspace%get_ncell()
      loop1_start = 1
      loop1_stop = undf_aspc1_r_u
      loop2_start = 1
      loop2_stop = undf_aspc1_exner
      loop3_start = 1
      loop3_stop = undf_aspc1_theta
      loop4_start = 1
      loop4_stop = undf_aspc1_moist_dyn_fac_1
      loop5_start = 1
      loop5_stop = undf_aspc1_moist_dyn_fac_2
      loop6_start = 1
      loop6_stop = undf_aspc1_moist_dyn_fac_3
      loop7_start = 1
      loop7_stop = undf_aspc1_ls_exner
      loop8_start = 1
      loop8_stop = undf_aspc1_ls_theta
      loop9_start = 1
      loop9_stop = undf_aspc1_ls_moist_dyn_fac_1
      loop10_start = 1
      loop10_stop = undf_aspc1_ls_moist_dyn_fac_2
      loop11_start = 1
      loop11_stop = undf_aspc1_ls_moist_dyn_fac_3
      !
      ! Call our kernels
      !
      DO cell = loop0_start, loop0_stop, 1
        CALL adj_hydrostatic_code(nlayers_r_u, r_u_data, exner_data, theta_data, moist_dyn_fac_1_data, moist_dyn_fac_2_data, &
&moist_dyn_fac_3_data, ls_exner_data, ls_theta_data, ls_moist_dyn_fac_1_data, ls_moist_dyn_fac_2_data, ls_moist_dyn_fac_3_data, &
&cp, ndf_any_w2, undf_any_w2, map_any_w2(:,cell), basis_any_w2_qr_xyoz, diff_basis_any_w2_qr_xyoz, ndf_w3, undf_w3, &
&map_w3(:,cell), basis_w3_qr_xyoz, ndf_wtheta, undf_wtheta, map_wtheta(:,cell), basis_wtheta_qr_xyoz, diff_basis_wtheta_qr_xyoz, &
&np_xy_qr_xyoz, np_z_qr_xyoz, weights_xy_qr_xyoz, weights_z_qr_xyoz)
      END DO
      !
      ! Zero summation variables
      !
      r_u_r_u_input_inner_prod = 0.0_r_def
      !
      DO df = loop1_start, loop1_stop, 1
        ! Built-in: X_innerproduct_Y (real-valued fields)
        r_u_r_u_input_inner_prod = r_u_r_u_input_inner_prod + r_u_data(df) * r_u_input_data(df)
      END DO
      !
      ! Zero summation variables
      !
      exner_exner_input_inner_prod = 0.0_r_def
      !
      DO df = loop2_start, loop2_stop, 1
        ! Built-in: X_innerproduct_Y (real-valued fields)
        exner_exner_input_inner_prod = exner_exner_input_inner_prod + exner_data(df) * exner_input_data(df)
      END DO
      !
      ! Zero summation variables
      !
      theta_theta_input_inner_prod = 0.0_r_def
      !
      DO df = loop3_start, loop3_stop, 1
        ! Built-in: X_innerproduct_Y (real-valued fields)
        theta_theta_input_inner_prod = theta_theta_input_inner_prod + theta_data(df) * theta_input_data(df)
      END DO
      !
      ! Zero summation variables
      !
      moist_dyn_fac_moist_dyn_fac_input_inner_prod = 0.0_r_def
      !
      DO df = loop4_start, loop4_stop, 1
        ! Built-in: X_innerproduct_Y (real-valued fields)
        moist_dyn_fac_moist_dyn_fac_input_inner_prod = moist_dyn_fac_moist_dyn_fac_input_inner_prod + moist_dyn_fac_1_data(df) * &
&moist_dyn_fac_input_data(df)
      END DO
      !
      ! Zero summation variables
      !
      moist_dyn_fac_moist_dyn_fac_input_inner_prod_1 = 0.0_r_def
      !
      DO df = loop5_start, loop5_stop, 1
        ! Built-in: X_innerproduct_Y (real-valued fields)
        moist_dyn_fac_moist_dyn_fac_input_inner_prod_1 = moist_dyn_fac_moist_dyn_fac_input_inner_prod_1 + moist_dyn_fac_2_data(df) &
&* moist_dyn_fac_input_1_data(df)
      END DO
      !
      ! Zero summation variables
      !
      moist_dyn_fac_moist_dyn_fac_input_inner_prod_2 = 0.0_r_def
      !
      DO df = loop6_start, loop6_stop, 1
        ! Built-in: X_innerproduct_Y (real-valued fields)
        moist_dyn_fac_moist_dyn_fac_input_inner_prod_2 = moist_dyn_fac_moist_dyn_fac_input_inner_prod_2 + moist_dyn_fac_3_data(df) &
&* moist_dyn_fac_input_2_data(df)
      END DO
      !
      ! Zero summation variables
      !
      ls_exner_ls_exner_input_inner_prod = 0.0_r_def
      !
      DO df = loop7_start, loop7_stop, 1
        ! Built-in: X_innerproduct_Y (real-valued fields)
        ls_exner_ls_exner_input_inner_prod = ls_exner_ls_exner_input_inner_prod + ls_exner_data(df) * ls_exner_input_data(df)
      END DO
      !
      ! Zero summation variables
      !
      ls_theta_ls_theta_input_inner_prod = 0.0_r_def
      !
      DO df = loop8_start, loop8_stop, 1
        ! Built-in: X_innerproduct_Y (real-valued fields)
        ls_theta_ls_theta_input_inner_prod = ls_theta_ls_theta_input_inner_prod + ls_theta_data(df) * ls_theta_input_data(df)
      END DO
      !
      ! Zero summation variables
      !
      ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod = 0.0_r_def
      !
      DO df = loop9_start, loop9_stop, 1
        ! Built-in: X_innerproduct_Y (real-valued fields)
        ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod = ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod + &
&ls_moist_dyn_fac_1_data(df) * ls_moist_dyn_fac_input_data(df)
      END DO
      !
      ! Zero summation variables
      !
      ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod_1 = 0.0_r_def
      !
      DO df = loop10_start, loop10_stop, 1
        ! Built-in: X_innerproduct_Y (real-valued fields)
        ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod_1 = ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod_1 + &
&ls_moist_dyn_fac_2_data(df) * ls_moist_dyn_fac_input_1_data(df)
      END DO
      !
      ! Zero summation variables
      !
      ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod_2 = 0.0_r_def
      !
      DO df = loop11_start, loop11_stop, 1
        ! Built-in: X_innerproduct_Y (real-valued fields)
        ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod_2 = ls_moist_dyn_fac_ls_moist_dyn_fac_input_inner_prod_2 + &
&ls_moist_dyn_fac_3_data(df) * ls_moist_dyn_fac_input_2_data(df)
      END DO
      !
      ! Deallocate basis arrays
      !
      DEALLOCATE (basis_any_w2_qr_xyoz, basis_w3_qr_xyoz, basis_wtheta_qr_xyoz, diff_basis_any_w2_qr_xyoz, &
&diff_basis_wtheta_qr_xyoz)
      !
    END SUBROUTINE invoke_1
  END MODULE adjt_hydrostatic_alg_mod_psy