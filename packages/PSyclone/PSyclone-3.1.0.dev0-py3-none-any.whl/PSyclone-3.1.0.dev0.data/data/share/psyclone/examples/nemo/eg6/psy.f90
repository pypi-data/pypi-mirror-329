program dummy
  use read_only_verify_psy_data_mod, only : read_only_verify_PSyDataType
  real, dimension(10,10) :: umask
  CHARACTER(LEN = 10) :: char_var
  integer :: ji
  integer :: jj
  logical :: logical_var
  INTEGER(KIND = 8) :: offset
  INTEGER, INTRINSIC :: loc
  INTEGER, INTRINSIC :: sizeof
  type(read_only_verify_PSyDataType), save, target :: read_only_verify_psy_data

  logical_var = .false.
  char_var = 'test'
  CALL read_only_verify_psy_data % PreStart("dummy", "r0", 2, 2)
  CALL read_only_verify_psy_data % PreDeclareVariable("char_var", char_var)
  CALL read_only_verify_psy_data % PreDeclareVariable("logical_var", logical_var)
  CALL read_only_verify_psy_data % PreDeclareVariable("char_var", char_var)
  CALL read_only_verify_psy_data % PreDeclareVariable("logical_var", logical_var)
  CALL read_only_verify_psy_data % PreEndDeclaration
  CALL read_only_verify_psy_data % ProvideVariable("char_var", char_var)
  CALL read_only_verify_psy_data % ProvideVariable("logical_var", logical_var)
  CALL read_only_verify_psy_data % PreEnd
  do jj = 1, 10, 1
    do ji = 1, 10, 1
      if (char_var == 'abc' .AND. logical_var) then
        umask(ji,jj) = 1
      else
        umask(ji,jj) = 3
      end if
    enddo
  enddo
  CALL read_only_verify_psy_data % PostStart
  CALL read_only_verify_psy_data % ProvideVariable("char_var", char_var)
  CALL read_only_verify_psy_data % ProvideVariable("logical_var", logical_var)
  CALL read_only_verify_psy_data % PostEnd
  ! PSyclone CodeBlock (unsupported code) reason:
  !  - Unsupported statement: Print_Stmt
  PRINT *, umask(1, 1), logical_var

end program dummy
