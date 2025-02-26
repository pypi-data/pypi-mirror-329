program main_update
  use compare_variables_mod, only : compare, compare_init, compare_summary
  use read_kernel_data_mod, only : ReadKernelDataType
  use update_field_mod, only : update_field_code
  integer :: i
  integer :: j
  real*8 :: x
  real*8 :: y
  real*8 :: z
  integer :: a_fld_whole_ystart
  integer :: a_fld_whole_ystop
  integer :: a_fld_whole_xstart
  integer :: a_fld_whole_xstop
  real*8, allocatable, dimension(:,:) :: a_fld
  real*8, allocatable, dimension(:,:) :: b_fld
  real*8, allocatable, dimension(:,:) :: c_fld
  real*8, allocatable, dimension(:,:) :: d_fld
  real*8 :: b_fld_grid_dx
  type(ReadKernelDataType) :: extract_psy_data
  real*8, allocatable, dimension(:,:) :: a_fld_post
  integer :: i_post
  integer :: j_post
  real*8 :: x_post
  real*8 :: y_post

  call extract_psy_data%OpenReadModuleRegion('main', 'update')
  call extract_psy_data%ReadVariable('a_fld', a_fld)
  call extract_psy_data%ReadVariable('a_fld%whole%xstart', a_fld_whole_xstart)
  call extract_psy_data%ReadVariable('a_fld%whole%xstop', a_fld_whole_xstop)
  call extract_psy_data%ReadVariable('a_fld%whole%ystart', a_fld_whole_ystart)
  call extract_psy_data%ReadVariable('a_fld%whole%ystop', a_fld_whole_ystop)
  call extract_psy_data%ReadVariable('b_fld', b_fld)
  call extract_psy_data%ReadVariable('b_fld%grid%dx', b_fld_grid_dx)
  call extract_psy_data%ReadVariable('c_fld', c_fld)
  call extract_psy_data%ReadVariable('d_fld', d_fld)
  call extract_psy_data%ReadVariable('x', x)
  call extract_psy_data%ReadVariable('z', z)
  call extract_psy_data%ReadVariable('i', i)
  call extract_psy_data%ReadVariable('j', j)
  call extract_psy_data%ReadVariable('y', y)
  call extract_psy_data%ReadVariable('a_fld_post', a_fld_post)
  call extract_psy_data%ReadVariable('i_post', i_post)
  call extract_psy_data%ReadVariable('j_post', j_post)
  call extract_psy_data%ReadVariable('x_post', x_post)
  call extract_psy_data%ReadVariable('y_post', y_post)
  do j = a_fld_whole_ystart, a_fld_whole_ystop, 1
    do i = a_fld_whole_xstart, a_fld_whole_xstop, 1
      call update_field_code(i, j, a_fld, b_fld, c_fld, d_fld, x, y, z, b_fld_grid_dx)
    enddo
  enddo
  call compare_init(5)
  call compare('a_fld', a_fld, a_fld_post)
  call compare('i', i, i_post)
  call compare('j', j, j_post)
  call compare('x', x, x_post)
  call compare('y', y, y_post)
  call compare_summary()

end program main_update
