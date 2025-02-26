module adj_hydrostatic_kernel_mod
  use argument_mod, only : any_w2, arg_type, cell_column, func_type, gh_basis, gh_diff_basis, gh_field, gh_inc, &
&gh_quadrature_xyoz, gh_read, gh_readwrite, gh_real, gh_scalar, gh_write
  use constants_mod, only : r_def
  use fs_continuity_mod, only : w3, wtheta
  use kernel_mod, only : kernel_type
  implicit none
  type, public, extends(kernel_type) :: adj_hydrostatic_kernel_type
  type(ARG_TYPE) :: META_ARGS(8) = (/ &
    arg_type(gh_field, gh_real, gh_read, any_w2), &
    arg_type(gh_field, gh_real, gh_readwrite, w3), &
    arg_type(gh_field, gh_real, gh_readwrite, wtheta), &
    arg_type(gh_field*3, gh_real, gh_write, wtheta), &
    arg_type(gh_field, gh_real, gh_read, w3), &
    arg_type(gh_field, gh_real, gh_read, wtheta), &
    arg_type(gh_field*3, gh_real, gh_read, wtheta), &
    arg_type(gh_scalar, gh_real, gh_read)/)
  type(FUNC_TYPE) :: META_FUNCS(3) = (/ &
    func_type(any_w2, gh_basis, gh_diff_basis), &
    func_type(w3, gh_basis), &
    func_type(wtheta, gh_basis, gh_diff_basis)/)
  INTEGER :: GH_SHAPE = gh_quadrature_xyoz
  INTEGER :: OPERATES_ON = cell_column
  CONTAINS
    PROCEDURE, NOPASS :: adj_hydrostatic_code
END TYPE adj_hydrostatic_kernel_type

  private

  public :: adj_hydrostatic_code

  contains
  subroutine adj_hydrostatic_code(nlayers, r_u, exner, theta, moist_dyn_gas, moist_dyn_tot, moist_dyn_fac, ls_exner, ls_theta, &
&ls_moist_dyn_gas, ls_moist_dyn_tot, ls_moist_dyn_fac, cp, ndf_w2, undf_w2, map_w2, w2_basis, w2_diff_basis, ndf_w3, undf_w3, &
&map_w3, w3_basis, ndf_wt, undf_wt, map_wt, wt_basis, wt_diff_basis, nqp_h, nqp_v, wqp_h, wqp_v)
    integer, intent(in) :: nlayers
    integer, intent(in) :: nqp_h
    integer, intent(in) :: nqp_v
    integer, intent(in) :: ndf_wt
    integer, intent(in) :: ndf_w2
    integer, intent(in) :: ndf_w3
    integer, intent(in) :: undf_wt
    integer, intent(in) :: undf_w2
    integer, intent(in) :: undf_w3
    integer, dimension(ndf_wt), intent(in) :: map_wt
    integer, dimension(ndf_w2), intent(in) :: map_w2
    integer, dimension(ndf_w3), intent(in) :: map_w3
    real(kind=r_def), dimension(1,ndf_w3,nqp_h,nqp_v), intent(in) :: w3_basis
    real(kind=r_def), dimension(3,ndf_w2,nqp_h,nqp_v), intent(in) :: w2_basis
    real(kind=r_def), dimension(1,ndf_wt,nqp_h,nqp_v), intent(in) :: wt_basis
    real(kind=r_def), dimension(1,ndf_w2,nqp_h,nqp_v), intent(in) :: w2_diff_basis
    real(kind=r_def), dimension(3,ndf_wt,nqp_h,nqp_v), intent(in) :: wt_diff_basis
    real(kind=r_def), dimension(undf_w2), intent(in) :: r_u
    real(kind=r_def), dimension(undf_w3), intent(inout) :: exner
    real(kind=r_def), dimension(undf_wt), intent(inout) :: theta
    real(kind=r_def), dimension(undf_wt), intent(inout) :: moist_dyn_gas
    real(kind=r_def), dimension(undf_wt), intent(inout) :: moist_dyn_tot
    real(kind=r_def), dimension(undf_wt), intent(out) :: moist_dyn_fac
    real(kind=r_def), dimension(undf_w3), intent(in) :: ls_exner
    real(kind=r_def), dimension(undf_wt), intent(in) :: ls_theta
    real(kind=r_def), dimension(undf_wt), intent(in) :: ls_moist_dyn_gas
    real(kind=r_def), dimension(undf_wt), intent(in) :: ls_moist_dyn_tot
    real(kind=r_def), dimension(undf_wt), intent(in) :: ls_moist_dyn_fac
    real(kind=r_def), intent(in) :: cp
    real(kind=r_def), dimension(nqp_h), intent(in) :: wqp_h
    real(kind=r_def), dimension(nqp_v), intent(in) :: wqp_v
    integer :: df
    integer :: k
    integer :: qp1
    integer :: qp2
    real(kind=r_def), dimension(ndf_w3) :: exner_e
    real(kind=r_def), dimension(ndf_wt) :: theta_v_e
    real(kind=r_def), dimension(ndf_w3) :: ls_exner_e
    real(kind=r_def), dimension(ndf_wt) :: ls_theta_v_e
    real(kind=r_def), dimension(3) :: grad_theta_v_at_quad
    real(kind=r_def), dimension(3) :: ls_grad_theta_v_at_quad
    real(kind=r_def), dimension(3) :: v
    real(kind=r_def) :: exner_at_quad
    real(kind=r_def) :: theta_v_at_quad
    real(kind=r_def) :: ls_exner_at_quad
    real(kind=r_def) :: ls_theta_v_at_quad
    real(kind=r_def) :: grad_term
    real(kind=r_def) :: dv
    integer :: i
    real(kind=r_def) :: res_dot_product
    integer :: i_1
    real(kind=r_def) :: res_dot_product_1
    integer :: idx
    integer :: idx_1

    grad_term = 0.0_r_def
    theta_v_e = 0.0_r_def
    theta_v_at_quad = 0.0_r_def
    grad_theta_v_at_quad = 0.0_r_def
    exner_e = 0.0_r_def
    exner_at_quad = 0.0_r_def
    res_dot_product = 0.0_r_def
    do k = nlayers - 1, 0, -1
      do df = 1, ndf_w3, 1
        ls_exner_e(df) = ls_exner(map_w3(df) + k)
      enddo
      do df = 1, ndf_wt, 1
        ls_theta_v_e(df) = ls_moist_dyn_gas(k + map_wt(df)) * ls_theta(k + map_wt(df)) / ls_moist_dyn_tot(k + map_wt(df))
      enddo
      do qp2 = nqp_v, 1, -1
        do qp1 = nqp_h, 1, -1
          ls_exner_at_quad = 0.0_r_def
          do df = 1, ndf_w3, 1
            ls_exner_at_quad = ls_exner_at_quad + ls_exner_e(df) * w3_basis(1,df,qp1,qp2)
          enddo
          ls_theta_v_at_quad = 0.0_r_def
          ls_grad_theta_v_at_quad(:) = 0.0_r_def
          do df = 1, ndf_wt, 1
            ls_theta_v_at_quad = ls_theta_v_at_quad + ls_theta_v_e(df) * wt_basis(1,df,qp1,qp2)
            ls_grad_theta_v_at_quad(:) = ls_grad_theta_v_at_quad(:) + ls_theta_v_e(df) * wt_diff_basis(:,df,qp1,qp2)
          enddo
          do df = ndf_w2, 1, -1
            v(:) = w2_basis(:,df,qp1,qp2)
            dv = w2_diff_basis(1,df,qp1,qp2)
            res_dot_product_1 = 0.0
            do i_1 = 1, 3, 1
              res_dot_product_1 = res_dot_product_1 + ls_grad_theta_v_at_quad(i_1) * v(i_1)
            enddo
            grad_term = grad_term + r_u(map_w2(df) + k) * wqp_h(qp1) * wqp_v(qp2)
            exner_at_quad = exner_at_quad + cp * dv * grad_term * ls_theta_v_at_quad
            theta_v_at_quad = theta_v_at_quad + cp * dv * ls_exner_at_quad * grad_term
            exner_at_quad = exner_at_quad + cp * grad_term * res_dot_product_1
            res_dot_product = res_dot_product + cp * ls_exner_at_quad * grad_term
            grad_term = 0.0
            do i = 3, 1, -1
              grad_theta_v_at_quad(i) = grad_theta_v_at_quad(i) + res_dot_product * v(i)
            enddo
            res_dot_product = 0.0
          enddo
          do df = ndf_wt, 1, -1
            do idx_1 = UBOUND(grad_theta_v_at_quad, dim=1), LBOUND(grad_theta_v_at_quad, dim=1), -1
              theta_v_e(df) = theta_v_e(df) + grad_theta_v_at_quad(idx_1) * wt_diff_basis(idx_1,df,qp1,qp2)
            enddo
            theta_v_e(df) = theta_v_e(df) + theta_v_at_quad * wt_basis(1,df,qp1,qp2)
          enddo
          do idx = UBOUND(grad_theta_v_at_quad, dim=1), LBOUND(grad_theta_v_at_quad, dim=1), -1
            grad_theta_v_at_quad(idx) = 0.0
          enddo
          theta_v_at_quad = 0.0
          do df = ndf_w3, 1, -1
            exner_e(df) = exner_e(df) + exner_at_quad * w3_basis(1,df,qp1,qp2)
          enddo
          exner_at_quad = 0.0
        enddo
      enddo
      do df = ndf_wt, 1, -1
        theta(k + map_wt(df)) = theta(k + map_wt(df)) + ls_theta_v_e(df) * theta_v_e(df) / ls_theta(k + map_wt(df))
        moist_dyn_tot(k + map_wt(df)) = moist_dyn_tot(k + map_wt(df)) - ls_theta_v_e(df) * theta_v_e(df) / ls_moist_dyn_tot(k + &
&map_wt(df))
        moist_dyn_gas(k + map_wt(df)) = moist_dyn_gas(k + map_wt(df)) + ls_theta_v_e(df) * theta_v_e(df) / ls_moist_dyn_gas(k + &
&map_wt(df))
        theta_v_e(df) = 0.0
      enddo
      do df = ndf_w3, 1, -1
        exner(map_w3(df) + k) = exner(map_w3(df) + k) + exner_e(df)
        exner_e(df) = 0.0
      enddo
    enddo

  end subroutine adj_hydrostatic_code

end module adj_hydrostatic_kernel_mod
