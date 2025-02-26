MODULE other_alg_mod
  USE field_mod, ONLY: field_type
  USE mesh_mod, ONLY: mesh_type
  USE constants_mod, ONLY: r_def
  IMPLICIT NONE
  CONTAINS
  SUBROUTINE my_alg(field_1, chksum1)
    USE other_alg_mod_psy, ONLY: invoke_0
    TYPE(field_type), INTENT(INOUT) :: field_1
    REAL(KIND = r_def), INTENT(OUT) :: chksum1
    CALL invoke_0(chksum1, field_1)
  END SUBROUTINE my_alg
END MODULE other_alg_mod