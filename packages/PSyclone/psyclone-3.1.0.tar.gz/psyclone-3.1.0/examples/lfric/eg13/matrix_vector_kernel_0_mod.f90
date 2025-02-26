module matrix_vector_kernel_0_mod
  use argument_mod, only : any_space_1, any_space_2, arg_type, cell_column, gh_field, gh_inc, gh_operator, gh_read, gh_real
  use constants_mod, only : i_def, r_def
  use kernel_mod, only : kernel_type
  implicit none
  type, public, extends(kernel_type) :: matrix_vector_kernel_type
  PRIVATE
  TYPE(arg_type) :: meta_args(3) = (/arg_type(gh_field, gh_real, gh_inc, any_space_1), arg_type(gh_field, gh_real, gh_read, &
&any_space_2), arg_type(gh_operator, gh_real, gh_read, any_space_1, any_space_2)/)
  INTEGER :: operates_on = cell_column
  CONTAINS
  PROCEDURE, NOPASS :: matrix_vector_0_code
END TYPE matrix_vector_kernel_type
  private

  public :: matrix_vector_0_code

  contains
  subroutine matrix_vector_0_code(cell, nlayers_dummy, lhs, x, ncell_3d, matrix, ndf1, undf1, map1, ndf2, undf2, map2)
    integer, parameter :: nlayers = 20
    integer(kind=i_def), intent(in) :: cell
    integer(kind=i_def), intent(in) :: ncell_3d
    integer(kind=i_def), intent(in) :: undf1
    integer(kind=i_def), intent(in) :: ndf1
    integer(kind=i_def), intent(in) :: undf2
    integer(kind=i_def), intent(in) :: ndf2
    integer(kind=i_def), dimension(ndf1), intent(in) :: map1
    integer(kind=i_def), dimension(ndf2), intent(in) :: map2
    real(kind=r_def), dimension(undf2), intent(in) :: x
    real(kind=r_def), dimension(undf1), intent(inout) :: lhs
    real(kind=r_def), dimension(ncell_3d,ndf1,ndf2), intent(in) :: matrix
    integer(kind=i_def), intent(in) :: nlayers_dummy
    integer(kind=i_def) :: df
    integer(kind=i_def) :: df2
    integer(kind=i_def) :: k
    integer(kind=i_def) :: ik

    do df = 1, ndf1, 1
      do df2 = 1, ndf2, 1
        do k = 0, nlayers - 1, 1
          ik = (cell - 1) * nlayers + k + 1
          lhs(map1(df) + k) = lhs(map1(df) + k) + matrix(ik,df,df2) * x(map2(df2) + k)
        enddo
      enddo
    enddo

  end subroutine matrix_vector_0_code

end module matrix_vector_kernel_0_mod
