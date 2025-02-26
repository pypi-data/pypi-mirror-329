program alg
  use field_mod, only : go_t_points, r2d_field
  use gocean_mod, only : gocean_initialise
  use grid_mod
  use kind_params_mod, only : go_wp
  use parallel_mod
  use psy_alg, only : invoke_0_inc_field
  integer, parameter :: nsteps = 10
  type(decomposition_type) :: decomp
  integer :: my_rank
  integer :: istp
  integer :: ierr
  integer :: this_step
  integer :: jpiglo
  integer :: jpjglo
  integer, allocatable, dimension(:,:) :: tmask
  type(r2d_field) :: fld1
  TYPE(grid_type), TARGET :: grid1
  integer :: nx
  integer :: ny

  jpiglo = 50
  jpjglo = 50
  call gocean_initialise()
  grid1 = grid_type(GO_ARAKAWA_C,(/GO_BC_PERIODIC, GO_BC_PERIODIC, GO_BC_NONE/),GO_OFFSET_SW)
  call grid1%decompose(jpiglo, jpjglo)
  my_rank = get_rank()
  ALLOCATE(tmask(1:grid1%subdomain%global%nx,1:grid1%subdomain%global%ny), STAT=ierr)
  if (ierr /= 0) then
    ! PSyclone CodeBlock (unsupported code) reason:
    !  - Unsupported statement: Stop_Stmt
    STOP 'Failed to allocate T mask'
  end if
  tmask(:,:) = 0
  call grid_init(grid1, 1000.0_go_wp, 1000.0_go_wp, tmask)
  fld1 = r2d_field(grid1,go_t_points)
  fld1%data(:,:) = 0.0_go_wp
  nx = fld1%whole%nx
  ny = fld1%whole%ny
  do istp = 1, nsteps, 1
    this_step = istp
    call invoke_0_inc_field(fld1, nx, ny, this_step)
  enddo
  ! PSyclone CodeBlock (unsupported code) reason:
  !  - Unsupported statement: Write_Stmt
  WRITE(*, *) "nsteps = ", nsteps, "field(2,2) = ", fld1 % data(2, 2)

end program alg
