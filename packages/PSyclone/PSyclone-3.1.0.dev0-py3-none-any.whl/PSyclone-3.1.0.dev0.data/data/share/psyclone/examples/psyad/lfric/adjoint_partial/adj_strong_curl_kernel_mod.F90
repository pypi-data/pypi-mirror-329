module adj_strong_curl_kernel_mod
  use argument_mod, only : arg_type, cell_column, func_type, gh_basis, gh_diff_basis, gh_evaluator, gh_field, gh_inc, gh_read, &
&gh_real
  use constants_mod, only : i_def, r_def
  use fs_continuity_mod, only : w1, w2
  use kernel_mod, only : kernel_type
  implicit none
  type, public, extends(kernel_type) :: adj_strong_curl_kernel_type
  type(ARG_TYPE) :: META_ARGS(2) = (/ &
    arg_type(gh_field, gh_real, gh_inc, w2), &
    arg_type(gh_field, gh_real, gh_inc, w1)/)
  type(FUNC_TYPE) :: META_FUNCS(2) = (/ &
    func_type(w2, gh_basis), &
    func_type(w1, gh_diff_basis)/)
  INTEGER :: GH_SHAPE = gh_evaluator
  INTEGER :: OPERATES_ON = cell_column
  CONTAINS
    PROCEDURE, NOPASS :: adj_strong_curl_code
END TYPE adj_strong_curl_kernel_type

  private

  public :: adj_strong_curl_code

  contains
  subroutine adj_strong_curl_code(nlayers, xi, u, ndf2, undf2, map2, basis_w2, ndf1, undf1, map1, diff_basis_w1)
    integer(kind=i_def), intent(in) :: nlayers
    integer(kind=i_def), intent(in) :: ndf1
    integer(kind=i_def), intent(in) :: undf1
    integer(kind=i_def), intent(in) :: ndf2
    integer(kind=i_def), intent(in) :: undf2
    integer(kind=i_def), dimension(ndf1), intent(in) :: map1
    integer(kind=i_def), dimension(ndf2), intent(in) :: map2
    real(kind=r_def), dimension(3,ndf2,ndf2), intent(in) :: basis_w2
    real(kind=r_def), dimension(3,ndf1,ndf2), intent(in) :: diff_basis_w1
    real(kind=r_def), dimension(undf2), intent(inout) :: xi
    real(kind=r_def), dimension(undf1), intent(inout) :: u
    integer(kind=i_def) :: df1
    integer(kind=i_def) :: df2
    integer(kind=i_def) :: k
    real(kind=r_def), dimension(3) :: curl_u
    integer :: i
    real(kind=r_def) :: res_dot_product
    integer :: idx
    integer :: idx_1

    res_dot_product = 0.0_r_def
    curl_u = 0.0_r_def
    do k = nlayers - 1, 0, -1
      do df2 = ndf2, 1, -1
        res_dot_product = res_dot_product + xi(map2(df2) + k)
        xi(map2(df2) + k) = 0.0
        do i = 3, 1, -1
          curl_u(i) = curl_u(i) + basis_w2(i,df2,df2) * res_dot_product
        enddo
        res_dot_product = 0.0
        do df1 = ndf1, 1, -1
          do idx_1 = UBOUND(curl_u, dim=1), LBOUND(curl_u, dim=1), -1
            u(k + map1(df1)) = u(k + map1(df1)) + diff_basis_w1(idx_1,df1,df2) * curl_u(idx_1)
          enddo
        enddo
        do idx = UBOUND(curl_u, dim=1), LBOUND(curl_u, dim=1), -1
          curl_u(idx) = 0.0
        enddo
      enddo
    enddo

  end subroutine adj_strong_curl_code

end module adj_strong_curl_kernel_mod
