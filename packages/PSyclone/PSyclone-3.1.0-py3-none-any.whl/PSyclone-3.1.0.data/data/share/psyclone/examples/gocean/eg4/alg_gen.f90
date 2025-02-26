program alg
  use field_mod
  use gocean_mod
  use grid_mod
  use kind_params_mod, only : go_wp
  use parallel_mod, only : get_rank, on_master
  use psy_alg, only : invoke_0_kern_use_var
  real(kind=go_wp), save :: dx = 1.0
  real(kind=go_wp), save :: dy = 1.0
  TYPE(grid_type), TARGET :: model_grid
  type(r2d_field) :: fld1
  integer, allocatable, dimension(:,:) :: tmask
  integer :: ierr

  call gocean_initialise()
  model_grid = grid_type(GO_ARAKAWA_C,(/GO_BC_EXTERNAL, GO_BC_EXTERNAL, GO_BC_NONE/),GO_OFFSET_NE)
  call model_grid%decompose(100, 100, 1, 1, 1)
  ALLOCATE(tmask(1:model_grid%subdomain%global%nx,1:model_grid%subdomain%global%ny), STAT=ierr)
  if (ierr /= 0) then
    call gocean_stop('Failed to allocate T-mask')
  end if
  tmask(:,:) = 1
  call grid_init(model_grid, dx, dy, tmask)
  fld1 = r2d_field(model_grid,GO_U_POINTS)
  call invoke_0_kern_use_var(fld1)

end program alg
