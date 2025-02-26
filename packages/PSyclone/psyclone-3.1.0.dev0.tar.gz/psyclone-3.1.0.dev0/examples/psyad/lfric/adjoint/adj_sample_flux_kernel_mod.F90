module adj_sample_flux_kernel_mod
  use argument_mod, only : any_space_1, arg_type, cell_column, func_type, gh_basis, gh_diff_basis, gh_evaluator, gh_field, gh_inc, &
&gh_read, gh_real
  use constants_mod, only : i_def, r_def
  use fs_continuity_mod, only : w0, w2
  use kernel_mod, only : kernel_type
  implicit none
  type, public, extends(kernel_type) :: adj_sample_flux_kernel_type
  type(ARG_TYPE) :: META_ARGS(4) = (/ &
    arg_type(gh_field, gh_real, gh_read, w2), &
    arg_type(gh_field, gh_real, gh_inc, w2), &
    arg_type(gh_field, gh_real, gh_read, w2), &
    arg_type(gh_field, gh_real, gh_read, any_space_1)/)
  type(FUNC_TYPE) :: META_FUNCS(1) = (/ &
    func_type(any_space_1, gh_basis)/)
  INTEGER :: GH_SHAPE = gh_evaluator
  INTEGER :: OPERATES_ON = cell_column
  CONTAINS
    PROCEDURE, NOPASS :: adj_sample_flux_code
END TYPE adj_sample_flux_kernel_type

  private

  public :: adj_sample_flux_code

  contains
  subroutine adj_sample_flux_code(nlayers, flux, u, rmultiplicity, q, ndf_f, undf_f, map_f, ndf_q, undf_q, map_q, basis_q)
    integer(kind=i_def), intent(in) :: nlayers
    integer(kind=i_def), intent(in) :: ndf_f
    integer(kind=i_def), intent(in) :: ndf_q
    integer(kind=i_def), intent(in) :: undf_f
    integer(kind=i_def), intent(in) :: undf_q
    integer(kind=i_def), dimension(ndf_f), intent(in) :: map_f
    integer(kind=i_def), dimension(ndf_q), intent(in) :: map_q
    real(kind=r_def), dimension(1,ndf_q,ndf_f), intent(in) :: basis_q
    real(kind=r_def), dimension(undf_f), intent(in) :: flux
    real(kind=r_def), dimension(undf_f), intent(inout) :: u
    real(kind=r_def), dimension(undf_f), intent(in) :: rmultiplicity
    real(kind=r_def), dimension(undf_q), intent(in) :: q
    integer(kind=i_def) :: df
    integer(kind=i_def) :: df_q
    integer(kind=i_def) :: k
    integer(kind=i_def) :: loc
    real(kind=r_def), dimension(ndf_q) :: q_cell
    real(kind=r_def) :: q_at_node

    do k = nlayers - 1, 0, -1
      do df_q = 1, ndf_q, 1
        q_cell(df_q) = q(map_q(df_q) + k)
      enddo
      do df = ndf_f, 1, -1
        q_at_node = 0.0_r_def
        do df_q = 1, ndf_q, 1
          q_at_node = q_at_node + basis_q(1,df_q,df) * q_cell(df_q)
        enddo
        loc = k + map_f(df)
        u(loc) = u(loc) + q_at_node * rmultiplicity(loc) * flux(loc)
      enddo
    enddo

  end subroutine adj_sample_flux_code

end module adj_sample_flux_kernel_mod
