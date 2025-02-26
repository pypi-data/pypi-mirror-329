program test
  use decomposition_mod, only : decomposition_type
  use field_mod
  use grid_mod
  use parallel_mod, only : parallel_init
  use psy_test, only : invoke_0, invoke_1_update_field
  use value_range_check_psy_data_mod, only : value_range_check_psydatainit, value_range_check_psydatashutdown, &
&value_range_check_psydatastart
  type(r2d_field) :: a_fld
  type(r2d_field) :: b_fld
  TYPE(grid_type), TARGET :: grid

  call parallel_init()
  call value_range_check_psydatastart()
  grid = grid_type(GO_ARAKAWA_C,(/GO_BC_PERIODIC, GO_BC_PERIODIC, GO_BC_NONE/),GO_OFFSET_SW)
  call grid%decompose(3, 3, 1, 1, 1, halo_width=1)
  call grid_init(grid, 1.0_8, 1.0_8)
  a_fld = r2d_field(grid,GO_T_POINTS)
  b_fld = r2d_field(grid,GO_T_POINTS)
  call invoke_0(a_fld, b_fld)
  call invoke_1_update_field(a_fld, b_fld)
  ! PSyclone CodeBlock (unsupported code) reason:
  !  - Unsupported statement: Print_Stmt
  PRINT *, "a_fld is", a_fld % data

end program test
