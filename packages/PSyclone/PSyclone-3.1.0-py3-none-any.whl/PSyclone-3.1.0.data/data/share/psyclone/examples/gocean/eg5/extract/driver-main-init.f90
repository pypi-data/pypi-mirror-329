program main_init
  use compare_variables_mod, only : compare, compare_init, compare_summary
  use init_field_mod, only : init_field_code
  use read_kernel_data_mod, only : ReadKernelDataType
  integer :: i
  integer :: j
  integer :: a_fld_whole_ystart
  integer :: a_fld_whole_ystop
  integer :: a_fld_whole_xstart
  integer :: a_fld_whole_xstop
  real*8, allocatable, dimension(:,:) :: a_fld
  integer :: b_fld_whole_ystart
  integer :: b_fld_whole_ystop
  integer :: b_fld_whole_xstart
  integer :: b_fld_whole_xstop
  real*8, allocatable, dimension(:,:) :: b_fld
  integer :: c_fld_whole_ystart
  integer :: c_fld_whole_ystop
  integer :: c_fld_whole_xstart
  integer :: c_fld_whole_xstop
  real*8, allocatable, dimension(:,:) :: c_fld
  integer :: d_fld_whole_ystart
  integer :: d_fld_whole_ystop
  integer :: d_fld_whole_xstart
  integer :: d_fld_whole_xstop
  real*8, allocatable, dimension(:,:) :: d_fld
  type(ReadKernelDataType) :: extract_psy_data
  real*8, allocatable, dimension(:,:) :: a_fld_post
  real*8, allocatable, dimension(:,:) :: b_fld_post
  real*8, allocatable, dimension(:,:) :: c_fld_post
  real*8, allocatable, dimension(:,:) :: d_fld_post
  integer :: i_post
  integer :: j_post

  call extract_psy_data%OpenReadModuleRegion('main', 'init')
  call extract_psy_data%ReadVariable('a_fld%whole%xstart', a_fld_whole_xstart)
  call extract_psy_data%ReadVariable('a_fld%whole%xstop', a_fld_whole_xstop)
  call extract_psy_data%ReadVariable('a_fld%whole%ystart', a_fld_whole_ystart)
  call extract_psy_data%ReadVariable('a_fld%whole%ystop', a_fld_whole_ystop)
  call extract_psy_data%ReadVariable('b_fld%whole%xstart', b_fld_whole_xstart)
  call extract_psy_data%ReadVariable('b_fld%whole%xstop', b_fld_whole_xstop)
  call extract_psy_data%ReadVariable('b_fld%whole%ystart', b_fld_whole_ystart)
  call extract_psy_data%ReadVariable('b_fld%whole%ystop', b_fld_whole_ystop)
  call extract_psy_data%ReadVariable('c_fld%whole%xstart', c_fld_whole_xstart)
  call extract_psy_data%ReadVariable('c_fld%whole%xstop', c_fld_whole_xstop)
  call extract_psy_data%ReadVariable('c_fld%whole%ystart', c_fld_whole_ystart)
  call extract_psy_data%ReadVariable('c_fld%whole%ystop', c_fld_whole_ystop)
  call extract_psy_data%ReadVariable('d_fld%whole%xstart', d_fld_whole_xstart)
  call extract_psy_data%ReadVariable('d_fld%whole%xstop', d_fld_whole_xstop)
  call extract_psy_data%ReadVariable('d_fld%whole%ystart', d_fld_whole_ystart)
  call extract_psy_data%ReadVariable('d_fld%whole%ystop', d_fld_whole_ystop)
  call extract_psy_data%ReadVariable('a_fld', a_fld)
  call extract_psy_data%ReadVariable('b_fld', b_fld)
  call extract_psy_data%ReadVariable('c_fld', c_fld)
  call extract_psy_data%ReadVariable('d_fld', d_fld)
  call extract_psy_data%ReadVariable('i', i)
  call extract_psy_data%ReadVariable('j', j)
  call extract_psy_data%ReadVariable('a_fld_post', a_fld_post)
  call extract_psy_data%ReadVariable('b_fld_post', b_fld_post)
  call extract_psy_data%ReadVariable('c_fld_post', c_fld_post)
  call extract_psy_data%ReadVariable('d_fld_post', d_fld_post)
  call extract_psy_data%ReadVariable('i_post', i_post)
  call extract_psy_data%ReadVariable('j_post', j_post)
  do j = a_fld_whole_ystart, a_fld_whole_ystop, 1
    do i = a_fld_whole_xstart, a_fld_whole_xstop, 1
      call init_field_code(i, j, a_fld, 1.0)
    enddo
  enddo
  do j = b_fld_whole_ystart, b_fld_whole_ystop, 1
    do i = b_fld_whole_xstart, b_fld_whole_xstop, 1
      call init_field_code(i, j, b_fld, 2.0)
    enddo
  enddo
  do j = c_fld_whole_ystart, c_fld_whole_ystop, 1
    do i = c_fld_whole_xstart, c_fld_whole_xstop, 1
      call init_field_code(i, j, c_fld, 3.0)
    enddo
  enddo
  do j = d_fld_whole_ystart, d_fld_whole_ystop, 1
    do i = d_fld_whole_xstart, d_fld_whole_xstop, 1
      call init_field_code(i, j, d_fld, 4.0)
    enddo
  enddo
  call compare_init(6)
  call compare('a_fld', a_fld, a_fld_post)
  call compare('b_fld', b_fld, b_fld_post)
  call compare('c_fld', c_fld, c_fld_post)
  call compare('d_fld', d_fld, d_fld_post)
  call compare('i', i, i_post)
  call compare('j', j, j_post)
  call compare_summary()

end program main_init
